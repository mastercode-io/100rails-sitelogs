from AnvilFusion.server import utils as fusion_server_utils
from ..app.models import Tenant, User, AppIntegration, AppInApiCredential, AppOutApiCredential
import anvil.server
import anvil.users
import anvil.secrets
from anvil import app
import base64
import json
import uuid
import secrets
import string
import time
import signal
from Crypto.Cipher import AES
from .resources import *
from ..background_tasks import *


app_api_origin = anvil.server.get_api_origin()
if app_api_origin:
    app_env_list = app_tables.app_environments.search()
    app_env_name = None
    for env in app_env_list:
        if env['key'] in app_api_origin:
            app_env_name = env['name']
            break


API_REQUEST_USER = 'api_request@oaylogs.com'
API_REQUEST_PASSWORD = anvil.secrets.get_secret('api_request_password')
RESPONSE_401 = anvil.server.HttpResponse(401, "Access Denied. Authentication failed.")
RESPONSE_404 = anvil.server.HttpResponse(404, "Resource not found.")
RESPONSE_405 = anvil.server.HttpResponse(405, "Method not allowed.")
API_RESPONSE_PAGE_LENGTH = 100


def app_env_info():
    print('--- App Info ---')
    print(f'git branch: {app.branch}')
    print(f'environment: {app.environment.name} ({app.environment.tags})')
    print(f'id: {app.id}')


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def get_api_service_login(tenant_uid, service_name):
    # tenant = Tenant.get(tenant_uid)
    return f"{service_name}_{tenant_uid}@paylogs.com"


@anvil.server.callable
def register_api_service(service_name, description, url, direction='in'):
    api_service = AppIntegration.get_by('service_name', service_name)
    if api_service:
        api_service['description'] = description
        api_service['url'] = url
        api_service['direction'] = direction
        api_service['status'] = 'active'
    else:
        api_service = AppIntegration(
            service_name=service_name,
            description=description,
            url=url,
            direction=direction,
            status='active',
        )
    api_service.save()
    return api_service


@anvil.server.callable
def generate_api_key(tenant_uid, api_service: AppIntegration):
    api_service_login = get_api_service_login(tenant_uid, api_service['service_name'])
    api_service_password = generate_password()
    api_service_user = User.get_by('email', api_service_login)
    if not api_service_user:
        api_user_row = anvil.users.signup_with_email(api_service_login, api_service_password)
        tenant = Tenant.get(tenant_uid)
        api_user_row.update(
            tenant_uid=tenant_uid,
            uid=str(uuid.uuid4()),
            confirmed_email=True,
            first_name=api_service['service_name'],
            last_name=tenant['name'],
        )
        print('api_user_row', api_user_row)
        print(tenant_uid, api_service['service_name'], tenant['name'])
        api_service_user = User.get(api_user_row['uid'])
    else:
        temp_user = anvil.users.signup_with_email(f'{str(uuid.uuid4())}@paylogs.com', api_service_password)
        api_service_user['password_hash'] = temp_user['password_hash']
        temp_user.delete()
    api_service_user.save()

    if api_service['direction'] == 'in' or api_service['direction'] == 'bidirectional':
        api_credential = AppInApiCredential.search(integration=api_service, api_user=api_service_user)
        if not api_credential:
            api_credential = AppInApiCredential(
                integration=api_service,
                api_user=api_service_user,
            )
        api_secret = generate_password()
        cipher = AES.new(api_secret.encode(), AES.MODE_EAX)
        cipher_text, tag = cipher.encrypt_and_digest(
            json.dumps({'api_user': api_service_login, 'password': api_service_password}).encode()
        )
        api_key = base64.urlsafe_b64encode(cipher.nonce + tag + cipher_text).decode()
        api_credential['api_key'] = api_key
        api_credential['api_secret'] = api_secret
        api_credential['tenant_uid'] = tenant_uid
        api_credential['status'] = 'active'
        api_credential.save()
        return api_credential


def decode_api_key(api_key):
    api_credential = AppInApiCredential.get_by('api_key', api_key)
    if api_credential:
        api_secret = api_credential['api_secret']
        encrypted_bytes = base64.urlsafe_b64decode(api_key)
        nonce = encrypted_bytes[:16]
        tag = encrypted_bytes[16:32]
        ciphertext = encrypted_bytes[32:]
        cipher = AES.new(api_secret.encode(), AES.MODE_EAX, nonce=nonce)
        json_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        json_str = json_bytes.decode('utf-8')
        api_login = json.loads(json_str)
        return api_credential['integration']['uid'], api_login['api_user'], api_login['password']


def authenticate_request(request: anvil.server.request):
    tenant_uid = request.headers.get('x-tenant-uid', None)
    api_key = request.headers.get('x-api-key', None)
    if not api_key:
        return None, anvil.server.HttpResponse(401, f'Missing x-api-key header: {request.headers}')
    else:
        print(app_env_info())
        print(f'API request environment: {app_env_name}')
        print(API_REQUEST_USER, API_REQUEST_PASSWORD)
        logged_user = fusion_server_utils.init_user_session(user_email=API_REQUEST_USER, password=API_REQUEST_PASSWORD)
        integration_uid, api_user, api_password = decode_api_key(api_key)
        integration = AppIntegration.get(integration_uid)
        if not api_user:
            return None, anvil.server.HttpResponse(401, f'Invalid x-api-key header: {request.headers}')
        else:
            logged_user = fusion_server_utils.init_user_session(user_email=api_user, password=api_password)
            print('logged_user', logged_user)
            if not logged_user:
                return None, anvil.server.HttpResponse(401, f'Invalid user credentials: {api_user}, {api_password}')
            else:
                return integration, None


@anvil.server.http_endpoint("/:resource_name/:resource_uid", methods=["GET", "POST"])
def resource_endpoint(resource_name, resource_uid, **params):
    integration, http_response = authenticate_request(anvil.server.request)
    if integration is None:
        return http_response
    resource_name = resource_name.lower()
    print(f"integration: {integration['service_name']}\n"
          f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"resource_name: {resource_name}, resource_uid: {resource_uid}, params: {params}\n")

    if resource_name == 'connection':
        if anvil.server.request.method != "GET":
            return RESPONSE_405
        else:
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    'service_name': integration['service_name'],
                    'description': integration['description'],
                    'url': integration['url'],
                }),
                {'content-type': 'application/json'},
            )
    if resource_name not in API_RESOURCES:
        return anvil.server.HttpResponse(404, f'Invalid resource name: {resource_name}')

    resource = API_RESOURCES[resource_name]
    resource_class = resource['model']

    # HTTP GET request handler
    if anvil.server.request.method == "GET":

        # get single resource object by uid or link_id
        link_id = params.get('link_id', None) if resource['remote_links'] else None
        if resource_uid or link_id:
            item = None
            if resource_uid:
                item = resource_class.get(resource_uid)
            elif link_id:
                item = resource_class.get_by('remote_links', {integration['uid']: link_id})
            if item:
                return anvil.server.HttpResponse(
                    200,
                    json.dumps(item.to_json_dict(
                        json_schema=resource['json_schema'],
                        integration_uid=integration['uid'])
                    ),
                    {'content-type': 'application/json'},
                )
            else:
                return anvil.server.HttpResponse(404, f'{resource_name} not found: {resource_uid}')

        # get list of resource objects with supported search, filter, sort, and pagination
        else:
            if resource['pagination']:
                page = params.get('page', 1)
                page_length = params.get('page_length', API_RESPONSE_PAGE_LENGTH)
                try:
                    page = int(page)
                except ValueError:
                    page = 1
                try:
                    page_length = int(page_length)
                except ValueError:
                    page_length = API_RESPONSE_PAGE_LENGTH
            else:
                page = 1
                page_length = None
            filters = resource['filters'](params, integration['uid']) if resource.get('filters', None) else {}
            if resource['sorting']:
                filters['search_query'] = resource['sorting']
            print('filters:', filters)
            items = resource_class.search(page=page, page_length=page_length, **filters)
            item_list = [item.to_json_dict(json_schema=resource['json_schema'], integration_uid=integration['uid'])
                         for item in items]
            resource_uri = f'{anvil.server.get_api_origin()}/{resource_name}/?page_length={page_length}'
            links = {
                'first': f'{resource_uri}&page=1',
                'last': f'{resource_uri}&page={items.total_pages}',
            }
            if page > 1:
                links['prev'] = f'{resource_uri}&page={page - 1}'
            if page < items.total_pages:
                links['next'] = f'{resource_uri}&page={page + 1}'
            return anvil.server.HttpResponse(
                200,
                json.dumps({
                    resource_name: item_list,
                    'count': len(item_list),
                    'page': page,
                    'total_pages': items.total_pages,
                    'links': links,
                }),
                {'content-type': 'application/json'},
            )

    # HTTP POST request handler
    elif anvil.server.request.method == "POST":

        post_data = anvil.server.request.body_json
        if post_data is None:
            try:
                post_data = json.loads(anvil.server.request.body, strict=False)
            except json.JSONDecodeError:
                print(f'Invalid JSON body: {anvil.server.request.body}')
                return anvil.server.HttpResponse(400, f'Invalid JSON body: {anvil.server.request.body}')

        if 'check_ids' in params:
            check_result = check_link_ids(resource, post_data, integration['uid'])
            return anvil.server.HttpResponse(
                200,
                json.dumps(check_result),
                {'content-type': 'application/json'},
            )

        link_id = params.get('link_id', None) if resource['remote_links'] else None
        if resource_uid or link_id:
            item = None
            item_reference = None
            if resource_uid:
                item = resource_class.get(resource_uid)
                item_reference = f'uid: {resource_uid}'
            elif link_id:
                item = resource_class.get_by('remote_links', {integration['uid']: link_id})
                item_reference = f'link_id: {link_id}'
            if item is None:
                return anvil.server.HttpResponse(404, f'{resource_name} not found: {item_reference}')
            elif resource_uid:
                post_data['uid'] = resource_uid
            elif link_id:
                post_data['link_id'] = link_id
                item_json, error = post_item(resource['name'], resource['model'], resource['json_schema'],
                                             post_data, integration)
                return anvil.server.HttpResponse(
                    200 if not error else error['status'],
                    json.dumps(item_json),
                    {'content-type': 'application/json'},
                )

        if resource_name not in post_data:
            post_list = [post_data]
        elif resource_name in post_data and not isinstance(post_data[resource_name], list):
            return anvil.server.HttpResponse(400, f'Invalid JSON body: expected list of {resource_name}')
        else:
            post_list = post_data[resource_name]
        result = post_items(resource['name'], resource['model'], resource['json_schema'],
                            post_list, integration)
        return anvil.server.HttpResponse(
            200 if not result['errors'] else 207,
            json.dumps(result),
            {'content-type': 'application/json'},
        )


@anvil.server.http_endpoint("/batch/:resource_name/:task_id", methods=["GET", "POST"])
def resource_batch_endpoint(resource_name, task_id, **params):

    integration, http_response = authenticate_request(anvil.server.request)
    if integration is None:
        return http_response
    resource_name = resource_name.lower()
    print(f"integration: {integration['service_name']}\n"
          f"method: {anvil.server.request.method}, headers: {anvil.server.request.headers}\n"
          f"resource_name: {resource_name}, task_id: {task_id}, params: {params}\n")

    if anvil.server.request.method == "GET":
        bg_task = get_background_task_status(task_id)
        if not bg_task:
            return anvil.server.HttpResponse(404, f'Invalid task_id: {task_id}')
        else:
            return anvil.server.HttpResponse(
                200,
                json.dumps(bg_task),
                {'content-type': 'application/json'},
            )

    elif anvil.server.request.method == "POST":
        if task_id:
            bg_task = get_background_task_status(task_id)
            if bg_task:
                return anvil.server.HttpResponse(400, f'Invalid request: cannot post to a task')
        if resource_name not in API_RESOURCES:
            return anvil.server.HttpResponse(404, f'Invalid resource name: {resource_name}')
        resource = API_RESOURCES[resource_name]
        post_data = anvil.server.request.body_json
        if post_data is None:
            try:
                post_data = json.loads(anvil.server.request.body, strict=False)
            except json.JSONDecodeError:
                print(f'Invalid JSON body: {anvil.server.request.body}')
                return anvil.server.HttpResponse(400, f'Invalid JSON body: {anvil.server.request.body}')
        if resource_name not in post_data:
            post_list = [post_data]
        elif resource_name in post_data and not isinstance(post_data[resource_name], list):
            return anvil.server.HttpResponse(400, f'Invalid JSON body: expected list of {resource_name}')
        else:
            post_list = post_data[resource_name]
        bg_task = anvil.server.launch_background_task(
            'background_task_manager',
            fusion_server_utils.get_logged_user(),
            'API batch post request',
            post_items.__module__,
            'post_items',
            resource['name'], resource['model'], resource['json_schema'], post_list, integration,
        )
        return anvil.server.HttpResponse(
            202,
            json.dumps({'task_id': bg_task.get_id()}),
            {'content-type': 'application/json'},
        )


def post_items(resource_name, resource_model, resource_json_schema, post_list, integration):
    item_list = []
    error_list = []
    for item in post_list:
        item_json, error = post_item(resource_name, resource_model, resource_json_schema, item, integration)
        if not error:
            item_list.append(item_json)
        else:
            error_list.append(item_json)
    return {
        resource_name: item_list,
        'errors': error_list,
    }


def post_item(resource_name, resource_model, resource_json_schema, post_data, integration):
    resource_class = resource_model
    item = None
    if post_data.get('uid', None) or post_data.get('link_id', None):
        if post_data.get('uid', None):
            item = resource_class.get(post_data['uid'])
            if item is None:
                post_data['error'] = f"ValidationError, {resource_name} not found: uid {post_data['uid']}"
                return post_data, {'status': 404, 'error': post_data['error']}
        elif post_data.get('link_id', None):
            item = resource_class.get_by('remote_links', {integration['uid']: post_data['link_id']})
    if item is None:
        item = resource_class()

    item_data = {}
    for field in resource_json_schema['fields']:
        if field in post_data:
            item_data[field] = type_check(post_data[field], resource_model._attributes[field].field_type)
    for relationship in resource_json_schema.get('relationships', {}):
        if relationship in post_data:
            rel_json = post_data[relationship]
            if rel_json:
                if 'uid' in rel_json:
                    item_data[relationship] = {'uid': rel_json['uid']}
                elif 'link_id' in rel_json and rel_json['link_id'] is not None:
                    rel_item = next(iter(resource_class._relationships[relationship].cls.search(
                        remote_links={integration['uid']: rel_json['link_id']}
                    )), None)
                    # print('rel_item', rel_item, 'remote_links', {integration['uid']: rel_json['link_id']})
                    if not rel_item:
                        post_data['error'] = f"ValidationError, {relationship} not found: {rel_json['link_id']}"
                        return post_data, {'status': 400, 'error': post_data['error']}
                    item_data[relationship] = {'uid': rel_item['uid']}
    if 'link_id' in post_data and 'remote_links' in resource_class._attributes:
        if not item.get('remote_links', None):
            item_data['remote_links'] = {}
        item_data['remote_links'][integration['uid']] = post_data['link_id']
    item.update(item_data)
    valid, error = item.validate()
    if not valid:
        post_data['error'] = f"ValidationError, {error}"
        return post_data, {'status': 400, 'error': post_data['error']}
    # print('item_data', item_data)
    # print(item['date'], item['start_time'], item['end_time'])
    item.save()
    item = resource_class.get(item['uid'])
    item_json = item.to_json_dict(json_schema=resource_json_schema, integration_uid=integration['uid'])
    return item_json, None


def check_link_ids(resource, post_data, integration_uid):
    print('check_link_ids', post_data)
    link_ids = post_data.get('link_id_list', []) or []
    check_result = {'link_id_list': link_ids}
    persist_id_list = []
    missed_id_list = []
    for link_id in link_ids:
        item = resource['model'].get_by('remote_links', {integration_uid: link_id})
        if item is not None:
            persist_id_list.append(link_id)
        else:
            missed_id_list.append(link_id)
    check_result['exist_id_list'] = persist_id_list
    check_result['missed_id_list'] = missed_id_list
    return check_result

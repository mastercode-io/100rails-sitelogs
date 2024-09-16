# from AnvilFusion.server import utils as fusion_server_utils
import anvil.server
import anvil.users
import anvil.secrets
import requests
import base64
import urllib
import json
from xero_python import api_client as xero_api


XERO_AUTH = json.loads(anvil.secrets.get_secret('xero_auth'))
XERO_CLIENT_ID = XERO_AUTH['client_id']
XERO_CLIENT_SECRET = XERO_AUTH['client_secret']
XERO_OAUTH_LOGIN_URL = 'https://login.xero.com/identity/connect/authorize'
XERO_OAUTH_TOKEN_URL = 'https://identity.xero.com/connect/token'
XERO_CONNECTION_URL = 'https://api.xero.com/connections'
XERO_OAUTH_REDIRECT_URL = 'https://bbezaphmpn72gfkm.anvil.app/XOLVUAFPYYUDPOS3TNHURVTN/integrations/xero/auth'


@anvil.server.callable
def get_xero_auth_url(tenant_uid, service_uid):
    state_token = json.dumps({'tenant_uid': tenant_uid, 'service_uid': service_uid})
    xero_api_scope = 'offline_access openid email profile payroll.settings.read payroll.employees payroll.timesheets'
    xero_auth_url = (f"{XERO_OAUTH_LOGIN_URL}?response_type=code&client_id={XERO_CLIENT_ID}"
                     f"&redirect_uri={XERO_OAUTH_REDIRECT_URL}&scope={xero_api_scope}&state={state_token}")
    print('xero auth url', xero_auth_url)
    return xero_auth_url


@anvil.server.route("/integrations/xero/auth", methods=["GET", "POST"])
def xero_auth(**params):
    state_token = json.loads(params.get("state", "{}"))
    tenant_uid = state_token.get('tenant_uid', None)
    service_uid = state_token.get('service_uid', None)

    xero_auth_code = params.get("code", None)
    if not xero_auth_code:
        return anvil.server.HttpResponse(status=400, body="Invalid authorization code")
    headers = {
        'Authorization': f"Basic {str(base64.b64encode(bytes(f'{XERO_CLIENT_ID}:{XERO_CLIENT_SECRET}', 'utf-8')), 'ascii')}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = f'grant_type=authorization_code&code={urllib.parse.quote(xero_auth_code)}&' \
           f'redirect_uri={urllib.parse.quote(XERO_OAUTH_REDIRECT_URL, safe="")}'

    response = requests.post(url=XERO_OAUTH_TOKEN_URL, data=body, headers=headers)
    print(f'Xero access token: {response.text}')
    xero_access_token = response.json()['access_token']
    xero_refresh_token = response.json()['refresh_token']
    headers = {
        'Authorization': f'Bearer {xero_access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url=XERO_CONNECTION_URL, headers=headers)
    xero_connections = response.json()
    xero_tenant_id = xero_connections[0]['tenantId']
    print(f'Xero connections: {xero_connections}')
    print(f'Xero tenant id: {xero_tenant_id}')

    print(f"xero_access_token: {xero_access_token}\nxero_refresh_token: {xero_refresh_token}\nxero_tenant_id: {xero_tenant_id}")
    print(f"state: {json.dumps(state_token)}")

    payroll_integration_data = {
        'tenant_uid': tenant_uid,
        'service_uid': service_uid,
        'connection_data': {
            'access_token': xero_access_token,
            'refresh_token': xero_refresh_token,
            'xero_tenant_id': xero_tenant_id,
        }
    }
    return anvil.server.FormResponse(
        'app.HomePage',
        start_page='payroll_settings',
        start_props={'payroll_integration_data': payroll_integration_data}
    )

# from AnvilFusion.server import utils as fusion_server_utils
import anvil.server
import anvil.users
import anvil.secrets
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import json


QB_AUTH = json.loads(anvil.secrets.get_secret('qb_auth_sandbox'))
QB_CLIENT_ID = QB_AUTH['client_id']
QB_CLIENT_SECRET = QB_AUTH['client_secret']
QB_OAUTH_REDIRECT_URL = 'https://bbezaphmpn72gfkm.anvil.app/XOLVUAFPYYUDPOS3TNHURVTN/integrations/qb/auth'
qb_auth_client = AuthClient(
    QB_CLIENT_ID,
    QB_CLIENT_SECRET,
    QB_OAUTH_REDIRECT_URL,
    'sandbox',
)


@anvil.server.callable
def get_qb_auth_url(tenant_uid, service_uid):
    state_token = json.dumps({'tenant_uid': tenant_uid, 'service_uid': service_uid})
    qb_auth_url = qb_auth_client.get_authorization_url([Scopes.ACCOUNTING], state_token=state_token)
    print('quickbooks auth url', qb_auth_url)
    return qb_auth_url


@anvil.server.route("/integrations/qb/auth", methods=["GET", "POST"])
def qb_auth(**params):
    qb_auth_code = params.get("code", None)
    realm_id = params.get("realmId", None)
    state_token = json.loads(params.get("state", "{}"))
    tenant_uid = state_token.get('tenant_uid', None)
    service_uid = state_token.get('service_uid', None)
    qb_auth_client.get_bearer_token(qb_auth_code, realm_id=realm_id)
    qb_access_token = qb_auth_client.access_token
    qb_refresh_token = qb_auth_client.refresh_token
    print(f"qb_access_token: {qb_access_token}\nqb_refresh_token: {qb_refresh_token}\nrealm_id: {realm_id}")
    print(f"state: {json.dumps(state_token)}")

    payroll_integration_data = {
        'tenant_uid': tenant_uid,
        'service_uid': service_uid,
        'connection_data': {
            'access_token': qb_access_token,
            'refresh_token': qb_refresh_token,
            'realm_id': realm_id,
        }
    }
    return anvil.server.FormResponse(
        'app.HomePage',
        start_page='payroll_settings',
        start_props={'payroll_integration_data': payroll_integration_data}
    )

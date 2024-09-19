import anvil.server
import anvil.tables.query as q
import anvil.js
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.datamodel.particles import SYSTEM_TENANT_UID
from ...app import models
from ..models import AppIntegration, Tenant, Account
from ..HomePage import navigation as nav


def add_enum_list():
    enum_name = 'DAY_TYPE_OPTIONS'
    enum_options = [
        'AnyDay',
        'Weekday',
        'Weekend',
        'Saturday',
        'Sunday',
        'PublicHoliday',
        'Week',
        'RDO',
    ]
    enum_values = {x: x for x in enum_options}
    enum = models.AppEnum(name=enum_name, options=enum_values).save()
    print(enum)


def add_integration():
    print('func')
    integration = AppIntegration.get_by('service_name', 'scaflog')
    tenant = Tenant.get_by('name', 'Scaffit')
    print(integration, tenant)
    print(integration['uid'], integration['service_name'])
    api_credentials = anvil.server.call('generate_api_key', tenant['uid'], integration)
    print(api_credentials)


def add_grid_view():
    models.AppGridView(
        name='PayrunList',
        model='Payrun',
        owner='system',
        columns=[
            {
                "name": "payrun_week",
                "label": "Year Week"
            },
            {
                "name": "pay_period_start",
                "label": "Pay Period Start",
                "format": "MMM dd"
            },
            {
                "name": "pay_period_end",
                "label": "Pay Period End",
                "format": "MMM dd"
            },
            {
                "name": "pay_date",
                "label": "Pay Date",
                "format": "MMM dd"
            },
            {
                "name": "status",
                "label": "Status"
            },
            {
                "name": "notes",
                "label": "Notes"
            }
        ],
    ).save()


def create_user():
    # email = 'brendan.k@rbscaff.com.au'
    # password = 'fpCwhPydSHEbaXO'
    # tenant = Tenant.get_by('name', 'RB Scaffolding')
    # email = 'brady.v@rbteam.com.au'
    # password = '4AzqGwM9x2FKu6q'
    email = 'al.cordovarojas@gmail.com'
    password = '4AzqGwM9x2FKu6q'
    tenant = Tenant.get_by('name', 'AGH')
    print(tenant)
    anvil.server.call('signup_user', email, password, tenant['uid'])


def update_permissions_schema():
    permissions_comps = [*models.AppComponent.search(tenant_uid=None)]
    for comp in permissions_comps:
        if comp['id'] == 'user_role_permissions':
            comp['props'] = nav.DEFAULT_USER_PERMISSIONS
            comp.save()
    pass


def bar():
    tenants = [*models.Tenant.search(tenant_uid=None)]
    # day_type_options = {
    #     "RDO": "RDO",
    #     "Week": "Week",
    #     "AnyDay": "Any Day",
    #     "Sunday": "Sunday",
    #     "Weekday": "Weekday",
    #     "Weekend": "Weekend",
    #     "Saturday": "Saturday",
    #     "PublicHoliday": "Public Holiday"
    # }
    # for tenant in tenants:
    #     enum = models.AppEnum(
    #         name='DYA_TYPE_OPTIONS',
    #         tenant_uid=tenant['uid'],
    #         options=day_type_options
    #     ).save()

    for tenant in tenants:
        user_role_permissions = nav.DEFAULT_USER_PERMISSIONS.copy()
        user_role_permissions['user_roles'].pop('portal_admin', None)
        if tenant['uid'] != SYSTEM_TENANT_UID:
            app_component = models.AppComponent(
                name='User Role Permissions',
                id='user_role_permissions',
                type='object',
                version='1.0',
                tenant_uid=tenant['uid'],
                props=user_role_permissions
            ).save()

    pass
    # search_query = [q.none_of(payrun=None)]
    # ts_list = models.Timesheet.search(search_query=search_query)
    # for ts in ts_list:
    #     ts['payrun'] = None
    #     ts.save()
    # payrun = models.Payrun.get_by('pay_period_start', datetime.date(2024, 4, 8))
    # print(payrun)
    # ts_list = models.Timesheet.search(date=q.between(datetime.date(2024, 4, 8), datetime.date(2024, 4, 15)))
    # print(len(ts_list))
    # for ts in ts_list:
    #     ts['payrun'] = payrun
    #     ts.save()
    # payrun = models.Payrun.get_by('pay_period_start', datetime.date(2024, 4, 15))
    # print(payrun)
    # ts_list = models.Timesheet.search(date=q.between(datetime.date(2024, 4, 15), datetime.date(2024, 4, 22)))
    # print(len(ts_list))
    # for ts in ts_list:
    #     ts['payrun'] = payrun
    #     ts.save()
    # ts_list = models.Timesheet.search(date=q.between(datetime.date(2024, 4, 22), datetime.date(2024, 4, 28)))
    # ts_list = models.Timesheet.search()
    # print(len(ts_list))
    # for ts in ts_list:
    #     ts['payrun'] = None
    #     ts.save()
    # tenant = Tenant.get_by('name', 'RB Scaffolding')
    # account = Account.get_by('tenant_uid', tenant['uid'])
    # account['default_pay_entity'] = tenant
    # rbt = Tenant(name='RBT').save()
    # account['data_files'] = [tenant, rbt]
    # account.save()


def connect_to_qb():
    qb_auth_url = anvil.server.call('get_qb_auth_url', AppEnv.logged_user['tenant_uid'])
    print('qb_auth_url', qb_auth_url)
    anvil.js.window.location.href = qb_auth_url


def update_users():
    tenants = [*models.Tenant.search(tenant_uid=None)]
    for tenant in tenants:
        print('tenant', tenant['uid'])
        AppEnv.set_current_tenant(tenant_uid=tenant['uid'])
        user_role = [*models.UserRole.search(tenant_uid=tenant['uid'], type='account_admin')][0]
        print('user_role', user_role['uid'])
        users = models.User.search(tenant_uid=tenant['uid'])
        for user in users:
            print('user', user['uid'])
            user['user_role'] = user_role
            user.save()
    AppEnv.set_current_tenant(tenant_uid=SYSTEM_TENANT_UID)


def foo():
    bar()
    pass

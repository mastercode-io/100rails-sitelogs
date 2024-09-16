from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from AnvilFusion.components.SubformGrid import SubformGrid
# from AnvilFusion.components.ListBox import ListBox
from AnvilFusion.components.ListView import ListView
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
# from AnvilFusion.tools.utils import AppEnv
from ..app.models import Tenant, Account, User


ACCOUNT_TYPE_STANDARD = 'Standard'
ACCOUNT_TYPE_MULTI_ENTITY = 'Multiple Pay Entities'
ACCOUNT_TYPE_TEMPLATES = 'Payroll Templates'
ACCOUNT_TYPES = [ACCOUNT_TYPE_STANDARD, ACCOUNT_TYPE_MULTI_ENTITY, ACCOUNT_TYPE_TEMPLATES]


class SettingsForm(FormBase):
    def __init__(self, active_tab=None, **kwargs):
        print('SettingsForm')
        kwargs['model'] = 'Account'

        self.account = None
        self.active_tab = active_tab

        self.business_name_new = TextInput(name='business_name', label='Business Name',
                                           on_change=self.business_name_new_change, required=True)
        self.account_name_new = TextInput(name='name', label='Account Name', required=True)
        self.pay_entity_name = TextInput(name='pay_entity_name', label='Entity Name', save=False,
                                         required=True)
        self.account_type_new = DropdownInput(name='type', label='Account Type',
                                              options=ACCOUNT_TYPES, value=ACCOUNT_TYPE_STANDARD,
                                              required=True)
        self.payroll_template = DropdownInput(name='payroll_template', label='Payroll Template', save=False,
                                              options=['Standard', 'Advanced'], value='Standard')

        self.subtitle = SectionSubtitle(name='company_info', value='Company Info')
        self.account_name = TextInput(name='name', label='Account Name', required=True)
        self.business_name = TextInput(name='business_name', label='Business Name', required=True)
        self.address = MultiFieldInput(name='address', model='Account')
        self.phone = TextInput(name='phone', label='Phone')
        self.email = TextInput(name='email', label='Email')
        self.website = TextInput(name='website', label='Website')
        self.logo = InlineMessage(name='logo', label='Logo')
        self.subscription_dates = MultiFieldInput(name='subscription_dates', model='Account', label='_', cols=2)

        self.user_view_config = {
            'model': 'User',
            'columns': [
                {'name': 'tenant_name', 'label': 'Data File'},
                {'name': 'full_name', 'label': 'User Name'},
                {'name': 'email', 'label': 'Email'},
                {'name': 'enabled', 'label': 'Enabled'},
                {'name': 'permissions', 'label': 'Permissions'},
            ],
        }
        self.users = SubformGrid(name='users', label='User List', model='User', is_dependent=True,
                                 # link_model='Tenant', link_field='case_workflow',
                                 form_container_id=kwargs.get('target'),
                                 view_config=self.user_view_config,
                                 )

        # self.pay_entities_view_config = {
        #     'model': 'Tenant',
        #     'columns': [
        #         {'name': 'name', 'label': 'Entity Name'},
        #     ],
        #     'modes': ['Edit'],
        # }
        # self.pay_entities = SubformGrid(name='pay_entities', label='Pay Entities', model='Tenant',
        #                                 is_dependent=False, get_data=False,
        #                                 view_config=self.pay_entities_view_config,
        #                                 form_container_id=kwargs.get('target'))
        # pay_entities = Tenant.get_grid_view(view_config={'model': 'Tenant', 'columns': [{'name': 'name'}]})
        self.pay_entities_view = ListView(name='pay_entities_box', header='Pay Entities',
                                          text_field='name', value_field='uid',
                                          on_change=self.pay_entities_view_on_change,
                                          select='single',
                                          save=False)

        incoming_links_view = {
            'model': 'AppInApiCredential',
            'columns': [
                {'name': 'api_secret', 'label': 'API Secret'},
                {'name': 'api_key', 'label': 'API Key'},
                {'name': 'api_user.tenant_name', 'label': 'Tenant'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.incoming_links = SubformGrid(
            name='incoming_links', label='Incoming', model='AppInApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=incoming_links_view,
        )

        outgoing_links_view = {
            'model': 'AppOutApiCredential',
            'columns': [
                {'name': 'auth_type', 'label': 'Auth Type'},
                {'name': 'api_credentials', 'label': 'API Credentials'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.outgoing_links = SubformGrid(
            name='outgoing_links', label='Outgoing', model='AppOutApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=outgoing_links_view,
        )

        # self.payroll_settings_frame = ContentFrame(name='payroll_settings')
        # self.payroll_settings_page = PayrollSettingsPage(container_id=self.payroll_settings_frame.container_id,
        #                                                  account=self.account)

        tabs = [
            {
                'name': 'new_account', 'label': 'New Account Info', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [
                                self.subtitle,
                                self.business_name_new,
                                self.account_name_new,
                                self.pay_entity_name,
                                self.account_type_new,
                                self.payroll_template,
                            ],
                        ]
                    },
                ],
            },
            {
                'name': 'account', 'label': 'Account Info', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [
                                self.subtitle,
                                self.account_name,
                                self.business_name,
                                self.phone,
                                self.email,
                                self.website
                            ],
                            [self.address],
                            [self.pay_entities_view]
                        ]
                    },
                ],
            },
            {
                'name': 'subscription', 'label': 'Subscription', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [self.subscription_dates],
                            [],
                        ]
                    }
                ],
            },
            {
                'name': 'billing', 'label': 'Billing', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            # []
                        ]
                    }
                ],
            },
            {
                'name': 'users', 'label': 'Users', 'sections':
                [
                    {
                        'name': '_', 'rows': [
                            [self.users]
                        ]
                    }
                ],
            },
            {
                'name': 'integrations', 'label': 'Integrations', 'sections':
                [
                    {
                        'name': '_', 'cols': [
                            [self.incoming_links],
                            [self.outgoing_links]
                        ]
                    }
                ],
            },
        ]
        tabs_config = {
            'header_class': 'e-fill pl-settings-dialog-tabs-header',
        }

        super().__init__(tabs=tabs,
                         header='Account Settings',
                         buttons_mode=kwargs.pop('buttons_mode', 'off'),
                         css_class=kwargs.pop('css_class', 'pl-settings-dialog'),
                         tabs_config=tabs_config,
                         fullscreen=kwargs.pop('fullscreen', True),
                         **kwargs)
        # self.fullscreen = True
        # self.pay_entities.bounding_box_id = self.container_uid


    def form_open(self, args, **kwargs):
        print('AccountForm.form_open')
        # super().form_open(args)
        print(self.data)
        if self.data['uid']:
            print('Update Account')
            print('active tab', self.active_tab)
            super().form_open(args)
            self.tabs.items[0].disabled = True
            self.tabs.items[0].visible = False
            for i, tab in enumerate(self.tabs.items[1:], start=1):
                tab.disabled = False
                tab.visible = True
                print(i, tab.id)
                if self.active_tab and tab.id == self.active_tab:
                    self.tabs.select(i)
            self.form.height = '80%'
            self.form.width = '80%'
            self.pay_entities_view.show()
            print(self.data['uid'], self.data['tenant_uid'])
            self.account = Account.get(self.data['uid'])
            print('business', self.account)
            self.account_name.value = self.account['name']
            self.business_name.value = self.account['name']
            self.phone.value = self.account['phone']
            self.email.value = self.account['email']
            self.website.value = self.account['website']
            self.address.value = self.account['address']
            self.subscription_dates.value = self.account['subscription_dates']

            user_list = []
            pay_entity_list = []
            for tenant in self.account['pay_entities']:
                print('tenant', tenant['uid'])
                user_list += User.get_grid_view(
                    view_config=self.user_view_config,
                    filters={'tenant_uid': tenant['uid']}
                )
                pay_entity_list.append(tenant.to_json_dict())
            print('user_list', user_list)
            print('pay_entity_list', pay_entity_list)
            self.users.value = user_list
            self.pay_entities_view.options = pay_entity_list
            # super().form_open(args)

        else:
            super().form_open(args)
            self.form.header = 'Create Account'
            print('Create Account', self.tabs.items)
            for tab in self.tabs.items[1:]:
                tab.disabled = True
                tab.visible = False
            self.pay_entities_view.hide()
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Create Account'
            self.form.height = 'auto'
            self.form.width = POPUP_WIDTH_COL2
        # super().form_open(args)


    def form_cancel(self, args):
        # AppEnv.reset_tenant()
        super().form_cancel(args)


    def form_save(self, args, **kwargs):

        if not self.data['uid']:
            add_new = True
            tenant = Tenant(name=self.pay_entity_name.value).save()
            print('a) tenant', tenant['uid'], tenant['tenant_uid'])
            tenant['tenant_uid'] = tenant['uid']
            tenant.save()
            print('b) tenant', tenant['uid'], tenant['tenant_uid'])
            # AppEnv.set_tenant(tenant_uid=tenant.uid)
            self.account = Account(
                tenant_uid=tenant['uid'],
                name=self.account_name_new.value,
                business_name=self.business_name_new.value,
                type=self.account_type_new.value,
                default_pay_entity=tenant,
                pay_entities=[tenant],
            ).save()
            tenant['account_uid'] = self.account['uid']
            tenant.save()
            self.form.header = 'Update Business Account'
            buttons = self.form.getButtons()
            for button in buttons:
                if button.cssClass == 'da-save-button':
                    button.content = 'Save'
                # for i in range(1, 4):
                #     self.tabs.enableTab(i, True)
            self.users.filters = {'tenant_uid': tenant['uid']}
            self.users.value = tenant
            self.data = self.account
            self.form_open(None, **kwargs)

        else:
            add_new = False
            self.account['name'] = self.business_name.value
            self.account['phone'] = self.phone.value
            self.account['email'] = self.email.value
            self.account['website'] = self.website.value
            self.account['address'] = self.address.value
            self.account['subscription_dates'] = self.subscription_dates.value
            self.account.save()

        self.update_source(self.data, add_new)


    def business_name_new_change(self, args):
        print('business_name_new_change', args)
        if not self.account_name_new.value:
            self.account_name_new.value = self.business_name_new.value
        if not self.pay_entity_name.value:
            self.pay_entity_name.value = self.business_name_new.value


    def pay_entities_view_on_change(self, args):
        print('pay_entities_view_on_change', args)
        print(self.pay_entities_view.value)


    def create_enums(self):
        pass


    def create_components(self):
        pass


    def create_user_roles(self):
        pass


    def create_pay_rules(self):
        pass


    def create_pay_templates(self):
        pass

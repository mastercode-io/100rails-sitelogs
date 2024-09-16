from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.Inputs import InplaceEditor
from AnvilFusion.components.Layouts import Tabs
from AnvilFusion.tools.utils import AppEnv
from ...app.models import Account, Tenant, PayrollConfig
import datetime
import time


class SettingsPage(PageBase):
    def __init__(self, account=None, **kwargs):
        print('SettingsPage')
        title = 'Settings'
        self.account = account
        if self.account is None:
            self.tenant = Tenant.get(AppEnv.logged_user.tenant_uid)
            self.account = Account.get(self.tenant['account_uid'])

        if self.account is None:
            self.error_message = InlineMessage(content='No account found', accent='warning', css_class='pl-message-bar')
            self.content = f'<div id="{self.error_message.container_id}"></div>'

        else:
            # self.users = SubformGrid(name='users',
            #                          model='User',)
            tabs_config = [
                {'name': 'account', 'label': 'Account Info', 'content': ''},
                {'name': 'subscription', 'label': 'Subscription', 'content': ''},
                {'name': 'billing', 'label': 'Billing', 'content': ''},
                {'name': 'users', 'label': 'Users', 'content': ''},
                {'name': 'pay_entities', 'label': 'Data Files', 'content': ''},
                {'name': 'payroll', 'label': 'Payroll', 'content': ''},
                {'name': 'integrations', 'label': 'Integrations', 'content': ''},
            ]
            self.settings_tabs = Tabs(tabs_config=tabs_config)
            self.content = f'<div id="{self.settings_tabs.container_id}"></div>'

            self.users = GridView(
                model='Timesheet',
                container_id=self.settings_tabs.items['users']['content_id'],
                grid_height_offset=150,
            )
            self.subscription = TextInput(name='subscription',
                                          label='Subscription',
                                          container_id=self.settings_tabs.items['subscription']['content_id'],
                                          value='Free')

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)
        self.users.bounding_box_id = self.settings_tabs.tabs_id


    def form_show(self, **args):
        super().form_show(**args)
        if self.account is None:
            self.error_message.show()
        else:
            self.settings_tabs.form_show()
            self.settings_tabs.set_tab_content(tab_name='account', content='Basic account info')
            self.users.form_show()
            self.subscription.show()

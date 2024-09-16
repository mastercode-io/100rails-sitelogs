from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from ..app.models import PayrollConfig, AppIntegration, AppIntegrationConnection, SYSTEM_TENANT_UID
from ..Pages.widgets import StepperWidget

PAYRUN_FREQUENCY = ['Weekly', 'Fortnightly', 'Monthly']
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
PAY_CATEGORY_TYPES = {
    'Single': 'Single category for each pay rule',
    'Role': 'Pay category for each pay rule/employee role',
}


class PayrollSettingsForm(FormBase):
    def __init__(self,
                 payroll_integration_data=None,
                 **kwargs):
        print('PayrollSettingsForm')
        kwargs['model'] = 'PayrollConfig'

        payroll_config = next(iter(PayrollConfig.search()), None)
        action = 'view' if payroll_config else 'edit'

        # save the payroll integration data if it was passed
        payroll_integration_data = payroll_integration_data
        print('payroll_config', payroll_config)
        print('payroll_integration_data', payroll_integration_data)
        if (payroll_config and payroll_integration_data
                and payroll_integration_data.get('tenant_uid', None) == AppEnv.logged_user.tenant_uid):
            service_uid = payroll_integration_data.get('service_uid', None)
            connection_data = payroll_integration_data.get('connection_data', {})
            payroll_integration = AppIntegration.get(service_uid)
            if payroll_integration['auth_type'] == 'API Key':
                payroll_connection = AppIntegrationConnection(
                    integration=payroll_integration,
                    api_key=connection_data.get('api_key', None),
                    api_user=connection_data.get('api_user', None),
                )
            else:
                payroll_connection = AppIntegrationConnection(
                    integration=payroll_integration,
                    auth_credentials=connection_data,
                )
            payroll_connection.save()
            payroll_config['payroll_integration'] = payroll_integration
            payroll_config['payroll_connection'] = payroll_connection
            payroll_config.save()
        print('payroll_connection', payroll_config['payroll_connection'])

        # Fields
        self.payrun_initial_date = DateInput(name='payrun_initial_date', label='Initial Payrun Date',
                                             string_format='d MMM yyy', required=True)

        self.integrations_subtitle = InlineMessage(content='Integrations',)
        self.use_payroll_integration = CheckboxInput(name='use_integration', label='Payroll Integration',
                                                     value=False,
                                                     on_change=self.use_payroll_integration_changed)
        self.payroll_integration = LookupInput(name='payroll_integration', label='Select Payroll App',
                                               model='AppIntegration', text_field='service_name',
                                               get_data=False, hidden=True,
                                               on_change=self.payroll_integration_selected)
        self.payroll_connection = LookupInput(name='payroll_connection', hidden=True)
        self.payroll_connection_message = InlineMessage(css_class='pl-message-bar')
        self.payroll_connection_button = Button(content='Create Connection to Payroll',
                                                action=self.create_payroll_connection, hidden=True)

        self.timesheet_integration_subtitle = InlineMessage(content='Time Tracking',)
        self.use_timesheet_integration = CheckboxInput(name='use_integration', label='Time Tracking Integration',
                                                       value=False, enabled=False,
                                                       on_change=self.use_timesheet_integration_changed)
        self.timesheet_integration = LookupInput(name='timesheet_integration', label='Select Time Tracking App',
                                                 model='AppIntegration', text_field='service_name',
                                                 get_data=False, hidden=True,
                                                 on_change=self.timesheet_integration_selected)
        self.timesheet_connection = LookupInput(name='timesheet_connection', hidden=True)
        self.timesheet_connection_message = InlineMessage(css_class='pl-message-bar', hidden=True)
        self.timesheet_connection_button = Button(content='Create Connection to Time Tracking',
                                                  action=self.create_timesheet_connection, hidden=True)

        self.frequency = DropdownInput(name='frequency', label='Pay Cycle Frequency',
                                       options=PAYRUN_FREQUENCY, value='Weekly',
                                       required=True)
        self.pay_period_start_day = DropdownInput(name='pay_period_start_day', label='Pay Period Start Day',
                                                  options=WEEK_DAYS, value='Monday',
                                                  required=True)
        self.pay_period_end_day = DropdownInput(name='pay_period_end_day', label='Pay Period End Day',
                                                options=WEEK_DAYS, value='Sunday',
                                                required=True)
        self.pay_day = DropdownInput(name='pay_day', label='Pay Day', options=WEEK_DAYS, value='Friday',
                                     required=True)

        self.pay_category_type = DropdownInput(name='pay_category_type', label='Pay Category Type',
                                               options=list(PAY_CATEGORY_TYPES.keys()), value='Single',
                                               on_change=self.pay_category_type_selected,
                                               required=True, save=False)

        self.public_holidays = InlineMessage(name='public_holidays', label='Public Holidays',
                                             content='Public holidays will be displayed here')
        self.payroll_rdo = InlineMessage(name='payroll_rdo', label='RDOs',
                                         content='RDOs will be displayed here')

        # Buttons
        self.action_button = Button(content='Edit',
                                    container_id='payrun-settings-action-button',
                                    action=self.action_handler)
        self.cancel_button = Button(content='Cancel',
                                    container_id='payrun-settings-cancel-button',
                                    action=self.cancel_handler)

        # Header
        self.form_header = f'\
            <div class="pl-form-header">\
                <div class="pl-form-header-title" style="float: left">Payroll Settings</div>\
                <div id="payrun-settings-cancel-button" style="float: right; margin-left: 15px;">{self.cancel_button}</div>\
                <div id="payrun-settings-action-button" style="float: right">{self.action_button}</div>\
            </div>'

        tabs = [
            {
                'name': 'payroll_calendar', 'label': 'Pay Calendar', 'sections': [
                    {
                        'name': 'pay_period', 'label': 'Pay Period', 'label_style': 'margin-bottom:10px',
                        'cols': [
                            [
                                self.frequency,
                                self.pay_period_start_day,
                                self.pay_period_end_day,
                                self.pay_day,
                            ],
                            [
                                self.public_holidays,
                                self.payroll_rdo,
                             ],
                            [
                                self.payrun_initial_date,
                                self.integrations_subtitle,
                                self.use_payroll_integration,
                                self.payroll_integration,
                                self.payroll_connection_message,
                                self.payroll_connection_button,
                                self.use_timesheet_integration,
                                self.timesheet_integration,
                                self.timesheet_connection_message,
                                self.timesheet_connection_button,
                            ]
                        ]
                    },
                ]
            },
            {
                'name': 'pay_templates', 'label': 'Pay Templates', 'sections': []
            },
            # {
            #     'name': 'payroll_integrations', 'label': 'Payroll Integrations', 'sections': []
            # }
        ]
        tabs_config = {
            'header_class': 'e-fill',
        }

        app_list = [app.to_json_dict() for app in AppIntegration.search(tenant_uid=SYSTEM_TENANT_UID)]
        self.payroll_integration.data = [app for app in app_list if app['service_type'] == 'Payroll']
        self.timesheet_integration.data = [app for app in app_list if app['service_type'] == 'Time Tracking']

        super().__init__(header=self.form_header,
                         # sections=sections,
                         tabs=tabs,
                         tabs_config=tabs_config,
                         action=action,
                         buttons_mode='off',
                         data=payroll_config,
                         **kwargs)
        self.fullscreen = True
        self.opened = False

    def form_open(self, args, **kwargs):
        super().form_open(args)
        self.payroll_integration.hide()
        # self.payroll_connection_message.hide()
        self.payroll_connection_button.hide()
        self.timesheet_integration.hide()
        self.timesheet_connection_message.hide()
        self.timesheet_connection_button.hide()
        self.action_button.content = 'Edit' if self.action == 'view' else 'Save'
        self.action_button.show()
        if self.action == 'edit':
            self.cancel_button.show()
        self.integration_actions()
        # if not self.opened:
        #     self.payrun_flow_steps_view.show()
        #     self.payrun_flow_steps_widget.form_show(height=self.form.element.offsetHeight - 100)
        #     self.opened = True
        # self.payrun_flow_changed(args)

    def action_handler(self, args):
        print('action_handler', args, self.action)
        if self.action == 'view':
            self.action = 'edit'
            self.frequency.enabled = True
            self.pay_period_start_day.enabled = True
            self.pay_period_end_day.enabled = True
            self.pay_day.enabled = True
            self.payrun_initial_date.enabled = True
            self.pay_category_type.enabled = True
            self.use_payroll_integration.enabled = True
            self.payroll_integration.enabled = True
            self.use_timesheet_integration.enabled = True
            self.timesheet_integration.enabled = True
        else:
            super().form_save(args, hide=False)
            self.action = 'view'
            payroll_config = next(iter(PayrollConfig.search()), None)
            if payroll_config:
                self.data = payroll_config
            # self.integration.enabled = False
            # self.frequency.enabled = False
            # self.pay_period_start_day.enabled = False
            # self.pay_period_end_day.enabled = False
            # self.pay_day.enabled = False
            # self.payrun_initial_date.enabled = False
            # self.pay_category_type.enabled = False
            # self.use_integration.enabled = False
            # self.integration.enabled = False
        self.form_open(args)


    def cancel_handler(self, args):
        print('cancel_handler', args)
        self.action = 'view'
        self.cancel_button.hide()
        self.form_open(args)


    def integration_actions(self):
        print('integration_actions')
        if self.data['payroll_integration'] is not None:
            print('payroll_integration', self.data['payroll_integration'])
            self.use_payroll_integration.value = True
            self.payroll_integration.show()
            self.payroll_integration.value = self.data['payroll_integration']
            # print(self.action, self.data['payroll_connection'])
            # if self.action == 'edit':
            #     if self.data['payroll_connection'] is None:
            #         self.payroll_connection_button.show()
            # else:
            #     self.payroll_integration.enabled = False

        if self.data['timesheet_integration'] is not None:
            print('timesheet_integration', self.data['timesheet_integration'])
            self.use_timesheet_integration.value = True
            self.timesheet_integration.show()
            self.timesheet_integration.value = self.data['timesheet_integration']
            if self.action == 'edit':
                if self.data['timesheet_connection'] is None:
                    self.timesheet_connection_button.show()
            else:
                self.timesheet_integration.enabled = False

        if self.action == 'edit':
            self.payroll_connection_message.show()
            self.payroll_connection_button.show()
            # self.timesheet_connection_button.hide()
        else:
            # self.payroll_connection_message.hide()
            self.payroll_connection_button.hide()
            # self.timesheet_connection_button.hide()


    def payrun_flow_changed(self, args):
        print('payrun_flow_changed', args)
        flow_steps = []
        step_num = 0
        for field in self.payrun_flow_steps_field.fields:
            if field.value is True:
                step_num += 1
                flow_steps.append({'label': field.label, 'iconCss': f'fa-solid fa-circle-{step_num}'})
        self.payrun_flow_steps_widget.steps = flow_steps

    def payroll_integration_selected(self, args):
        print('integration_selected', args)
        if not args.get('value') and not self.payroll_integration.value:
            self.payroll_connection_message.accent = 'info'
            self.payroll_connection_message.content = ''
            # self.payroll_connection_button.hide()
        else:
            integration = AppIntegration.get(self.payroll_integration.value['uid'])
            connection = AppIntegrationConnection.get_by('integration', integration)
            print('integration', integration)
            print('payroll_connection', connection)
            print(self.data['payroll_integration']['uid'], self.payroll_integration.value['uid'])
            self.payroll_connection.value = connection
            print('payroll_connection.value', self.payroll_connection.value)
            self.payroll_connection_message.show()
            if (self.data['payroll_integration']['uid'] == self.payroll_integration.value['uid']
                    and self.payroll_connection.value is not None):
                self.payroll_connection_message.accent = None
                self.payroll_connection_message.content = (f"Connected to "
                                                           f"<b>{self.payroll_integration.value['name']}</b>")
                self.payroll_connection_button.content = (f"Update Connection to "
                                                          f"{self.data['payroll_integration']['service_name']}")
            else:
                self.payroll_connection_message.accent = 'warning'
                self.payroll_connection_message.content = (f"No connection found for this integration: "
                                                           f"<b>{self.payroll_integration.value['name']}</b>")
                self.payroll_connection_button.content = (f"Create Connection to "
                                                          f"{self.payroll_integration.value['name']}")
            if self.action == 'edit':
                self.payroll_connection_button.show()

    def use_payroll_integration_changed(self, args):
        print('use_integration_changed', args)
        if self.use_payroll_integration.value is True:
            self.payroll_integration.show()
        else:
            self.payroll_integration.hide()

    def timesheet_integration_selected(self, args):
        print('timesheet_integration_selected', args)
        # if not args.get('value') or not self.timesheet_integration.value:
        #     self.timesheet_connection_message.accent = None
        #     self.timesheet_connection_message.content = ''
        #     self.timesheet_connection_button.hide()
        # else:
        #     timesheet_integration = AppIntegration.get(self.timesheet_integration.value['uid'])
        #     timesheet_connection = AppIntegrationConnection.get_by('integration', timesheet_integration)
        #     if not timesheet_connection:
        #         self.timesheet_connection_message.accent = 'warning'
        #         self.timesheet_connection_message.content = (f"No connection found for this integration: "
        #                                                      f"<b>{self.timesheet_integration.value['name']}</b>")
        #         if self.action == 'edit':
        #             self.timesheet_connection_button.show()
        #         if self.action == 'view':
        #             self.timesheet_connection_button.enabled = False

    def use_timesheet_integration_changed(self, args):
        print('use_integration_changed', args)
        if self.use_timesheet_integration.value is True:
            self.timesheet_integration.show()
        else:
            self.timesheet_integration.hide()

    def pay_category_type_selected(self, args):
        print('pay_category_type_selected', args)
        if not args.get('value') or not self.pay_category_type.value:
            self.pay_category_type.value = 'single'
        if self.pay_category_type.value == 'single':
            self.pay_category_type.label = PAY_CATEGORY_TYPES['single']
        elif self.pay_category_type.value == 'role':
            self.pay_category_type.label = PAY_CATEGORY_TYPES['role']

    def create_payroll_connection(self, args):
        print('create_connection', args)
        self.form_save(None, hide=False)
        self.payroll_connection_message.accent = 'info'
        self.payroll_connection_message.content = 'Creating connection...'
        auth_url = None
        if self.payroll_integration.value['name'] == 'QuickBooks':
            auth_url = anvil.server.call('get_qb_auth_url',
                                         AppEnv.logged_user['tenant_uid'],
                                         self.payroll_integration.value['uid'])
        if self.payroll_integration.value['name'] == 'Xero':
            auth_url = anvil.server.call('get_xero_auth_url',
                                         AppEnv.logged_user['tenant_uid'],
                                         self.payroll_integration.value['uid'])
        print('auth_url', auth_url)
        if auth_url is not None:
            anvil.js.window.location.href = auth_url


    def create_timesheet_connection(self, args):
        print('create_connection', args)
        self.timesheet_connection_message.accent = 'info'
        self.timesheet_connection_message.content = 'Creating connection...'

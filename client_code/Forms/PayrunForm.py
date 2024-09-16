from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
from ..app.models import Payrun, PayrollConfig
import anvil.tables as tables
import datetime
import calendar


PAYRUN_STATUSES = [
    'Created',
    'Preview',
    'Approved',
    'Submitted',
    'Paid'
]
PAY_DAY_DELTA = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
}
DATE_FORMAT = 'd MMM yyyy'


class PayrunForm(FormBase):
    def __init__(self, **kwargs):
        print('PayrunForm')
        kwargs['model'] = 'Payrun'

        self.message = InlineMessage()
        self.select_pay_period = DropdownInput(name='select_pay_period', label='Select Pay Period',
                                               save=False
                                               )
        self.pay_period_start = DateInput(name='pay_period_start', label='Pay Period Start',
                                          string_format=DATE_FORMAT, enabled=False)
        self.pay_period_end = DateInput(name='pay_period_end', label='Pay Period End',
                                        string_format=DATE_FORMAT, enabled=False)
        self.pay_date = DateInput(name='pay_date', label='Pay Date', string_format=DATE_FORMAT,)
        self.status = DropdownInput(name='status', label='Status', options=PAYRUN_STATUSES, value='Created',
                                    enabled=True)
        self.notes = MultiLineInput(name='notes', label='Notes', rows=4)

        payrun_items_view = {
            'model': 'PayrunItem',
            'columns': [
                {'name': 'employee.full_name', 'label': 'Employee'},
                {'name': 'timesheet.date', 'label': 'Timesheet Date'},
                {'name': 'pay_category.name', 'label': 'Category'},
                {'name': 'pay_rate', 'label': 'Rate'},
                {'name': 'units', 'label': 'Units'},
                {'name': 'amount', 'label': 'Amount'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ]
        }
        self.show_payrun_items = CheckboxInput(name='show_payrun_items', label='Show Payrun Items',
                                               value=False, save=False,
                                               on_change=self.show_payrun_items_switch)
        self.payrun_items = SubformGrid(name='payrun_items', label='Payrun Items', model='PayrunItem',
                                        link_model='PayRun', link_field='payrun',
                                        form_container_id=kwargs.get('target'),
                                        view_config=payrun_items_view,
                                        )

        sections = [
            {
                'name': '_', 'rows': [
                    [self.message],
                ]
            },
            {
                'name': '_', 'cols': [
                    [self.pay_period_start, self.pay_period_end, self.pay_date,
                     self.show_payrun_items],
                    [self.notes, self.status],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.payrun_items],
                ]
            }
        ]

        if kwargs.get('data') is None or kwargs['data']['uid'] is None:
            super().__init__(sections=sections,
                             width=POPUP_WIDTH_COL3,
                             header='Create Payrun',
                             button_save_label='Create',
                             **kwargs)
            self.create = True
        else:
            super().__init__(sections=sections,
                             width=POPUP_WIDTH_COL3,
                             header='View Payrun',
                             **kwargs)
            self.create = False

        # super().__init__(sections=sections, **kwargs)
        self.payroll_config = next(iter(PayrollConfig.search()), None)


    def form_open(self, args, **kwargs):
        if not self.payroll_config:
            self.message.message_type = 'e-warning'
            self.message.content = 'Payrun settings not configured'
            self.action = 'view'
        super().form_open(args, **kwargs)
        if not self.fullscreen:
            self.payrun_items.hide()
        if self.action == 'add':
            self.set_payrun_dates()
            self.show_payrun_items.hide()


    def set_payrun_dates(self):
        if self.payroll_config:
            last_payrun = next(iter(Payrun.search(
                search_query=tables.order_by('pay_period_start', ascending=False),
            )), None)
            if last_payrun:
                self.pay_period_start.value = last_payrun['pay_period_end'] + datetime.timedelta(days=1)
            else:
                self.pay_period_start.value = self.payroll_config['payrun_initial_date']
            if self.payroll_config['frequency'] == 'Weekly':
                self.pay_period_end.value = self.pay_period_start.value + datetime.timedelta(days=6)
            elif self.payroll_config['frequency'] == 'Fortnightly':
                self.pay_period_end.value = self.pay_period_start.value + datetime.timedelta(days=13)
            elif self.payroll_config['frequency'] == 'Monthly':
                self.pay_period_end.value = self.pay_period_start.value + datetime.timedelta(
                    days=calendar.monthrange(self.pay_period_start.value.year, self.pay_period_start.value.month)[1])
            self.pay_date.value = self.pay_period_end.value + datetime.timedelta(
                days=PAY_DAY_DELTA[self.payroll_config['pay_day']]
            )

    def show_payrun_items_switch(self, args):
        if self.show_payrun_items.value:
            if not self.fullscreen:
                self.fullscreen = True
                self.form.show(True)
            else:
                self.payrun_items.show()
                self.show_payrun_items.hide()
                self.show_payrun_items.value = False


from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
import anvil.tables.query as q
from ..app.models import EmployeeRole


class TimesheetForm(FormBase):
    def __init__(self, **kwargs):
        print('TimesheetForm')
        kwargs['model'] = 'Timesheet'

        roles = [*EmployeeRole.search(name=q.any_of(q.ilike('%manager%'), q.ilike('%supervisor%')))]
        approved_by_filters = {
            'role': roles,
        }

        self.employee = LookupInput(name='employee', label='Employee', model='Employee', text_field='full_name')
        self.date = DateInput(name='date', label='Date')
        self.job = LookupInput(name='job', label='Job Name', model='Job')
        self.start_time = TimeInput(name='start_time', label='Start Time')
        self.end_time = TimeInput(name='end_time', label='End Time')
        self.status = DropdownInput(name='status', label='Status', options=['Draft', 'Approved', 'Processed'])
        self.approved_by = LookupInput(name='approved_by', label='Approved By', model='Employee', text_field='full_name',
                                       filters=approved_by_filters)
        self.notes = MultiLineInput(name='notes', label='Notes')
        self.total_pay = NumberInput(name='total_pay', label='Total Pay')
        self.pay_lines = InlineMessage(name='pay_lines', label='Pay Lines', css_class='pl-message-field')

        sections = [
            {
                'name': '_', 'cols': [
                    [self.employee, self.job, self.approved_by, self.status],
                    [self.date, self.start_time, self.end_time, self.total_pay],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.pay_lines],
                    [self.notes],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        if self.data['status'] == 'Processed':
            self.action = 'view'
            self.form.header = 'View Timesheet'

    def form_open(self, args, **kwargs):
        super().form_open(args, **kwargs)
        print('TimesheetForm.form_open', self.data['pay_lines'])
        if self.data['pay_lines']:
            self.pay_lines.content = self.data['pay_lines_view']
            self.pay_lines.show()
        else:
            self.pay_lines.hide()

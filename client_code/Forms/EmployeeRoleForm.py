from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class EmployeeRoleForm(FormBase):
    def __init__(self, **kwargs):
        print('EmployeeRoleForm')
        kwargs['model'] = 'EmployeeRole'

        self.name = TextInput(name='name', label='Name')
        self.pay_rate = NumberInput(name='pay_rate', label='Pay Rate')
        self.pay_rate_template = LookupInput(
            name='pay_rate_template',
            label='Pay Rate Template',
            model='PayRateTemplate'
        )
        self.status = DropdownInput(
            name='status',
            label='Status',
            options=['Active', 'Inactive', 'Draft']
        )

        fields = [
            self.name,
            self.pay_rate,
            self.pay_rate_template,
            self.status
        ]

        super().__init__(fields=fields, **kwargs)

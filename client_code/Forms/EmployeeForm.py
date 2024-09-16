from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class EmployeeForm(FormBase):
    def __init__(self, **kwargs):
        print('EmployeeForm')
        kwargs['model'] = 'Employee'

        self.first_name = TextInput(name='first_name', label='First Name')
        self.last_name = TextInput(name='last_name', label='Last Name')
        self.email = TextInput(name='email', label='Email')
        self.mobile = TextInput(name='mobile', label='Mobile')
        self.role = LookupInput(name='role', label='Role', model='EmployeeRole')
        self.pay_rate = NumberInput(name='pay_rate', label='Pay Rate', number_format='c2')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'])
        self.address = MultiFieldInput(name='address', label='_', model='Employee')
        # self.custom_fields = MultiFieldInput(name='custom_fields', label='Custom Fields', model='Employee')

        sections = [
            {
                'name': '_', 'cols': [
                    [
                         self.first_name,
                         self.last_name,
                         self.email,
                         self.mobile,
                         self.role,
                         self.pay_rate,
                         self.status
                    ],
                    [self.address],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True

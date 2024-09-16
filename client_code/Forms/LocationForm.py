from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class LocationForm(FormBase):
    def __init__(self, **kwargs):
        print('LocationForm')
        kwargs['model'] = 'Location'

        self.name = TextInput(name='name', label='Name')
        self.description = MultiLineInput(name='description', label='Description')
        self.address = MultiFieldInput(name='address', model='Location', label='_')
        self.pay_rate_template = LookupInput(name='pay_rate_template', label='Pay Rate Template', model='PayRateTemplate')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'])


        sections = [
            {
                'name': '_', 'cols': [
                    [self.name, self.description, self.pay_rate_template, self.status],
                    [self.address],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

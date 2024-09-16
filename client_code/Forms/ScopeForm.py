from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.MultiFieldInput import MultiFieldInput
from ..app.models import JobType


class ScopeForm(FormBase):
    def __init__(self, **kwargs):
        print('ScopeForm')
        kwargs['model'] = 'Scope'

        self.name = TextInput(name='name', label='Name')
        self.type = LookupInput(name='type', label='Scope Type', model='ScopeType',
                                on_change=self.scope_type_on_change)
        self.short_code = DropdownInput(name='short_code', label='Short Code', enabled=False)
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')
        # self.custom_fields = MultiFieldInput(name='custom_fields', label='Custom Fields', model='Scope', cols=2)

        fields = [
            self.name,
            self.type,
            self.short_code,
            self.description,
            self.status,
        ]

        super().__init__(fields=fields, **kwargs)
        self.scope_type_on_change({})

    def scope_type_on_change(self, args):
        if self.type.value is None or args.get('value', None) is None:
            self.short_code.options = []
        elif self.type.value['name'] == 'Job Type':
            self.short_code.options = [j['short_code'] for j in JobType.search()]
        else:
            self.short_code.options = []
        self.short_code.enabled = True if self.short_code.options else False
        self.short_code.value = self.data['short_code']

from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
# from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class AppEnumForm(FormBase):
    def __init__(self, **kwargs):
        print('AppEnumForm')
        kwargs['model'] = 'AppEnum'

        self.name = TextInput(name='name', label='Name (ID)')
        self.description = MultiLineInput(name='description', label='Description')
        self.options = MultiLineInput(name='options', label='Options', rows=5, is_object=True)

        sections = [
            {
                'name': '_', 'cols': [
                    [
                         self.name,
                         self.description,
                    ],
                    [
                         self.options,
                    ],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

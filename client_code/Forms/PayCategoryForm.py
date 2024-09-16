from AnvilFusion.components.FormBase import FormBase
from AnvilFusion.components.FormInputs import *


class PayCategoryForm(FormBase):
    def __init__(self, **kwargs):
        print('PayCategoryForm')
        kwargs['model'] = 'PayCategory'


        sections = [
            {
              'name': '_', 'rows': [
                {}
            ]
            },
            {
                'name': '_', 'cols': [
                    [],
                    [],
                ]
            }
        ]

        super().__init__(sections=sections, **kwargs)
        # self.fullscreen = True

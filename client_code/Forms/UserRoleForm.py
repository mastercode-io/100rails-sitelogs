from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL3
from AnvilFusion.components.FormInputs import *
from AnvilFusion.tools.utils import AppEnv
# from AnvilFusion.components.MultiFieldInput import MultiFieldInput


class UserRoleForm(FormBase):
    def __init__(self, **kwargs):
        print('UserRoleForm')
        kwargs['model'] = 'UserRole'

        role_types = [{'id': k, 'text': v} for k, v in AppEnv.enum_constants['USER_ROLE_TYPES'].items()]
        # role_types = []
        print('role_types', role_types)
        self.name = TextInput(name='name', label='Name')
        self.type = DropdownInput(name='type', label='Type', options=role_types,
                                  text_field='text', value_field='id')
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.permissions = MultiLineInput(name='permissions', label='Permissions',
                                          rows=3, is_object=True)
        self.access_permissions = MultiLineInput(name='access_permissions', label='Access Permissions',
                                                 rows=5, is_object=True)

        sections = [
            {
                'name': '_', 'cols': [
                    [self.name, self.type],
                    [self.description],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.permissions],
                    [self.access_permissions],
                ]
            }
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL3, **kwargs)

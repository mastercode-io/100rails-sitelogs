from AnvilFusion.components.FormBase import FormBase, POPUP_WIDTH_COL2
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.components.GridView import GRID_TOOLBAR_COMMAND_SEARCH, GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE
from AnvilFusion.components.MultiFieldInput import MultiFieldInput


SERVICE_TYPES = [
    'Time Tracking',
    'Payroll',
]
CONNECTION_TYPES = [
    'OAuth',
    'API Key',
    'Username/Password',
]


class AppIntegrationForm(FormBase):
    def __init__(self, **kwargs):
        print('AppIntegrationForm')
        kwargs['model'] = 'AppIntegration'

        self.service_name = TextInput(name='service_name', label='Service Name', required=True)
        self.type = DropdownInput(name='type', label='Service Type',
                                  options=SERVICE_TYPES, required=True)
        self.url = TextInput(name='url', label='URL')
        self.connection_type = DropdownInput(name='connection_type', label='Connection Type',
                                             options=CONNECTION_TYPES,
                                             required=True)
        self.description = MultiLineInput(name='description', label='Description', rows=4)
        self.status = DropdownInput(name='status', label='Status',
                                    options=['Active', 'Inactive'], required=True)

        incoming_links_view = {
            'model': 'AppInApiCredential',
            'columns': [
                {'name': 'api_secret', 'label': 'API Secret'},
                {'name': 'api_key', 'label': 'API Key'},
                {'name': 'api_user.tenant_name', 'label': 'Tenant'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.incoming_links = SubformGrid(
            name='incoming_links', label='Incoming API Links', model='AppInApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=incoming_links_view,
        )

        outgoing_links_view = {
            'model': 'AppOutApiCredential',
            'columns': [
                {'name': 'auth_type', 'label': 'Auth Type'},
                {'name': 'api_credentials', 'label': 'API Credentials'},
                {'name': 'status', 'label': 'Status'},
            ],
            'toolbar': [
                GRID_TOOLBAR_COMMAND_SEARCH,
                GRID_TOOLBAR_COMMAND_SEARCH_TOGGLE,
            ],
            'content_wrap': False,
        }
        self.outgoing_links = SubformGrid(
            name='outgoing_links', label='Outgoing API Links', model='AppOutApiCredential',
            link_model='AppIntegration', link_field='integration',
            form_container_id=kwargs.get('target'),
            view_config=outgoing_links_view,
        )

        sections = [
            {
                'name': '_',
                'cols': [
                    [self.service_name, self.type, self.url, self.connection_type],
                    [self.description, self.status],
                ]
            },
            {
                'name': '_',
                'cols': [
                    [self.incoming_links],
                    [self.outgoing_links],
                ]
            },
        ]

        super().__init__(sections=sections, width=POPUP_WIDTH_COL2, **kwargs)
        self.fullscreen = True

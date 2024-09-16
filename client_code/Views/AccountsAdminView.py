import time
stime = time.time()
from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv
print('AccountsAdminView import modules:', time.time() - stime)


class AccountsAdminView(GridView):
    def __init__(self, **kwargs):
        print('AccountsAdminView')
        view_config = {
            'model': 'Account',
            'columns': [
                {'name': 'name', 'label': 'Account Name'},
                {'name': 'business_name', 'label': 'Business Name'},
                {'name': 'default_pay_entity.name', 'label': 'Default Pay Entity'},
                {'name': 'pay_entities.name', 'label': 'Pay Entities'},
                {'name': '_spacer', 'no_data': True},
            ],
        }

        # context_menu_items = [
        #     {'id': 'select_tenant', 'label': 'Lock Dataset', 'action': lock_dataset},
        #     {'id': 'reset_tenant', 'label': 'Reset Dataset', 'action': reset_dataset},
        # ]
        stime = time.time()
        super().__init__(
            model='Account',
            view_config=view_config,
            # context_menu_items=context_menu_items,
            add_edit_form='SettingsForm',
            add_edit_form_props={
                'buttons_mode': 'default',
                'fullscreen': False,
                'width': '80%',
                'height': '80%',
                'css_class': None,
            },
            **kwargs)
        print('AccountsAdminView __init__:', time.time() - stime)

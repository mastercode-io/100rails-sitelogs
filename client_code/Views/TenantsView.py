from AnvilFusion.components.GridView import GridView
from AnvilFusion.tools.utils import AppEnv


def lock_dataset(args):
    # print('lock_dataset', args.rowInfo.rowData.uid)
    AppEnv.set_tenant_admin(tenant_uid=args.rowInfo.rowData.uid, reload_func=AppEnv.after_login)


def reset_dataset(args):
    # print('reset_dataset', args.rowInfo.rowData.uid)
    AppEnv.reset_tenant_admin(reload_func=AppEnv.after_login)


class TenantsView(GridView):
    def __init__(self, **kwargs):
        print('TenantsView')
        view_config = {
            'model': 'Tenant',
            'columns': [
                {'name': 'name', 'label': 'Account Name'},
                {'name': 'status', 'label': 'Status'},
                {'name': '_spacer', 'no_data': True},
            ],
        }

        context_menu_items = [
            {'id': 'select_tenant', 'label': 'Lock Dataset', 'action': lock_dataset},
            {'id': 'reset_tenant', 'label': 'Reset Dataset', 'action': reset_dataset},
        ]

        super().__init__(
            model='Tenant',
            view_config=view_config,
            context_menu_items=context_menu_items,
            **kwargs)

from AnvilFusion.tools.utils import AppEnv, init_user_session
from AnvilFusion.datamodel import migrate
from .app import models
from . import Forms
from . import Views
from . import Pages

AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages

init_user_session()
migrate.migrate_db_schema()

# columns = [
#     {"name": "email", "label": "Email"},
#     {"name": "enabled", "label": "Enabled"},
#     {"name": "last_login", "label": "Las Login"},
#     {"name": "permissions", "label": "Permissions"}
# ]
# model = 'User'
# grid_view = AppEnv.data_models.AppGridView(model=model, columns=columns).save()
# print(grid_view)
# view_obj = AppEnv.data_models.AppGridView.get_by('model', model)
# view_config = view_obj['config'] or {}
# view_config['model'] = model
# view_config['columns'] = view_obj['columns'] or []
# grid_data = AppEnv.data_models.TimesheetType.get_grid_view(view_config,
#                                                            search_queries=None,
#                                                            filters=None,
#                                                            include_rows=False)
# print(grid_data)
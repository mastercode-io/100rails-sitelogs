import time
stime = time.time()

from ._anvil_designer import HomePageNewTemplate
import anvil.js
from anvil.js.window import ej, jQuery
import anvil.users
import anvil.tables
from AnvilFusion.tools.utils import AppEnv, DotDict, init_user_session
from AnvilFusion.components.FormInputs import DropdownInput
from AnvilFusion.datamodel.particles import SYSTEM_TENANT_UID
from .. import models
from ... import Forms
from ... import Views
from ... import Pages
from . import navigation as nav


print('HomePage IMPORT', time.time() - stime)

AppEnv.APP_ID = "Sitelogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.2"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages
AppEnv.grid_settings = {}
AppEnv.theme = {
    'components': {
        'alert': {
            'success': {'class': 'alert alert-success', 'icon': 'fa-regular fa-circle-check pl-message-icon'},
            'info': {'class': 'alert alert-info', 'icon': 'fa-regular fa-circle-info pl-message-icon'},
            'warning': {'class': 'alert alert-warning', 'icon': 'fa-regular fa-triangle-exclamation pl-message-icon'},
            'error': {'class': 'alert alert-error', 'icon': 'fa-regular fa-circle-xmark pl-message-icon'},
        },
    }
}
AppEnv.start_menu = "timesheet_menu"


class HomePageNew(HomePageNewTemplate):
    def __init__(self, **props):
        self.firs_load = True
        self.account = None
        self.user_app_permissions = None
        self.appbar_settings_menu_show = False
        self.content_id = "sl-content"
        self.content_control = None
        self.start_page = props.get('start_page', None)
        self.start_props = props.get('start_props', {})

        self.appbar_menu = nav.AppbarMenu(
            container_el="sl-appbar-menu-left",
            target_el=".sl-page-container",
            content_id=self.content_id,
            menu_items={},
            nav_items=nav.PL_NAV_ITEMS,
        )

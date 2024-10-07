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
import nav
import schema


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

        self.appbar_menu_left = nav.AppbarMenu(
            container_el="sl-appbar-menu-left",
            target_el=".sl-page-container",
            content_id=self.content_id,
            menu_items=schema.SL_MENU_ITEMS,
            nav_items=schema.SL_NAV_ITEMS,
        )

        right_menu_items = [
            {'prefixIcon': 'fa-solid fa-comments sl-appbar-menu-icon', 'id': 'assistant'},
            {'prefixIcon': 'fa-solid fa-bell sl-appbar-menu-icon', 'id': 'notifications'},
            {'prefixIcon': 'fa-solid fa-user sl-appbar-menu-icon', 'id': 'user_menu'},
        ]

        self.appbar_menu_right = nav.AppbarMenu(
            container_el="sl-appbar-menu-right",
            target_el=".sl-page-container",
            content_id=self.content_id,
            menu_items=right_menu_items,
            nav_items=schema.SL_NAV_ITEMS,
        )


    def form_show(self, **event_args):
        if self.firs_load:
            self.firs_load = False
            self.appbar_menu_right.show()

            appbar_logo_el = anvil.js.window.document.getElementById('sl-appbar-logo')
            appbar_spacer_el = anvil.js.window.document.getElementById('sl-appbar-spacer')
            appbar_menu_right_el = anvil.js.window.document.getElementById('sl-appbar-menu-right')
            print(appbar_logo_el, appbar_spacer_el, appbar_menu_right_el)
            appbar_menu_left_width = (anvil.js.window.innerWidth - appbar_logo_el.offsetWidth -
                                      appbar_menu_right_el.offsetWidth - appbar_spacer_el.offsetWidth - 100)
            self.appbar_menu_left.width = appbar_menu_left_width
            self.appbar_menu_left.show()

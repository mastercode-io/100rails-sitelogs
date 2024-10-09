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

        dropdown_item = {
            'id': 'dropdown',
            'type': 'Input',
            'text': 'Dropdown',
            'template': ej.splitbuttons.DropDownButton({
                'items': [
                    {'text': 'Item 1'},
                    {'text': 'Item 2'},
                    {'text': 'Item 3'},
                ],
                'content': 'Dropdown',
                'select': self.menu_select,
                # 'created': self.menu_created,
            })
        }
        schema.SL_MENU_ITEMS.append(dropdown_item)
        self.appbar_menu_left = nav.AppbarMenu(
            container_el="sl-appbar-menu-left",
            target_el=".sl-page-container",
            content_id=self.content_id,
            menu_items=schema.SL_MENU_ITEMS,
            nav_items=schema.SL_NAV_ITEMS,
        )

        right_menu_items = [
            {
                'id': 'assistant',
                'template': '<button class="e-btn e-tbar-btn"><span><i class="fa-solid fa-comments '
                            'sl-appbar-menu-icon"></i</span></button>'
            },
            {
                'id': 'notifications',
                'template': '<button class="e-btn e-tbar-btn"><span><i class="fa-solid fa-bell '
                            'sl-appbar-menu-icon"></i</span></button>'
            },
            {
                'id': 'user_menu',
                'template': '<button class="e-btn e-tbar-btn"><span><i class="fa-solid fa-user '
                            'sl-appbar-menu-icon"></i</span></button>'
            },
        ]

        self.appbar_menu_right = nav.AppbarMenu(
            container_el="sl-appbar-menu-right",
            target_el=".sl-page-container",
            content_id=self.content_id,
            menu_items=right_menu_items,
            nav_items=schema.SL_NAV_ITEMS,
            on_created=self.show_menu_left,

        )


    def form_show(self, **event_args):
        if self.firs_load:
            self.firs_load = False
            self.appbar_menu_right.show()


    def show_menu_left(self, args):
        time.sleep(1)
        appbar_menu_left_width = anvil.js.window.innerWidth
        for el in ('sl-appbar-logo', 'sl-appbar-spacer', 'sl-appbar-menu-right'):
            appbar_menu_left_width -= anvil.js.window.document.getElementById(el).getBoundingClientRect().width
        self.appbar_menu_left.width = appbar_menu_left_width
        self.appbar_menu_left.show()

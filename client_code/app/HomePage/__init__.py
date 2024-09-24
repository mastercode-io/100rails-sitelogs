import time


stime = time.time()
from ._anvil_designer import HomePageTemplate
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
import navigation as nav
# from ..copilot import Copilot
import json


print('HomePage IMPORT', time.time() - stime)

AppEnv.APP_ID = "PayLogs"
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


class HomePage(HomePageTemplate):
    def __init__(self, **kwargs):

        self.firs_load = True
        self.account = None
        self.user_app_permissions = None
        self.appbar_settings_menu_show = False
        self.content_id = "pl-content"
        self.content_control = None
        self.start_page = kwargs.get('start_page', None)
        self.start_props = kwargs.get('start_props', {})

        # Appbar configuration
        self.appbar = ej.navigations.AppBar({"colorMode": "Primary", "isSticky": True})
        self.appbar_logo = ej.buttons.Button({"cssClass": "e-inherit"})
        # self.appbar_sidebar_toggle = ej.buttons.Button(
        #     {"cssClass": "e-inherit", "iconCss": "fa-solid fa-bars pl-appbar-menu-icon"}
        # )
        self.appbar_assistant_toggle = ej.buttons.Button(
            {"cssClass": "e-inherit", "iconCss": "fa-solid fa-comments pl-appbar-menu-icon"}
        )

        self.assistant = nav.Assistant(
            target_el=".pl-page-container",
            container_id="pl-assistant",
            content_id=self.content_id,
        )
        # self.sidebar = nav.Sidebar(
        #     target_el=".pl-page-container",
        #     container_id="pl-sidebar",
        #     content_id=self.content_id,
        # )
        self.appbar_menu = nav.AppbarMenu(
            container_el="sl-appbar-menu-left",
            target_el=".pl-page-container",
            container_id="pl-sidebar",
            content_id=self.content_id,
            menu_items={},
            nav_items=nav.PL_NAV_ITEMS,
            # sidebar=self.sidebar,
        )

        self.appbar_notification_list = ej.splitbuttons.DropDownButton(
            {
                "cssClass": "e-inherit e-caret-hide pl-menu-font",
                "iconCss": "fa-solid fa-bell pl-appbar-menu-icon",
                "items": [{"text": "No new notifications", "disabled": True}],
                "open": self.appbar_menu_popup_open,
            }
        )
        self.appbar_user_menu_items = [
            {
                "text": "User<br>user@100rails.com",
                "disabled": True,
                "id": "pl-appbar-user-account-name",
            },
            {
                "text": "User Profile",
                "iconCss": "fa-regular fa-user-gear",
                "id": "pl-appbar-user-profile",
            },
            {
                "text": "Account Settings",
                "iconCss": "fa-regular fa-cog",
                "id": "pl-appbar-account-settings",
            },
            {
                "text": "Sign Out",
                "iconCss": "fa-regular fa-arrow-right-from-bracket",
                "id": "pl-appbar-sign-out",
            },
        ]
        self.appbar_user_menu = ej.splitbuttons.DropDownButton(
            {
                "cssClass": "e-inherit e-caret-hide pl-menu-font",
                "iconCss": "fa-solid fa-user pl-appbar-menu-icon",
                "items": self.appbar_user_menu_items,
                "open": self.appbar_menu_popup_open,
                "select": self.appbar_user_menu_select,
                "beforeItemRender": self.appbar_user_menu_item_render,
            }
        )
        self.appbar_data_file = DropdownInput(name='data_file',
                                              container_id='pl-appbar-data-file',
                                              container_class='pl-appbar-data-file',
                                              on_change=self.appbar_data_file_select)
        # self.appbar_settings_menu_items = nav.PL_MENU_ITEMS['settings_menu']
        #     [
        #     {'id': 'settings_users', 'text': 'Users', 'items': []},
        #     {'id': 'settings_locations', 'text': 'Locations', 'items': []},
        #     {'id': 'settings_employee_roles', 'text': 'Employee Roles', 'items': []},
        #     {'id': 'settings_job_types', 'text': 'Job Types', 'items': []},
        #     {'id': 'settings_timesheet_types', 'text': 'Timesheet Types', 'items': []},
        # ]
        # self.appbar_settings_menu = ej.splitbuttons.DropDownButton(
        #     {
        #         "cssClass": "e-inherit e-caret-hide pl-menu-font",
        #         "iconCss": "fa-solid fa-cog pl-appbar-menu-icon",
        #         "items": self.appbar_settings_menu_items,
        #         "open": self.appbar_menu_popup_open,
        #         "select": self.appbar_settings_menu_select,
        #     }
        # )
        self.appbar_settings_button = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-list-check pl-appbar-menu-icon',
        })
        # self.appbar_settings_form = ej.buttons.Button({
        #     'cssClass': 'e-inherit e-caret-hide pl-menu-font',
        #     'iconCss': 'fa-solid fa-input-text pl-appbar-menu-icon',
        # })
        self.appbar_assistant_button = ej.buttons.Button({
            'cssClass': 'e-inherit e-caret-hide pl-menu-font',
            'iconCss': 'fa-solid fa-comments pl-appbar-menu-icon',
        })

        AppEnv.login_user = self.login_user
        AppEnv.after_login = self.after_login


    def appbar_user_menu_item_render(self, args):
        if args.item.id == 'pl-appbar-user-account-name':
            args.element.innerHTML = AppEnv.logged_user.user_name + '<br>' + AppEnv.logged_user.email
            args.element.classList.add('pl-appbar-user-account-name')
        elif args.item.id == 'pl-appbar-sign-out':
            args.element.classList.add('pl-appbar-sign-out')
        else:
            args.element.classList.add('pl-appbar-user-menu-item')


    def login_user(self):
        # print('login_user')
        stime = time.time()
        AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm, after_login=self.after_login)
        print('login_user: ', time.time() - stime)
        if AppEnv.logged_user:
            self.after_login()


    def after_login(self):
        stime = time.time()
        AppEnv.init_enumerations(model_list=models.ENUM_MODEL_LIST)
        AppEnv.init_enum_constants()
        do_something()
        print('LOAD CONST: ', time.time() - stime)
        # AppEnv.navigation = self.sidebar
        stime = time.time()
        AppEnv.assistant = self.assistant

        if AppEnv.logged_user.tenant_uid == SYSTEM_TENANT_UID or AppEnv.logged_user.user_role_type == 'portal_admin':
            app_comps = models.AppComponent.search(tenant_uid=SYSTEM_TENANT_UID, id='user_role_permissions')
            app_permissions = next(iter(app_comps), None)
        else:
            app_permissions = models.AppComponent.get_by('id', 'user_role_permissions')
        self.user_app_permissions = app_permissions['props']['user_roles'][AppEnv.logged_user.user_role_type][
            'permissions']
        # user_app_menu = nav.get_user_menu_items(
        #     nav.PL_MENU_ITEMS,
        #     self.user_app_permissions['app_menu'])
        user_app_menu = self.appbar_menu.get_user_menu_items(
            nav.PL_MENU_ITEMS,
            self.user_app_permissions['app_menu'])
        self.appbar_menu.menu_items = user_app_menu
        self.appbar_menu.show()

        # if ('settings_button' in self.user_app_permissions['special_menu']
        #         and self.user_app_permissions['special_menu']['settings_button']['has_access']):
        #     self.appbar_settings_button.appendTo(jQuery("#pl-appbar-settings-menu")[0])
        #     self.appbar_settings_button.element.onclick = self.appbar_settings_button_click
        #     settings_button_tooltip = ej.popups.Tooltip({
        #         "content": "Payroll Settings",
        #         "position": "BottomCenter",
        #     })
        #     settings_button_tooltip.appendTo(self.appbar_settings_button.element)
        #
        # if ('assistant_button' in self.user_app_permissions['special_menu']
        #         and self.user_app_permissions['special_menu']['assistant_button']['has_access']):
        #     self.appbar_assistant_toggle.appendTo(jQuery("#pl-appbar-assistant-toggle")[0])
        #     self.appbar_assistant_toggle.element.onclick = self.assistant.toggle
        #     assistant_button_tooltip = ej.popups.Tooltip({
        #         "content": "Ask Assistant",
        #         "position": "BottomCenter",
        #     })
        #     assistant_button_tooltip.appendTo(self.appbar_assistant_toggle.element)
        #
        # user_menu_items = []
        # user_menu_permissions = self.user_app_permissions['special_menu']['user_menu']['items']
        # for item in self.appbar_user_menu_items:
        #     if item['id'] in user_menu_permissions and user_menu_permissions[item['id']]['has_access']:
        #         user_menu_items.append(item)
        # self.appbar_user_menu = ej.splitbuttons.DropDownButton(
        #     {
        #         "cssClass": "e-inherit e-caret-hide pl-menu-font",
        #         "iconCss": "fa-solid fa-user pl-appbar-menu-icon",
        #         "items": user_menu_items,
        #         "open": self.appbar_menu_popup_open,
        #         "select": self.appbar_user_menu_select,
        #         "beforeItemRender": self.appbar_user_menu_item_render,
        #     }
        # )
        # self.appbar_user_menu.appendTo(jQuery("#pl-appbar-user-menu")[0])
        # user_menu_tooltip = ej.popups.Tooltip({
        #     "content": "User Menu",
        #     "position": "BottomCenter",
        # })
        # user_menu_tooltip.appendTo(self.appbar_user_menu.element)

        if not self.start_page:
            self.start_page = self.user_app_permissions['start_page']

        # self.appbar_user_menu.items[0].text = AppEnv.logged_user.user_name + '<br>' + AppEnv.logged_user.email
        # anvil.js.window.document.getElementById('pl-appbar-spacer').innerHTML = AppEnv.logged_user.app_mode

        tenant = models.Tenant.get(AppEnv.logged_user.tenant_uid)
        self.account = models.Account.get(tenant['account_uid'])
        if AppEnv.logged_user.app_mode == 'Super Admin Mode' or AppEnv.logged_user.app_mode == 'Developer Mode':
            tenant_list = models.Tenant.search(tenant_uid=None, search_query=anvil.tables.order_by('account_uid'))
            AppEnv.logged_user.pay_entities = [df.to_json_dict() for df in tenant_list]
        elif self.account is not None:
            AppEnv.logged_user.pay_entities = [df.to_json_dict() for df in self.account['pay_entities']]
        self.appbar_data_file.options = AppEnv.logged_user.pay_entities
        self.appbar_data_file.value = AppEnv.logged_user.tenant_uid
        # self.appbar_data_file.show()
        # data_file_tooltip = ej.popups.Tooltip({
        #     "content": "Select Data File",
        #     "position": "BottomCenter",
        # })
        # data_file_tooltip.appendTo(f'#{self.appbar_data_file.container_id}')
        # if self.appbar_data_file.control:
        #     self.appbar_data_file.control.showClearButton = False
        print('LOAD UI: ', time.time() - stime)

        self.assistant.show()
        stime = time.time()
        if self.start_page:
            self.appbar_menu.show_selected(self.start_page, props=self.start_props)
        print('SHOW START PAGE: ', time.time() - stime)
        # self.sidebar.show(AppEnv.start_menu)
        # self.sidebar.refresh_content()

        # copilot = Copilot()
        # message = 'what are you?'
        # thread = copilot.send_message(message)
        # print('copilot', message)
        # print(thread)


    def form_show(self, **event_args):
        # Append appbar controls to elements
        self.appbar.appendTo(jQuery("#pl-appbar")[0])
        # self.appbar_notification_list.appendTo(jQuery("#pl-appbar-notification-list")[0])
        # appbar_notifications_tooltip = ej.popups.Tooltip({
        #     "content": "Notifications",
        #     "position": "BottomCenter",
        # })
        # appbar_notifications_tooltip.appendTo(self.appbar_notification_list.element)
        self.login_user()


    # def settings_click(self, args):
    #     print('settings menu', args.item.id)
    # self.sidebar.show_menu("settings_menu")

    # Sidebar toggle event handler

    def sidebar_toggle(self, args):
        pass
        # self.sidebar.toggle(args)


    # def appbar_settings_button_click(self, args):
    #     print('appbar_settings_button_click')
    #     tenant = models.Tenant.get(AppEnv.logged_user.tenant_uid)
    #     print('tenant', tenant)
    #     nav.PL_NAV_ITEMS['settings_account']['props'] = {'data': tenant}
    #     self.appbar_menu.show_selected('settings_account')

    def appbar_settings_button_click(self, args):
        # print('appbar_settings_button_click')
        # tenant = models.Tenant.get_row(AppEnv.logged_user.tenant_uid)
        # recs = models.Account.search(pay_entities=[tenant])
        # print('recs', len(recs))
        # account = next(iter(models.Account.search(pay_entities=[tenant])), None)
        # print('tenant', tenant)
        # print('account', account)
        # nav.PL_NAV_ITEMS['settings_form']['props'] = {'data': account}
        self.appbar_menu.show_selected('payroll_settings')


    # def appbar_assistant_button_click(self, args):
    #     print('appbar_assistant_button_click')
    #     if AppEnv.assistant is None:
    #         AppEnv.assistant = Forms.AssistantForm(target=self.content_id)
    #     AppEnv.assistant.form_show()

    # Appbar menu popup window position adjustment

    @staticmethod
    def appbar_menu_popup_open(args):
        args.element.parentElement.style.top = (
                str(float(args.element.parentElement.style.top[:-2]) + 3) + "px"
        )


    # Sidebar menu popup window position adjustment

    @staticmethod
    def sidebar_menu_popup_open(args):
        args.element.parentElement.style.top = (
                str(
                    args.element.getBoundingClientRect().top
                    - args.element.parentElement.offsetHeight
                    + 44
                )
                + "px"
        )
        args.element.parentElement.style.left = "100px"


    def appbar_user_menu_select(self, args):
        # print('appbar_user_menu_select', args.item.id)
        if args.item.id == 'pl-appbar-sign-out':
            anvil.users.logout()
            if self.content_control:
                self.content_control.destroy()
                self.content_control = None
            # self.sidebar.show_menu(AppEnv.start_menu)
            self.login_user()
            self.appbar_user_menu.items[0].text = 'Sign In'
            self.appbar_user_menu.items[0].iconCss = 'fa-solid fa-sign-in'
            self.appbar_user_menu.items[0].id = 'pl-appbar-sign-in'
        elif args.item.id == 'pl-appbar-sign-in':
            AppEnv.logged_user = init_user_session(login_form=Forms.UserLoginForm)
            self.appbar_user_menu.items[0].text = AppEnv.logged_user['email']
            self.appbar_user_menu.items[0].disabled = True
        elif args.item.id == 'pl-appbar-account-settings':
            nav.PL_NAV_ITEMS['settings_form']['props'] = {'data': self.account}
            self.appbar_menu.show_selected('settings_form')


    def appbar_settings_menu_select(self, args):
        # print('appbar_user_menu_select', args.item.id)
        self.appbar_menu.show_selected(args.item.id)


    def appbar_data_file_select(self, args):
        # print('appbar_data_file_select', args)
        # print(self.appbar_data_file.value)
        if self.firs_load:
            self.firs_load = False
        else:
            AppEnv.set_current_tenant(tenant_uid=self.appbar_data_file.value, reload_func=self.after_login)


def do_something():
    print('do_something')
    print(anvil.server.get_api_origin())
    # new_api_key = anvil.server.call('generate_tenant_api_key', AppEnv.logged_user.tenant_uid, 'scaflog')
    # print('new_api_key', new_api_key)
    # enum_name = 'DAY_TYPE_OPTIONS'
    # enum_options = [
    #     'Any Day',
    #     'Weekday',
    #     'Weekend',
    #     'Saturday',
    #     'Sunday',
    #     'Public Holiday',
    #     'Week',
    # ]
    # enum_values = {x: x for x in enum_options}
    # enum = models.AppEnum(name=enum_name, options=enum_values).save()
    # print(enum)

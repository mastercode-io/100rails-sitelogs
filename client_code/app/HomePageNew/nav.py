# Application navigation
from anvil.js.window import jQuery, ej, Event
import anvil.js
import time
from AnvilFusion.tools.utils import AppEnv
from AnvilFusion.datamodel import migrate
from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormBase import FormBase
from ...Pages import CopilotChat
from .schema import *


# Sidebar control CSS
PL_SIDEBAR_CSS = 'e-inherit e-caret-hide pm-sidebar-menu'
PL_SIDEBAR_WIDTH = 200
PL_SIDEBAR_POPUP_OFFSET = 1
PL_ASSISTANT_WIDTH = 300


# def get_user_menu_items(menu_items: dict, user_permissions: dict):
#     user_menu_items = {}
#     for menu_id, subitems in menu_items.items():
#         if user_permissions[menu_id]['has_access']:
#             user_menu_subitems = get_user_menu_subitems(subitems, user_permissions[menu_id]['items'])
#             user_menu_items[menu_id] = user_menu_subitems
#     return user_menu_items


# def get_user_menu_items(menu_items: list, user_permissions: dict):
#     user_menu_items = []
#     for item in menu_items:
#         if item['id'] in user_permissions and user_permissions[item['id']]['has_access']:
#             user_menu_item = {'id': item['id'], 'text': item['text']}
#             if 'items' in item:
#                 user_menu_item['items'] = get_user_menu_items(item['items'], user_permissions[item['id']]['items'])
#             else:
#                 user_menu_item['items'] = []
#             user_menu_items.append(user_menu_item)
#     return user_menu_items


# Appbar navigation class
class AppbarMenu:
    def __init__(self,
                 app_menu=None,
                 permissions=None,
                 menu_items=None,
                 nav_items=None,
                 width='auto',
                 container_el=None,
                 target_el=None,
                 container_id=None,
                 content_id=None,
                 on_created=None,
                 ):
        self.app_menu = app_menu
        self.permissions = permissions
        self.menu_items = menu_items
        self.nav_items = nav_items
        self.container_el = container_el
        self.target_el = target_el
        self.container_id = container_id
        self.content_id = content_id
        self.width = width
        self.menu = None
        self.selected_el = None
        self.nav_target_id = None
        self.content_control = None
        self.on_created = on_created

        if self.menu_items is None:
            self.menu_items = self.get_user_menu_items(self.app_menu, self.permissions)
        for item in self.menu_items:
            item['click'] = self.show_submenu


    @staticmethod
    def get_user_menu_items(menu_items: list, user_permissions: dict):
        user_menu_items = []
        for item in menu_items:
            if item['id'] in user_permissions and user_permissions[item['id']]['has_access']:
                user_menu_item = {
                    'id': item['id'],
                    'type': 'Button',
                    'text': item['text'],
                    # 'template': ej.splitbuttons.DropDownButton({
                    #     'items': [ej.navigations.ContextMenu({'items': sub['items']}) if 'items' in sub else sub for sub in item.get('items', [])],
                    #     'content': item['text'],
                    #     'select': self.menu_select,
                    # 'created': self.menu_created,
                    # })
                }
                user_menu_items.append(user_menu_item)
                print(item['id'], item.get('items', []))
        return user_menu_items


    def show(self):
        print('AppBar Show')

        if self.menu:
            self.menu.items = self.menu_items
        else:
            jQuery(f"#{self.container_el}").addClass('sl-menu-container')
            # self.menu = ej.navigations.Menu({
            #     # 'cssClass': 'e-inherit pl-appbar-menu',
            #     'cssClass': 'e-inherit rounded-box pl-appbar-menu',
            #     'items': self.menu_items,
            #     'select': self.menu_select,
            #     'overflowMode': 'Popup',
            #     'enableScrolling': True
            # })
            self.menu = ej.navigations.Toolbar({
                # 'cssClass': 'e-inherit pl-appbar-menu',
                'cssClass': 'e-inherit sl-appbar-menu',
                'items': self.menu_items,
                # 'clicked': self.menu_select,
                'width': self.width,
                'overflowMode': 'Popup',
                'created': self.on_created,
                # 'clicked': self.show_submenu,
            })
            self.menu.appendTo(jQuery(f"#{self.container_el}")[0])


    def show_submenu(self, args):
        subitems = [
            {'id': 'sub1', 'text': 'Submenu 1'},
            {'id': 'sub2', 'text': 'Submenu 2'},
            {'id': 'sub3', 'text': 'Submenu 3'},
        ]
        print('show submenu', args)
        print('event')
        for k in args.originalEvent.keys():
            print(k, args.originalEvent[k])
        print('item')
        for k in args.item.keys():
            print(k, args.item[k])
        # submenu = ej.navigations.ContextMenu({
        #     'items': subitems,
        #     # 'select': self.menu_select,
        # }, '#sl-appbar-menu-left-submenu')
        # submenu.open(args.event.target)


    def menu_select(self, args):
        if self.selected_el is not None:
            self.selected_el.classList.remove('sl-appbar-menu-selected')
        self.selected_el = args.element
        self.selected_el.classList.add('sl-appbar-menu-selected')
        menu_id = args.item.properties.id
        print(menu_id)
        for k in args.item.properties.keys():
            print(k, args.item.properties[k])
        self.show_selected(menu_id)
        # self.sidebar.show_menu(menu_id)


    def show_selected(self, menu_id=None, props=None):
        component = self.nav_items.get(menu_id)
        if component is None:
            return

        if self.content_control is not None and self.nav_target_id is None:
            self.content_control.destroy()

        nav_container_id = self.content_id if self.nav_target_id is None else self.nav_target_id
        if component['type'] == 'custom':
            view_class = getattr(AppEnv.views, component['class'])
            self.content_control = view_class(container_id=nav_container_id, **component.get('props', {}))
            # try:
            #     view_class = getattr(AppEnv.views, component['class'])
            #     self.content_control = view_class(container_id=nav_container_id, **component.get('props', {}))
            # except Exception as e:
            #     print('Load Form Exception', e.args)

        if component['type'] == 'view':
            if 'config' in component:
                self.content_control = GridView(view_name=component['config'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))
            elif hasattr(AppEnv.views, f"{component['model']}View"):
                view_class = getattr(AppEnv.views, f"{component['model']}View")
                self.content_control = view_class(container_id=nav_container_id,
                                                  **component.get('props', {}))
            else:
                self.content_control = GridView(model=component['model'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))

        elif component['type'] == 'form':
            print('form', component)
            # try:
            form_pros = props or component.get('props', {})
            form_class = getattr(AppEnv.forms, component.get('class', f"{component.get('model')}Form"))
            self.content_control = form_class(target=nav_container_id, **form_pros)
            # except Exception as e:
            #     print(e.args)
            #     self.content_control = FormBase(model=component.get('model'), target=nav_container_id)

        elif component['type'] == 'page':
            print('page', component)
            try:
                if component.get('page', None):
                    page_class = component['page']
                else:
                    page_class = getattr(AppEnv.pages, f"{component['name']}")
                self.content_control = page_class(container_id=nav_container_id, **component.get('props', {}))
            except Exception as e:
                print('Load Page Exception', e.args)
                # self.content_control = Pages.BaseForm(model=component['model'], target=self.content_id)
        elif component['type'] == 'function':
            try:
                func_name = component['function']
                if callable(func_name):
                    func_name(**component.get('props', {}))
            except Exception as e:
                print('Run Function Exception', e.args)
            return

        if hasattr(self.content_control, 'target_id'):
            self.nav_target_id = self.content_control.target_id

        # try:
        self.content_control.form_show()
        # except Exception as e:
        #     print(e)
        # if self.control.isOpen:
        #     self.control.toggle()
        #     self.control.toggle()


    def refresh_content(self):
        if self.content_control:
            try:
                self.content_control.refresh()
            except Exception as e:
                pass


class Assistant:
    def __init__(self,
                 target_el,
                 container_id,
                 content_id,
                 sidebar_width=PL_ASSISTANT_WIDTH,
                 **properties):

        self.target_el = target_el
        self.container_id = container_id
        self.content_id = content_id
        self.nav_target_id = None
        self.sidebar_width = sidebar_width
        self.content_control = None
        self.control = None
        self.chat = None
        self.open = False
        self.toggled = False


    # Show sidebar menu
    def show(self):
        print('show assistant')
        if not self.control:
            self.control = ej.navigations.Sidebar({
                'width': self.sidebar_width,
                'target': self.target_el,
                # 'mediaQuery': '(min-width: 600px)',
                'isOpen': False,
                'animate': False,
                'position': 'Right',
                'type': 'Push',
                # 'open': self.sidebar_event,
                # 'close': self.sidebar_event,
            })
            self.control.appendTo(f"#{self.container_id}")
            self.chat = CopilotChat(container_id=self.container_id)
            # container_el = anvil.js.window.document.getElementById(self.container_id)
            # container_el.innerHTML = f'''
            #     <div id="pl-assistant-container" style="margin: 5px; height: 100%;">
            #         <h5 id="pl-assistant-header" style="margin-top: 15px;">PayLogs Assistant</h5>
            #         <div id="pl-assistant-chat" style="height: 90%;"><div>
            #     </div>
            # '''
            # self.chat = jQuery(f"#pl-assistant-chat").kendoChat({
            #     'post': self.chat_post,
            #     'height': '85%',
            # }).data('kendoChat')
            # self.chat = AssistantChat(container_id='pl-assistant-chat')
            # self.chat.form_show()
            self.control.hide()


    # Sidebar toggle
    def toggle(self, args):
        # print('toggle assistant')
        self.toggled = True
        if self.open:
            self.control.hide()
            self.open = False
        else:
            self.control.show()
            self.open = True
        # AppEnv.navigation.refresh_content()
        # time.sleep(0.5)
        # resize_event = anvil.js.new(Event, 'resize')
        # anvil.js.window.dispatchEvent(resize_event)
        # if not self.open:
        #     self.control.hide()


    def sidebar_event(self, args):
        if self.toggled:
            self.toggled = False
            args.cancel = True
            print('assistant toggled', args)
        else:
            print('assistant event', args)
        # if self.open:
        #     self.control.show()
        # else:
        #     self.control.hide()


# Sidebar navigation class
class Sidebar:
    def __init__(self,
                 target_el,
                 container_id,
                 content_id,
                 sidebar_width=PL_SIDEBAR_WIDTH,
                 sections=None,
                 nav_items=None,
                 **properties):

        if sections is None:
            sections = PL_MENU_ITEMS
        if nav_items is None:
            nav_items = PL_NAV_ITEMS
        self.target_el = target_el
        self.container_id = container_id
        self.content_id = content_id
        self.nav_target_id = None
        self.sidebar_width = sidebar_width
        self.content_control = None
        self.nav_items = nav_items
        self.control = None
        self.menu = None
        self.open = True


    # Show sidebar menu
    def show(self, menu_id):
        print('show', menu_id)
        if not self.menu:
            self.menu = ej.navigations.TreeView({
                'fields': {
                    'cssClass': PL_SIDEBAR_CSS,
                    'dataSource': '',
                    'id': 'id',
                    'text': 'text',
                    'child': 'items'
                },
                'expandOn': 'Click',
                'nodeSelected': self.menu_select,
            })
            self.menu.appendTo(jQuery(f"#{self.container_id}-menu")[0])

        if not self.control:
            self.control = ej.navigations.Sidebar({
                'width': self.sidebar_width,
                'target': self.target_el,
                # 'mediaQuery': '(min-width: 600px)',
                'isOpen': True,
                'animate': False,
                'type': 'Push',
                # 'open': self.sidebar_event,
                # 'close': self.sidebar_event,
            })
            self.control.appendTo(f"#{self.container_id}")

        self.show_menu(menu_id)


    # Sidebar toggle
    def toggle(self, args):
        if self.open:
            self.open = False
            self.control.hide()
        else:
            self.open = True
            self.control.show()
        # self.refresh_content()
        # time.sleep(0.5)
        # resize_event = anvil.js.new(Event, 'resize')
        # anvil.js.window.dispatchEvent(resize_event)
        # if not self.open:
        #     self.control.hide()


    def sidebar_event(self, args):
        print('sidebar event', args)
        if args.name == 'open' and self.open:
            args.cancel = True
        elif args.name == 'close' and not self.open:
            args.cancel = True


    def show_menu(self, menu_id):
        # self.menu.fields.dataSource = PL_MENU_ITEMS.get(menu_id, list(PL_MENU_ITEMS.keys())[0])
        if menu_id in PL_MENU_ITEMS:
            subcomponent = PL_DEFAULT_NAV_ITEMS.get(menu_id)
            if not subcomponent:
                subcomponent = PL_MENU_ITEMS[menu_id][0]['id']
            menu_items = PL_MENU_ITEMS[menu_id]
            for item in menu_items:
                if item['id'] == subcomponent:
                    item['selected'] = True
                    item['expanded'] = True
            self.menu.fields.dataSource = menu_items
            self.menu_select(None, subcomponent=subcomponent)


    def menu_select(self, args, subcomponent=None, menu_item_id=None):
        if subcomponent is None:
            if args and 'e-level-1' in list(args.node.classList):
                # print('Accordion')
                self.menu.collapseAll()
                self.menu.expandAll([args.node])
                self.nav_target_id = None

            menu_item_id = args.nodeData.id if args else menu_item_id
            component = PL_NAV_ITEMS[menu_item_id] if menu_item_id in PL_NAV_ITEMS else None
        else:
            component = PL_NAV_ITEMS.get(subcomponent)
        if component is None:
            return

        if self.content_control is not None and self.nav_target_id is None:
            self.content_control.destroy()

        nav_container_id = self.content_id if self.nav_target_id is None else self.nav_target_id
        if component['type'] == 'custom':
            try:
                view_class = getattr(AppEnv.views, component['class'])
                self.content_control = view_class(container_id=nav_container_id, **component.get('props', {}))
            except Exception as e:
                print(e)

        if component['type'] == 'view':
            if 'config' in component:
                self.content_control = GridView(view_name=component['config'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))
            elif hasattr(AppEnv.views, f"{component['model']}View"):
                view_class = getattr(AppEnv.views, f"{component['model']}View")
                self.content_control = view_class(container_id=nav_container_id,
                                                  **component.get('props', {}))
            else:
                self.content_control = GridView(model=component['model'],
                                                container_id=nav_container_id,
                                                **component.get('props', {}))

        elif component['type'] == 'form':
            print('form', component)
            # try:
            form_class = getattr(AppEnv.forms, component.get('class', f"{component.get('model')}Form"))
            self.content_control = form_class(target=nav_container_id)
            # except Exception as e:
            #     print(e.args)
            #     self.content_control = FormBase(model=component.get('model'), target=nav_container_id)

        elif component['type'] == 'page':
            print('page', component)
            try:
                if component.get('page', None):
                    page_class = component['page']
                else:
                    page_class = getattr(AppEnv.pages, f"{component['name']}")
                self.content_control = page_class(container_id=nav_container_id, **component.get('props', {}))
            except Exception as e:
                print('Exception', e.args)
                # self.content_control = Pages.BaseForm(model=component['model'], target=self.content_id)
        elif component['type'] == 'function':
            try:
                func_name = component['function']
                if callable(func_name):
                    func_name(**component.get('props', {}))
            except Exception as e:
                print(e.args)
            return

        if hasattr(self.content_control, 'target_id'):
            self.nav_target_id = self.content_control.target_id

        # try:
        self.content_control.form_show()
        # except Exception as e:
        #     print(e)
        if self.control.isOpen:
            self.control.toggle()
            self.control.toggle()

        if 'subcomponent' in component:
            time.sleep(0.5)
            self.menu_select(None, subcomponent=component['subcomponent'])


    def refresh_content(self):
        if self.content_control:
            try:
                self.content_control.refresh()
            except Exception as e:
                pass

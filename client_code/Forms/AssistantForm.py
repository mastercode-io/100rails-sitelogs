from AnvilFusion.tools.utils import AppEnv
import anvil.js.window
from anvil.js.window import ej, jQuery
import uuid
from datetime import datetime, timedelta


class AssistantForm:
    def __init__(self, target):
        print('AssistantForm', target)

        self.target_el = anvil.js.window.document.getElementById(target)
        self.container_id = str(f"assistant-{uuid.uuid4()}")
        self.container_el = anvil.js.window.document.createElement('div')
        self.container_el.setAttribute('id', self.container_id)
        # self.container_el.style.visibility = 'hidden'
        self.target_el.append(self.container_el)
        self.form_id = str(f"assistant-form-{uuid.uuid4()}")
        self.chat_id = str(f"assistant-chat-{uuid.uuid4()}")
        self.chat_el = None
        self.chat = None

        self.form_content = f'<div id="{self.form_id}" style="padding-top:1em;!important"><div id="{self.chat_id}""></div></div>'

        self.form = ej.popups.Dialog({
            'header': 'Assistant',
            'content': self.form_content,
            'showCloseIcon': True,
            'target': self.target_el,
            'isModal': False,
            'width': '500px',
            # 'height': '99%',
            'visible': True,
            'position': {'X': 'right', 'Y': '15'},
            'animationSettings': {'effect': 'Zoom'},
            'cssClass': 'e-fixed py-dialog',
            'open': self.form_open,
            'close': self.form_close,
            # 'beforeOpen': self.before_open,
            # 'created': self.form_created,
        })
        self.form.cssClass = 'e-fixed py-dialog'
        self.form.appendTo(self.container_el)
        self.chat = jQuery(f"#{self.chat_id}").kendoChat({
            'post': self.chat_post,
            # 'height': '95%',
        }).data('kendoChat')
        self.chat_el = anvil.js.window.document.getElementById(self.chat_id)


    def form_show(self):
        print('show assistant form', self.chat, self.chat_el)
        self.form.show()
        max_height = int(self.container_el.style['max-height'][0:-2])
        self.form.element.style.height = f'{max_height - 15}px'
        # if self.chat is None:
        #     self.chat = jQuery(f"#{self.chat_id}").kendoChat({
        #         'post': self.chat_post,
        #         'height': '95%',
        #     }).data('kendoChat')
        self.chat_el.style.height = f'{max_height - 100}px'
        print('kendo chat', self.chat)


    def form_open(self, args):
        print('form_open')


    def form_close(self, args):
        print('form_close')


    def chat_post(self, args):
        print('chat_post', args)

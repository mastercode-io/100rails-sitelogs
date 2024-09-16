from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from .run_script import foo


class RunScriptPage(PageBase):
    def __init__(self, **kwargs):
        print('RunScriptPage')
        title = 'Run Script (developer)'
        self.run_button = Button(content='Run Script', action=self.run_button_action)
        self.execution_log = InlineMessage(name='execution_log')
        self.content = f'<br><div id="{self.run_button.container_id}"></div><br><br>'
        self.content += f'<div id="{self.execution_log.container_id}" style="overflow-y: scroll; height: 100%;"></div>'
        print(self.content)

        super().__init__(page_title=None, content=self.content, overflow='auto', **kwargs)


    def form_show(self, **args):
        print('RunScriptPage.form_show')
        super().form_show(**args)
        self.run_button.show()
        self.execution_log.show()


    def run_button_action(self, args):
        print('RunScriptPage.run_button_action')
        result = foo()
        self.execution_log.content = f'<br>Script result: {result}'

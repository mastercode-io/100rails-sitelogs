from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from anvil.tables import query as q
from ..app.models import Employee, EmployeeRole, Job, Location, Timesheet, TimesheetType
from datetime import datetime, timedelta
import uuid
import json


class TransferDataPage(PageBase):
    def __init__(self, **kwargs):
        print('TransferDataPage')
        title = 'Transfer Data with Integration Service'

        self.connected_app = LookupInput(name='connected_app',
                                         label='Connected App',
                                         model='AppOutApiCredential',
                                         text_field='integration.service_name',
                                         on_change=self.enable_import_button)
        self.import_button = Button(content='Import Timesheets',
                                    action=self.import_button_action)
        # self.import_button = ej.buttons.Button({
        #     'content': 'Import Records',
        #     'isPrimary': True,
        #     'size': 'large',
        # })
        # self.import_button_id = f'migrate-button-{uuid.uuid4()}'
        self.execution_log = InlineMessage(content='execution log')

        self.content = f'<br><div id="{self.connected_app.container_id}" style="width:300px;"></div>'
        self.content += f'<br><div id="{self.import_button.container_id}"></div>'
        self.content += f'<div id="{self.execution_log.container_id}" style="overflow-y: scroll; height: 100%;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)

        self.file_content = None


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.connected_app.show()
        self.import_button.show()
        self.import_button.enabled = False
        # self.import_button.appendTo(f'#{self.import_button_id}')
        # self.import_button.element.onclick = self.import_button_action
        self.execution_log.show()
        self.execution_log.content = 'Click <b>Import Timesheets</b> to start import<br><br>'


    def enable_import_button(self, args):
        print('enable_import_button', self.connected_app.value, args)
        if self.connected_app.value:
            self.import_button.enabled = True
        else:
            self.import_button.enabled = False

    def import_button_action(self, args):
        print('import_button_action', args)
        # self.execution_log.content += '<br>Import completed'


    def log_message(self, message):
        self.execution_log.content += str(message) + '<br>'

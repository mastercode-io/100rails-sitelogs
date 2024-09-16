from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from datetime import datetime
import uuid


class CalendarPage(PageBase):
    def __init__(self, **kwargs):
        print('CalendarPage')
        title = 'Payroll Calendar'
        self.start_date = DateInput(name='start_date', label='Start Date', value=datetime.now().date())
        self.edn_date = DateInput(name='end_date', label='End Date', value=datetime.now().date())
        self.select_period = ej.buttons.Button({
            'content': 'Select Period',
            'isPrimary': True,
            'size': 'large',
        })
        self.select_period_button_id = f'select-period-{uuid.uuid4()}'
        self.calendar = ej.calendars.Calendar({
            'value': datetime.now().date(),
            'weekNumber': True,
            # 'change': self.calendar_change,
        })
        self.calendar_id = f'calendar-{uuid.uuid4()}'

        self.content = f'<br><div id="{self.start_date.container_id}" style="width:300px;"></div>'
        self.content += f'<div id="{self.edn_date.container_id}" style="width:300px;"></div>'
        self.content += f'<br><div id="{self.select_period_button_id}"></div><br><br>'
        self.content += f'<div id="{self.calendar_id}"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)

        self.file_content = None


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.start_date.show()
        self.edn_date.show()
        self.select_period.appendTo(f'#{self.select_period_button_id}')
        self.select_period.element.onclick = self.select_period_action
        self.calendar.appendTo(f'#{self.calendar_id}')


    def select_period_action(self, args):
        print('select_period_action')

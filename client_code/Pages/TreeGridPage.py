from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from anvil.tables import query as q
from ..app.models import Employee, Timesheet
from datetime import datetime, timedelta
import uuid
import json


class TreeGridPage(PageBase):

    def __init__(self, **kwargs):
        print('TreeGridPage')
        title = 'Tree Grid'

        self.container_id = f'tree-grid-page-{uuid.uuid4()}'
        self.content = f'<br><div id="{self.container_id}"></div>'

        self.grid_data = None
        self.timesheet_fields = {
            'columns': [
                {'name': 'payrun.payrun_week', 'label': 'Payrun Week'},
                {'name': 'employee.uid', 'label': 'Employee Name'},
                {'name': 'job.name', 'label': 'Job Name'},
                {'name': 'job.job_type.short_code', 'label': 'Job Type'},
                {'name': 'date', 'label': 'Date', 'format': 'E dd MMM, yyyy'},
                {'name': 'start_time', 'label': 'Start Time', 'format': 'HH:mm'},
                {'name': 'end_time', 'label': 'End Time', 'format': 'HH:mm'},
                {'name': 'total_hours_view', 'label': 'Total Hours'},
                {'name': 'total_hours', 'visible': False},
                {'name': 'total_pay', 'label': 'Total Pay'},
                {'name': 'pay_lines', 'visible': False},
                {'name': 'pay_lines_view', 'label': 'Pay Lines', 'width': 300, 'disable_html_encode': False},
                {'name': 'status', 'label': 'Status'},
            ]
        }
        self.employee_fields = {
            'columns': [
                {'name': 'full_name', 'label': 'Employee Name'},
            ]
        }

        self.tree_grid = ej.treegrid.TreeGrid({
            'dataSource': self.grid_data,
            'idMapping': 'uid',
            'parentIdMapping': 'employee__uid',
            'columns': [
                {'field': 'full_name', 'headerText': 'Employee'},
                {'field': 'job__name', 'headerText': 'Job Name'},
                {'field': 'job__type', 'headerText': 'Job Type'},
                {'field': 'date', 'headerText': 'Date'},
                {'field': 'start_time', 'headerText': 'start time'},
                {'field': 'end_time', 'headerText': 'end time'},
                {'field': 'total_hours_view', 'headerText': 'total hours'},
                {'field': 'total_pay', 'headerText': 'total pay'},
            ],
            'treeColumnIndex': 1,
            'allowSorting': True,
            'allowFiltering': True,
            'allowTextWrap': True,
            'allowResizing': True,
            'allowReordering': True,
        })

        super().__init__(page_title=title, content=self.content, **kwargs)

    def form_show(self, **args):
        print('TreeGridPage.form_show')
        super().form_show(**args)
        emp_data = Employee.get_grid_view(self.employee_fields)
        ts_data = Timesheet.get_grid_view(self.timesheet_fields)
        for i in range(5):
            print(emp_data[i])
        for i in range(5):
            print(ts_data[i])
        self.grid_data = emp_data + ts_data
        self.tree_grid.dataSource = self.grid_data
        self.tree_grid.appendTo(f'#{self.container_id}')
        self.tree_grid.refresh()

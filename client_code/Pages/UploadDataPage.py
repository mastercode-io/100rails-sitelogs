from AnvilFusion.components.PageBase import PageBase
from AnvilFusion.components.FormInputs import *
from anvil.js.window import ej
from ..app.models import Employee, EmployeeRole, Job, Location, Timesheet, TimesheetType
from datetime import datetime, timedelta
import uuid
import json


MODELS_LIST = [
    'Employee',
    'Job',
    'Timesheet'
]

EMPLOYEE_FIELDS = {
    'first_name': lambda rec, _: rec['Full_Name'].strip().split(' ', 1)[0],
    'last_name': lambda rec, _: rec['Full_Name'].strip().split(' ', 1)[1] if ' ' in rec['Full_Name'].strip() else None,
    'email': lambda rec, _: rec.get('Work_Email', '').strip(),
    'mobile': lambda rec, _: rec.get('Work_Phone', '').strip(),
    'pay_rate': lambda rec, _: float(rec['Pay_Rate'].strip()) if rec.get('Pay_Rate', None) else None,
    'role': lambda rec, roles: [roles[rec['Default_Payroll_Role'].strip()]] if rec.get('Default_Payroll_Role', None) else None,
}

JOB_FIELDS = {
    'number': 'Quote_Job_Number',
    'name': lambda rec, _: rec.get('Job_Reference', None),
    'location': lambda rec, locations: locations[rec['Service_Location']] if rec.get('Service_Location', None) else None,
}

# timesheet_type = Relationship("TimesheetType")
# employee = Relationship("Employee")
# payrun = Relationship("PayRun")
# job = Relationship("Job")
# date = Attribute(field_type=types.FieldTypes.DATE)
# start_time = Attribute(field_type=types.FieldTypes.DATETIME)
# end_time = Attribute(field_type=types.FieldTypes.DATETIME)
# status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
TIMESHEET_FIELDS = {
    'timesheet_type': lambda rec, timesheet_types: timesheet_types[rec['Related_Time_Type']],
    'employee': lambda rec, employees: employees[rec['Related_Staff.Full_Name'].strip()],
    'job': lambda rec, jobs: [jobs[rec['Job_Number'].strip()]] if rec.get('Job_Number') else None,
    'date': 'Date',
}



class UploadDataPage(PageBase):
    def __init__(self, **kwargs):
        print('UploadDataPage')
        title = 'Upload Data'
        self.select_model = DropdownInput(name='select_model', label='Select Data Type', options=MODELS_LIST)
        self.upload_file = FileUploadInput(name='upload_file', label='Upload File', on_change=self.file_selected)
        self.import_button = ej.buttons.Button({
            'content': 'Import Records',
            'isPrimary': True,
            'size': 'large',
        })
        self.import_button_id = f'migrate-button-{uuid.uuid4()}'
        self.execution_log = InlineMessage(name='execution_log')
        self.record_count = InlineMessage(name='record_count')

        self.content = f'<br><div id="{self.select_model.container_id}" style="width:300px;"></div>'
        self.content += f'<div id="{self.upload_file.container_id}" style="width:300px;"></div>'
        self.content += f'<br><div id="{self.import_button_id}"></div><br><br>'
        self.content += f'<div id="{self.execution_log.container_id}" style="overflow-y: scroll; height: 100%;"></div>'
        self.content += f'<div id="{self.record_count.container_id}" style="overflow-y: scroll; height: 100%;"></div>'

        super().__init__(page_title=title, content=self.content, overflow='auto', **kwargs)

        self.file_content = None


    def form_show(self, **args):
        # print('MigratePage.form_show')
        super().form_show(**args)
        self.select_model.show()
        self.upload_file.show()
        self.import_button.appendTo(f'#{self.import_button_id}')
        self.import_button.element.onclick = self.import_button_action
        self.execution_log.show()
        self.execution_log.content = 'Click <b>Import Records</b> to start import<br><br>'
        self.record_count.show()


    def import_button_action(self, args):
        print('import_button_action')
        if self.select_model.value:
            self.execution_log.content = f'Importing {self.select_model.value} records<br><br>'
            if self.select_model.value == 'Employee' and 'Employees' in self.file_content:
                self.import_employees(self.file_content['Employees'])
            elif self.select_model.value == 'Job' and 'Jobs' in self.file_content:
                self.import_jobs(self.file_content['Jobs'])
            elif self.select_model.value == 'Timesheet' and 'Timesheets' in self.file_content:
                self.import_timesheets(self.file_content['Timesheets'])

        self.execution_log.content += '<br>Import completed'


    def log_message(self, message):
        self.execution_log.content += str(message) + '<br>'


    def file_selected(self, args):
        # print('file_selected', self.upload_file.value)
        file_obj = self.upload_file.value
        self.file_content = json.loads(file_obj.rawFile.text())
        if self.select_model.value == 'Employee':
            self.log_message(f'Uploaded {len(self.file_content["Employees"])} {self.select_model.value} records')


    def import_employees(self, employees):
        print('import_employees')
        self.log_message(f'Importing/updating {len(employees)} employees')

        # import employee roles
        uploaded_employee_roles = set(record['Default_Payroll_Role'].strip() for record in employees
                                      if record.get('Default_Payroll_Role', None))
        existing_employee_roles = set([role['name'] for role in EmployeeRole.search()])
        new_employee_roles = uploaded_employee_roles - existing_employee_roles
        if new_employee_roles:
            self.log_message(f'Adding {len(new_employee_roles)} employee roles')
            for role_name in new_employee_roles:
                EmployeeRole(name=role_name, status='Active').save()
        employee_roles = {role.name: role for role in EmployeeRole.search()}

        count_new = 0
        count_updated = 0
        new_employees = []
        for record in employees:
            employee_data = {k: v(record, employee_roles) if callable(v) else record[v] for k, v in EMPLOYEE_FIELDS.items()}
            employee_data['status'] = 'Active'
            employee = next(iter(Employee.search(first_name=employee_data['first_name'], last_name=employee_data['last_name'])), None)
            if employee:
                employee.update(employee_data)
                employee.save()
                count_updated += 1
            else:
                employee = Employee(**employee_data)
                employee.save()
                new_employees.append(employee)
                count_new += 1
            self.record_count.content = (f'Imported {count_new} employee records\nUpdated {count_updated} employee '
                                         f'records')
        return new_employees


    def import_jobs(self, jobs):
        print('import_jobs')
        self.log_message(f'Importing {len(jobs)} jobs')

        # import job types
        locations = {location['name']: location for location in Location.search(status='Active')}
        existing_jobs = [job['number'] for job in Job.search()]
        print('existing_jobs:', len(existing_jobs))

        count = 0
        new_jobs = []
        for record in jobs:
            if record['Quote_Job_Number'] not in existing_jobs:
                job_data = {k: v(record, locations) if callable(v) else record[v] for k, v in JOB_FIELDS.items()}
                job_data['status'] = 'Active'
                new_jobs.append(Job(**job_data).save())
                count += 1
                self.record_count.content = f'Imported {count} job records'
        return new_jobs


    def import_timesheets(self, timesheets):
        print('import_timesheets')

        # import timesheet types
        uploaded_timesheet_types = set(record['Related_Time_Type'] for record in timesheets)
        existing_timesheet_types = set([timesheet_type['name'] for timesheet_type in TimesheetType.search()])
        new_timesheet_types = uploaded_timesheet_types - existing_timesheet_types
        if new_timesheet_types:
            self.log_message(f'Adding {len(new_timesheet_types)} timesheet types')
            for timesheet_type_name in new_timesheet_types:
                TimesheetType(name=timesheet_type_name, status='Active').save()
        timesheet_types = {timesheet_type['name']: timesheet_type for timesheet_type in TimesheetType.search()}
        jobs = {job['number']: job for job in Job.search()}
        employees = {employee['full_name']: employee for employee in Employee.search()}

        self.log_message(f'Importing {len(timesheets)} timesheets')
        count = 0
        for record in timesheets:

            # add job if not exists
            if record['Related_Job.Quote_Job_Number'] not in jobs:
                new_jobs = self.import_jobs([{
                    'Quote_Job_Number': record['Related_Job.Quote_Job_Number'],
                    'Job_Reference': record['Related_Job.Job_Reference'],
                    'Service_Location': record['Related_Job.Service_Location'],
                    'Status': 'Active',
                }])
                jobs[record['Related_Job.Quote_Job_Number']] = new_jobs[0]

            # add employee if not exists
            if record['Related_Staff.Full_Name'].strip() not in employees:
                new_employees = self.import_employees([{
                    'Full_Name': record['Related_Staff.Full_Name'].strip(),
                    'Default_Payroll_Role': record['Related_Staff.Default_Payroll_Role'],
                    'Status': 'Active',
                }])
                employees[record['Related_Staff.Full_Name'].strip()] = new_employees[0]

            ts_date = datetime.strptime(record['Timesheet_Date'], '%d-%b-%Y').date()
            ts_start_time = datetime(ts_date.year, ts_date.month, ts_date.day,
                                     int(record['Start_Time'].split(':')[0]),
                                     int(record['Start_Time'].split(':')[1]))
            ts_end_time = datetime(ts_date.year, ts_date.month, ts_date.day,
                                   int(record['End_Time'].split(':')[0]),
                                   int(record['End_Time'].split(':')[1]))
            if ts_end_time < ts_start_time:
                ts_end_time += timedelta(days=1)
            timesheet_data = {
                'timesheet_type': timesheet_types[record['Related_Time_Type']],
                'employee': employees[record['Related_Staff.Full_Name'].strip()],
                'job': jobs[record['Related_Job.Quote_Job_Number']],
                'date': ts_date,
                'start_time': ts_start_time,
                'end_time': ts_end_time,
                'status': 'Approved',
            }
            Timesheet(**timesheet_data).save()
            count += 1
            self.record_count.content = f'Imported {count} timesheet records'

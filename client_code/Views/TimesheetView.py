from AnvilFusion.components.GridView import GridView
from AnvilFusion.components.FormInputs import Button, DropdownInput
from AnvilFusion.tools.utils import AppEnv
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from ..app.models import Payrun, Timesheet, PayRateRule, PayRateTemplate, PayRateTemplateItem, Scope, ScopeType
from ..payroll.pay_awards import PayItemAward, PayLine
import datetime
import json


class TimesheetView(GridView):
    def __init__(self, **kwargs):
        print('TimesheetView')

        view_config = {
            'model': 'Timesheet',
            'columns': [
                {'name': 'payrun.payrun_week', 'label': 'Payrun Week'},
                {'name': 'employee.full_name', 'label': 'Employee Name'},
                {'name': 'job.name', 'label': 'Job Name'},
                {'name': 'job.job_type.short_code', 'label': 'Job Type'},
                {'name': 'date', 'label': 'Date', 'format': 'E dd MMM'},
                {'name': 'start_time', 'label': 'Start Time', 'format': 'HH:mm'},
                {'name': 'end_time', 'label': 'End Time', 'format': 'HH:mm'},
                {'name': 'total_hours_view', 'label': 'Total Hours'},
                {'name': 'total_hours', 'visible': False},
                {'name': 'total_pay', 'label': 'Total Pay'},
                {'name': 'pay_lines', 'visible': False},
                {'name': 'pay_lines_view', 'label': 'Pay Lines', 'width': 300, 'disable_html_encode': False},
                {'name': 'status', 'label': 'Status'},
            ],
        }

        self.timesheet_view = DropdownInput(
            placeholder='Select View',
            css_class='e-outline pl-grid-toolbar-action-button pl-timesheet-toolbar-item-select-view',
            float_label=False,
            options=['Unassigned', 'Active Payrun', 'Past Periods'],
            required=True,
            on_change=self.timesheet_view_selected,
        )

        toolbar_actions = [
            {
                'name': 'select_payrun',
                'input': self.timesheet_view,
                'selected_records': False,
                'toolbar_click': False,
            },
            {
                'name': 'calculate_awards',
                'input': Button(
                    content='CALC Awards',
                    css_class='e-outline pl-grid-toolbar-action-button',
                    action=self.calculate_awards_action,
                ),
                'selected_records': True,
                'toolbar_click': True,
            },
            {
                'name': 'assign_payrun',
                'input': Button(
                    content='ASSIGN Payrun',
                    css_class='e-outline pl-grid-toolbar-action-button',
                    action=self.assign_unassign_action,
                ),
                'selected_records': True,
                'toolbar_click': False,
            },
            {
                'name': 'unassign_payrun',
                'input': Button(
                    content='UNASSIGN',
                    css_class='e-outline pl-grid-toolbar-action-button',
                    action=self.assign_unassign_action,
                ),
                'selected_records': False,
                'toolbar_click': False,
            },
        ]

        context_menu_items = [
            {'id': 'calculate_awards', 'label': 'Calculate Pay Awards', 'action': self.calculate_awards},
        ]
        self.grid_group_settings = {
            'Unassigned': {
                'columns': ['employee__full_name'],
                'showDropArea': False,
                # 'captionTemplate': '<div>${key} - ${data}</div>',
                'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
            },
            'Active Payrun': {
                'columns': ['employee__full_name'],
                'showDropArea': False,
                # 'captionTemplate': '<div>${key} - ${data}</div>',
                'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
            },
            'Past Periods': {
                'columns': ['payrun__payrun_week'],
                'showDropArea': False,
                # 'captionTemplate': None,
                # 'captionTemplate': '<div>${captionTimesheetListView(data)}</div>',
            },
        }

        super().__init__(
            model='Timesheet',
            title='Timesheet View',
            view_config=view_config,
            context_menu_items=context_menu_items,
            toolbar_actions=toolbar_actions,
            **kwargs)

        anvil.js.window['captionTimesheetListView'] = self.grouping_caption
        # anvil.js.window['timesheetListGroupingTotalHours'] = self.grouping_total_hours
        self.grid.allowGrouping = True
        self.grid.groupSettings = self.grid_group_settings['Unassigned']
        self.grid.aggregates = [{
            'columns': [
                {
                    'type': 'Custom',
                    'field': 'total_hours_view',
                    'columnName': 'total_hours_view',
                    'groupCaptionTemplate': '${Custom}',
                    'customAggregate': self.grouping_total_hours,
                },
            ],
        }]
        self.grid.allowSorting = True
        self.grid.sortSettings = {
            'columns': [
                {'field': 'employee__full_name', 'direction': 'Ascending'},
                {'field': 'date', 'direction': 'Ascending'},
                {'field': 'start_time', 'direction': 'Ascending'}
            ]
        }

        try:
            self.active_payrun = next(iter(Payrun.search(status='Preview')), None) or next(
                iter(Payrun.search(status='Created')), None)
        except StopIteration:
            self.active_payrun = None
            self.first_load = True


    def form_show(self, **args):
        print('TimesheetView.form_show')
        super().form_show(get_data=False, **args)
        self.timesheet_view.value = 'Unassigned'
        # print('toolbar')
        # for k in self.grid.toolbar.keys():
        #     print(k, self.grid.toolbar[k])


    def grouping_caption(self, args):
        # print('due_date_caption', args)
        # caption_color = 'color:#a63333;' if args['key'] == -100 else ''
        caption_color = 'color:#6750A4;'
        if self.timesheet_view.value in ('Unassigned', 'Active Payrun'):
            return (f'<div class="template" style="{caption_color}">'
                    f'{args.items[0].employee__full_name}</div>')
        else:
            return (f'<div class="template" style="{caption_color}">'
                    f'{args.key}</div>')


    def grouping_total_hours(self, data, column):
        if isinstance(data, list):
            return
        # print('grouping_total_hours', data.field)
        if self.timesheet_view.value in ('Unassigned', 'Active Payrun') or data.field == 'employee__full_name':
            week_total = sum(ts['total_hours'] for ts in data.items if ts['total_hours'])
            hours = int(week_total)
            minutes = int((week_total - hours) * 60)
            return f"{hours}:{minutes:02d} hrs per week"
        else:
            # print('__start__')
            # print(data)
            # print('__end__')
            return


    def query_cell_info(self, args):
        if 'field' in args.column.keys() and args.column['field'] == 'end_time':
            if args.data['start_time'] is not None and args.data['end_time'] is not None:
                # print(args.data['start_time'], args.data['end_time'])
                if isinstance(args.data['start_time'], str):
                    start_date = datetime.datetime.fromisoformat(args.data['start_time']).date()
                else:
                    start_date = datetime.datetime.fromtimestamp(args.data['start_time'].getTime() / 1000).date()
                if isinstance(args.data['end_time'], str):
                    end_date = datetime.datetime.fromisoformat(args.data['end_time']).date()
                else:
                    end_date = datetime.datetime.fromtimestamp(args.data['end_time'].getTime() / 1000).date()
                plus_days = (end_date - start_date).days
                if plus_days > 0:
                    args.cell.innerHTML = f'{args.cell.innerHTML} +{plus_days} day(s)'
        super().query_cell_info(args)


    def calculate_awards_action(self, args):
        selected_records = {rec['employee__full_name']: rec for rec in self.grid.getSelectedRecords()}
        for employee_name in selected_records:
            self.calculate_awards({'rowInfo': {'rowData': selected_records[employee_name]}})


    def timesheet_view_selected(self, args):
        print('timesheet_view_selected', args)
        if args['value'] == 'Unassigned':
            self.edit_mode = 'dialog'
            self.grid.allowSelection = True
            self.grid.editSettings.allowDeleting = True
            self.grid.columns[self.grid_column_indexes['_selected']].visible = True
            self.grid.columns[self.grid_column_indexes['payrun__payrun_week']].visible = False
            self.grid_data = Timesheet.get_grid_view(view_config=self.view_config,
                                                     filters={'payrun': None})
            self.grid.clearGrouping()
            self.grid.groupColumn('employee__full_name')
            self.grid.element.querySelector(f'.e-toolbar .e-toolbar-item[title="Add"]').style.display = 'inline-flex'
            for action_item in self.toolbar_actions:
                if action_item == 'assign_payrun':
                    self.toolbar_actions[action_item]['selected_records'] = True
                if action_item == 'unassign_payrun':
                    self.toolbar_actions[action_item]['selected_records'] = False

        elif args['value'] == 'Active Payrun':
            self.edit_mode = 'dialog'
            self.grid.allowSelection = True
            self.grid.editSettings.allowDeleting = False
            self.grid.element.querySelector(f'.e-toolbar .e-toolbar-item[title="Add"]').style.display = 'none'
            self.grid.columns[self.grid_column_indexes['_selected']].visible = True
            self.grid.columns[self.grid_column_indexes['payrun__payrun_week']].visible = False
            if self.active_payrun is None:
                self.grid_data = []
            else:
                self.grid_data = Timesheet.get_grid_view(view_config=self.view_config,
                                                         filters={'payrun': self.active_payrun})
            self.grid.clearGrouping()
            self.grid.groupColumn('employee__full_name')
            for action_item in self.toolbar_actions:
                if action_item == 'assign_payrun':
                    self.toolbar_actions[action_item]['selected_records'] = False
                if action_item == 'unassign_payrun':
                    self.toolbar_actions[action_item]['selected_records'] = True

        elif args['value'] == 'Past Periods':
            self.edit_mode = 'view'
            self.grid.allowSelection = False
            self.grid.element.querySelector(f'.e-toolbar .e-toolbar-item[title="Add"]').style.display = 'none'
            self.grid.columns[self.grid_column_indexes['_selected']].visible = False
            self.grid.columns[self.grid_column_indexes['payrun__payrun_week']].visible = True
            if self.active_payrun is not None:
                active_row = Payrun.get_row(self.active_payrun['uid'])
                self.grid_data = Timesheet.get_grid_view(view_config=self.view_config,
                                                         search_queries=[q.all_of(payrun=q.none_of(None, active_row))])
            else:
                self.grid_data = []
            self.grid.clearGrouping()
            self.grid.groupColumn('payrun__payrun_week')
            self.grid.groupColumn('employee__full_name')

        else:
            self.grid_data = []
        print('grid_data', len(self.grid_data))
        self.grid.dataSource = self.grid_data
        # grouped_rows = self.grid.getContentTable().querySelectorAll('.e-recordplusexpand, .e-recordpluscollapse')
        # print('grouped_rows', grouped_rows)
        # for row in grouped_rows:
        #     print(row)
        #     self.grid.groupModule.expandCollapseRows(row)


    def assign_unassign_action(self, args):
        args.cancel = True
        if 'rowInfo' in args:
            for key in args['rowInfo']:
                print(key, args['rowInfo'][key])
            timesheet_uids = [args['rowInfo']['rowData']['uid']]
        else:
            timesheet_uids = [rec['uid'] for rec in self.grid.getSelectedRecords()]
        print('assign_unassign_action', timesheet_uids)
        self.show_confirm_dialog = False
        self.assign_unassign_payrun(timesheet_uids)
        self.show_confirm_dialog = True
        self.grid.refresh()


    def assign_unassign_payrun(self, timesheet_uids):
        print('assign_unassign_payrun', timesheet_uids)
        if self.timesheet_view.value == 'Unassigned':
            if self.active_payrun is None:
                return
            payrun = self.active_payrun
        else:
            payrun = None
        for ts_uid in timesheet_uids:
            ts = Timesheet.get(ts_uid)
            ts['payrun'] = payrun
            ts.save()
            row_index = self.grid.getRowIndexByPrimaryKey(ts_uid)
            row = self.grid.getRowByIndex(row_index)
            print('delete row', ts_uid, row_index, row)
            # self.grid.dataSource.remove(grid_row)
            # self.grid.deleteRow(row)
        for ts_uid in timesheet_uids:
            self.grid.deleteRecord('uid', ts_uid)


    def calculate_awards(self, args):
        print('calculate_awards', args['rowInfo']['rowData'])
        ts = Timesheet.get(args['rowInfo']['rowData']['uid'])
        employee = ts['employee']
        ts_date = ts['date']
        start_of_week = ts_date - datetime.timedelta(days=ts_date.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        print('week dates', start_of_week, end_of_week)

        stime = datetime.datetime.now()

        job_type_scopes = [*Scope.search(type=ScopeType.get_by('name', 'Job Type'))]
        print('job_type_scopes', len(job_type_scopes))
        # get start and end of week
        # get all timesheets for the week
        timesheets = [*Timesheet.search(
            date=q.all_of(q.greater_than_or_equal_to(start_of_week), q.less_than_or_equal_to(end_of_week)),
            employee=employee,
            search_query=tables.order_by('date', ascending=True)
        )]
        print('timesheets', len(timesheets))
        ts_row_index_list = [self.grid.getRowIndexByPrimaryKey(ts['uid']) for ts in timesheets]
        self.grid.selectRows(ts_row_index_list)
        pay_lines = []
        for ts in timesheets:
            # print(ts['job']['job_type']['short_code'])
            scope = next((s for s in job_type_scopes if s['short_code'] == ts['job']['job_type']['short_code']), None)
            pay_rate_template = PayRateTemplate.get_by('scope', scope)
            pay_item_list = [item for item in PayRateTemplateItem.search(
                pay_rate_template=pay_rate_template,
                search_query=tables.order_by('order_number', ascending=True)
            ) if item['pay_rate_rule']['time_scope'] != 'Week']
            unallocated_time = [(ts['start_time'], ts['end_time'])]
            ts_pay_lines = []
            total_pay = 0
            for pay_item in pay_item_list:
                if unallocated_time:
                    start_time, end_time = unallocated_time.pop(0)
                else:
                    # start_time = end_time = None
                    break
                # print('pay_item', pay_item, start_time, end_time)
                pay_line, unallocated_time = PayItemAward(pay_item).calculate_award(
                    date=ts['date'],
                    start_time=start_time,
                    end_time=end_time,
                    total_hours=ts['total_hours'],
                    employee_base_rate=employee['pay_rate'],
                    employee_role=employee['role'],
                )
                # print('pay_line', pay_line, unallocated_time)
                if pay_line:
                    pay_line.timesheet = ts
                    ts_pay_lines.append(pay_line)
                    total_pay += pay_line.pay_amount
            if ts_pay_lines:
                pay_lines.extend(ts_pay_lines)
                ts['total_pay'] = total_pay
                ts['pay_lines'] = [str(pl) for pl in ts_pay_lines]
                ts.save()
                self.update_grid(ts, False)
        self.grid.clearSelection()
        pay_rule_list = PayRateRule.search(
            time_scope='Week',
            search_query=tables.order_by('overtime_start', ascending=True)
        )
        for pay_rule in pay_rule_list:
            # print('pay_rule', pay_rule.name)
            week_hours = 0
            week_pay_lines = []
            overtime_lines = []
            is_overtime = False
            for pay_line in pay_lines:
                if pay_line.count_overtime is False:
                    week_pay_lines.append(pay_line)
                    continue
                elif is_overtime:
                    overtime_lines.append(pay_line)
                    continue
                else:
                    week_hours += pay_line.units
                    # print('week_hours', week_hours, pay_line)
                if week_hours <= pay_rule['overtime_start']:
                    week_pay_lines.append(pay_line)
                else:
                    print('pay_line', pay_line, week_hours, pay_rule['overtime_start'])
                    overtime_hours = week_hours - pay_rule['overtime_start']
                    overtime_line = pay_line.split(overtime_hours)
                    week_pay_lines.append(pay_line)
                    overtime_lines.append(overtime_line)
                    is_overtime = True
            pay_lines = week_pay_lines.copy()
            if overtime_lines:
                for overtime_line in overtime_lines:
                    overtime_line.pay_rate = overtime_line.base_rate * pay_rule['pay_rate_multiplier']
                    overtime_line.pay_rate_title = pay_rule['name']
                    print('overtime_line', overtime_line)
                print('overtime_lines', overtime_lines)
                pay_lines.extend(overtime_lines)

        etime = datetime.datetime.now()
        print('calc time', etime - stime)
        print('pay_lines')
        for pl in pay_lines:
            print(pl)

        # for ts in timesheets:
        #     self.update_grid(ts, False)


    @staticmethod
    def calculate_pay_lines(
            time_frames=None,
            pay_item=None,
            employee=None,
    ):
        pay_rule = pay_item['pay_rate_rule']
        rule_start_time = pay_rule['start_time'].time()
        rule_end_time = pay_rule['end_time'].time()
        max_hours = pay_rule['max_time'] or -1
        unallocated_time_frames = []
        pay_lines = []
        for frame in time_frames:
            start_time, end_time = frame
            if end_time.time() <= rule_start_time or start_time.time() >= rule_end_time:
                unallocated_time_frames.append(frame)
                continue
            if start_time.time() < rule_start_time:
                unallocated_time_frames.append(
                    (start_time, datetime.datetime.combine(start_time.date(), rule_start_time)))
                do_start_time = datetime.datetime.combine(start_time.date(), rule_start_time)
            else:
                do_start_time = start_time
            if end_time.time() > rule_end_time:
                unallocated_time_frames.append((datetime.datetime.combine(end_time.date(), rule_end_time), end_time))
                do_end_time = datetime.datetime.combine(end_time.date(), rule_end_time)
            else:
                do_end_time = end_time
            units = (do_end_time - do_start_time).total_seconds() / 3600
            if 0 <= max_hours < units:
                overtime_hours = units - max_hours
                units = max_hours
                unallocated_time_frames.append((do_end_time, end_time))
            elif max_hours != -1:
                max_hours -= units
            pay_rate = pay_item['pay_rate'] or employee['pay_rate']
            if pay_rule['pay_rate_type'] == 'Rate Per Unit':
                pay_amount = pay_rate * units
            elif pay_rule['pay_rate_type'] == 'Multiplier':
                pay_rate = pay_rate * pay_item['pay_rate_multiplier']
                pay_amount = pay_rate * units
            elif pay_rule['pay_rate_type'] == 'Fixed Amount':
                pay_amount = pay_item['pay_rate']
                units = 1
            else:
                pay_amount = 0
            if pay_amount:
                pay_line = {
                    'pay_rate_title': pay_item['pay_rate_title'],
                    'pay_category': pay_item['pay_category'],
                    'date': do_start_time.date(),
                    'start_time': do_start_time,
                    'end_time': do_end_time,
                    'pay_rate': pay_rate,
                    'units': units,
                    'pay_amount': pay_amount,
                }
                pay_lines.append(pay_line)
        return unallocated_time_frames, pay_lines


    @staticmethod
    def calculate_week_overtime(pay_lines=None, pay_items=None):
        for pay_item in pay_items:
            pay_rule = pay_item['pay_rule']
            if pay_rule['time_scope'] != 'Week':
                continue
            overtime_start = pay_rule['overtime_start']
            max_hours = pay_rule['max_hours'] or 0
            if not overtime_start or not max_hours:
                continue
            week_hours = 0
            overtime_hours = 0
            week_pay_lines = []
            for pl in pay_lines:
                if overtime_hours:
                    week_pay_lines.append(pl)
                    continue
                if pl['hours'] and 'earnings' in pay_rule['earnings_type'].lower():
                    week_hours += pl['hours']
                else:
                    week_pay_lines.append(pl)
                    continue
                if week_hours > overtime_start:
                    overtime_hours = week_hours - overtime_start
                    pl['hours'] -= overtime_hours
                    pl['pay_amount'] -= overtime_hours * pl['pay_rate']
                    week_pay_lines.append(pl)
                    if max_hours and overtime_hours > max_hours:
                        rule_hours = max_hours
                        overtime_hours -= max_hours
                    else:
                        rule_hours = overtime_hours
                    overtime_pl = {
                        'pay_rate_title': pay_item['pay_rate_title'],
                        'pay_category': pay_item['pay_category'],
                        'date': pl['date'],
                        'start_time': pl['end_time'],
                        'end_time': pl['end_time'] + datetime.timedelta(hours=overtime_hours),
                        'pay_rate': pl['pay_rate'],
                        'hours': rule_hours,
                        'pay_amount': rule_hours * pl['pay_rate'],
                    }
                    week_pay_lines.append(overtime_pl)
                    if overtime_hours:
                        pl_tail = pl.copy()
                        pl_tail['hours'] = overtime_hours
                        pl_tail['pay_amount'] = overtime_hours * pl['pay_rate']
                        pl_tail['start_time'] = pl['end_time'] + datetime.timedelta(hours=overtime_hours)
                        pl_tail['end_time'] = pl['end_time'] + datetime.timedelta(hours=overtime_hours)
                        week_pay_lines.append(pl_tail)
                else:
                    week_pay_lines.append(pl)

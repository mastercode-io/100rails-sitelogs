from AnvilFusion.datamodel.particles import (
    model_type,
    Attribute,
    Relationship,
    Computed,
)
from AnvilFusion.datamodel import types
from datetime import date, datetime, timedelta


WEEK_DAY_NAME = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

TIMESHEET_STATUS = [
    "Draft",
    "Approved",
    "Processed",
]


@model_type
class TimesheetType:
    _title = "short_code"

    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)

    configuration_schema = {
        "job_required": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "sick_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "annual_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "paid_breaks": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "unpaid_leave": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "worked_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "other": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_time": Attribute(field_type=types.FieldTypes.BOOLEAN),
        "break_length": Attribute(field_type=types.FieldTypes.NUMBER),
    }
    configuration = Attribute(
        field_type=types.FieldTypes.OBJECT, schema=configuration_schema

    )


@model_type
class Timesheet:
    _title = "employee"

    timesheet_type = Relationship("TimesheetType")
    employee = Relationship("Employee")
    payrun = Relationship("Payrun")
    job = Relationship("Job")
    tags = Relationship("Tag", with_many=True)
    date = Attribute(field_type=types.FieldTypes.DATE)
    start_time = Attribute(field_type=types.FieldTypes.DATETIME)
    end_time = Attribute(field_type=types.FieldTypes.DATETIME)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    approved_by = Relationship("Employee")
    notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    total_pay = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_lines = Attribute(field_type=types.FieldTypes.OBJECT)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)

    @staticmethod
    def calculate_total_hours(args):
        if args["start_time"] is None or args["end_time"] is None:
            return 0
        if args["start_time"] <= args["end_time"]:
            return (args["end_time"] - args["start_time"]).total_seconds() / 3600
        else:
            return ((args["end_time"] + timedelta(days=1)) - args["start_time"]).total_seconds() / 3600
    total_hours = Computed(("start_time", "end_time"), "calculate_total_hours")

    @staticmethod
    def calculate_total_hours_view(args):
        if not isinstance(args["start_time"], datetime) or not isinstance(args["end_time"], datetime):
            return 0
        if args["start_time"] <= args["end_time"]:
            total_hours = (args["end_time"] - args["start_time"]).total_seconds() / 3600
        else:
            total_hours = ((args["end_time"] + timedelta(days=1)) - args["start_time"]).total_seconds() / 3600
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        return f"{hours}:{minutes:02d}"
    total_hours_view = Computed(("start_time", "end_time"), "calculate_total_hours_view")

    @staticmethod
    def get_day_type(args):
        if not isinstance(args["date"], date):
            return None, None
        day_of_week = args['date'].weekday()
        if day_of_week == 5 or day_of_week == 6:  # Saturday or Sunday
            return "Weekend", WEEK_DAY_NAME[day_of_week]
        else:
            return "Weekday", WEEK_DAY_NAME[day_of_week]
    day_type = Computed(("date",), "get_day_type")

    @staticmethod
    def print_pay_lines(args):
        if args['pay_lines'] is not None:
            return '<br>'.join(args['pay_lines'])
        else:
            return ''
    pay_lines_view = Computed(("pay_lines",), "print_pay_lines")

    def validate(self):
        if isinstance(self.start_time, datetime) and isinstance(self.end_time, datetime):
            if self.start_time > self.end_time:
                self.end_time = datetime.combine(self.start_time.date() + timedelta(days=1), self.end_time.time())

        if not isinstance(self.status, str) or self.status.capitalize() not in TIMESHEET_STATUS:
            self.status = "Draft"

        return True, None

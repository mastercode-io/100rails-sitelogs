from AnvilFusion.datamodel import types
from ..app import models
from anvil.tables import query as q
import anvil.tables as tables
import datetime
from AnvilFusion.datamodel import types


def type_check(value, field_type):
    try:
        if field_type == types.FieldTypes.DATE:
            return datetime.date.fromisoformat(value)
        elif field_type == types.FieldTypes.DATETIME:
            return datetime.datetime.fromisoformat(value)
        elif field_type == types.FieldTypes.TIME:
            return datetime.datetime.fromisoformat(value)
        elif field_type == types.FieldTypes.NUMBER:
            return float(value)
        elif field_type == types.FieldTypes.DECIMAL:
            return float(value)
        elif field_type == types.FieldTypes.CURRENCY:
            return float(value)
        elif field_type == types.FieldTypes.BOOLEAN:
            if isinstance(value, str):
                if value.lower() in ['true', 'yes', '1']:
                    return True
                elif value.lower() in ['false', 'no', '0']:
                    return False
                else:
                    return None
            return bool(value)
        else:
            return value
    except Exception as e: # noqa
        return None


def get_timesheet_filters(params, integration_uid):
    start_date = params.get('start_date', '')
    end_date = params.get('end_date', '')
    employee_uid = params.get('employee_uid', None)
    employee_link_id = params.get('employee_link_id', None)
    filters = {}
    if employee_uid:
        employee = models.Employee.get(employee_uid)
        if employee is not None:
            filters['employee'] = employee
    elif employee_link_id:
        filters['remote_links'] = {integration_uid: employee_link_id}
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        start_date = None
    try:
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        end_date = None
    if start_date and not end_date:
        filters['date'] = q.greater_than_or_equal_to(start_date)
    elif end_date and not start_date:
        filters['date'] = q.less_than_or_equal_to(end_date)
    elif start_date and end_date:
        filters['date'] = q.between(start_date, end_date, max_inclusive=True)
    return filters


EMPLOYEE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'first_name',
        'last_name',
        'short_code',
        'email',
        'mobile',
        'status',
        'address',
        'custom_fields',
        'remote_links',
    ],
    'relationships': {
        'role': {
            'fields': [
                'name',
                'pay_rate',
                'remote_links'
            ],
        },
    },
}

EMPLOYEE_ROLE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'pay_rate',
        'status',
        'remote_links',
    ]
}

JOB_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'number',
        'description',
        'status',
        'custom_fields',
        'remote_links',
    ],
    'relationships': {
        'job_type': {
            'fields': [
                'name',
                'short_code',
                'remote_links'
            ],
        },
        'location': {
            'fields': [
                'name',
                'address',
                'remote_links'
            ],
        },
    },
}

JOB_TYPE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'short_code',
        'description',
        'status',
        'remote_links',
    ],
}

LOCATION_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'short_code',
        'description',
        'address',
        'status',
        'remote_links',
    ],
}

PAY_CATEGORY_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'pay_category_code',
        'pay_category_type',
        'description',
        'status',
        'remote_links',
    ],
}
TIMESHEET_JSON_SCHEMA = {
    'fields': [
        'uid',
        'date',
        'start_time',
        'end_time',
        'total_hours',
        'total_pay',
        'pay_lines',
        'status',
        'notes',
        'remote_links',
    ],
    'relationships': {
        'timesheet_type': {
            'fields': [
                'name',
                'short_code',
                'remote_links'
            ],
        },
        'employee': {
            'fields': [
                'full_name',
                'remote_links'
            ],
        },
        'approved_by': {
            'fields': [
                'full_name',
                'remote_links'
            ],
        },
        'job': {
            'fields': [
                'name',
                'number',
                'remote_links'
            ],
        },
    },
}

TIMESHEET_TYPE_JSON_SCHEMA = {
    'fields': [
        'uid',
        'name',
        'short_code',
        'description',
        'status',
        'configuration',
        'remote_links',
    ],
}

API_RESOURCES = {
    # /api/employees/
    'employees': {
        'name': 'employees',
        'model': models.Employee,
        'json_schema': EMPLOYEE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('first_name', ascending=True),
            tables.order_by('last_name', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': None,
    },

    # /api/employee_roles/
    'employee_roles': {
        'name': 'employee_roles',
        'model': models.EmployeeRole,
        'json_schema': EMPLOYEE_ROLE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    # /api/jobs/
    'jobs': {
        'name': 'jobs',
        'model': models.Job,
        'json_schema': JOB_JSON_SCHEMA,
        'sorting': [
            tables.order_by('number', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': None,
    },

    # /api/job_types/
    'job_types': {
        'name': 'job_types',
        'model': models.JobType,
        'json_schema': JOB_TYPE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    # /api/locations/
    'locations': {
        'name': 'locations',
        'model': models.Location,
        'json_schema': LOCATION_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    # /api/pay_categories/
    'pay_categories': {
        'name': 'pay_categories',
        'model': models.PayCategory,
        'json_schema': PAY_CATEGORY_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },

    # /api/timesheets/
    'timesheets': {
        'name': 'timesheets',
        'model': models.Timesheet,
        'json_schema': TIMESHEET_JSON_SCHEMA,
        'sorting': [
            tables.order_by('employee', ascending=True),
            tables.order_by('date', ascending=True),
        ],
        'pagination': True,
        'remote_links': True,
        'filters': get_timesheet_filters,
    },

    # /api/timesheet_types/
    'timesheet_types': {
        'name': 'timesheet_types',
        'model': models.TimesheetType,
        'json_schema': TIMESHEET_TYPE_JSON_SCHEMA,
        'sorting': [
            tables.order_by('name', ascending=True),
        ],
        'pagination': False,
        'remote_links': True,
        'filters': None,
    },
}

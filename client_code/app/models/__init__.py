from AnvilFusion.datamodel.particles import (
    model_type,
    Attribute,
    Relationship,
    Computed,
    SYSTEM_TENANT_UID
)
from AnvilFusion.datamodel import types
from datetime import date, datetime, timedelta

from .timesheet import TimesheetType, Timesheet

TimesheetType.__module__ = __name__
Timesheet.__module__ = __name__

# Model list for enumerations
ENUM_MODEL_LIST = {
    # 'Activity': {'model': 'Activity', 'text_field': 'name'},
}

''' remote_links = Attribute(field_type=types.FieldTypes.OBJECT)
    is a special field that is used to store links to external resources
    in the format:
    {
        AppIntegration.uid: remote_link_id (string ID of a resource in the external system)),
        ...
    }
'''


# ------------------------------
# Framework object model classes
# ------------------------------
@model_type
class AppInApiCredential:
    _title = "integration.service_name"
    integration = Relationship("AppIntegration")
    api_secret = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    api_key = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    api_user = Relationship("User")
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class AppOutApiCredential:
    _title = "integration.service_name"
    integration = Relationship("AppIntegration")
    auth_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    api_credentials = Attribute(field_type=types.FieldTypes.OBJECT)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class AppIntegration:
    _title = "service_name"
    service_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    service_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    url = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    auth_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    auth_data = Attribute(field_type=types.FieldTypes.OBJECT)
    direction = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class AppIntegrationConnection:
    _title = "integration.service_name"
    integration = Relationship("AppIntegration")
    auth_credentials = Attribute(field_type=types.FieldTypes.OBJECT)
    api_key = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    api_user = Relationship("User")
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class AppAuditLog:
    model_type = types.ModelTypes.SYSTEM
    table_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    record_uid = Attribute(field_type=types.FieldTypes.UID)
    action_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    action_time = Attribute(field_type=types.FieldTypes.DATETIME)
    action_by = Attribute(field_type=types.FieldTypes.UID)
    previous_state = Attribute(field_type=types.FieldTypes.OBJECT)
    new_state = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class AppErrorLog:
    model_type = types.ModelTypes.SYSTEM
    component = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    action = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    error_message = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    error_time = Attribute(field_type=types.FieldTypes.DATETIME)
    user_uid = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppComponent:
    model_type = types.ModelTypes.SYSTEM
    type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    version = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    id = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    props = Attribute(field_type=types.FieldTypes.OBJECT)
    items = Relationship("AppComponent", with_many=True)
    permissions = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class AppGridView:
    _title = "name"
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    columns = Attribute(field_type=types.FieldTypes.OBJECT)
    config = Attribute(field_type=types.FieldTypes.OBJECT)
    permissions = Attribute(field_type=types.FieldTypes.OBJECT)
    owner = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class AppEnum:
    _title = "name"
    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    options = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class AppUploadsCache:
    _model_type = types.ModelTypes.SYSTEM
    _singular_name = "AppUploadsCache"
    _plural_name = "AppUploadsCache"
    _table_name = "app_uploads_cache"
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=types.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
    link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=types.FieldTypes.UID)
    content = Attribute(field_type=types.FieldTypes.MEDIA)


@model_type
class AppCustomFieldsSchema:
    _title = "name"

    _model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    model = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    schema = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Upload:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mime_type = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    size = Attribute(field_type=types.FieldTypes.NUMBER)
    meta_info = Attribute(field_type=types.FieldTypes.OBJECT)
    link_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    link_uid = Attribute(field_type=types.FieldTypes.UID)
    location = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class File:
    model_type = types.ModelTypes.SYSTEM
    path = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    file = Attribute(field_type=types.FieldTypes.MEDIA)
    file_version = Attribute(field_type=types.FieldTypes.SINGLE_LINE)


@model_type
class Tenant:
    _title = "name"

    model_type = types.ModelTypes.SYSTEM
    account_uid = Attribute(field_type=types.FieldTypes.UID)
    # tenant_uid = Attribute(field_type=types.FieldTypes.UID)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class SubscriptionPlan:
    _title = "name"

    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    price = Attribute(field_type=types.FieldTypes.CURRENCY)
    features = Attribute(field_type=types.FieldTypes.OBJECT)
    components = Relationship("AppComponent", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    app_config_schema = {
        "app_menu": Attribute(field_type=types.FieldTypes.OBJECT),
        "special_menus": Attribute(field_type=types.FieldTypes.OBJECT),
        "components": Attribute(field_type=types.FieldTypes.OBJECT),
        "limits": Attribute(field_type=types.FieldTypes.OBJECT),
    }
    app_config = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class User:
    _title = "full_name"

    model_type = types.ModelTypes.SYSTEM
    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.EMAIL)
    enabled = Attribute(field_type=types.FieldTypes.BOOLEAN)
    last_login = Attribute(field_type=types.FieldTypes.DATETIME)
    password_hash = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    n_password_failures = Attribute(field_type=types.FieldTypes.NUMBER)
    confirmed_email = Attribute(field_type=types.FieldTypes.BOOLEAN)
    signed_up = Attribute(field_type=types.FieldTypes.DATETIME)
    user_role = Relationship("UserRole", with_many=False)

    permissions_schema = {
        "administrator": Attribute(field_type=types.FieldTypes.BOOLEAN),
    }
    permissions = Attribute(field_type=types.FieldTypes.OBJECT, schema=permissions_schema)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"
    full_name = Computed(("first_name", "last_name"), "get_full_name")

    @staticmethod
    def get_tenant_name(args):
        if args['tenant_uid'] == '00000000-0000-0000-0000-000000000000':
            return 'System'
        elif args['tenant_uid'] is not None:
            tenant = Tenant.get(args['tenant_uid'])
            if tenant:
                return tenant['name']
            else:
                return 'Not Found'
        return 'N/A'
    tenant_name = Computed(["tenant_uid"], "get_tenant_name")


@model_type
class UserRole:
    _title = "name"

    model_type = types.ModelTypes.SYSTEM
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    permissions_schema = {
        "administrator": Attribute(field_type=types.FieldTypes.BOOLEAN),
    }
    permissions = Attribute(field_type=types.FieldTypes.OBJECT, schema=permissions_schema)
    access_permissions_schema = {
        "app_menu": Attribute(field_type=types.FieldTypes.OBJECT),
        "special_menus": Attribute(field_type=types.FieldTypes.OBJECT),
        "components": Attribute(field_type=types.FieldTypes.OBJECT),
    }
    access_permissions = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class UserProfile:
    _title = "user"
    user = Relationship("User")


# -------------------------
# Data object model classes
# -------------------------
@model_type
class Account:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    business_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "time_zone": Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    phone = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    website = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    logo = Attribute(field_type=types.FieldTypes.MEDIA)
    subscription_dates_schema = {
        "status": Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
        "start_date": Attribute(field_type=types.FieldTypes.DATE),
        "end_date": Attribute(field_type=types.FieldTypes.DATE),
        "trial_start": Attribute(field_type=types.FieldTypes.DATE),
        "trial_end": Attribute(field_type=types.FieldTypes.DATE),
        "current_period_start": Attribute(field_type=types.FieldTypes.DATE),
        "current_period_end": Attribute(field_type=types.FieldTypes.DATE),
    }
    subscription_dates = Attribute(field_type=types.FieldTypes.OBJECT, schema=subscription_dates_schema)
    subscription_plan = Relationship("SubscriptionPlan")
    default_pay_entity = Relationship("Tenant")
    pay_entities = Relationship("Tenant", with_many=True)


@model_type
class Calendar:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    week_start = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    workdays = Attribute(field_type=types.FieldTypes.ENUM_MULTI)
    weekend = Attribute(field_type=types.FieldTypes.ENUM_MULTI)
    public_holidays = Attribute(field_type=types.FieldTypes.OBJECT)
    special_holidays = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Employee:
    _title = "full_name"

    first_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    last_name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    email = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    mobile = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    role = Relationship("EmployeeRole")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)

    @staticmethod
    def get_full_name(args):
        return f"{args['first_name']} {args['last_name']}"

    full_name = Computed(("first_name", "last_name"), "get_full_name")


@model_type
class EmployeeRole:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Job:
    _title = "name"

    job_type = Relationship("JobType")
    location = Relationship("Location")
    tags = Relationship("Tag", with_many=True)
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    number = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class JobType:
    _title = "short_code"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    # pay_rate_template = Relationship("PayRateTemplate")
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Location:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    address_schema = {
        "address_line_1": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "address_line_2": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "city_district": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "state_province": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "country": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "postal_code": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    address = Attribute(field_type=types.FieldTypes.OBJECT, schema=address_schema)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)

    @staticmethod
    def get_address_oneline(args):
        if not args["address"]:
            return ''
        address_online = ''
        address_online += f'{args["address"].get("address_line_1", "")}, '
        address_online += f'{args["address"].get("address_line_2", "")}, '
        address_online += f'{args["address"].get("city_district", "")}, '
        address_online += f'{args["address"].get("state_province", "")}, '
        address_online += f'{args["address"].get("country", "")}, '
        address_online += f'{args["address"].get("postal_code", "")}'
        address_online = address_online.strip(', ')
        address_online = address_online.replace(', ,', ',')
        return address_online

    address_oneline = Computed(["address"], "get_address_oneline")


@model_type
class PayCategory:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_category_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_category_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class PayRateRule:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    scope = Relationship("Scope")
    tags = Relationship("Tag", with_many=True)
    time_scope = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    time_limits = Attribute(field_type=types.FieldTypes.BOOLEAN)
    start_time = Attribute(field_type=types.FieldTypes.TIME)
    end_time = Attribute(field_type=types.FieldTypes.TIME)
    max_hours = Attribute(field_type=types.FieldTypes.NUMBER)
    count_overtime = Attribute(field_type=types.FieldTypes.BOOLEAN)
    overtime_start = Attribute(field_type=types.FieldTypes.NUMBER)
    unit_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    earnings_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)

    calculation_settings_schema = {
        "exclude_break_time": Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
        "exclude_week_overtime": Attribute(field_type=types.FieldTypes.ENUM_SINGLE),
    }
    calculation_settings = Attribute(field_type=types.FieldTypes.OBJECT, schema=calculation_settings_schema)


@model_type
class PayRateTemplate:
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    scope = Relationship("Scope")
    pay_rate_items = Relationship("PayRateTemplateItem", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRateTemplateItem:
    _title = "default_pay_rate_title"
    pay_rate_template = Relationship("PayRateTemplate")
    pay_rate_rule = Relationship("PayRateRule")
    default_pay_category = Relationship("PayCategory")
    default_pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    pay_rate_multiplier = Attribute(field_type=types.FieldTypes.NUMBER)
    default_pay_rate_title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    order_number = Attribute(field_type=types.FieldTypes.NUMBER)
    specific_roles = Relationship("PayRateTemplateSpecificRole", with_many=True)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayRateTemplateSpecificRole:
    _title = "name"
    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate_template_item = Relationship("PayRateTemplateItem")
    employee_role = Relationship("EmployeeRole")
    pay_category = Relationship("PayCategory")
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class PayrollConfig:
    _title = "integration.name"

    payroll_integration = Relationship("AppIntegration")
    payroll_connection = Relationship("AppIntegrationConnection")
    timesheet_integration = Relationship("AppIntegration")
    timesheet_connection = Relationship("AppIntegrationConnection")
    frequency = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_period_start_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_period_end_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    pay_day = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    payrun_initial_date = Attribute(field_type=types.FieldTypes.DATE)
    pay_category_type = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Payrun:
    _title = "pay_period_start"

    pay_period_start = Attribute(field_type=types.FieldTypes.DATE)
    pay_period_end = Attribute(field_type=types.FieldTypes.DATE)
    pay_date = Attribute(field_type=types.FieldTypes.DATE)
    status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)
    action_log_schema = {
        "action": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "timestamp": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
        "user_name": Attribute(field_type=types.FieldTypes.SINGLE_LINE),
    }
    action_log = Attribute(field_type=types.FieldTypes.OBJECT, schema=action_log_schema)

    @staticmethod
    def get_payrun_week(args):
        if args['pay_period_end']:
            return f"{args['pay_period_end'].year} - wk{args['pay_period_end'].isocalendar()[1]}"
        else:
            return ''
    payrun_week = Computed(["pay_period_end"], "get_payrun_week")


@model_type
class PayrunItem:
    _title = "title"

    payrun = Relationship("Payrun")
    employee = Relationship("Employee")
    timesheet = Relationship("Timesheet")
    pay_category = Relationship("PayCategory")
    title = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    pay_rate = Attribute(field_type=types.FieldTypes.CURRENCY)
    units = Attribute(field_type=types.FieldTypes.NUMBER)
    amount = Attribute(field_type=types.FieldTypes.CURRENCY)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)
    remote_links = Attribute(field_type=types.FieldTypes.OBJECT)


@model_type
class Scope:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    type = Relationship("ScopeType")
    custom_fields = Attribute(field_type=types.FieldTypes.OBJECT)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class ScopeType:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)


@model_type
class Tag:
    _title = "name"

    name = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    short_code = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
    description = Attribute(field_type=types.FieldTypes.MULTI_LINE)
    status = Attribute(field_type=types.FieldTypes.ENUM_SINGLE)

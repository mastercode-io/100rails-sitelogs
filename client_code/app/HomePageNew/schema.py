# Description: Application menu and permissions schema

SL_MENU_ITEMS = [
    {'id': 'dashboard_menu', 'text': 'DASHBOARD', 'items': [
        {'id': 'dashboard_overview', 'text': 'Overview', 'items': []},
        {'id': 'dashboard_metrics', 'text': 'Metrics', 'items': []},
        {'id': 'dashboard_notifications', 'text': 'Notifications', 'items': []},
    ]},
    {'id': 'projects_menu', 'text': 'PROJECTS', 'items': [
        {'id': 'projects_leads', 'text': 'Leads', 'items': [
            {'id': 'projects_leads_new', 'text': 'New Lead', 'items': []},
            {'id': 'projects_leads_manage', 'text': 'Manage Leads', 'items': []},
        ]},
        {'id': 'projects_quotes', 'text': 'Quotes', 'items': [
            {'id': 'projects_quotes_create', 'text': 'Create Quote', 'items': []},
            {'id': 'projects_quotes_manage', 'text': 'Manage Quotes', 'items': []},
        ]},
        {'id': 'projects_active', 'text': 'Active Projects', 'items': [
            {'id': 'projects_active_view', 'text': 'View Projects', 'items': []},
            {'id': 'projects_active_edit', 'text': 'Edit Projects', 'items': []},
        ]},
        {'id': 'projects_completed', 'text': 'Completed Projects', 'items': [
            {'id': 'projects_completed_archive', 'text': 'Archive Projects', 'items': []},
            {'id': 'projects_completed_reports', 'text': 'Project Reports', 'items': []},
        ]},
    ]},
    {'id': 'scheduling_menu', 'text': 'SCHEDULING', 'items': [
        {'id': 'scheduling_calendar', 'text': 'Calendar', 'items': []},
        {'id': 'scheduling_staff_assignment', 'text': 'Staff Assignment', 'items': []},
        {'id': 'scheduling_gear_assignment', 'text': 'Gear Assignment', 'items': []},
        {'id': 'scheduling_recurring_events', 'text': 'Recurring Events', 'items': []},
    ]},
    {'id': 'operations_menu', 'text': 'OPERATIONS', 'items': [
        {'id': 'operations_checklists', 'text': 'Checklists', 'items': []},
        {'id': 'operations_dockets', 'text': 'Dockets', 'items': []},
        {'id': 'operations_incident_reporting', 'text': 'Incident Reporting', 'items': []},
    ]},
    {'id': 'timesheets_menu', 'text': 'TIMESHEETS', 'items': [
        {'id': 'timesheets_overview', 'text': 'Overview', 'items': []},
        {'id': 'timesheets_approval_queue', 'text': 'Approval Queue', 'items': []},
        {'id': 'timesheets_gps_verification', 'text': 'GPS Verification', 'items': []},
    ]},
    {'id': 'invoicing_menu', 'text': 'INVOICING', 'items': [
        {'id': 'invoicing_create', 'text': 'Create Invoice', 'items': []},
        {'id': 'invoicing_manage', 'text': 'Manage Invoices', 'items': []},
        {'id': 'invoicing_payments', 'text': 'Payment Tracking', 'items': []},
    ]},
    {'id': 'payroll_menu', 'text': 'PAYROLL', 'items': [
        {'id': 'payroll_dashboard', 'text': 'Dashboard', 'items': []},
        {'id': 'payroll_payruns', 'text': 'Payruns', 'items': []},
        {'id': 'payroll_payslips', 'text': 'Pay Slips', 'items': []},
        {'id': 'payroll_compliance', 'text': 'Compliance', 'items': []},
        {'id': 'payroll_reports', 'text': 'Payroll Reports', 'items': []},
    ]},
    {'id': 'reports_menu', 'text': 'REPORTS', 'items': [
        {'id': 'reports_financial', 'text': 'Financial Reports', 'items': []},
        {'id': 'reports_project', 'text': 'Project Reports', 'items': []},
        {'id': 'reports_employee', 'text': 'Employee Reports', 'items': []},
    ]},
    {'id': 'integrations_menu', 'text': 'INTEGRATIONS', 'items': [
        {'id': 'integrations_accounting', 'text': 'Accounting', 'items': [
            {'id': 'integrations_accounting_xero', 'text': 'Xero', 'items': []},
            {'id': 'integrations_accounting_quickbooks', 'text': 'QuickBooks', 'items': []},
            {'id': 'integrations_accounting_myob', 'text': 'MYOB', 'items': []},
        ]},
        {'id': 'integrations_email', 'text': 'Email', 'items': []},
        {'id': 'integrations_document_generation', 'text': 'Document Generation', 'items': []},
        {'id': 'integrations_other_services', 'text': 'Other Services', 'items': []},
    ]},
    {'id': 'utilities_menu', 'text': 'UTILITIES', 'items': [
        {'id': 'utilities_settings', 'text': 'Settings', 'items': []},
        {'id': 'utilities_user_management', 'text': 'User Management', 'items': []},
        {'id': 'utilities_data_import_export', 'text': 'Data Import/Export', 'items': []},
        {'id': 'utilities_document_templates', 'text': 'Document Templates', 'items': []},
    ]},
    {'id': 'admin_menu', 'text': 'ADMIN', 'items': [
        {'id': 'admin_accounts', 'text': 'Accounts', 'items': []},
        {'id': 'admin_tenants', 'text': 'Tenants', 'items': []},
        {'id': 'admin_user_roles', 'text': 'User Roles', 'items': []},
        {'id': 'admin_permissions', 'text': 'Permissions', 'items': []},
        {'id': 'admin_pay_rules', 'text': 'Pay Rules', 'items': []},
        {'id': 'admin_pay_templates', 'text': 'Pay Templates', 'items': []},
        {'id': 'admin_settings', 'text': 'Settings', 'items': [
            {'id': 'admin_settings_scope_types', 'text': 'Scope Types', 'items': []},
        ]},
        {'id': 'admin_integrations', 'text': 'Integrations', 'items': []},
    ]},
    {'id': 'developer_menu', 'text': 'DEVELOPER', 'items': [
        {'id': 'developer_components', 'text': 'Components', 'items': [
            {'id': 'developer_views', 'text': 'Views', 'items': []},
            {'id': 'developer_pages', 'text': 'Pages', 'items': []},
            {'id': 'developer_forms', 'text': 'Forms', 'items': []},
        ]},
        {'id': 'developer_schema', 'text': 'App Schema', 'items': [
            {'id': 'developer_enums', 'text': 'Enumerations', 'items': []},
            {'id': 'developer_models', 'text': 'Models', 'items': []},
            {'id': 'developer_migrate', 'text': 'Migrate DB', 'items': []},
        ]},
        {'id': 'developer_tools', 'text': 'Tools', 'items': [
            {'id': 'developer_import', 'text': 'Import Data', 'items': []},
            {'id': 'developer_export', 'text': 'Export Data', 'items': []},
            {'id': 'developer_run_script', 'text': 'Run Script', 'items': []},
        ]},
        {'id': 'developer_prototype', 'text': 'Prototype', 'items': [
            {'id': 'developer_tenant_form', 'text': 'Tenant Form', 'items': []},
            {'id': 'developer_tree_grid', 'text': 'Tree Grid View', 'items': []},
        ]},
    ]},
]
# Navigation items/actions
SL_NAV_ITEMS = {
    'payroll_dashboard': {'name': 'CompanyDashboardPage', 'type': 'page', 'action': 'open', 'props': {}},
    'payroll_payruns': {'model': 'Payrun', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_timesheets': {'class': 'TimesheetView', 'type': 'custom', 'action': 'open', 'props': {}},
    'payroll_transfer_data': {'type': 'page', 'name': 'TransferDataPage', 'action': 'open', 'props': {}},
    'payroll_pay_categories': {'model': 'PayCategory', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_rules': {'model': 'PayRateRule', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_scopes': {'model': 'Scope', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_pay_rate_templates': {'model': 'PayRateTemplate', 'type': 'view', 'action': 'open', 'props': {}},
    'payroll_settings': {'class': 'PayrollSettingsForm', 'type': 'form', 'action': 'open', 'props': {}},

    'directory_employees': {'model': 'Employee', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_locations': {'model': 'Location', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_jobs': {'model': 'Job', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_job_types': {'model': 'JobType', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_employee_roles': {'model': 'EmployeeRole', 'type': 'view', 'action': 'open', 'props': {}},
    'directory_timesheet_types': {'model': 'TimesheetType', 'type': 'view', 'action': 'open', 'props': {}},

    'settings_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    'settings_form': {'class': 'SettingsForm', 'type': 'form', 'action': 'open', 'props': {}},

    'admin_accounts': {'class': 'AccountsAdminView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_tenants': {'class': 'TenantsView', 'type': 'custom', 'action': 'open', 'props': {}},
    'admin_users': {'model': 'User', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_settings_scope_types': {'model': 'ScopeType', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_integrations': {'model': 'AppIntegration', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_user_roles': {'model': 'UserRole', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_pay_rules': {'model': 'PayRateRule', 'type': 'view', 'action': 'open', 'props': {}},
    'admin_pay_templates': {'model': 'PayRateTemplate', 'type': 'view', 'action': 'open', 'props': {}},

    'developer_views': {'model': 'AppGridView', 'type': 'view', 'action': 'open', 'props': {}},
    'developer_enums': {'model': 'AppEnum', 'type': 'view', 'action': 'open', 'props': {}},
    # 'developer_migrate': {'type': 'page', 'page': MigratePage, 'props': {}},
    # 'developer_run_script': {'type': 'page', 'page': RunScriptPage, 'props': {}},
    'developer_tenant_form': {'type': 'form', 'class': 'SettingsForm', 'props': {}},
    'developer_tree_grid': {'type': 'page', 'name': 'TreeGridPage', 'props': {}},
}


SL_DEFAULT_NAV_ITEMS = {
    'payroll_menu': 'payroll_dashboard',
    'directory_menu': 'directory_employees',
    'settings_menu': 'settings_users',
    'admin_menu': 'admin_tenants',
    'developer_menu': 'developer_views',
}


DEFAULT_USER_PERMISSIONS = {
    'user_roles': {
        'portal_admin': {
            'permissions': {
                'app_menu': {
                    'dashboard_menu': {'has_access': True, 'items': {
                        'dashboard_overview': {'has_access': True, 'items': {}},
                        'dashboard_metrics': {'has_access': True, 'items': {}},
                        'dashboard_notifications': {'has_access': True, 'items': {}},
                    }},
                    'projects_menu': {'has_access': True, 'items': {
                        'projects_leads': {'has_access': True, 'items': {
                            'projects_leads_new': {'has_access': True, 'items': {}},
                            'projects_leads_manage': {'has_access': True, 'items': {}},
                        }},
                        'projects_quotes': {'has_access': True, 'items': {
                            'projects_quotes_create': {'has_access': True, 'items': {}},
                            'projects_quotes_manage': {'has_access': True, 'items': {}},
                        }},
                        'projects_active': {'has_access': True, 'items': {
                            'projects_active_view': {'has_access': True, 'items': {}},
                            'projects_active_edit': {'has_access': True, 'items': {}},
                        }},
                        'projects_completed': {'has_access': True, 'items': {
                            'projects_completed_archive': {'has_access': True, 'items': {}},
                            'projects_completed_reports': {'has_access': True, 'items': {}},
                        }},
                    }},
                    'scheduling_menu': {'has_access': True, 'items': {
                        'scheduling_calendar': {'has_access': True, 'items': {}},
                        'scheduling_staff_assignment': {'has_access': True, 'items': {}},
                        'scheduling_gear_assignment': {'has_access': True, 'items': {}},
                        'scheduling_recurring_events': {'has_access': True, 'items': {}},
                    }},
                    'operations_menu': {'has_access': True, 'items': {
                        'operations_checklists': {'has_access': True, 'items': {}},
                        'operations_dockets': {'has_access': True, 'items': {}},
                        'operations_incident_reporting': {'has_access': True, 'items': {}},
                    }},
                    'timesheets_menu': {'has_access': True, 'items': {
                        'timesheets_overview': {'has_access': True, 'items': {}},
                        'timesheets_approval_queue': {'has_access': True, 'items': {}},
                        'timesheets_gps_verification': {'has_access': True, 'items': {}},
                    }},
                    'invoicing_menu': {'has_access': True, 'items': {
                        'invoicing_create': {'has_access': True, 'items': {}},
                        'invoicing_manage': {'has_access': True, 'items': {}},
                        'invoicing_payments': {'has_access': True, 'items': {}},
                    }},
                    'payroll_menu': {'has_access': True, 'items': {
                        'payroll_dashboard': {'has_access': True, 'items': {}},
                        'payroll_payruns': {'has_access': True, 'items': {}},
                        'payroll_payslips': {'has_access': True, 'items': {}},
                        'payroll_compliance': {'has_access': True, 'items': {}},
                        'payroll_reports': {'has_access': True, 'items': {}},
                    }},
                    'reports_menu': {'has_access': True, 'items': {
                        'reports_financial': {'has_access': True, 'items': {}},
                        'reports_project': {'has_access': True, 'items': {}},
                        'reports_employee': {'has_access': True, 'items': {}},
                    }},
                    'integrations_menu': {'has_access': True, 'items': {
                        'integrations_accounting': {'has_access': True, 'items': {
                            'integrations_accounting_xero': {'has_access': True, 'items': {}},
                            'integrations_accounting_quickbooks': {'has_access': True, 'items': {}},
                            'integrations_accounting_myob': {'has_access': True, 'items': {}},
                        }},
                        'integrations_email': {'has_access': True, 'items': {}},
                        'integrations_document_generation': {'has_access': True, 'items': {}},
                        'integrations_other_services': {'has_access': True, 'items': {}},
                    }},
                    'utilities_menu': {'has_access': True, 'items': {
                        'utilities_settings': {'has_access': True, 'items': {}},
                        'utilities_user_management': {'has_access': True, 'items': {}},
                        'utilities_data_import_export': {'has_access': True, 'items': {}},
                        'utilities_document_templates': {'has_access': True, 'items': {}},
                    }},
                    'admin_menu': {'has_access': True, 'items': {
                        'admin_accounts': {'has_access': True, 'items': {}},
                        'admin_tenants': {'has_access': True, 'items': {}},
                        'admin_user_roles': {'has_access': True, 'items': {}},
                        'admin_permissions': {'has_access': True, 'items': {}},
                        'admin_pay_rules': {'has_access': True, 'items': {}},
                        'admin_pay_templates': {'has_access': True, 'items': {}},
                        'admin_settings': {'has_access': True, 'items': {
                            'admin_settings_scope_types': {'has_access': True, 'items': {}},
                        }},
                        'admin_integrations': {'has_access': True, 'items': {}},
                    }},
                    'developer_menu': {'has_access': True, 'items': {
                        'developer_components': {'has_access': True, 'items': {
                            'developer_views': {'has_access': True, 'items': {}},
                            'developer_pages': {'has_access': True, 'items': {}},
                            'developer_forms': {'has_access': True, 'items': {}},
                        }},
                        'developer_schema': {'has_access': True, 'items': {
                            'developer_enums': {'has_access': True, 'items': {}},
                            'developer_models': {'has_access': True, 'items': {}},
                            'developer_migrate': {'has_access': True, 'items': {}},
                        }},
                        'developer_tools': {'has_access': True, 'items': {
                            'developer_import': {'has_access': True, 'items': {}},
                            'developer_export': {'has_access': True, 'items': {}},
                            'developer_run_script': {'has_access': True, 'items': {}},
                        }},
                        'developer_prototype': {'has_access': True, 'items': {
                            'developer_tenant_form': {'has_access': True, 'items': {}},
                            'developer_tree_grid': {'has_access': True, 'items': {}},
                        }},
                    }},
                },
                'special_menu': {
                    'user_menu': {'has_access': True, 'items': {
                        'pl-appbar-user-account-name': {'has_access': True},
                        'pl-appbar-user-profile': {'has_access': True},
                        'pl-appbar-account-settings': {'has_access': True},
                        'pl-appbar-sign-out': {'has_access': True},
                    }},
                    'settings_button': {'has_access': True},
                    'assistant_button': {'has_access': True},
                },
                'start_page': None,
            }
        },
        'account_admin': {
            'permissions': {
                'app_menu': {
                    'dashboard_menu': {'has_access': True, 'items': {
                        'dashboard_overview': {'has_access': True, 'items': {}},
                        'dashboard_metrics': {'has_access': True, 'items': {}},
                        'dashboard_notifications': {'has_access': True, 'items': {}},
                    }},
                    'projects_menu': {'has_access': True, 'items': {
                        'projects_leads': {'has_access': True, 'items': {
                            'projects_leads_new': {'has_access': True, 'items': {}},
                            'projects_leads_manage': {'has_access': True, 'items': {}},
                        }},
                        'projects_quotes': {'has_access': True, 'items': {
                            'projects_quotes_create': {'has_access': True, 'items': {}},
                            'projects_quotes_manage': {'has_access': True, 'items': {}},
                        }},
                        'projects_active': {'has_access': True, 'items': {
                            'projects_active_view': {'has_access': True, 'items': {}},
                            'projects_active_edit': {'has_access': True, 'items': {}},
                        }},
                        'projects_completed': {'has_access': True, 'items': {
                            'projects_completed_archive': {'has_access': True, 'items': {}},
                            'projects_completed_reports': {'has_access': True, 'items': {}},
                        }},
                    }},
                    'scheduling_menu': {'has_access': True, 'items': {
                        'scheduling_calendar': {'has_access': True, 'items': {}},
                        'scheduling_staff_assignment': {'has_access': True, 'items': {}},
                        'scheduling_gear_assignment': {'has_access': True, 'items': {}},
                        'scheduling_recurring_events': {'has_access': True, 'items': {}},
                    }},
                    'operations_menu': {'has_access': True, 'items': {
                        'operations_checklists': {'has_access': True, 'items': {}},
                        'operations_dockets': {'has_access': True, 'items': {}},
                        'operations_incident_reporting': {'has_access': True, 'items': {}},
                    }},
                    'timesheets_menu': {'has_access': True, 'items': {
                        'timesheets_overview': {'has_access': True, 'items': {}},
                        'timesheets_approval_queue': {'has_access': True, 'items': {}},
                        'timesheets_gps_verification': {'has_access': True, 'items': {}},
                    }},
                    'invoicing_menu': {'has_access': True, 'items': {
                        'invoicing_create': {'has_access': True, 'items': {}},
                        'invoicing_manage': {'has_access': True, 'items': {}},
                        'invoicing_payments': {'has_access': True, 'items': {}},
                    }},
                    'payroll_menu': {'has_access': True, 'items': {
                        'payroll_dashboard': {'has_access': True, 'items': {}},
                        'payroll_payruns': {'has_access': True, 'items': {}},
                        'payroll_payslips': {'has_access': True, 'items': {}},
                        'payroll_compliance': {'has_access': True, 'items': {}},
                        'payroll_reports': {'has_access': True, 'items': {}},
                    }},
                    'reports_menu': {'has_access': True, 'items': {
                        'reports_financial': {'has_access': True, 'items': {}},
                        'reports_project': {'has_access': True, 'items': {}},
                        'reports_employee': {'has_access': True, 'items': {}},
                    }},
                    'integrations_menu': {'has_access': True, 'items': {
                        'integrations_accounting': {'has_access': True, 'items': {
                            'integrations_accounting_xero': {'has_access': True, 'items': {}},
                            'integrations_accounting_quickbooks': {'has_access': True, 'items': {}},
                            'integrations_accounting_myob': {'has_access': True, 'items': {}},
                        }},
                        'integrations_email': {'has_access': True, 'items': {}},
                        'integrations_document_generation': {'has_access': True, 'items': {}},
                        'integrations_other_services': {'has_access': True, 'items': {}},
                    }},
                    'utilities_menu': {'has_access': True, 'items': {
                        'utilities_settings': {'has_access': True, 'items': {}},
                        'utilities_user_management': {'has_access': True, 'items': {}},
                        'utilities_data_import_export': {'has_access': True, 'items': {}},
                        'utilities_document_templates': {'has_access': True, 'items': {}},
                    }},
                    'admin_menu': {'has_access': False, 'items': {}},
                    'developer_menu': {'has_access': False, 'items': {}},
                },
                'special_menu': {
                    'user_menu': {'has_access': True, 'items': {
                        'pl-appbar-user-account-name': {'has_access': True},
                        'pl-appbar-user-profile': {'has_access': True},
                        'pl-appbar-account-settings': {'has_access': True},
                        'pl-appbar-sign-out': {'has_access': True},
                    }},
                    'settings_button': {'has_access': True},
                    'assistant_button': {'has_access': True},
                },
                'start_page': None,
            }
        },
        'payroll_admin': {
            'permissions': {
                'app_menu': {
                    'dashboard_menu': {'has_access': False, 'items': {}},
                    'projects_menu': {'has_access': False, 'items': {}},
                    'scheduling_menu': {'has_access': False, 'items': {}},
                    'operations_menu': {'has_access': False, 'items': {}},
                    'timesheets_menu': {'has_access': False, 'items': {}},
                    'invoicing_menu': {'has_access': False, 'items': {}},
                    'payroll_menu': {'has_access': True, 'items': {
                        'payroll_dashboard': {'has_access': True, 'items': {}},
                        'payroll_payruns': {'has_access': True, 'items': {}},
                        'payroll_payslips': {'has_access': True, 'items': {}},
                        'payroll_compliance': {'has_access': True, 'items': {}},
                        'payroll_reports': {'has_access': True, 'items': {}},
                    }},
                    'reports_menu': {'has_access': False, 'items': {}},
                    'integrations_menu': {'has_access': False, 'items': {}},
                    'utilities_menu': {'has_access': False, 'items': {}},
                    'admin_menu': {'has_access': False, 'items': {}},
                    'developer_menu': {'has_access': False, 'items': {}},
                },
                'special_menu': {
                    'user_menu': {'has_access': True, 'items': {
                        'pl-appbar-user-account-name': {'has_access': True},
                        'pl-appbar-user-profile': {'has_access': True},
                        'pl-appbar-account-settings': {'has_access': True},
                        'pl-appbar-sign-out': {'has_access': True},
                    }},
                    'settings_button': {'has_access': True},
                    'assistant_button': {'has_access': True},
                },
                'start_page': 'payroll_dashboard',
            }
        },
        'payroll_manager': {
            'permissions': {
                'app_menu': {
                    'dashboard_menu': {'has_access': False, 'items': {}},
                    'projects_menu': {'has_access': False, 'items': {}},
                    'scheduling_menu': {'has_access': False, 'items': {}},
                    'operations_menu': {'has_access': False, 'items': {}},
                    'timesheets_menu': {'has_access': True, 'items': {
                        'timesheets_overview': {'has_access': True, 'items': {}},
                        'timesheets_approval_queue': {'has_access': True, 'items': {}},
                        'timesheets_gps_verification': {'has_access': True, 'items': {}},
                    }},
                    'invoicing_menu': {'has_access': False, 'items': {}},
                    'payroll_menu': {'has_access': True, 'items': {
                        'payroll_dashboard': {'has_access': False, 'items': {}},
                        'payroll_payruns': {'has_access': True, 'items': {}},
                        'payroll_payslips': {'has_access': True, 'items': {}},
                        'payroll_compliance': {'has_access': True, 'items': {}},
                        'payroll_reports': {'has_access': True, 'items': {}},
                    }},
                    'reports_menu': {'has_access': False, 'items': {}},
                    'integrations_menu': {'has_access': False, 'items': {}},
                    'utilities_menu': {'has_access': False, 'items': {}},
                    'admin_menu': {'has_access': False, 'items': {}},
                    'developer_menu': {'has_access': False, 'items': {}},
                },
                'special_menu': {
                    'user_menu': {'has_access': True, 'items': {
                        'pl-appbar-user-account-name': {'has_access': True},
                        'pl-appbar-user-profile': {'has_access': True},
                        'pl-appbar-account-settings': {'has_access': False},
                        'pl-appbar-sign-out': {'has_access': True},
                    }},
                    'settings_button': {'has_access': False},
                    'assistant_button': {'has_access': False},
                },
                'start_page': 'payroll_payruns',
            }
        },
        # Add additional roles as needed
    }
}

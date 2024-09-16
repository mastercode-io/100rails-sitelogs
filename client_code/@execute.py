from AnvilFusion.tools.utils import AppEnv, init_user_session
from .app import models
from . import Forms
from . import Views
from . import Pages
from . import api
import uuid
import anvil.server
import anvil.users

AppEnv.APP_ID = "PayLogs"
AppEnv.ANVIL_FUSION_VERSION = "0.0.1"
AppEnv.data_models = models
AppEnv.forms = Forms
AppEnv.views = Views
AppEnv.pages = Pages


def add_enum_list():
    enum_name = 'DAY_TYPE_OPTIONS'
    enum_options = [
        'Any Day',
        'Weekday',
        'Weekend',
        'Saturday',
        'Sunday',
        'Public Holiday',
        'Week',
        'RDO',
    ]
    enum_values = {x: x for x in enum_options}
    enum = models.AppEnum(name=enum_name, options=enum_values).save()
    print(enum)


init_user_session()

# pay_period_start = Attribute(field_type=types.FieldTypes.DATE)
# pay_period_end = Attribute(field_type=types.FieldTypes.DATE)
# pay_date = Attribute(field_type=types.FieldTypes.DATE)
# status = Attribute(field_type=types.FieldTypes.SINGLE_LINE)
# notes = Attribute(field_type=types.FieldTypes.MULTI_LINE)

view_columns = [
    {'name': 'payrun_week', 'label': 'Year Week'},
    {'name': 'pay_period_start', 'label': 'Pay Period Start'},
    {'name': 'pay_period_end', 'label': 'Pay Period End'},
    {'name': 'pay_date', 'label': 'Pay Date'},
    {'name': 'status', 'label': 'Status'},
    {'name': 'notes', 'label': 'Notes'},
]

grid_view = models.AppGridView.get_by('name', 'PayrunList')
if not grid_view:
    grid_view = models.AppGridView(
        name='PayrunList',
        model='Payrun',
        owner='system')
grid_view['columns'] = view_columns
grid_view.save()
print(grid_view)

# pay_rates = {
#     "C1-CAS-CW1-LAB-ORD": 32.0,
#     "C1-CAS-CW2-SCAF-ORD": 42.0,
#     "C1-CAS-CW3-SCAF-ORD": 42.0,
#     "C1-CAS-CW4-SCAF-ORD": 42.0,
#     "C1-CAS-YD1-ORD": 35.0,
#     "C1-CAS-YD2-ORD": 28.0,
#     "C1-PFT-YDM-ORD": 45.0,
#     "C1-PPT-TD1-ORD": 35.0,
#     "C1-PPT-YD1-ORD": 35.0,
#     "C1-PPT-YD2-ORD": 28.0,
#     "C1-CAS-CW2-LH-ORD": 58.68,
#     # "C1-PFT-CW4-ORD": 53.98,
#     "SUP2 SALARY": 51.44,
#     "SUP3 SALARY": 52.92,
#     "C1-CAS-YD1-OT150%": 52.5,
#     "C1-CAS-YD1-OT200%": 70.0,
#     "C1-CAS-YD2-OT150%": 42.0,
#     "C1-CAS-YD2-OT200%": 56.0,
#     "C1-PFT-YDM-OT150%": 67.5,
#     "C1-PFT-YDM-OT200%": 90.0,
#     "C1-PPT-TD1-OT150%": 52.5,
#     "C1-PPT-TD1-OT200%": 70.0,
#     "C1-PPT-YD1-OT150%": 52.5,
#     "C1-PPT-YD1-OT200%": 70.0,
#     "C1-PPT-YD2-OT150%": 42.0,
#     "C1-PPT-YD2-OT200%": 56.0,
#     "CAS-YD1-ORD": 56.48,
#     "CAS-YD1-OT200%": 112.96,
#     "CAS-YDM-ORD": 56.48,
#     "CAS-YDM-OT150%": 84.72,
#     "CAS-YDM-OT200%": 112.96,
#     "CAS-YD1-OT150%": 84.72,
#     "SUP2 OT150%": 77.16,
#     "SUP2 OT200%": 102.88,
#     "SUP3 OT150%": 77.16,
#     "SUP3 OT200%": 102.88,
#     "C1-CAS-TD1-ORD": 46.9,
#     "C1-PFT-CW1-LAB-ORD": 26.88,
#     "C1-PFT-CW1-LAB-OT150%": 40.32,
#     "C1-PFT-CW1-LAB-OT200%": 53.76,
#     "C1-PFT-CW2-SCAF-ORD": 35.28,
#     "C1-PFT-CW2-SCAF-OT150%": 52.92,
#     "C1-PFT-CW2-SCAF-OT200%": 70.56,
#     "C1-PFT-CW2-LH-ORD": 49.48,
#     "C1-PFT-CW2-LH-OT150%": 74.22,
#     "C1-PFT-CW2-LH-OT200%": 98.96,
#     "C1-PFT-CW3-SCAF-ORD": 35.28,
#     "C1-PFT-CW3-SCAF-OT150%": 52.92,
#     "C1-PFT-CW3-SCAF-OT200%": 70.56,
#     "C1-PFT-CW4-SCAF-ORD": 35.28,
#     "C1-PFT-CW4-SCAF-OT150%": 52.92,
#     "C1-PFT-CW4-SCAF-OT200%": 70.56,
#     "C1-PFT-TD1-ORD": 39.4,
#     "C1-PFT-TD1-OT150%": 59.1,
#     "C1-PFT-TD1-OT200%": 78.79,
#     "C1-PFT-YD1-ORD": 47.63,
#     "C1-PFT-YD1-OT150%": 71.45,
#     "C1-PFT-YD1-OT200%": 95.26,
#     "C1-PFT-YD2-ORD": 23.52,
#     "C1-PFT-YD2-OT150%": 35.28,
#     "C1-PFT-YD2-OT200%": 47.04,
#     "SUP2 C1 RDO ": 54.01,
#     "SUP2 C1 RDO Leave": 54.01,
#     "SUP3 C1 RDO ": 55.57
# }

# pay_rates = {
#     "T1-CAS-CW1-LAB-ORD": 59.54,
#     "T1-CAS-CW2-SCAF-ORD": 61.85,
#     "T1-CAS-CW3-SCAF-ORD": 65.61,
#     "T1-CAS-CW4-SCAF-ORD": 70.86,
#     "T1-PFT-CW4-DELO-ORD": 56.69,
#     "RDO T1 CAS CW1": 59.54,
#     "RDO T1 CAS CW2": 61.85,
#     "RDO T1 CAS CW3": 65.61,
#     "RDO T1 CAS CW4": 70.86,
#     "RDO T1 PFT CW4": 56.69,
#     "RDO T1 CAS CW1 Leave": 59.54,
#     "RDO T1 CAS CW2 Leave": 61.85,
#     "RDO T1 CAS CW3 Leave": 65.61,
#     "RDO T1 CAS CW4 Leave": 70.86,
#     "RDO T1 PFT CW4 Leave": 56.69,
#     "T1-CAS-CW1-LAB-OT200%": 119.08,
#     "T1-CAS-CW2-SCAF-OT200%": 123.7,
#     "T1-CAS-CW3-SCAF-OT200%": 131.22,
#     "T1-CAS-CW4-SCAF-OT200%": 141.72,
#     "T1-PFT-CW4-DELO-OT200%": 113.38,
#     "SUP2 OT150%": 77.16,
#     "SUP2 OT200%": 102.88,
#     "SUP3 OT150%": 79.38,
#     "SUP3 OT200%": 105.84,
#     "T1-PFT-CW2-SCAF-OT200%": 98.96,
#     "T1-PFT-CW2-SCAF-ORD": 49.48,
#     "T1-PFT-CW3-SCAF-ORD": 52.49,
#     "T1-PFT-CW3-SCAF-OT200%": 104.98,
#     "T1-PFT-CW4-SCAF-ORD": 56.69,
#     "T1-PFT-CW4-SCAF-OT200%": 113.38,
#     "SUP2 C1 RDO ": 54.01,
#     "SUP2 C1 RDO Leave": 54.01
# }

# pay_rates = {
#     "T2-CAS-CW1-LAB-ORD": 59.94,
#     "T2-CAS-CW2-SCAF-ORD": 61.85,
#     "T2-CAS-CW3-SCAF-ORD": 65.61,
#     "T2-CAS-CW4-SCAF-ORD": 70.86,
#     "RDO T2 CAS CW1": 59.94,
#     "RDO T2 CAS CW2": 61.85,
#     "RDO T2 CAS CW3": 65.61,
#     "RDO T2 CAS CW4": 70.86,
#     "RDO T2 PFT CW4": 56.69,
#     "RDO T2 CAS CW1 Leave": 59.94,
#     "RDO T2 CAS CW2 Leave": 61.85,
#     "RDO T2 CAS CW3 Leave": 65.61,
#     "RDO T2 CAS CW4 Leave": 70.86,
#     "RDO T2 PFT CW4 Leave": 56.69,
#     "T2-CAS-CW1-LAB-OT150%": 72.36,
#     "T2-CAS-CW2-SCAF-OT150%": 92.78,
#     "T2-CAS-CW3-SCAF-OT150%": 98.42,
#     "T2-CAS-CW4-SCAF-OT150%": 106.29,
#     "T2-CAS-CW1-LAB-OT200%": 119.08,
#     "T2-CAS-CW2-SCAF-OT200%": 123.7,
#     "T2-CAS-CW3-SCAF-OT200%": 131.22,
#     "T2-CAS-CW4-SCAF-OT200%": 141.72,
#     "T2-PFT-CW4-SCAF-OT150%": 85.04,
#     "T2-PFT-CW4-SCAF-OT200%": 113.38,
#     "T2-PFT-CW4-DELO-ORD": 56.69,
#     "T2-PFT-CW4-DELO-OT150%": 85.04,
#     "T2-PFT-CW4-DELO-OT200%": 113.38,
#     "SUP2 OT150%": 77.16,
#     "SUP2 OT200%": 102.88,
#     "SUP3 OT150%": 79.38,
#     "SUP3 OT200%": 105.84,
#     "SUP2 SALARY": 54.01,
#     "T2-PFT-CW1-LAB-ORD": 47.63,
#     "T2-PFT-CW1-LAB-OT150%": 71.45,
#     "T2-PFT-CW1-LAB-OT200%": 95.26,
#     "T2-PFT-CW2-SCAF-ORD": 49.48,
#     "T2-PFT-CW2-SCAF-OT150%": 74.22,
#     "T2-PFT-CW2-SCAF-OT200%": 98.96,
#     "T2-PFT-CW3-SCAF-ORD": 52.49,
#     "T2-PFT-CW3-SCAF-OT150%": 78.73,
#     "T2-PFT-CW3-SCAF-OT200%": 104.98
# }
#
# ord_rates = [x for x in pay_rates.keys() if 'ORD' in x or 'SALARY' in x]
# mult15_rates = [x for x in pay_rates.keys() if 'OT150%' in x]
# mult20_rates = [x for x in pay_rates.keys() if 'OT200%' in x]
# print(len(ord_rates), len(mult15_rates), len(mult20_rates))
#
# ORD_RULE = 'ORD'
# OT150WD_RULE = 'OT150% WD'
# OT200WD_RULE = 'OT200% WD'
# OTSAT150_RULE = 'OT150% SAT'
# OTSAT200_RULE = 'OT200% SAT'
# OTSUN200_RULE = 'OT200% SUN'
# OTPH200_RULE = 'OT200% PH'
#
# pay_rate_template = models.PayRateTemplate.get_by('name', 'T2 Job')
# print(pay_rate_template)
# rate_item = [*models.PayRateTemplateItem.search(pay_rate_template=pay_rate_template,
#                                                 default_pay_rate_title=OTPH200_RULE)]
# print(rate_item, OTPH200_RULE)
# for rate_name in mult20_rates:
#     if 'SUP' in rate_name:
#         role_name = rate_name[0:4] + ' SALARY'
#         cat_name = rate_name
#     else:
#         # role_name = rate_name[3:] if 'T2-' in rate_name else rate_name
#         role_name = (rate_name[3:-7] if 'T2-' in rate_name else rate_name[:-7]) + '-ORD'
#         cat_name = ''.join(rate_name.split('-SCAF'))
#         cat_name = ''.join(cat_name.split('-LAB'))
#         cat_name = ''.join(cat_name.split('-DELO'))
#     rate = pay_rates[rate_name]
#     role = models.EmployeeRole.get_by('name', f'** {role_name}')
#     pay_category = models.PayCategory.get_by('name', f'{cat_name}')
#     if not role or not pay_category:
#         print(f'Role or PayCategory not found for {role_name}/{rate_name}({cat_name}): {role} {pay_category}')
#         continue
    # specific_role = models.PayRateTemplateSpecificRole(
    #     pay_rate_template_item=rate_item[0],
    #     name=role_name,
    #     employee_role=role,
    #     pay_category=pay_category,
    #     pay_rate=rate,
    # )
    # specific_role.save()
    # print('saved', specific_role, role_name, rate_name, rate)

from AnvilFusion.components.FormBase import FormBase, SubformBase
from AnvilFusion.components.FormInputs import *
from AnvilFusion.components.SubformGrid import SubformGrid
from AnvilFusion.datamodel.types import FieldTypes
from ..app.models import PayRateRule


class PayRateTemplateItemForm(FormBase):
    def __init__(self, **kwargs):
        print('PayRateTemplateItemForm')
        kwargs['model'] = 'PayRateTemplateItem'

        self.order_number = NumberInput(name='order_number', label='Order', format='##')
        self.default_pay_rate_title = TextInput(name='default_pay_rate_title', label='Default Title')
        self.pay_rate_rule = LookupInput(name='pay_rate_rule', label='Rule', model='PayRateRule',
                                         on_change=self.pay_rate_rule_selected)
        self.default_pay_category = LookupInput(name='default_pay_category', label='Default Pay Category',
                                                model='PayCategory', on_change=self.pay_category_selected)
        self.default_pay_rate = NumberInput(name='default_pay_rate', label='Default Rate', format='c2')
        self.pay_rate_multiplier = NumberInput(name='pay_rate_multiplier', label='Multiplier', format='p2')
        self.status = RadioButtonInput(name='status', label='Status', options=['Active', 'Inactive'], value='Active')

        specific_roles_fields = [
            TextInput(name='name', on_change=self.specific_role_change),
            LookupInput(name='employee_role', model='EmployeeRole', on_change=self.specific_role_change,
                        grid_field='employee_role.name', inline_grid=True),
            LookupInput(name='pay_category', model='PayCategory', on_change=self.specific_role_change,
                        grid_field='pay_category.name', inline_grid=True),
            NumberInput(name='pay_rate', format='c2', on_change=self.specific_role_change, field_type=FieldTypes.CURRENCY),
        ]
        specific_roles_view = {
            'model': 'PayRateTemplateSpecificRole',
            'columns': [
                {'name': 'name', 'label': 'Name'},
                {'name': 'employee_role.name', 'label': 'Employee Role'},
                {'name': 'pay_category.name', 'label': 'Payroll Category'},
                {'name': 'pay_rate', 'label': 'Rate'},
            ],
            'inline_edit_fields': specific_roles_fields,
        }
        self.specific_roles = SubformGrid(
            name='specific_roles', label='Pay Rate Specific Roles', model='PayRateTemplateSpecificRole',
            link_model='PayRateTemplateItem', link_field='pay_rate_template_item',
            # add_edit_form='PayRateTemplateSpecificRoleForm', form_container_id=kwargs.get('target'),
            view_config=specific_roles_view, edit_mode='inline',
        )
        print('specific_roles', self.specific_roles.container_id)
        self.specific_roles.grid_height = '100%'

        # self.subform_base = SubformBase(
        #     name='subform_base', model='PayRateTemplateSpecificRole', fields=specific_roles_columns,
        #     link_model='PayRateTemplateItem', link_field='pay_rate_template_item',
        # )

        sections = [
            {
                'name': '_', 'cols': [
                    [
                        self.pay_rate_rule,
                        self.order_number,
                        self.status,
                    ],
                    [
                        self.default_pay_category,
                        self.default_pay_rate_title,
                        self.default_pay_rate,
                        self.pay_rate_multiplier,
                    ],
                ]
            },
            {
                'name': '_', 'rows': [
                    [self.specific_roles],
                ]
            },
            # {
            #     'name': '_', 'rows': [
            #         [self.subform_base],
            #     ]
            # }
        ]

        # super().__init__(sections=sections, subforms=[self.subform_base], **kwargs)
        super().__init__(sections=sections, **kwargs)
        self.fullscreen = True


    def pay_rate_rule_selected(self, args):
        print('pay_rate_rule_selected', self.pay_rate_rule.value, args)
        if self.pay_rate_rule.value is None or args.get('value', None) is None:
            self.default_pay_rate.value = None
            self.pay_rate_multiplier.value = None
        else:
            pay_rate_rule = PayRateRule.get(self.pay_rate_rule.value['uid'])
            self.default_pay_rate.value = pay_rate_rule['pay_rate']
            self.pay_rate_multiplier.value = pay_rate_rule['pay_rate_multiplier']
            self.default_pay_rate_title.value = pay_rate_rule['name']

    def pay_category_selected(self, args):
        print('pay_category_selected', self.default_pay_category.value, args)
        if self.default_pay_category.value is None or args.get('value', None) is None:
            self.default_pay_rate_title.value = None
        else:
            self.default_pay_rate_title.value = self.default_pay_category.value['name']

    def specific_role_change(self, args):
        # print('specific_role_change', args)
        pass

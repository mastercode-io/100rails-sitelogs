from ..app.models import PayRateRule, PayRateTemplateItem, PayRateTemplateSpecificRole
import json
from datetime import datetime, timedelta

WEEK_DAY_NAME = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
MIDNIGHT = datetime(1970, 1, 1, 0, 0, 0)


def day_type(date):
    day_of_week = date.weekday()
    if day_of_week == 5 or day_of_week == 6:  # Saturday or Sunday
        return "Any Day", "Weekend", WEEK_DAY_NAME[day_of_week]
    else:
        return "Any Day", "Weekday", WEEK_DAY_NAME[day_of_week]


class PyaRateRuleAward(PayRateRule):
    def __init__(self, instance=None):
        self.__dict__.e(instance.__dict__)
        if self.start_time is None or self.start_time.time() == MIDNIGHT.time():
            self.start_time = datetime(1970, 1, 1, 0, 0, 1)
        if self.end_time is None or self.end_time.time() == MIDNIGHT.time():
            self.end_time = datetime(1970, 1, 1, 23, 59, 59)

    def allocate_time(self, date, start_time, end_time, total_hours=None):
        units = 0
        unallocated_time = []
        if self.time_scope in day_type(date):
            if self.unit_type == 'Day' or self.pay_rate_type == 'Fixed Amount':
                units = 1
                unallocated_time.append((start_time, end_time))
            elif 'Allowance' in self.earnings_type and self.unit_type == 'Hour':
                units = total_hours
                unallocated_time.append((start_time, end_time))
            elif self.unit_type == 'Hour' and start_time is not None and end_time is not None:
                allocated_start_time = start_time
                allocated_end_time = start_time
                if end_time.time() <= self.start_time.time() or start_time.time() >= self.end_time.time():
                    unallocated_time.append((start_time, end_time))
                elif start_time.time() < self.start_time.time():
                    # allocated_start_time = datetime.combine(start_time.date(), self.start_time.time())
                    allocated_start_time = start_time.replace(
                        hour=self.start_time.hour,
                        minute=self.start_time.minute,
                        second=self.start_time.second,
                        microsecond=self.start_time.microsecond
                    )
                    unallocated_time.append((start_time, allocated_start_time))
                else:
                    allocated_start_time = start_time
                if end_time.time() > self.end_time.time():
                    allocated_end_time = end_time.replace(
                        hour=self.end_time.hour,
                        minute=self.end_time.minute,
                        second=self.end_time.second,
                        microsecond=self.end_time.microsecond
                    )
                    unallocated_time.append((allocated_end_time, end_time))
                else:
                    allocated_end_time = end_time
                # if 'OT150% WD' in self.name or 'OT200% WD' in self.name or 'ORD' in self.name:
                #     print(self.name, allocated_start_time, allocated_end_time)
                units = (allocated_end_time - allocated_start_time).total_seconds() / 3600
                # if 'OT150% WD' in self.name or 'OT200% WD' in self.name or 'ORD' in self.name:
                #     print(self.name, units)
                if self.max_hours and units > self.max_hours:
                    units = self.max_hours
                    unallocated_time.append(
                        (allocated_start_time + timedelta(hours=self.max_hours), allocated_end_time))
                # if 'OT150% WD' in self.name or 'OT200% WD' in self.name or 'ORD' in self.name:
                #     print(self.name, units, unallocated_time)
        else:
            unallocated_time.append((start_time, end_time))
        # print(self.name, units, unallocated_time)
        return units, self.merge_time_periods(unallocated_time)

    @staticmethod
    def merge_time_periods(time_periods):
        if not time_periods:
            return []
        time_periods.sort(key=lambda x: x[0])
        merged_periods = [time_periods[0]]
        for current in time_periods[1:]:
            previous = merged_periods[-1]
            if current[0] <= previous[1]:
                merged_periods[-1] = (previous[0], max(previous[1], current[1]))
            else:
                merged_periods.append(list(current))
        return merged_periods


class PayItemAward(PayRateTemplateItem):
    def __init__(self, instance=None):
        self.__dict__.update(instance.__dict__)
        self.pay_rate_template_item = instance

    def calculate_award(self, date, start_time, end_time, total_hours=None,
                        employee_base_rate=None, employee_role=None):
        units, unallocated_time = PyaRateRuleAward(self.pay_rate_rule).allocate_time(
            date, start_time, end_time, total_hours=total_hours
        )
        base_rate = self.default_pay_rate or employee_base_rate or employee_role['pay_rate']
        specific_rate = None
        if employee_role:
            specific_roles = [*PayRateTemplateSpecificRole.search(pay_rate_template_item=self.pay_rate_template_item,
                                                                  employee_role=employee_role)]
            if specific_roles:
                specific_rate = specific_roles[0].pay_rate
                # print(f'Using specific rate {specific_rate} for {employee_role.name} on {self.pay_rate_rule.name}')
            else:
                pass
                # print(f'Using default/base rate {self.default_pay_rate}/{base_rate} for {self.pay_rate_rule.name}')
        if specific_rate:
            print('specific rate', specific_rate)
            payline_rate = specific_rate
        else:
            print(self.pay_rate_rule.name, self.pay_rate_rule.pay_rate_type, base_rate, self.pay_rate_multiplier)
            if self.pay_rate_rule.pay_rate_type == 'Multiplier':
                payline_rate = base_rate * self.pay_rate_multiplier
            else:
                payline_rate = base_rate
        if units:
            pay_line = PayLine(
                pay_rate_title=self.default_pay_rate_title,
                pay_category=self.default_pay_category,
                date=date,
                base_rate=base_rate,
                pay_rate=payline_rate,
                unit_type=self.pay_rate_rule.unit_type,
                units=units,
                count_overtime=self.pay_rate_rule.count_overtime,
            )
        else:
            pay_line = None
        return pay_line, unallocated_time


class PayLine:
    def __init__(self, **kwargs):
        self.pay_rate_title = kwargs.get('pay_rate_title')
        self.pay_category = kwargs.get('pay_category')
        self.timesheet = kwargs.get('timesheet')
        self.date = kwargs.get('date')
        self.base_rate = kwargs.get('base_rate')
        self.pay_rate = kwargs.get('pay_rate')
        self.unit_type = kwargs.get('unit_type')
        self.units = kwargs.get('units')
        self.count_overtime = kwargs.get('count_overtime', False)
        self._pay_amount = None

    @property
    def pay_amount(self):
        if self.pay_rate is not None and self.units is not None:
            self._pay_amount = round(self.pay_rate * self.units, 2)
        return self._pay_amount

    def __str__(self):
        return (f'${self.pay_amount:.2f} - @{self.pay_rate_title} {self.pay_rate:.2f} x '
                f'{format(self.units, ".2f").rstrip("0").rstrip(".")} {self.unit_type}')

    def __repr__(self):
        return (f"PayLine("
                f"pay_rate_title='{self.pay_rate_title}', "
                f"pay_category='{self.pay_category}', "
                f"timesheet='{self.timesheet}',"
                f"date='{self.date}', "
                f"base_rate={self.base_rate}, "
                f"pay_rate={self.pay_rate}, "
                f"unit_type='{self.unit_type}', "
                f"units={self.units}, "
                f"count_overtime={self.count_overtime}"
                f")")

    def to_dict(self):
        return {
            'pay_rate_title': self.pay_rate_title,
            'pay_category': self.pay_category,
            'date': self.date,
            'timesheet': self.timesheet,
            'base_rate': self.base_rate,
            'pay_rate': self.pay_rate,
            'unit_type': self.unit_type,
            'units': self.units,
            'pay_amount': self.pay_amount,
            'count_overtime': self.count_overtime,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def split(self, units):
        if units > self.units:
            raise ValueError('units to split is greater than units on pay line')
        self.units -= units
        return PayLine(
            pay_rate_title=self.pay_rate_title,
            pay_category=self.pay_category,
            timesheet=self.timesheet,
            date=self.date,
            base_rate=self.base_rate,
            pay_rate=self.pay_rate,
            unit_type=self.unit_type,
            units=units,
            count_overtime=self.count_overtime,
        )

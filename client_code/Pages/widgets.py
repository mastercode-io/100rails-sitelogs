import anvil.js
from anvil.js.window import ej
from AnvilFusion.tools import utils


STAT_ACCENTS = {
    'primary': 'text-primary',
    'secondary': 'text-secondary',
    'success': 'text-success',
    'error': 'text-error',
    'warning': 'text-warning',
    'info': 'text-info',
    'neutral': 'text-neutral',
    'accent': 'accent',
}
STAT_UP = 'success'
STAT_DOWN = 'error'
STAT_UNCHANGED = 'neutral'
ICON_UP = 'fa-solid fa-up-right'
ICON_DOWN = 'fa-solid fa-down-right'
ICON_UNCHANGED = 'fa-solid fa-arrows-left-right'


class TickerWidget:

    def __init__(self,
                 title=None,
                 symbol=None,
                 value=None,
                 value_format=None,
                 change=None,
                 change_format=None,
                 **kwargs):

        self.title = title or ''
        self.symbol = symbol
        self.value = value or 0
        self.value_format = value_format or '{:,.0f}'
        self.change = change or 0
        self.change_format = change_format or '{:,.0f}'

        if '%' in self.change_format:
            self.change = (self.change / (self.value + abs(self.change)))

        if self.change > 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: green;">\
                    <i class="fa-solid fa-caret-up" style="font-size: 70px;\
                     position: relative; top: 20px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Up by {self.change_format.format(self.change)}\
                </div>'
            value_el_position = 7
        elif self.change < 0:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: red;">\
                    <i class="fa-solid fa-caret-down" style="font-size: 70px;\
                     position: relative; top: 10px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Down by {self.change_format.format(-self.change)}\
                </div>'
            value_el_position = 7

        else:
            self.ticker_direction = f'\
                <div style="font-size: 16px; color: grey;">\
                    <i class="fa-solid fa-dash" style="font-size: 40px;\
                     position: relative; top: 10px; margin-top: -30px;"></i>\
                    &nbsp;&nbsp;&nbsp;Unchanged\
                </div>'
            value_el_position = 0

        self.html = f'\
            <div style="padding: 10px; height:100%;">\
                <div height="100%" style="border: 1px solid; border-radius: 5px; border-color: lightgrey;\
                background-color: #F5F5F5; height:100%; text-align: center; \
                display: flex; flex-direction: column; justify-content: space-evenly;">\
                    <div style="font-size: 14px; font-weight: bold;">\
                        {self.title}{(" (" + self.symbol + ")") if self.symbol else ""}\
                    </div>\
                    <div style="font-size: 30px; font-weight: bold;\
                    position: relative; top: {value_el_position}px;">\
                        {self.value_format.format(self.value)}\
                    </div>\
                    {self.ticker_direction}\
                </div>\
            </div>'

    def form_show(self):
        pass

    def destroy(self):
        pass


class StatWidget:

    def __init__(self,
                 title=None,
                 value=None,
                 value_format=None,
                 description=None,
                 accent=None,
                 icon=None,
                 **kwargs):
        self.title = title or ''
        self.value = value or ''
        self.value_format = value_format or '{:,.0f}'
        self.description = description or ''
        self.accent = accent or STAT_UNCHANGED
        self.icon = icon
        if not icon and self.accent:
            self.icon = ICON_UP if self.accent == STAT_UP else ICON_DOWN if self.accent == STAT_DOWN else ICON_UNCHANGED

        self.html = (f'\
            <div class="stats shadow pl-stat-widget">\
                <div class="stat">\
                    <div class="stat-title" style="font-size: 2.5rem!important; line-height: 1.5!important">{self.title}</div>\
                    <div class="stat-value {STAT_ACCENTS[self.accent]}" '
                     f'style="font-size: 5rem!important; line-height: 1.5!important;">\
                        {self.value_format.format(self.value)}&nbsp;\
                        <div style="float: right"><i class="{self.icon}" style="align: right!important"></i></div>\
                    </div>\
                    <div class="stat-desc" style="font-size: 1.5rem!important; line-height: 1.5!important">{self.description}</div>\
                </div>\
            </div>')

    def form_show(self):
        pass

    def destroy(self):
        pass


class CircularChartWidget:

    def __init__(self,
                 title=None,
                 chart_type=None,
                 data=None,
                 value_prefix=None,
                 value_suffix=None,
                 **kwargs):
        self._element_id = utils.new_el_id()
        self.title = title or ''
        self.chart_type = chart_type or 'pie'
        self.data = data or []

        value_prefix = value_prefix or ''
        value_suffix = value_suffix or ''

        chart_config = {
            'series': [{
                'dataSource': self.data,
                'xName': 'label',
                'yName': 'value',
                'dataLabel': {'visible': True, 'position': 'Outside', 'name': 'label',
                              'template': f'<div>${{point.x}}</div>\
                                            <div>{value_prefix}${{point.y}}{value_suffix}</div>'},
                'innerRadius': '60%' if self.chart_type == 'doughnut' else '0%',
            }],
            'legendSettings': {'visible': False, 'visibility': 'Hidden'},
        }
        self.chart = ej.charts.AccumulationChart(chart_config)

        self.html = f'\
            <div style="padding: 10px; text-align: center; display: flex; flex-direction: column; height: 100%;">\
                <div style="font-size: 14px; font-weight: bold;">{self.title}</div>\
                <div id="{self._element_id}"></div>\
            </div>'

    def form_show(self):
        self.chart.appendTo(f"#{self._element_id}")

    def destroy(self):
        self.chart.destroy()


class ChartWidget:

    def __init__(self,
                 title=None,
                 chart_config=None,
                 data=None,
                 **kwargs):
        self._element_id = utils.new_el_id()
        self.title = title or ''
        self.chart_config = chart_config or {'series': [{'dataSource': []}]}
        self._data = data or []

        chart_config['series'][0]['dataSource'] = self._data
        self.chart = ej.charts.Chart(chart_config)

        self.html = f'\
            <div style="padding: 10px; text-align: center; display: flex; flex-direction: column; height: 100%;">\
                <div style="font-size: 14px; font-weight: bold;">{self.title}</div>\
                <div id="{self._element_id}"></div>\
            </div>'

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.chart.series[0].dataSource = value

    def form_show(self):
        self.chart.appendTo(f"#{self._element_id}")

    def destroy(self):
        self.chart.destroy()


class StepperWidget:

    def __init__(self, title=None,
                 steps=None, step_type=None,
                 label_position=None,
                 direction=None, **kwargs):
        self._element_id = utils.new_el_id()
        self.title = title or ''
        self._steps = steps or []
        self.direction = direction or 'horizontal'
        self.step_type = step_type or 'default'
        if label_position is None:
            self.label_position = 'Top'
        elif label_position.lower() in ['top', 'bottom']:
            self.label_position = label_position.capitalize()
        elif label_position.lower() == 'left':
            self.label_position = 'Start'
        elif label_position.lower() == 'right':
            self.label_position = 'End'
        self.control = None

        self.html = (f'\
            <div class="form-group da-form-group" '
                     f'style="margin-left: auto; margin-right: auto; width: 50%; height: 100%">\
                <div style="font-size: 14px; font-weight: 500; margin-bottom: 20px;">{self.title}</div>\
                <div id="{self._element_id}"></div>\
            </div>')

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, value):
        self._steps = value
        if self.control is not None:
            self.control.destroy()
            self.control = None
            self.form_show()

    def form_show(self, height=None, width=None):
        if self.control is None:
            self.control = ej.navigations.Stepper({
                'steps': self._steps,
                'orientation': self.direction,
                'stepType': self.step_type,
                'labelPosition': self.label_position,
            })
        self.control.appendTo(f"#{self._element_id}")
        self.control.element.style.height = height or '100%'
        self.control.element.style.width = width or '100%'

    def destroy(self):
        self.control.destroy()


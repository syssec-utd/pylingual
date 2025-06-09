from msrest.serialization import Model

class MeterDigestCalendarizedTrendResponseResults(Model):
    """MeterDigestCalendarizedTrendResponseResults.

    :param period_name: Calendar Period Name
    :type period_name: str
    :param calendar_period: Calendar Period
    :type calendar_period: int
    :param calendar_year: Calendar Year
    :type calendar_year: int
    :param fiscal_period: Fiscal Period
    :type fiscal_period: int
    :param fiscal_year: Fiscal Year
    :type fiscal_year: int
    :param days: The number of days in the period
    :type days: int
    :param total_cost: Total Cost
    :type total_cost: float
    :param native_use: Native Use
    :type native_use: float
    :param native_use_unit_cost: Native Unit Cost
    :type native_use_unit_cost: float
    :param common_use: Common Use
    :type common_use: float
    :param common_use_unit_cost: Common Use Unit Cost
    :type common_use_unit_cost: float
    :param native_actual_demand: Native Actual Demand
    :type native_actual_demand: float
    :param native_actual_demand_unit_cost: Native Actual Demand Unit Cost
    :type native_actual_demand_unit_cost: float
    :param native_billed_demand: Native Billed Demand
    :type native_billed_demand: float
    :param native_billed_demand_unit_cost: Native Billed Demand Unit Cost
    :type native_billed_demand_unit_cost: float
    :param load_factor: Load Factor
    :type load_factor: float
    :param average_daily_temperature: Average Daily Temperature
    :type average_daily_temperature: int
    """
    _attribute_map = {'period_name': {'key': 'periodName', 'type': 'str'}, 'calendar_period': {'key': 'calendarPeriod', 'type': 'int'}, 'calendar_year': {'key': 'calendarYear', 'type': 'int'}, 'fiscal_period': {'key': 'fiscalPeriod', 'type': 'int'}, 'fiscal_year': {'key': 'fiscalYear', 'type': 'int'}, 'days': {'key': 'days', 'type': 'int'}, 'total_cost': {'key': 'totalCost', 'type': 'float'}, 'native_use': {'key': 'nativeUse', 'type': 'float'}, 'native_use_unit_cost': {'key': 'nativeUseUnitCost', 'type': 'float'}, 'common_use': {'key': 'commonUse', 'type': 'float'}, 'common_use_unit_cost': {'key': 'commonUseUnitCost', 'type': 'float'}, 'native_actual_demand': {'key': 'nativeActualDemand', 'type': 'float'}, 'native_actual_demand_unit_cost': {'key': 'nativeActualDemandUnitCost', 'type': 'float'}, 'native_billed_demand': {'key': 'nativeBilledDemand', 'type': 'float'}, 'native_billed_demand_unit_cost': {'key': 'nativeBilledDemandUnitCost', 'type': 'float'}, 'load_factor': {'key': 'loadFactor', 'type': 'float'}, 'average_daily_temperature': {'key': 'averageDailyTemperature', 'type': 'int'}}

    def __init__(self, *, period_name: str=None, calendar_period: int=None, calendar_year: int=None, fiscal_period: int=None, fiscal_year: int=None, days: int=None, total_cost: float=None, native_use: float=None, native_use_unit_cost: float=None, common_use: float=None, common_use_unit_cost: float=None, native_actual_demand: float=None, native_actual_demand_unit_cost: float=None, native_billed_demand: float=None, native_billed_demand_unit_cost: float=None, load_factor: float=None, average_daily_temperature: int=None, **kwargs) -> None:
        super(MeterDigestCalendarizedTrendResponseResults, self).__init__(**kwargs)
        self.period_name = period_name
        self.calendar_period = calendar_period
        self.calendar_year = calendar_year
        self.fiscal_period = fiscal_period
        self.fiscal_year = fiscal_year
        self.days = days
        self.total_cost = total_cost
        self.native_use = native_use
        self.native_use_unit_cost = native_use_unit_cost
        self.common_use = common_use
        self.common_use_unit_cost = common_use_unit_cost
        self.native_actual_demand = native_actual_demand
        self.native_actual_demand_unit_cost = native_actual_demand_unit_cost
        self.native_billed_demand = native_billed_demand
        self.native_billed_demand_unit_cost = native_billed_demand_unit_cost
        self.load_factor = load_factor
        self.average_daily_temperature = average_daily_temperature
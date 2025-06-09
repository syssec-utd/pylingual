from msrest.serialization import Model

class SavingsDailyData(Model):
    """SavingsDaily Data - a class that represents CA Savings for a given day per
    meter/bill.

    :param batcc_non_weather_native_use: Baseline Adjusted to Current
     Conditions (BATCC) non-weather use in native units
    :type batcc_non_weather_native_use: float
    :param batcc_weather_native_use: Baseline Adjusted to Current Conditions
     (BATCC) weather use in native units
    :type batcc_weather_native_use: float
    :param baseline_non_weather_native_use: Baseline non-weather Use in native
     units
    :type baseline_non_weather_native_use: float
    :param baseline_weather_native_use: Baseline weather use in native units
    :type baseline_weather_native_use: float
    :param batcc_cost: Baseline Adjusted to Current Conditions (BATCC) cost
    :type batcc_cost: float
    :param average_unit_cost: Average unit cost
    :type average_unit_cost: float
    :param baseline_cooling_degree_days: Number of cooling degrees used on
     this day in the baseline
    :type baseline_cooling_degree_days: int
    :param current_cooling_degree_days: Number of cooling degrees used on this
     day
    :type current_cooling_degree_days: int
    :param baseline_heating_degree_days: Number of heating degrees used on
     this day in the baseline
    :type baseline_heating_degree_days: int
    :param current_heating_degree_days: Number of heating degrees used on this
     day
    :type current_heating_degree_days: int
    :param special_adjustment: Indicates whether or not a Special Adjustment
     was in effect on this day
    :type special_adjustment: bool
    :param area_adjustment: Indicates whether or not an Area Adjustment was in
     effect on this day
    :type area_adjustment: bool
    :param weather_adjustment: Indicates whether or not Weather Adjustment was
     in effect on this day
    :type weather_adjustment: bool
    :param other_adjustment: Indicates whether or not Other Adjustment was in
     effect on this day
    :type other_adjustment: bool
    :param date_property: Daily savings date
    :type date_property: datetime
    :param messages: List of Processor Messages for this day
    :type messages: list[~energycap.sdk.models.Message]
    :param cost_unit:
    :type cost_unit: ~energycap.sdk.models.UnitChild
    """
    _attribute_map = {'batcc_non_weather_native_use': {'key': 'batccNonWeatherNativeUse', 'type': 'float'}, 'batcc_weather_native_use': {'key': 'batccWeatherNativeUse', 'type': 'float'}, 'baseline_non_weather_native_use': {'key': 'baselineNonWeatherNativeUse', 'type': 'float'}, 'baseline_weather_native_use': {'key': 'baselineWeatherNativeUse', 'type': 'float'}, 'batcc_cost': {'key': 'batccCost', 'type': 'float'}, 'average_unit_cost': {'key': 'averageUnitCost', 'type': 'float'}, 'baseline_cooling_degree_days': {'key': 'baselineCoolingDegreeDays', 'type': 'int'}, 'current_cooling_degree_days': {'key': 'currentCoolingDegreeDays', 'type': 'int'}, 'baseline_heating_degree_days': {'key': 'baselineHeatingDegreeDays', 'type': 'int'}, 'current_heating_degree_days': {'key': 'currentHeatingDegreeDays', 'type': 'int'}, 'special_adjustment': {'key': 'specialAdjustment', 'type': 'bool'}, 'area_adjustment': {'key': 'areaAdjustment', 'type': 'bool'}, 'weather_adjustment': {'key': 'weatherAdjustment', 'type': 'bool'}, 'other_adjustment': {'key': 'otherAdjustment', 'type': 'bool'}, 'date_property': {'key': 'date', 'type': 'iso-8601'}, 'messages': {'key': 'messages', 'type': '[Message]'}, 'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'}}

    def __init__(self, *, batcc_non_weather_native_use: float=None, batcc_weather_native_use: float=None, baseline_non_weather_native_use: float=None, baseline_weather_native_use: float=None, batcc_cost: float=None, average_unit_cost: float=None, baseline_cooling_degree_days: int=None, current_cooling_degree_days: int=None, baseline_heating_degree_days: int=None, current_heating_degree_days: int=None, special_adjustment: bool=None, area_adjustment: bool=None, weather_adjustment: bool=None, other_adjustment: bool=None, date_property=None, messages=None, cost_unit=None, **kwargs) -> None:
        super(SavingsDailyData, self).__init__(**kwargs)
        self.batcc_non_weather_native_use = batcc_non_weather_native_use
        self.batcc_weather_native_use = batcc_weather_native_use
        self.baseline_non_weather_native_use = baseline_non_weather_native_use
        self.baseline_weather_native_use = baseline_weather_native_use
        self.batcc_cost = batcc_cost
        self.average_unit_cost = average_unit_cost
        self.baseline_cooling_degree_days = baseline_cooling_degree_days
        self.current_cooling_degree_days = current_cooling_degree_days
        self.baseline_heating_degree_days = baseline_heating_degree_days
        self.current_heating_degree_days = current_heating_degree_days
        self.special_adjustment = special_adjustment
        self.area_adjustment = area_adjustment
        self.weather_adjustment = weather_adjustment
        self.other_adjustment = other_adjustment
        self.date_property = date_property
        self.messages = messages
        self.cost_unit = cost_unit
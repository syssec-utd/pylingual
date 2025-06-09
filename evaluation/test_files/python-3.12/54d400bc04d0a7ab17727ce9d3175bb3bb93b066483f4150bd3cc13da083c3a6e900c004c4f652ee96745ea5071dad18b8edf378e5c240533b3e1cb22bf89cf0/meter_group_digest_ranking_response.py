from msrest.serialization import Model

class MeterGroupDigestRankingResponse(Model):
    """MeterGroupDigestRankingResponse.

    :param high_cost:
    :type high_cost: float
    :param low_cost:
    :type low_cost: float
    :param average_cost:
    :type average_cost: float
    :param median_cost:
    :type median_cost: float
    :param high_use:
    :type high_use: float
    :param low_use:
    :type low_use: float
    :param average_use:
    :type average_use: float
    :param median_use:
    :type median_use: float
    :param high_unit_cost:
    :type high_unit_cost: float
    :param low_unit_cost:
    :type low_unit_cost: float
    :param average_unit_cost:
    :type average_unit_cost: float
    :param median_unit_cost:
    :type median_unit_cost: float
    :param high_value:
    :type high_value: float
    :param low_value:
    :type low_value: float
    :param average_value:
    :type average_value: float
    :param median_value:
    :type median_value: float
    :param cost_unit:
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param use_unit:
    :type use_unit: ~energycap.sdk.models.UnitChild
    :param benchmark_unit:
    :type benchmark_unit: str
    :param benchmark_value_unit:
    :type benchmark_value_unit: str
    :param benchmark_factor_unit:
    :type benchmark_factor_unit: str
    :param high_savings_opportunity:
    :type high_savings_opportunity: float
    :param results:
    :type results: list[~energycap.sdk.models.MeterGroupDigestRankingChild]
    :param meter_group_id:
    :type meter_group_id: int
    :param meter_group_code:
    :type meter_group_code: str
    :param meter_group_info:
    :type meter_group_info: str
    :param meter_group_display:
    :type meter_group_display: str
    :param updated: The date and time the data was updated
    :type updated: datetime
    """
    _attribute_map = {'high_cost': {'key': 'highCost', 'type': 'float'}, 'low_cost': {'key': 'lowCost', 'type': 'float'}, 'average_cost': {'key': 'averageCost', 'type': 'float'}, 'median_cost': {'key': 'medianCost', 'type': 'float'}, 'high_use': {'key': 'highUse', 'type': 'float'}, 'low_use': {'key': 'lowUse', 'type': 'float'}, 'average_use': {'key': 'averageUse', 'type': 'float'}, 'median_use': {'key': 'medianUse', 'type': 'float'}, 'high_unit_cost': {'key': 'highUnitCost', 'type': 'float'}, 'low_unit_cost': {'key': 'lowUnitCost', 'type': 'float'}, 'average_unit_cost': {'key': 'averageUnitCost', 'type': 'float'}, 'median_unit_cost': {'key': 'medianUnitCost', 'type': 'float'}, 'high_value': {'key': 'highValue', 'type': 'float'}, 'low_value': {'key': 'lowValue', 'type': 'float'}, 'average_value': {'key': 'averageValue', 'type': 'float'}, 'median_value': {'key': 'medianValue', 'type': 'float'}, 'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'}, 'use_unit': {'key': 'useUnit', 'type': 'UnitChild'}, 'benchmark_unit': {'key': 'benchmarkUnit', 'type': 'str'}, 'benchmark_value_unit': {'key': 'benchmarkValueUnit', 'type': 'str'}, 'benchmark_factor_unit': {'key': 'benchmarkFactorUnit', 'type': 'str'}, 'high_savings_opportunity': {'key': 'highSavingsOpportunity', 'type': 'float'}, 'results': {'key': 'results', 'type': '[MeterGroupDigestRankingChild]'}, 'meter_group_id': {'key': 'meterGroupId', 'type': 'int'}, 'meter_group_code': {'key': 'meterGroupCode', 'type': 'str'}, 'meter_group_info': {'key': 'meterGroupInfo', 'type': 'str'}, 'meter_group_display': {'key': 'meterGroupDisplay', 'type': 'str'}, 'updated': {'key': 'updated', 'type': 'iso-8601'}}

    def __init__(self, **kwargs):
        super(MeterGroupDigestRankingResponse, self).__init__(**kwargs)
        self.high_cost = kwargs.get('high_cost', None)
        self.low_cost = kwargs.get('low_cost', None)
        self.average_cost = kwargs.get('average_cost', None)
        self.median_cost = kwargs.get('median_cost', None)
        self.high_use = kwargs.get('high_use', None)
        self.low_use = kwargs.get('low_use', None)
        self.average_use = kwargs.get('average_use', None)
        self.median_use = kwargs.get('median_use', None)
        self.high_unit_cost = kwargs.get('high_unit_cost', None)
        self.low_unit_cost = kwargs.get('low_unit_cost', None)
        self.average_unit_cost = kwargs.get('average_unit_cost', None)
        self.median_unit_cost = kwargs.get('median_unit_cost', None)
        self.high_value = kwargs.get('high_value', None)
        self.low_value = kwargs.get('low_value', None)
        self.average_value = kwargs.get('average_value', None)
        self.median_value = kwargs.get('median_value', None)
        self.cost_unit = kwargs.get('cost_unit', None)
        self.use_unit = kwargs.get('use_unit', None)
        self.benchmark_unit = kwargs.get('benchmark_unit', None)
        self.benchmark_value_unit = kwargs.get('benchmark_value_unit', None)
        self.benchmark_factor_unit = kwargs.get('benchmark_factor_unit', None)
        self.high_savings_opportunity = kwargs.get('high_savings_opportunity', None)
        self.results = kwargs.get('results', None)
        self.meter_group_id = kwargs.get('meter_group_id', None)
        self.meter_group_code = kwargs.get('meter_group_code', None)
        self.meter_group_info = kwargs.get('meter_group_info', None)
        self.meter_group_display = kwargs.get('meter_group_display', None)
        self.updated = kwargs.get('updated', None)
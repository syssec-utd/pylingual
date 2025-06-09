import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['AlarmEscalationsCriticalArgs', 'AlarmEscalationsInfoArgs', 'AlarmEscalationsWarnArgs', 'AlarmPrometheusArgs', 'DynamicTagGroupMatchExpressArgs', 'EventRuleEventPatternArgs', 'GroupMetricRuleEscalationsArgs', 'GroupMetricRuleEscalationsCriticalArgs', 'GroupMetricRuleEscalationsInfoArgs', 'GroupMetricRuleEscalationsWarnArgs', 'GroupMetricRuleTargetArgs', 'HybridMonitorSlsTaskAttachLabelArgs', 'HybridMonitorSlsTaskSlsProcessConfigArgs', 'HybridMonitorSlsTaskSlsProcessConfigExpressArgs', 'HybridMonitorSlsTaskSlsProcessConfigFilterArgs', 'HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs', 'HybridMonitorSlsTaskSlsProcessConfigGroupByArgs', 'HybridMonitorSlsTaskSlsProcessConfigStatisticArgs', 'MetricRuleBlackListMetricArgs', 'MetricRuleTemplateAlertTemplateArgs', 'MetricRuleTemplateAlertTemplateEscalationsArgs', 'MetricRuleTemplateAlertTemplateEscalationsCriticalArgs', 'MetricRuleTemplateAlertTemplateEscalationsInfoArgs', 'MetricRuleTemplateAlertTemplateEscalationsWarnArgs', 'MonitorGroupInstancesInstanceArgs', 'SiteMonitorIspCityArgs', 'SlsGroupSlsGroupConfigArgs']

@pulumi.input_type
class AlarmEscalationsCriticalArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        :param pulumi.Input[str] statistics: It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        :param pulumi.Input[str] threshold: It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        :param pulumi.Input[int] times: Critical level alarm retry times. Default to 3.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        Critical level alarm retry times. Default to 3.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class AlarmEscalationsInfoArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        :param pulumi.Input[str] statistics: It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        :param pulumi.Input[str] threshold: It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        :param pulumi.Input[int] times: Critical level alarm retry times. Default to 3.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        Critical level alarm retry times. Default to 3.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class AlarmEscalationsWarnArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        :param pulumi.Input[str] statistics: It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        :param pulumi.Input[str] threshold: It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        :param pulumi.Input[int] times: Critical level alarm retry times. Default to 3.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        Critical level alarm comparison operator. Valid values: ["<=", "<", ">", ">=", "==", "!="]. Default to "==".
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.statistics' instead.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        It has been deprecated from provider version 1.94.0 and 'escalations_critical.threshold' instead.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        Critical level alarm retry times. Default to 3.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class AlarmPrometheusArgs:

    def __init__(__self__, *, annotations: Optional[pulumi.Input[Mapping[str, Any]]]=None, level: Optional[pulumi.Input[str]]=None, prom_ql: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[Mapping[str, Any]] annotations: The annotations of the Prometheus alert rule. When a Prometheus alert is triggered, the system renders the annotated keys and values to help you understand the metrics and alert rule.
        :param pulumi.Input[str] level: The level of the alert. Valid values: `Critical`, `Warn`, `Info`.
        :param pulumi.Input[str] prom_ql: The PromQL query statement. **Note:** The data obtained by using the PromQL query statement is the monitoring data. You must include the alert threshold in this statement.
        :param pulumi.Input[int] times: Critical level alarm retry times. Default to 3.
        """
        if annotations is not None:
            pulumi.set(__self__, 'annotations', annotations)
        if level is not None:
            pulumi.set(__self__, 'level', level)
        if prom_ql is not None:
            pulumi.set(__self__, 'prom_ql', prom_ql)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The annotations of the Prometheus alert rule. When a Prometheus alert is triggered, the system renders the annotated keys and values to help you understand the metrics and alert rule.
        """
        return pulumi.get(self, 'annotations')

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'annotations', value)

    @property
    @pulumi.getter
    def level(self) -> Optional[pulumi.Input[str]]:
        """
        The level of the alert. Valid values: `Critical`, `Warn`, `Info`.
        """
        return pulumi.get(self, 'level')

    @level.setter
    def level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'level', value)

    @property
    @pulumi.getter(name='promQl')
    def prom_ql(self) -> Optional[pulumi.Input[str]]:
        """
        The PromQL query statement. **Note:** The data obtained by using the PromQL query statement is the monitoring data. You must include the alert threshold in this statement.
        """
        return pulumi.get(self, 'prom_ql')

    @prom_ql.setter
    def prom_ql(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'prom_ql', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        Critical level alarm retry times. Default to 3.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class DynamicTagGroupMatchExpressArgs:

    def __init__(__self__, *, tag_value: pulumi.Input[str], tag_value_match_function: pulumi.Input[str]):
        """
        :param pulumi.Input[str] tag_value: The tag value. The Tag value must be used in conjunction with the tag value matching method TagValueMatchFunction.
        :param pulumi.Input[str] tag_value_match_function: Matching method of tag value. Valid values: `all`, `startWith`,`endWith`,`contains`,`notContains`,`equals`.
        """
        pulumi.set(__self__, 'tag_value', tag_value)
        pulumi.set(__self__, 'tag_value_match_function', tag_value_match_function)

    @property
    @pulumi.getter(name='tagValue')
    def tag_value(self) -> pulumi.Input[str]:
        """
        The tag value. The Tag value must be used in conjunction with the tag value matching method TagValueMatchFunction.
        """
        return pulumi.get(self, 'tag_value')

    @tag_value.setter
    def tag_value(self, value: pulumi.Input[str]):
        pulumi.set(self, 'tag_value', value)

    @property
    @pulumi.getter(name='tagValueMatchFunction')
    def tag_value_match_function(self) -> pulumi.Input[str]:
        """
        Matching method of tag value. Valid values: `all`, `startWith`,`endWith`,`contains`,`notContains`,`equals`.
        """
        return pulumi.get(self, 'tag_value_match_function')

    @tag_value_match_function.setter
    def tag_value_match_function(self, value: pulumi.Input[str]):
        pulumi.set(self, 'tag_value_match_function', value)

@pulumi.input_type
class EventRuleEventPatternArgs:

    def __init__(__self__, *, product: pulumi.Input[str], event_type_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, level_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, name_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, sql_filter: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] product: The type of the cloud service.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] event_type_lists: The type of the event-triggered alert rule. Valid values:
        :param pulumi.Input[Sequence[pulumi.Input[str]]] level_lists: The level of the event-triggered alert rule. Valid values:
        :param pulumi.Input[Sequence[pulumi.Input[str]]] name_lists: The name of the event-triggered alert rule.
        :param pulumi.Input[str] sql_filter: The SQL condition that is used to filter events. If the content of an event meets the specified SQL condition, an alert is automatically triggered.
        """
        pulumi.set(__self__, 'product', product)
        if event_type_lists is not None:
            pulumi.set(__self__, 'event_type_lists', event_type_lists)
        if level_lists is not None:
            pulumi.set(__self__, 'level_lists', level_lists)
        if name_lists is not None:
            pulumi.set(__self__, 'name_lists', name_lists)
        if sql_filter is not None:
            pulumi.set(__self__, 'sql_filter', sql_filter)

    @property
    @pulumi.getter
    def product(self) -> pulumi.Input[str]:
        """
        The type of the cloud service.
        """
        return pulumi.get(self, 'product')

    @product.setter
    def product(self, value: pulumi.Input[str]):
        pulumi.set(self, 'product', value)

    @property
    @pulumi.getter(name='eventTypeLists')
    def event_type_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The type of the event-triggered alert rule. Valid values:
        """
        return pulumi.get(self, 'event_type_lists')

    @event_type_lists.setter
    def event_type_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'event_type_lists', value)

    @property
    @pulumi.getter(name='levelLists')
    def level_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The level of the event-triggered alert rule. Valid values:
        """
        return pulumi.get(self, 'level_lists')

    @level_lists.setter
    def level_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'level_lists', value)

    @property
    @pulumi.getter(name='nameLists')
    def name_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The name of the event-triggered alert rule.
        """
        return pulumi.get(self, 'name_lists')

    @name_lists.setter
    def name_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'name_lists', value)

    @property
    @pulumi.getter(name='sqlFilter')
    def sql_filter(self) -> Optional[pulumi.Input[str]]:
        """
        The SQL condition that is used to filter events. If the content of an event meets the specified SQL condition, an alert is automatically triggered.
        """
        return pulumi.get(self, 'sql_filter')

    @sql_filter.setter
    def sql_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sql_filter', value)

@pulumi.input_type
class GroupMetricRuleEscalationsArgs:

    def __init__(__self__, *, critical: Optional[pulumi.Input['GroupMetricRuleEscalationsCriticalArgs']]=None, info: Optional[pulumi.Input['GroupMetricRuleEscalationsInfoArgs']]=None, warn: Optional[pulumi.Input['GroupMetricRuleEscalationsWarnArgs']]=None):
        """
        :param pulumi.Input['GroupMetricRuleEscalationsCriticalArgs'] critical: The critical level.
        :param pulumi.Input['GroupMetricRuleEscalationsInfoArgs'] info: The info level.
        :param pulumi.Input['GroupMetricRuleEscalationsWarnArgs'] warn: The warn level.
        """
        if critical is not None:
            pulumi.set(__self__, 'critical', critical)
        if info is not None:
            pulumi.set(__self__, 'info', info)
        if warn is not None:
            pulumi.set(__self__, 'warn', warn)

    @property
    @pulumi.getter
    def critical(self) -> Optional[pulumi.Input['GroupMetricRuleEscalationsCriticalArgs']]:
        """
        The critical level.
        """
        return pulumi.get(self, 'critical')

    @critical.setter
    def critical(self, value: Optional[pulumi.Input['GroupMetricRuleEscalationsCriticalArgs']]):
        pulumi.set(self, 'critical', value)

    @property
    @pulumi.getter
    def info(self) -> Optional[pulumi.Input['GroupMetricRuleEscalationsInfoArgs']]:
        """
        The info level.
        """
        return pulumi.get(self, 'info')

    @info.setter
    def info(self, value: Optional[pulumi.Input['GroupMetricRuleEscalationsInfoArgs']]):
        pulumi.set(self, 'info', value)

    @property
    @pulumi.getter
    def warn(self) -> Optional[pulumi.Input['GroupMetricRuleEscalationsWarnArgs']]:
        """
        The warn level.
        """
        return pulumi.get(self, 'warn')

    @warn.setter
    def warn(self, value: Optional[pulumi.Input['GroupMetricRuleEscalationsWarnArgs']]):
        pulumi.set(self, 'warn', value)

@pulumi.input_type
class GroupMetricRuleEscalationsCriticalArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for critical-level alerts.
        :param pulumi.Input[str] statistics: The statistical aggregation method for critical-level alerts.
        :param pulumi.Input[str] threshold: The threshold for critical-level alerts.
        :param pulumi.Input[int] times: The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for critical-level alerts.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for critical-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for critical-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class GroupMetricRuleEscalationsInfoArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for critical-level alerts.
        :param pulumi.Input[str] statistics: The statistical aggregation method for critical-level alerts.
        :param pulumi.Input[str] threshold: The threshold for critical-level alerts.
        :param pulumi.Input[int] times: The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for critical-level alerts.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for critical-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for critical-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class GroupMetricRuleEscalationsWarnArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[int]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for critical-level alerts.
        :param pulumi.Input[str] statistics: The statistical aggregation method for critical-level alerts.
        :param pulumi.Input[str] threshold: The threshold for critical-level alerts.
        :param pulumi.Input[int] times: The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for critical-level alerts.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for critical-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for critical-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[int]]:
        """
        The consecutive number of times for which the metric value is measured before a critical-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class GroupMetricRuleTargetArgs:

    def __init__(__self__, *, arn: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, json_params: Optional[pulumi.Input[str]]=None, level: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] arn: The Alibaba Cloud Resource Name (ARN) of the resource.
        :param pulumi.Input[str] id: The ID of the resource for which alerts are triggered.
        :param pulumi.Input[str] json_params: The parameters of the alert callback. The parameters are in the JSON format.
               
               > **NOTE:** Currently, the Alibaba Cloud Resource Name (ARN) of the resource. To use, please [submit an application](https://www.alibabacloud.com/help/en/cloudmonitor/latest/describemetricruletargets).
        :param pulumi.Input[str] level: The level of the alert. Valid values: `Critical`, `Warn`, `Info`.
        """
        if arn is not None:
            pulumi.set(__self__, 'arn', arn)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if json_params is not None:
            pulumi.set(__self__, 'json_params', json_params)
        if level is not None:
            pulumi.set(__self__, 'level', level)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Alibaba Cloud Resource Name (ARN) of the resource.
        """
        return pulumi.get(self, 'arn')

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'arn', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource for which alerts are triggered.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter(name='jsonParams')
    def json_params(self) -> Optional[pulumi.Input[str]]:
        """
        The parameters of the alert callback. The parameters are in the JSON format.

        > **NOTE:** Currently, the Alibaba Cloud Resource Name (ARN) of the resource. To use, please [submit an application](https://www.alibabacloud.com/help/en/cloudmonitor/latest/describemetricruletargets).
        """
        return pulumi.get(self, 'json_params')

    @json_params.setter
    def json_params(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'json_params', value)

    @property
    @pulumi.getter
    def level(self) -> Optional[pulumi.Input[str]]:
        """
        The level of the alert. Valid values: `Critical`, `Warn`, `Info`.
        """
        return pulumi.get(self, 'level')

    @level.setter
    def level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'level', value)

@pulumi.input_type
class HybridMonitorSlsTaskAttachLabelArgs:

    def __init__(__self__, *, name: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] name: The tag key of the metric.
        :param pulumi.Input[str] value: The value of the key that is used to filter logs imported from Log Service.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if value is not None:
            pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The tag key of the metric.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the key that is used to filter logs imported from Log Service.
        """
        return pulumi.get(self, 'value')

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'value', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigArgs:

    def __init__(__self__, *, expresses: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigExpressArgs']]]]=None, filter: Optional[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterArgs']]=None, group_bies: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigGroupByArgs']]]]=None, statistics: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigStatisticArgs']]]]=None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigExpressArgs']]] expresses: The extended fields that specify the results of basic operations that are performed on aggregation results. See the following `Block express`.
        :param pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterArgs'] filter: The conditions that are used to filter logs imported from Log Service. See the following `Block filter`.
        :param pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigGroupByArgs']]] group_bies: The dimension based on which data is aggregated. This parameter is equivalent to the GROUP BY clause in SQL. See the following `Block group_by`.
        :param pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigStatisticArgs']]] statistics: The method that is used to aggregate logs imported from Log Service. See the following `Block statistics`.
        """
        if expresses is not None:
            pulumi.set(__self__, 'expresses', expresses)
        if filter is not None:
            pulumi.set(__self__, 'filter', filter)
        if group_bies is not None:
            pulumi.set(__self__, 'group_bies', group_bies)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)

    @property
    @pulumi.getter
    def expresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigExpressArgs']]]]:
        """
        The extended fields that specify the results of basic operations that are performed on aggregation results. See the following `Block express`.
        """
        return pulumi.get(self, 'expresses')

    @expresses.setter
    def expresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigExpressArgs']]]]):
        pulumi.set(self, 'expresses', value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterArgs']]:
        """
        The conditions that are used to filter logs imported from Log Service. See the following `Block filter`.
        """
        return pulumi.get(self, 'filter')

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterArgs']]):
        pulumi.set(self, 'filter', value)

    @property
    @pulumi.getter(name='groupBies')
    def group_bies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigGroupByArgs']]]]:
        """
        The dimension based on which data is aggregated. This parameter is equivalent to the GROUP BY clause in SQL. See the following `Block group_by`.
        """
        return pulumi.get(self, 'group_bies')

    @group_bies.setter
    def group_bies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigGroupByArgs']]]]):
        pulumi.set(self, 'group_bies', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigStatisticArgs']]]]:
        """
        The method that is used to aggregate logs imported from Log Service. See the following `Block statistics`.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigStatisticArgs']]]]):
        pulumi.set(self, 'statistics', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigExpressArgs:

    def __init__(__self__, *, alias: Optional[pulumi.Input[str]]=None, express: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] alias: The alias of the aggregation result.
        :param pulumi.Input[str] express: The extended fields that specify the results of basic operations that are performed on aggregation results. See the following `Block express`.
        """
        if alias is not None:
            pulumi.set(__self__, 'alias', alias)
        if express is not None:
            pulumi.set(__self__, 'express', express)

    @property
    @pulumi.getter
    def alias(self) -> Optional[pulumi.Input[str]]:
        """
        The alias of the aggregation result.
        """
        return pulumi.get(self, 'alias')

    @alias.setter
    def alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'alias', value)

    @property
    @pulumi.getter
    def express(self) -> Optional[pulumi.Input[str]]:
        """
        The extended fields that specify the results of basic operations that are performed on aggregation results. See the following `Block express`.
        """
        return pulumi.get(self, 'express')

    @express.setter
    def express(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'express', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigFilterArgs:

    def __init__(__self__, *, filters: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs']]]]=None, relation: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs']]] filters: The conditions that are used to filter logs imported from Log Service. See the following `Block filters`.
        :param pulumi.Input[str] relation: The relationship between multiple filter conditions. Valid values: `and`(default value), `or`.
        """
        if filters is not None:
            pulumi.set(__self__, 'filters', filters)
        if relation is not None:
            pulumi.set(__self__, 'relation', relation)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs']]]]:
        """
        The conditions that are used to filter logs imported from Log Service. See the following `Block filters`.
        """
        return pulumi.get(self, 'filters')

    @filters.setter
    def filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs']]]]):
        pulumi.set(self, 'filters', value)

    @property
    @pulumi.getter
    def relation(self) -> Optional[pulumi.Input[str]]:
        """
        The relationship between multiple filter conditions. Valid values: `and`(default value), `or`.
        """
        return pulumi.get(self, 'relation')

    @relation.setter
    def relation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'relation', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigFilterFilterArgs:

    def __init__(__self__, *, operator: Optional[pulumi.Input[str]]=None, sls_key_name: Optional[pulumi.Input[str]]=None, value: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] operator: The method that is used to filter logs imported from Log Service. Valid values: `>`, `>=`, `=`, `<=`, `<`, `!=`, `contain`, `notContain`.
        :param pulumi.Input[str] sls_key_name: The name of the key that is used to aggregate logs imported from Log Service.
        :param pulumi.Input[str] value: The value of the key that is used to filter logs imported from Log Service.
        """
        if operator is not None:
            pulumi.set(__self__, 'operator', operator)
        if sls_key_name is not None:
            pulumi.set(__self__, 'sls_key_name', sls_key_name)
        if value is not None:
            pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def operator(self) -> Optional[pulumi.Input[str]]:
        """
        The method that is used to filter logs imported from Log Service. Valid values: `>`, `>=`, `=`, `<=`, `<`, `!=`, `contain`, `notContain`.
        """
        return pulumi.get(self, 'operator')

    @operator.setter
    def operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'operator', value)

    @property
    @pulumi.getter(name='slsKeyName')
    def sls_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the key that is used to aggregate logs imported from Log Service.
        """
        return pulumi.get(self, 'sls_key_name')

    @sls_key_name.setter
    def sls_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sls_key_name', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the key that is used to filter logs imported from Log Service.
        """
        return pulumi.get(self, 'value')

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'value', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigGroupByArgs:

    def __init__(__self__, *, alias: Optional[pulumi.Input[str]]=None, sls_key_name: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] alias: The alias of the aggregation result.
        :param pulumi.Input[str] sls_key_name: The name of the key that is used to aggregate logs imported from Log Service.
        """
        if alias is not None:
            pulumi.set(__self__, 'alias', alias)
        if sls_key_name is not None:
            pulumi.set(__self__, 'sls_key_name', sls_key_name)

    @property
    @pulumi.getter
    def alias(self) -> Optional[pulumi.Input[str]]:
        """
        The alias of the aggregation result.
        """
        return pulumi.get(self, 'alias')

    @alias.setter
    def alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'alias', value)

    @property
    @pulumi.getter(name='slsKeyName')
    def sls_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the key that is used to aggregate logs imported from Log Service.
        """
        return pulumi.get(self, 'sls_key_name')

    @sls_key_name.setter
    def sls_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sls_key_name', value)

@pulumi.input_type
class HybridMonitorSlsTaskSlsProcessConfigStatisticArgs:

    def __init__(__self__, *, alias: Optional[pulumi.Input[str]]=None, function: Optional[pulumi.Input[str]]=None, parameter_one: Optional[pulumi.Input[str]]=None, parameter_two: Optional[pulumi.Input[str]]=None, sls_key_name: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] alias: The alias of the aggregation result.
        :param pulumi.Input[str] function: The function that is used to aggregate log data within a statistical period. Valid values: `count`, `sum`, `avg`, `max`, `min`, `value`, `countps`, `sumps`, `distinct`, `distribution`, `percentile`.
        :param pulumi.Input[str] parameter_one: The value of the function that is used to aggregate logs imported from Log Service.
               - If you set the `function` parameter to `distribution`, this parameter specifies the lower limit of the statistical interval. For example, if you want to calculate the number of HTTP requests whose status code is 2XX, set this parameter to 200.
               - If you set the `function` parameter to `percentile`, this parameter specifies the percentile at which the expected value is. For example, 0.5 specifies P50.
        :param pulumi.Input[str] parameter_two: The value of the function that is used to aggregate logs imported from Log Service. **Note:** This parameter is required only if the `function` parameter is set to `distribution`. This parameter specifies the upper limit of the statistical interval.
        :param pulumi.Input[str] sls_key_name: The name of the key that is used to aggregate logs imported from Log Service.
        """
        if alias is not None:
            pulumi.set(__self__, 'alias', alias)
        if function is not None:
            pulumi.set(__self__, 'function', function)
        if parameter_one is not None:
            pulumi.set(__self__, 'parameter_one', parameter_one)
        if parameter_two is not None:
            pulumi.set(__self__, 'parameter_two', parameter_two)
        if sls_key_name is not None:
            pulumi.set(__self__, 'sls_key_name', sls_key_name)

    @property
    @pulumi.getter
    def alias(self) -> Optional[pulumi.Input[str]]:
        """
        The alias of the aggregation result.
        """
        return pulumi.get(self, 'alias')

    @alias.setter
    def alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'alias', value)

    @property
    @pulumi.getter
    def function(self) -> Optional[pulumi.Input[str]]:
        """
        The function that is used to aggregate log data within a statistical period. Valid values: `count`, `sum`, `avg`, `max`, `min`, `value`, `countps`, `sumps`, `distinct`, `distribution`, `percentile`.
        """
        return pulumi.get(self, 'function')

    @function.setter
    def function(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'function', value)

    @property
    @pulumi.getter(name='parameterOne')
    def parameter_one(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the function that is used to aggregate logs imported from Log Service.
        - If you set the `function` parameter to `distribution`, this parameter specifies the lower limit of the statistical interval. For example, if you want to calculate the number of HTTP requests whose status code is 2XX, set this parameter to 200.
        - If you set the `function` parameter to `percentile`, this parameter specifies the percentile at which the expected value is. For example, 0.5 specifies P50.
        """
        return pulumi.get(self, 'parameter_one')

    @parameter_one.setter
    def parameter_one(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'parameter_one', value)

    @property
    @pulumi.getter(name='parameterTwo')
    def parameter_two(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the function that is used to aggregate logs imported from Log Service. **Note:** This parameter is required only if the `function` parameter is set to `distribution`. This parameter specifies the upper limit of the statistical interval.
        """
        return pulumi.get(self, 'parameter_two')

    @parameter_two.setter
    def parameter_two(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'parameter_two', value)

    @property
    @pulumi.getter(name='slsKeyName')
    def sls_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the key that is used to aggregate logs imported from Log Service.
        """
        return pulumi.get(self, 'sls_key_name')

    @sls_key_name.setter
    def sls_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sls_key_name', value)

@pulumi.input_type
class MetricRuleBlackListMetricArgs:

    def __init__(__self__, *, metric_name: pulumi.Input[str], resource: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] metric_name: The name of the monitoring indicator.
        :param pulumi.Input[str] resource: The extended dimension information of the instance. For example, '{"device":"C:"}' indicates that the blacklist policy is applied to all C disks under the ECS instance.
        """
        pulumi.set(__self__, 'metric_name', metric_name)
        if resource is not None:
            pulumi.set(__self__, 'resource', resource)

    @property
    @pulumi.getter(name='metricName')
    def metric_name(self) -> pulumi.Input[str]:
        """
        The name of the monitoring indicator.
        """
        return pulumi.get(self, 'metric_name')

    @metric_name.setter
    def metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'metric_name', value)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input[str]]:
        """
        The extended dimension information of the instance. For example, '{"device":"C:"}' indicates that the blacklist policy is applied to all C disks under the ECS instance.
        """
        return pulumi.get(self, 'resource')

    @resource.setter
    def resource(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource', value)

@pulumi.input_type
class MetricRuleTemplateAlertTemplateArgs:

    def __init__(__self__, *, category: pulumi.Input[str], metric_name: pulumi.Input[str], namespace: pulumi.Input[str], rule_name: pulumi.Input[str], escalations: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsArgs']]=None, webhook: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] category: The abbreviation of the service name. Valid values: `ecs`, `rds`, `ads`, `slb`, `vpc`, `apigateway`, `cdn`, `cs`, `dcdn`, `ddos`, `eip`, `elasticsearch`, `emr`, `ess`, `hbase`, `iot_edge`, `kvstore_sharding`, `kvstore_splitrw`, `kvstore_standard`, `memcache`, `mns`, `mongodb`, `mongodb_cluster`, `mongodb_sharding`, `mq_topic`, `ocs`, `opensearch`, `oss`, `polardb`, `petadata`, `scdn`, `sharebandwidthpackages`, `sls`, `vpn`.
        :param pulumi.Input[str] metric_name: The name of the metric.
               
               > **NOTE:** For more information, see [DescribeMetricMetaList](https://www.alibabacloud.com/help/doc-detail/98846.htm) or [Appendix 1: Metrics](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] namespace: The namespace of the service.
               
               > **NOTE:** For more information, see [DescribeMetricMetaList](https://www.alibabacloud.com/help/doc-detail/98846.htm) or [Appendix 1: Metrics](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        :param pulumi.Input[str] rule_name: The name of the alert rule.
        :param pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsArgs'] escalations: The information about the trigger condition based on the alert level. See the following `Block escalations`.
        :param pulumi.Input[str] webhook: The callback URL to which a POST request is sent when an alert is triggered based on the alert rule.
        """
        pulumi.set(__self__, 'category', category)
        pulumi.set(__self__, 'metric_name', metric_name)
        pulumi.set(__self__, 'namespace', namespace)
        pulumi.set(__self__, 'rule_name', rule_name)
        if escalations is not None:
            pulumi.set(__self__, 'escalations', escalations)
        if webhook is not None:
            pulumi.set(__self__, 'webhook', webhook)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input[str]:
        """
        The abbreviation of the service name. Valid values: `ecs`, `rds`, `ads`, `slb`, `vpc`, `apigateway`, `cdn`, `cs`, `dcdn`, `ddos`, `eip`, `elasticsearch`, `emr`, `ess`, `hbase`, `iot_edge`, `kvstore_sharding`, `kvstore_splitrw`, `kvstore_standard`, `memcache`, `mns`, `mongodb`, `mongodb_cluster`, `mongodb_sharding`, `mq_topic`, `ocs`, `opensearch`, `oss`, `polardb`, `petadata`, `scdn`, `sharebandwidthpackages`, `sls`, `vpn`.
        """
        return pulumi.get(self, 'category')

    @category.setter
    def category(self, value: pulumi.Input[str]):
        pulumi.set(self, 'category', value)

    @property
    @pulumi.getter(name='metricName')
    def metric_name(self) -> pulumi.Input[str]:
        """
        The name of the metric.

        > **NOTE:** For more information, see [DescribeMetricMetaList](https://www.alibabacloud.com/help/doc-detail/98846.htm) or [Appendix 1: Metrics](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        """
        return pulumi.get(self, 'metric_name')

    @metric_name.setter
    def metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'metric_name', value)

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Input[str]:
        """
        The namespace of the service.

        > **NOTE:** For more information, see [DescribeMetricMetaList](https://www.alibabacloud.com/help/doc-detail/98846.htm) or [Appendix 1: Metrics](https://www.alibabacloud.com/help/doc-detail/28619.htm).
        """
        return pulumi.get(self, 'namespace')

    @namespace.setter
    def namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace', value)

    @property
    @pulumi.getter(name='ruleName')
    def rule_name(self) -> pulumi.Input[str]:
        """
        The name of the alert rule.
        """
        return pulumi.get(self, 'rule_name')

    @rule_name.setter
    def rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'rule_name', value)

    @property
    @pulumi.getter
    def escalations(self) -> Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsArgs']]:
        """
        The information about the trigger condition based on the alert level. See the following `Block escalations`.
        """
        return pulumi.get(self, 'escalations')

    @escalations.setter
    def escalations(self, value: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsArgs']]):
        pulumi.set(self, 'escalations', value)

    @property
    @pulumi.getter
    def webhook(self) -> Optional[pulumi.Input[str]]:
        """
        The callback URL to which a POST request is sent when an alert is triggered based on the alert rule.
        """
        return pulumi.get(self, 'webhook')

    @webhook.setter
    def webhook(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'webhook', value)

@pulumi.input_type
class MetricRuleTemplateAlertTemplateEscalationsArgs:

    def __init__(__self__, *, critical: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsCriticalArgs']]=None, info: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsInfoArgs']]=None, warn: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsWarnArgs']]=None):
        """
        :param pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsCriticalArgs'] critical: The condition for triggering critical-level alerts. See the following `Block critical`.
        :param pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsInfoArgs'] info: The condition for triggering info-level alerts. See the following `Block info`.
        :param pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsWarnArgs'] warn: The condition for triggering warn-level alerts. See the following `Block warn`.
        """
        if critical is not None:
            pulumi.set(__self__, 'critical', critical)
        if info is not None:
            pulumi.set(__self__, 'info', info)
        if warn is not None:
            pulumi.set(__self__, 'warn', warn)

    @property
    @pulumi.getter
    def critical(self) -> Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsCriticalArgs']]:
        """
        The condition for triggering critical-level alerts. See the following `Block critical`.
        """
        return pulumi.get(self, 'critical')

    @critical.setter
    def critical(self, value: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsCriticalArgs']]):
        pulumi.set(self, 'critical', value)

    @property
    @pulumi.getter
    def info(self) -> Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsInfoArgs']]:
        """
        The condition for triggering info-level alerts. See the following `Block info`.
        """
        return pulumi.get(self, 'info')

    @info.setter
    def info(self, value: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsInfoArgs']]):
        pulumi.set(self, 'info', value)

    @property
    @pulumi.getter
    def warn(self) -> Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsWarnArgs']]:
        """
        The condition for triggering warn-level alerts. See the following `Block warn`.
        """
        return pulumi.get(self, 'warn')

    @warn.setter
    def warn(self, value: Optional[pulumi.Input['MetricRuleTemplateAlertTemplateEscalationsWarnArgs']]):
        pulumi.set(self, 'warn', value)

@pulumi.input_type
class MetricRuleTemplateAlertTemplateEscalationsCriticalArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        :param pulumi.Input[str] statistics: The statistical aggregation method for warn-level alerts.
        :param pulumi.Input[str] threshold: The threshold for warn-level alerts.
        :param pulumi.Input[str] times: The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for warn-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for warn-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[str]]:
        """
        The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class MetricRuleTemplateAlertTemplateEscalationsInfoArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        :param pulumi.Input[str] statistics: The statistical aggregation method for warn-level alerts.
        :param pulumi.Input[str] threshold: The threshold for warn-level alerts.
        :param pulumi.Input[str] times: The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for warn-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for warn-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[str]]:
        """
        The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class MetricRuleTemplateAlertTemplateEscalationsWarnArgs:

    def __init__(__self__, *, comparison_operator: Optional[pulumi.Input[str]]=None, statistics: Optional[pulumi.Input[str]]=None, threshold: Optional[pulumi.Input[str]]=None, times: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] comparison_operator: The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        :param pulumi.Input[str] statistics: The statistical aggregation method for warn-level alerts.
        :param pulumi.Input[str] threshold: The threshold for warn-level alerts.
        :param pulumi.Input[str] times: The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        if comparison_operator is not None:
            pulumi.set(__self__, 'comparison_operator', comparison_operator)
        if statistics is not None:
            pulumi.set(__self__, 'statistics', statistics)
        if threshold is not None:
            pulumi.set(__self__, 'threshold', threshold)
        if times is not None:
            pulumi.set(__self__, 'times', times)

    @property
    @pulumi.getter(name='comparisonOperator')
    def comparison_operator(self) -> Optional[pulumi.Input[str]]:
        """
        The comparison operator of the threshold for warn-level alerts. Valid values: `GreaterThanOrEqualToThreshold`, `GreaterThanThreshold`, `LessThanOrEqualToThreshold`, `LessThanThreshold`, `NotEqualToThreshold`, `GreaterThanYesterday`, `LessThanYesterday`, `GreaterThanLastWeek`, `LessThanLastWeek`, `GreaterThanLastPeriod`, `LessThanLastPeriod`.
        """
        return pulumi.get(self, 'comparison_operator')

    @comparison_operator.setter
    def comparison_operator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'comparison_operator', value)

    @property
    @pulumi.getter
    def statistics(self) -> Optional[pulumi.Input[str]]:
        """
        The statistical aggregation method for warn-level alerts.
        """
        return pulumi.get(self, 'statistics')

    @statistics.setter
    def statistics(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'statistics', value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[str]]:
        """
        The threshold for warn-level alerts.
        """
        return pulumi.get(self, 'threshold')

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'threshold', value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[str]]:
        """
        The consecutive number of times for which the metric value is measured before a warn-level alert is triggered.
        """
        return pulumi.get(self, 'times')

    @times.setter
    def times(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'times', value)

@pulumi.input_type
class MonitorGroupInstancesInstanceArgs:

    def __init__(__self__, *, category: pulumi.Input[str], instance_id: pulumi.Input[str], instance_name: pulumi.Input[str], region_id: pulumi.Input[str]):
        """
        :param pulumi.Input[str] category: The category of instance.
        :param pulumi.Input[str] instance_id: The id of instance.
        :param pulumi.Input[str] instance_name: The name of instance.
        :param pulumi.Input[str] region_id: The region id of instance.
        """
        pulumi.set(__self__, 'category', category)
        pulumi.set(__self__, 'instance_id', instance_id)
        pulumi.set(__self__, 'instance_name', instance_name)
        pulumi.set(__self__, 'region_id', region_id)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input[str]:
        """
        The category of instance.
        """
        return pulumi.get(self, 'category')

    @category.setter
    def category(self, value: pulumi.Input[str]):
        pulumi.set(self, 'category', value)

    @property
    @pulumi.getter(name='instanceId')
    def instance_id(self) -> pulumi.Input[str]:
        """
        The id of instance.
        """
        return pulumi.get(self, 'instance_id')

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'instance_id', value)

    @property
    @pulumi.getter(name='instanceName')
    def instance_name(self) -> pulumi.Input[str]:
        """
        The name of instance.
        """
        return pulumi.get(self, 'instance_name')

    @instance_name.setter
    def instance_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'instance_name', value)

    @property
    @pulumi.getter(name='regionId')
    def region_id(self) -> pulumi.Input[str]:
        """
        The region id of instance.
        """
        return pulumi.get(self, 'region_id')

    @region_id.setter
    def region_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'region_id', value)

@pulumi.input_type
class SiteMonitorIspCityArgs:

    def __init__(__self__, *, city: pulumi.Input[str], isp: pulumi.Input[str]):
        pulumi.set(__self__, 'city', city)
        pulumi.set(__self__, 'isp', isp)

    @property
    @pulumi.getter
    def city(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'city')

    @city.setter
    def city(self, value: pulumi.Input[str]):
        pulumi.set(self, 'city', value)

    @property
    @pulumi.getter
    def isp(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'isp')

    @isp.setter
    def isp(self, value: pulumi.Input[str]):
        pulumi.set(self, 'isp', value)

@pulumi.input_type
class SlsGroupSlsGroupConfigArgs:

    def __init__(__self__, *, sls_logstore: pulumi.Input[str], sls_project: pulumi.Input[str], sls_region: pulumi.Input[str], sls_user_id: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] sls_logstore: The name of the Log Store.
        :param pulumi.Input[str] sls_project: The name of the Project.
        :param pulumi.Input[str] sls_region: The Sls Region.
        :param pulumi.Input[str] sls_user_id: The ID of the Sls User.
        """
        pulumi.set(__self__, 'sls_logstore', sls_logstore)
        pulumi.set(__self__, 'sls_project', sls_project)
        pulumi.set(__self__, 'sls_region', sls_region)
        if sls_user_id is not None:
            pulumi.set(__self__, 'sls_user_id', sls_user_id)

    @property
    @pulumi.getter(name='slsLogstore')
    def sls_logstore(self) -> pulumi.Input[str]:
        """
        The name of the Log Store.
        """
        return pulumi.get(self, 'sls_logstore')

    @sls_logstore.setter
    def sls_logstore(self, value: pulumi.Input[str]):
        pulumi.set(self, 'sls_logstore', value)

    @property
    @pulumi.getter(name='slsProject')
    def sls_project(self) -> pulumi.Input[str]:
        """
        The name of the Project.
        """
        return pulumi.get(self, 'sls_project')

    @sls_project.setter
    def sls_project(self, value: pulumi.Input[str]):
        pulumi.set(self, 'sls_project', value)

    @property
    @pulumi.getter(name='slsRegion')
    def sls_region(self) -> pulumi.Input[str]:
        """
        The Sls Region.
        """
        return pulumi.get(self, 'sls_region')

    @sls_region.setter
    def sls_region(self, value: pulumi.Input[str]):
        pulumi.set(self, 'sls_region', value)

    @property
    @pulumi.getter(name='slsUserId')
    def sls_user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Sls User.
        """
        return pulumi.get(self, 'sls_user_id')

    @sls_user_id.setter
    def sls_user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sls_user_id', value)
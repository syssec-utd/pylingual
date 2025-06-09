import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetFusionAlertRuleResult', 'AwaitableGetFusionAlertRuleResult', 'get_fusion_alert_rule', 'get_fusion_alert_rule_output']

@pulumi.output_type
class GetFusionAlertRuleResult:
    """
    Represents Fusion alert rule.
    """

    def __init__(__self__, alert_rule_template_name=None, description=None, display_name=None, enabled=None, etag=None, id=None, kind=None, last_modified_utc=None, name=None, scenario_exclusion_patterns=None, severity=None, source_settings=None, system_data=None, tactics=None, techniques=None, type=None):
        if alert_rule_template_name and (not isinstance(alert_rule_template_name, str)):
            raise TypeError("Expected argument 'alert_rule_template_name' to be a str")
        pulumi.set(__self__, 'alert_rule_template_name', alert_rule_template_name)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if enabled and (not isinstance(enabled, bool)):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, 'enabled', enabled)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if last_modified_utc and (not isinstance(last_modified_utc, str)):
            raise TypeError("Expected argument 'last_modified_utc' to be a str")
        pulumi.set(__self__, 'last_modified_utc', last_modified_utc)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if scenario_exclusion_patterns and (not isinstance(scenario_exclusion_patterns, list)):
            raise TypeError("Expected argument 'scenario_exclusion_patterns' to be a list")
        pulumi.set(__self__, 'scenario_exclusion_patterns', scenario_exclusion_patterns)
        if severity and (not isinstance(severity, str)):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, 'severity', severity)
        if source_settings and (not isinstance(source_settings, list)):
            raise TypeError("Expected argument 'source_settings' to be a list")
        pulumi.set(__self__, 'source_settings', source_settings)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tactics and (not isinstance(tactics, list)):
            raise TypeError("Expected argument 'tactics' to be a list")
        pulumi.set(__self__, 'tactics', tactics)
        if techniques and (not isinstance(techniques, list)):
            raise TypeError("Expected argument 'techniques' to be a list")
        pulumi.set(__self__, 'techniques', techniques)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='alertRuleTemplateName')
    def alert_rule_template_name(self) -> str:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, 'alert_rule_template_name')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the alert rule
        Expected value is 'Fusion'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='lastModifiedUtc')
    def last_modified_utc(self) -> str:
        """
        The last time that this alert has been modified.
        """
        return pulumi.get(self, 'last_modified_utc')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='scenarioExclusionPatterns')
    def scenario_exclusion_patterns(self) -> Optional[Sequence['outputs.FusionScenarioExclusionPatternResponse']]:
        """
        Configuration to exclude scenarios in fusion detection.
        """
        return pulumi.get(self, 'scenario_exclusion_patterns')

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, 'severity')

    @property
    @pulumi.getter(name='sourceSettings')
    def source_settings(self) -> Optional[Sequence['outputs.FusionSourceSettingsResponse']]:
        """
        Configuration for all supported source signals in fusion detection.
        """
        return pulumi.get(self, 'source_settings')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tactics(self) -> Sequence[str]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, 'tactics')

    @property
    @pulumi.getter
    def techniques(self) -> Sequence[str]:
        """
        The techniques of the alert rule
        """
        return pulumi.get(self, 'techniques')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetFusionAlertRuleResult(GetFusionAlertRuleResult):

    def __await__(self):
        if False:
            yield self
        return GetFusionAlertRuleResult(alert_rule_template_name=self.alert_rule_template_name, description=self.description, display_name=self.display_name, enabled=self.enabled, etag=self.etag, id=self.id, kind=self.kind, last_modified_utc=self.last_modified_utc, name=self.name, scenario_exclusion_patterns=self.scenario_exclusion_patterns, severity=self.severity, source_settings=self.source_settings, system_data=self.system_data, tactics=self.tactics, techniques=self.techniques, type=self.type)

def get_fusion_alert_rule(resource_group_name: Optional[str]=None, rule_id: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetFusionAlertRuleResult:
    """
    Gets the alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleId'] = rule_id
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20230201preview:getFusionAlertRule', __args__, opts=opts, typ=GetFusionAlertRuleResult).value
    return AwaitableGetFusionAlertRuleResult(alert_rule_template_name=__ret__.alert_rule_template_name, description=__ret__.description, display_name=__ret__.display_name, enabled=__ret__.enabled, etag=__ret__.etag, id=__ret__.id, kind=__ret__.kind, last_modified_utc=__ret__.last_modified_utc, name=__ret__.name, scenario_exclusion_patterns=__ret__.scenario_exclusion_patterns, severity=__ret__.severity, source_settings=__ret__.source_settings, system_data=__ret__.system_data, tactics=__ret__.tactics, techniques=__ret__.techniques, type=__ret__.type)

@_utilities.lift_output_func(get_fusion_alert_rule)
def get_fusion_alert_rule_output(resource_group_name: Optional[pulumi.Input[str]]=None, rule_id: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetFusionAlertRuleResult]:
    """
    Gets the alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    ...
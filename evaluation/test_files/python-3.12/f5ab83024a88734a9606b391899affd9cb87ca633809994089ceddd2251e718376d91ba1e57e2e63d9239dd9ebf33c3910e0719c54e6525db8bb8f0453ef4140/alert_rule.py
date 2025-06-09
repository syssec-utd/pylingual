import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['AlertRuleArgs', 'AlertRule']

@pulumi.input_type
class AlertRuleArgs:

    def __init__(__self__, *, kind: pulumi.Input[Union[str, 'AlertRuleKind']], resource_group_name: pulumi.Input[str], workspace_name: pulumi.Input[str], rule_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a AlertRule resource.
        :param pulumi.Input[Union[str, 'AlertRuleKind']] kind: The kind of the alert rule
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] rule_id: Alert rule ID
        """
        pulumi.set(__self__, 'kind', kind)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'workspace_name', workspace_name)
        if rule_id is not None:
            pulumi.set(__self__, 'rule_id', rule_id)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[Union[str, 'AlertRuleKind']]:
        """
        The kind of the alert rule
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[Union[str, 'AlertRuleKind']]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='workspaceName')
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, 'workspace_name')

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'workspace_name', value)

    @property
    @pulumi.getter(name='ruleId')
    def rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        Alert rule ID
        """
        return pulumi.get(self, 'rule_id')

    @rule_id.setter
    def rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'rule_id', value)
warnings.warn('Please use one of the variants: FusionAlertRule, MLBehaviorAnalyticsAlertRule, MicrosoftSecurityIncidentCreationAlertRule, NrtAlertRule, ScheduledAlertRule, ThreatIntelligenceAlertRule.', DeprecationWarning)

class AlertRule(pulumi.CustomResource):
    warnings.warn('Please use one of the variants: FusionAlertRule, MLBehaviorAnalyticsAlertRule, MicrosoftSecurityIncidentCreationAlertRule, NrtAlertRule, ScheduledAlertRule, ThreatIntelligenceAlertRule.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[Union[str, 'AlertRuleKind']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_id: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Alert rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'AlertRuleKind']] kind: The kind of the alert rule
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: AlertRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Alert rule.

        :param str resource_name: The name of the resource.
        :param AlertRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AlertRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[Union[str, 'AlertRuleKind']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_id: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        pulumi.log.warn('AlertRule is deprecated: Please use one of the variants: FusionAlertRule, MLBehaviorAnalyticsAlertRule, MicrosoftSecurityIncidentCreationAlertRule, NrtAlertRule, ScheduledAlertRule, ThreatIntelligenceAlertRule.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AlertRuleArgs.__new__(AlertRuleArgs)
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = kind
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['rule_id'] = rule_id
            if workspace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__['workspace_name'] = workspace_name
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:securityinsights:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20190101preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20200101:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20210301preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20210901preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20211001:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20211001preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220101preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220401preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220501preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220701preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220801:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220801preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220901preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221001preview:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221101:AlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221101preview:AlertRule')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AlertRule, __self__).__init__('azure-native:securityinsights/v20220601preview:AlertRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'AlertRule':
        """
        Get an existing AlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = AlertRuleArgs.__new__(AlertRuleArgs)
        __props__.__dict__['etag'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return AlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the alert rule
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['MicrosoftSecurityIncidentCreationAlertRuleArgs', 'MicrosoftSecurityIncidentCreationAlertRule']

@pulumi.input_type
class MicrosoftSecurityIncidentCreationAlertRuleArgs:

    def __init__(__self__, *, display_name: pulumi.Input[str], enabled: pulumi.Input[bool], kind: pulumi.Input[str], product_filter: pulumi.Input[Union[str, 'MicrosoftSecurityProductName']], resource_group_name: pulumi.Input[str], workspace_name: pulumi.Input[str], alert_rule_template_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_names_exclude_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_names_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, rule_id: Optional[pulumi.Input[str]]=None, severities_filter: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]]]=None):
        """
        The set of arguments for constructing a MicrosoftSecurityIncidentCreationAlertRule resource.
        :param pulumi.Input[str] display_name: The display name for alerts created by this alert rule.
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'MicrosoftSecurityIncidentCreation'.
        :param pulumi.Input[Union[str, 'MicrosoftSecurityProductName']] product_filter: The alerts' productName on which the cases will be generated
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[str] description: The description of the alert rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] display_names_exclude_filter: the alerts' displayNames on which the cases will not be generated
        :param pulumi.Input[Sequence[pulumi.Input[str]]] display_names_filter: the alerts' displayNames on which the cases will be generated
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]] severities_filter: the alerts' severities on which the cases will be generated
        """
        pulumi.set(__self__, 'display_name', display_name)
        pulumi.set(__self__, 'enabled', enabled)
        pulumi.set(__self__, 'kind', 'MicrosoftSecurityIncidentCreation')
        pulumi.set(__self__, 'product_filter', product_filter)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'workspace_name', workspace_name)
        if alert_rule_template_name is not None:
            pulumi.set(__self__, 'alert_rule_template_name', alert_rule_template_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_names_exclude_filter is not None:
            pulumi.set(__self__, 'display_names_exclude_filter', display_names_exclude_filter)
        if display_names_filter is not None:
            pulumi.set(__self__, 'display_names_filter', display_names_filter)
        if rule_id is not None:
            pulumi.set(__self__, 'rule_id', rule_id)
        if severities_filter is not None:
            pulumi.set(__self__, 'severities_filter', severities_filter)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of the alert rule
        Expected value is 'MicrosoftSecurityIncidentCreation'.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='productFilter')
    def product_filter(self) -> pulumi.Input[Union[str, 'MicrosoftSecurityProductName']]:
        """
        The alerts' productName on which the cases will be generated
        """
        return pulumi.get(self, 'product_filter')

    @product_filter.setter
    def product_filter(self, value: pulumi.Input[Union[str, 'MicrosoftSecurityProductName']]):
        pulumi.set(self, 'product_filter', value)

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
    @pulumi.getter(name='alertRuleTemplateName')
    def alert_rule_template_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, 'alert_rule_template_name')

    @alert_rule_template_name.setter
    def alert_rule_template_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'alert_rule_template_name', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayNamesExcludeFilter')
    def display_names_exclude_filter(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the alerts' displayNames on which the cases will not be generated
        """
        return pulumi.get(self, 'display_names_exclude_filter')

    @display_names_exclude_filter.setter
    def display_names_exclude_filter(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'display_names_exclude_filter', value)

    @property
    @pulumi.getter(name='displayNamesFilter')
    def display_names_filter(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        the alerts' displayNames on which the cases will be generated
        """
        return pulumi.get(self, 'display_names_filter')

    @display_names_filter.setter
    def display_names_filter(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'display_names_filter', value)

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

    @property
    @pulumi.getter(name='severitiesFilter')
    def severities_filter(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]]]:
        """
        the alerts' severities on which the cases will be generated
        """
        return pulumi.get(self, 'severities_filter')

    @severities_filter.setter
    def severities_filter(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]]]):
        pulumi.set(self, 'severities_filter', value)

class MicrosoftSecurityIncidentCreationAlertRule(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, alert_rule_template_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, display_names_exclude_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_names_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, kind: Optional[pulumi.Input[str]]=None, product_filter: Optional[pulumi.Input[Union[str, 'MicrosoftSecurityProductName']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_id: Optional[pulumi.Input[str]]=None, severities_filter: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Represents MicrosoftSecurityIncidentCreation rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alert_rule_template_name: The Name of the alert rule template used to create this rule.
        :param pulumi.Input[str] description: The description of the alert rule.
        :param pulumi.Input[str] display_name: The display name for alerts created by this alert rule.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] display_names_exclude_filter: the alerts' displayNames on which the cases will not be generated
        :param pulumi.Input[Sequence[pulumi.Input[str]]] display_names_filter: the alerts' displayNames on which the cases will be generated
        :param pulumi.Input[bool] enabled: Determines whether this alert rule is enabled or disabled.
        :param pulumi.Input[str] kind: The kind of the alert rule
               Expected value is 'MicrosoftSecurityIncidentCreation'.
        :param pulumi.Input[Union[str, 'MicrosoftSecurityProductName']] product_filter: The alerts' productName on which the cases will be generated
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]] severities_filter: the alerts' severities on which the cases will be generated
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: MicrosoftSecurityIncidentCreationAlertRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Represents MicrosoftSecurityIncidentCreation rule.

        :param str resource_name: The name of the resource.
        :param MicrosoftSecurityIncidentCreationAlertRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MicrosoftSecurityIncidentCreationAlertRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, alert_rule_template_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, display_names_exclude_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_names_filter: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, kind: Optional[pulumi.Input[str]]=None, product_filter: Optional[pulumi.Input[Union[str, 'MicrosoftSecurityProductName']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_id: Optional[pulumi.Input[str]]=None, severities_filter: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AlertSeverity']]]]]=None, workspace_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MicrosoftSecurityIncidentCreationAlertRuleArgs.__new__(MicrosoftSecurityIncidentCreationAlertRuleArgs)
            __props__.__dict__['alert_rule_template_name'] = alert_rule_template_name
            __props__.__dict__['description'] = description
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['display_names_exclude_filter'] = display_names_exclude_filter
            __props__.__dict__['display_names_filter'] = display_names_filter
            if enabled is None and (not opts.urn):
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__['enabled'] = enabled
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = 'MicrosoftSecurityIncidentCreation'
            if product_filter is None and (not opts.urn):
                raise TypeError("Missing required property 'product_filter'")
            __props__.__dict__['product_filter'] = product_filter
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['rule_id'] = rule_id
            __props__.__dict__['severities_filter'] = severities_filter
            if workspace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__['workspace_name'] = workspace_name
            __props__.__dict__['etag'] = None
            __props__.__dict__['last_modified_utc'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:securityinsights:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20190101preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20200101:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20210301preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20210901preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20211001:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20211001preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220101preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220401preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220501preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220601preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220801:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220801preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20220901preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221001preview:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221101:MicrosoftSecurityIncidentCreationAlertRule'), pulumi.Alias(type_='azure-native:securityinsights/v20221101preview:MicrosoftSecurityIncidentCreationAlertRule')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MicrosoftSecurityIncidentCreationAlertRule, __self__).__init__('azure-native:securityinsights/v20220701preview:MicrosoftSecurityIncidentCreationAlertRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'MicrosoftSecurityIncidentCreationAlertRule':
        """
        Get an existing MicrosoftSecurityIncidentCreationAlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = MicrosoftSecurityIncidentCreationAlertRuleArgs.__new__(MicrosoftSecurityIncidentCreationAlertRuleArgs)
        __props__.__dict__['alert_rule_template_name'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['display_names_exclude_filter'] = None
        __props__.__dict__['display_names_filter'] = None
        __props__.__dict__['enabled'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['last_modified_utc'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['product_filter'] = None
        __props__.__dict__['severities_filter'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return MicrosoftSecurityIncidentCreationAlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='alertRuleTemplateName')
    def alert_rule_template_name(self) -> pulumi.Output[Optional[str]]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, 'alert_rule_template_name')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='displayNamesExcludeFilter')
    def display_names_exclude_filter(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        the alerts' displayNames on which the cases will not be generated
        """
        return pulumi.get(self, 'display_names_exclude_filter')

    @property
    @pulumi.getter(name='displayNamesFilter')
    def display_names_filter(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        the alerts' displayNames on which the cases will be generated
        """
        return pulumi.get(self, 'display_names_filter')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, 'enabled')

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
        Expected value is 'MicrosoftSecurityIncidentCreation'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='lastModifiedUtc')
    def last_modified_utc(self) -> pulumi.Output[str]:
        """
        The last time that this alert has been modified.
        """
        return pulumi.get(self, 'last_modified_utc')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='productFilter')
    def product_filter(self) -> pulumi.Output[str]:
        """
        The alerts' productName on which the cases will be generated
        """
        return pulumi.get(self, 'product_filter')

    @property
    @pulumi.getter(name='severitiesFilter')
    def severities_filter(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        the alerts' severities on which the cases will be generated
        """
        return pulumi.get(self, 'severities_filter')

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
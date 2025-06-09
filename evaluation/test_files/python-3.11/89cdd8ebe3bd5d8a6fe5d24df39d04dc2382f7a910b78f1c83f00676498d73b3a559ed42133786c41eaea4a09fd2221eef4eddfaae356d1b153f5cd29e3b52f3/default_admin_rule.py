import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['DefaultAdminRuleArgs', 'DefaultAdminRule']

@pulumi.input_type
class DefaultAdminRuleArgs:

    def __init__(__self__, *, configuration_name: pulumi.Input[str], kind: pulumi.Input[str], network_manager_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], rule_collection_name: pulumi.Input[str], flag: Optional[pulumi.Input[str]]=None, rule_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a DefaultAdminRule resource.
        :param pulumi.Input[str] configuration_name: The name of the network manager Security Configuration.
        :param pulumi.Input[str] kind: Whether the rule is custom or default.
               Expected value is 'Default'.
        :param pulumi.Input[str] network_manager_name: The name of the network manager.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] rule_collection_name: The name of the network manager security Configuration rule collection.
        :param pulumi.Input[str] flag: Default rule flag.
        :param pulumi.Input[str] rule_name: The name of the rule.
        """
        pulumi.set(__self__, 'configuration_name', configuration_name)
        pulumi.set(__self__, 'kind', 'Default')
        pulumi.set(__self__, 'network_manager_name', network_manager_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'rule_collection_name', rule_collection_name)
        if flag is not None:
            pulumi.set(__self__, 'flag', flag)
        if rule_name is not None:
            pulumi.set(__self__, 'rule_name', rule_name)

    @property
    @pulumi.getter(name='configurationName')
    def configuration_name(self) -> pulumi.Input[str]:
        """
        The name of the network manager Security Configuration.
        """
        return pulumi.get(self, 'configuration_name')

    @configuration_name.setter
    def configuration_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'configuration_name', value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        Whether the rule is custom or default.
        Expected value is 'Default'.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='networkManagerName')
    def network_manager_name(self) -> pulumi.Input[str]:
        """
        The name of the network manager.
        """
        return pulumi.get(self, 'network_manager_name')

    @network_manager_name.setter
    def network_manager_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'network_manager_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='ruleCollectionName')
    def rule_collection_name(self) -> pulumi.Input[str]:
        """
        The name of the network manager security Configuration rule collection.
        """
        return pulumi.get(self, 'rule_collection_name')

    @rule_collection_name.setter
    def rule_collection_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'rule_collection_name', value)

    @property
    @pulumi.getter
    def flag(self) -> Optional[pulumi.Input[str]]:
        """
        Default rule flag.
        """
        return pulumi.get(self, 'flag')

    @flag.setter
    def flag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'flag', value)

    @property
    @pulumi.getter(name='ruleName')
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rule.
        """
        return pulumi.get(self, 'rule_name')

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'rule_name', value)

class DefaultAdminRule(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, configuration_name: Optional[pulumi.Input[str]]=None, flag: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, network_manager_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_collection_name: Optional[pulumi.Input[str]]=None, rule_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Network default admin rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_name: The name of the network manager Security Configuration.
        :param pulumi.Input[str] flag: Default rule flag.
        :param pulumi.Input[str] kind: Whether the rule is custom or default.
               Expected value is 'Default'.
        :param pulumi.Input[str] network_manager_name: The name of the network manager.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] rule_collection_name: The name of the network manager security Configuration rule collection.
        :param pulumi.Input[str] rule_name: The name of the rule.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DefaultAdminRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Network default admin rule.

        :param str resource_name: The name of the resource.
        :param DefaultAdminRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DefaultAdminRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, configuration_name: Optional[pulumi.Input[str]]=None, flag: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, network_manager_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_collection_name: Optional[pulumi.Input[str]]=None, rule_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DefaultAdminRuleArgs.__new__(DefaultAdminRuleArgs)
            if configuration_name is None and (not opts.urn):
                raise TypeError("Missing required property 'configuration_name'")
            __props__.__dict__['configuration_name'] = configuration_name
            __props__.__dict__['flag'] = flag
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = 'Default'
            if network_manager_name is None and (not opts.urn):
                raise TypeError("Missing required property 'network_manager_name'")
            __props__.__dict__['network_manager_name'] = network_manager_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if rule_collection_name is None and (not opts.urn):
                raise TypeError("Missing required property 'rule_collection_name'")
            __props__.__dict__['rule_collection_name'] = rule_collection_name
            __props__.__dict__['rule_name'] = rule_name
            __props__.__dict__['access'] = None
            __props__.__dict__['description'] = None
            __props__.__dict__['destination_port_ranges'] = None
            __props__.__dict__['destinations'] = None
            __props__.__dict__['direction'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['priority'] = None
            __props__.__dict__['protocol'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['source_port_ranges'] = None
            __props__.__dict__['sources'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20210201preview:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20210501preview:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20220101:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20220201preview:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20220401preview:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20220501:DefaultAdminRule'), pulumi.Alias(type_='azure-native:network/v20220901:DefaultAdminRule')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DefaultAdminRule, __self__).__init__('azure-native:network/v20220701:DefaultAdminRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DefaultAdminRule':
        """
        Get an existing DefaultAdminRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DefaultAdminRuleArgs.__new__(DefaultAdminRuleArgs)
        __props__.__dict__['access'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['destination_port_ranges'] = None
        __props__.__dict__['destinations'] = None
        __props__.__dict__['direction'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['flag'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['priority'] = None
        __props__.__dict__['protocol'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['source_port_ranges'] = None
        __props__.__dict__['sources'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return DefaultAdminRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Output[str]:
        """
        Indicates the access allowed for this particular rule
        """
        return pulumi.get(self, 'access')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        A description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='destinationPortRanges')
    def destination_port_ranges(self) -> pulumi.Output[Sequence[str]]:
        """
        The destination port ranges.
        """
        return pulumi.get(self, 'destination_port_ranges')

    @property
    @pulumi.getter
    def destinations(self) -> pulumi.Output[Sequence['outputs.AddressPrefixItemResponse']]:
        """
        The destination address prefixes. CIDR or destination IP ranges.
        """
        return pulumi.get(self, 'destinations')

    @property
    @pulumi.getter
    def direction(self) -> pulumi.Output[str]:
        """
        Indicates if the traffic matched against the rule in inbound or outbound.
        """
        return pulumi.get(self, 'direction')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def flag(self) -> pulumi.Output[Optional[str]]:
        """
        Default rule flag.
        """
        return pulumi.get(self, 'flag')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Whether the rule is custom or default.
        Expected value is 'Default'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[int]:
        """
        The priority of the rule. The value can be between 1 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        """
        return pulumi.get(self, 'priority')

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        Network protocol this rule applies to.
        """
        return pulumi.get(self, 'protocol')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='sourcePortRanges')
    def source_port_ranges(self) -> pulumi.Output[Sequence[str]]:
        """
        The source port ranges.
        """
        return pulumi.get(self, 'source_port_ranges')

    @property
    @pulumi.getter
    def sources(self) -> pulumi.Output[Sequence['outputs.AddressPrefixItemResponse']]:
        """
        The CIDR or source IP ranges.
        """
        return pulumi.get(self, 'sources')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
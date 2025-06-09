import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['AzureFirewallArgs', 'AzureFirewall']

@pulumi.input_type
class AzureFirewallArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], application_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallApplicationRuleCollectionArgs']]]]=None, azure_firewall_name: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallIPConfigurationArgs']]]]=None, location: Optional[pulumi.Input[str]]=None, nat_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNatRuleCollectionArgs']]]]=None, network_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNetworkRuleCollectionArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a AzureFirewall resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input['AzureFirewallApplicationRuleCollectionArgs']]] application_rule_collections: Collection of application rule collections used by Azure Firewall.
        :param pulumi.Input[str] azure_firewall_name: The name of the Azure Firewall.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['AzureFirewallIPConfigurationArgs']]] ip_configurations: IP configuration of the Azure Firewall resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input['AzureFirewallNatRuleCollectionArgs']]] nat_rule_collections: Collection of NAT rule collections used by Azure Firewall.
        :param pulumi.Input[Sequence[pulumi.Input['AzureFirewallNetworkRuleCollectionArgs']]] network_rule_collections: Collection of network rule collections used by Azure Firewall.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if application_rule_collections is not None:
            pulumi.set(__self__, 'application_rule_collections', application_rule_collections)
        if azure_firewall_name is not None:
            pulumi.set(__self__, 'azure_firewall_name', azure_firewall_name)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if ip_configurations is not None:
            pulumi.set(__self__, 'ip_configurations', ip_configurations)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if nat_rule_collections is not None:
            pulumi.set(__self__, 'nat_rule_collections', nat_rule_collections)
        if network_rule_collections is not None:
            pulumi.set(__self__, 'network_rule_collections', network_rule_collections)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

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
    @pulumi.getter(name='applicationRuleCollections')
    def application_rule_collections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallApplicationRuleCollectionArgs']]]]:
        """
        Collection of application rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'application_rule_collections')

    @application_rule_collections.setter
    def application_rule_collections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallApplicationRuleCollectionArgs']]]]):
        pulumi.set(self, 'application_rule_collections', value)

    @property
    @pulumi.getter(name='azureFirewallName')
    def azure_firewall_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Azure Firewall.
        """
        return pulumi.get(self, 'azure_firewall_name')

    @azure_firewall_name.setter
    def azure_firewall_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'azure_firewall_name', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter(name='ipConfigurations')
    def ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallIPConfigurationArgs']]]]:
        """
        IP configuration of the Azure Firewall resource.
        """
        return pulumi.get(self, 'ip_configurations')

    @ip_configurations.setter
    def ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallIPConfigurationArgs']]]]):
        pulumi.set(self, 'ip_configurations', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='natRuleCollections')
    def nat_rule_collections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNatRuleCollectionArgs']]]]:
        """
        Collection of NAT rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'nat_rule_collections')

    @nat_rule_collections.setter
    def nat_rule_collections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNatRuleCollectionArgs']]]]):
        pulumi.set(self, 'nat_rule_collections', value)

    @property
    @pulumi.getter(name='networkRuleCollections')
    def network_rule_collections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNetworkRuleCollectionArgs']]]]:
        """
        Collection of network rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'network_rule_collections')

    @network_rule_collections.setter
    def network_rule_collections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFirewallNetworkRuleCollectionArgs']]]]):
        pulumi.set(self, 'network_rule_collections', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class AzureFirewall(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallApplicationRuleCollectionArgs']]]]]=None, azure_firewall_name: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallIPConfigurationArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, nat_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNatRuleCollectionArgs']]]]]=None, network_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNetworkRuleCollectionArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Azure Firewall resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallApplicationRuleCollectionArgs']]]] application_rule_collections: Collection of application rule collections used by Azure Firewall.
        :param pulumi.Input[str] azure_firewall_name: The name of the Azure Firewall.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallIPConfigurationArgs']]]] ip_configurations: IP configuration of the Azure Firewall resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNatRuleCollectionArgs']]]] nat_rule_collections: Collection of NAT rule collections used by Azure Firewall.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNetworkRuleCollectionArgs']]]] network_rule_collections: Collection of network rule collections used by Azure Firewall.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: AzureFirewallArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Azure Firewall resource

        :param str resource_name: The name of the resource.
        :param AzureFirewallArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(AzureFirewallArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallApplicationRuleCollectionArgs']]]]]=None, azure_firewall_name: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallIPConfigurationArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, nat_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNatRuleCollectionArgs']]]]]=None, network_rule_collections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFirewallNetworkRuleCollectionArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AzureFirewallArgs.__new__(AzureFirewallArgs)
            __props__.__dict__['application_rule_collections'] = application_rule_collections
            __props__.__dict__['azure_firewall_name'] = azure_firewall_name
            __props__.__dict__['id'] = id
            __props__.__dict__['ip_configurations'] = ip_configurations
            __props__.__dict__['location'] = location
            __props__.__dict__['nat_rule_collections'] = nat_rule_collections
            __props__.__dict__['network_rule_collections'] = network_rule_collections
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20180401:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20180601:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20180701:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20180801:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20181101:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20181201:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190201:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190401:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190601:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190701:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190801:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20190901:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20191101:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20191201:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200301:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200401:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200501:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200601:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200701:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20200801:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20201101:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20210201:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20210301:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20210501:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20210801:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20220101:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20220501:AzureFirewall'), pulumi.Alias(type_='azure-native:network/v20220701:AzureFirewall')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AzureFirewall, __self__).__init__('azure-native:network/v20181001:AzureFirewall', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'AzureFirewall':
        """
        Get an existing AzureFirewall resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = AzureFirewallArgs.__new__(AzureFirewallArgs)
        __props__.__dict__['application_rule_collections'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['ip_configurations'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['nat_rule_collections'] = None
        __props__.__dict__['network_rule_collections'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return AzureFirewall(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='applicationRuleCollections')
    def application_rule_collections(self) -> pulumi.Output[Optional[Sequence['outputs.AzureFirewallApplicationRuleCollectionResponse']]]:
        """
        Collection of application rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'application_rule_collections')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='ipConfigurations')
    def ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.AzureFirewallIPConfigurationResponse']]]:
        """
        IP configuration of the Azure Firewall resource.
        """
        return pulumi.get(self, 'ip_configurations')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='natRuleCollections')
    def nat_rule_collections(self) -> pulumi.Output[Optional[Sequence['outputs.AzureFirewallNatRuleCollectionResponse']]]:
        """
        Collection of NAT rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'nat_rule_collections')

    @property
    @pulumi.getter(name='networkRuleCollections')
    def network_rule_collections(self) -> pulumi.Output[Optional[Sequence['outputs.AzureFirewallNetworkRuleCollectionResponse']]]:
        """
        Collection of network rule collections used by Azure Firewall.
        """
        return pulumi.get(self, 'network_rule_collections')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
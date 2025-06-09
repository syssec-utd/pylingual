import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['DdosProtectionPlanArgs', 'DdosProtectionPlan']

@pulumi.input_type
class DdosProtectionPlanArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], ddos_protection_plan_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a DdosProtectionPlan resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] ddos_protection_plan_name: The name of the DDoS protection plan.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if ddos_protection_plan_name is not None:
            pulumi.set(__self__, 'ddos_protection_plan_name', ddos_protection_plan_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
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
    @pulumi.getter(name='ddosProtectionPlanName')
    def ddos_protection_plan_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the DDoS protection plan.
        """
        return pulumi.get(self, 'ddos_protection_plan_name')

    @ddos_protection_plan_name.setter
    def ddos_protection_plan_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ddos_protection_plan_name', value)

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
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class DdosProtectionPlan(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, ddos_protection_plan_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        A DDoS protection plan in a resource group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ddos_protection_plan_name: The name of the DDoS protection plan.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DdosProtectionPlanArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A DDoS protection plan in a resource group.

        :param str resource_name: The name of the resource.
        :param DdosProtectionPlanArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(DdosProtectionPlanArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, ddos_protection_plan_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DdosProtectionPlanArgs.__new__(DdosProtectionPlanArgs)
            __props__.__dict__['ddos_protection_plan_name'] = ddos_protection_plan_name
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['resource_guid'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['virtual_networks'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20180201:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20180401:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20180601:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20180701:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20180801:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20181001:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20181101:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20181201:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190201:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190401:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190601:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190701:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190801:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20190901:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20191101:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20191201:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20200301:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20200401:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20200601:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20200701:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20200801:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20201101:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20210201:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20210301:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20210501:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20210801:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20220101:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20220501:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20220701:DdosProtectionPlan'), pulumi.Alias(type_='azure-native:network/v20220901:DdosProtectionPlan')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DdosProtectionPlan, __self__).__init__('azure-native:network/v20200501:DdosProtectionPlan', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DdosProtectionPlan':
        """
        Get an existing DdosProtectionPlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DdosProtectionPlanArgs.__new__(DdosProtectionPlanArgs)
        __props__.__dict__['etag'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['resource_guid'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['virtual_networks'] = None
        return DdosProtectionPlan(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

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
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the DDoS protection plan resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the DDoS protection plan resource. It uniquely identifies the resource, even if the user changes its name or migrate the resource across subscriptions or resource groups.
        """
        return pulumi.get(self, 'resource_guid')

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

    @property
    @pulumi.getter(name='virtualNetworks')
    def virtual_networks(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        The list of virtual networks associated with the DDoS protection plan resource. This list is read-only.
        """
        return pulumi.get(self, 'virtual_networks')
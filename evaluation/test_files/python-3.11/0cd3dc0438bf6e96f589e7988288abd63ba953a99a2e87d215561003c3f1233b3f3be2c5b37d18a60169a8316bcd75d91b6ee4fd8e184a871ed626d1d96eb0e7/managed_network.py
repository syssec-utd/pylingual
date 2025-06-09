import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['ManagedNetworkArgs', 'ManagedNetwork']

@pulumi.input_type
class ManagedNetworkArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], location: Optional[pulumi.Input[str]]=None, managed_network_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input['ScopeArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ManagedNetwork resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_network_name: The name of the Managed Network.
        :param pulumi.Input['ScopeArgs'] scope: The collection of management groups, subscriptions, virtual networks, and subnets by the Managed Network. This is a read-only property that is reflective of all ScopeAssignments for this Managed Network
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if managed_network_name is not None:
            pulumi.set(__self__, 'managed_network_name', managed_network_name)
        if scope is not None:
            pulumi.set(__self__, 'scope', scope)
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
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='managedNetworkName')
    def managed_network_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Managed Network.
        """
        return pulumi.get(self, 'managed_network_name')

    @managed_network_name.setter
    def managed_network_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'managed_network_name', value)

    @property
    @pulumi.getter
    def scope(self) -> Optional[pulumi.Input['ScopeArgs']]:
        """
        The collection of management groups, subscriptions, virtual networks, and subnets by the Managed Network. This is a read-only property that is reflective of all ScopeAssignments for this Managed Network
        """
        return pulumi.get(self, 'scope')

    @scope.setter
    def scope(self, value: Optional[pulumi.Input['ScopeArgs']]):
        pulumi.set(self, 'scope', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class ManagedNetwork(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, location: Optional[pulumi.Input[str]]=None, managed_network_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[pulumi.InputType['ScopeArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        The Managed Network resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] managed_network_name: The name of the Managed Network.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['ScopeArgs']] scope: The collection of management groups, subscriptions, virtual networks, and subnets by the Managed Network. This is a read-only property that is reflective of all ScopeAssignments for this Managed Network
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ManagedNetworkArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The Managed Network resource
        API Version: 2019-06-01-preview.

        :param str resource_name: The name of the resource.
        :param ManagedNetworkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedNetworkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, location: Optional[pulumi.Input[str]]=None, managed_network_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[pulumi.InputType['ScopeArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedNetworkArgs.__new__(ManagedNetworkArgs)
            __props__.__dict__['location'] = location
            __props__.__dict__['managed_network_name'] = managed_network_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['scope'] = scope
            __props__.__dict__['tags'] = tags
            __props__.__dict__['connectivity'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:managednetwork/v20190601preview:ManagedNetwork')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedNetwork, __self__).__init__('azure-native:managednetwork:ManagedNetwork', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ManagedNetwork':
        """
        Get an existing ManagedNetwork resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ManagedNetworkArgs.__new__(ManagedNetworkArgs)
        __props__.__dict__['connectivity'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['scope'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return ManagedNetwork(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def connectivity(self) -> pulumi.Output['outputs.ConnectivityCollectionResponse']:
        """
        The collection of groups and policies concerned with connectivity
        """
        return pulumi.get(self, 'connectivity')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the ManagedNetwork resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Optional['outputs.ScopeResponse']]:
        """
        The collection of management groups, subscriptions, virtual networks, and subnets by the Managed Network. This is a read-only property that is reflective of all ScopeAssignments for this Managed Network
        """
        return pulumi.get(self, 'scope')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, 'type')
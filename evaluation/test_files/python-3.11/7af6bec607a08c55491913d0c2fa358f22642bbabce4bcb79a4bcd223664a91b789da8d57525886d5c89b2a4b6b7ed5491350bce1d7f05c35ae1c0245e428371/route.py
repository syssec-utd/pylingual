import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['RouteInitArgs', 'Route']

@pulumi.input_type
class RouteInitArgs:

    def __init__(__self__, *, next_hop_type: pulumi.Input[Union[str, 'RouteNextHopType']], resource_group_name: pulumi.Input[str], route_table_name: pulumi.Input[str], address_prefix: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, next_hop_ip_address: Optional[pulumi.Input[str]]=None, provisioning_state: Optional[pulumi.Input[str]]=None, route_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Route resource.
        :param pulumi.Input[Union[str, 'RouteNextHopType']] next_hop_type: The type of Azure hop the packet should be sent to. Possible values are: 'VirtualNetworkGateway', 'VnetLocal', 'Internet', 'VirtualAppliance', and 'None'
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] route_table_name: The name of the route table.
        :param pulumi.Input[str] address_prefix: The destination CIDR to which the route applies.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] next_hop_ip_address: The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
        :param pulumi.Input[str] provisioning_state: The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        :param pulumi.Input[str] route_name: The name of the route.
        """
        pulumi.set(__self__, 'next_hop_type', next_hop_type)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'route_table_name', route_table_name)
        if address_prefix is not None:
            pulumi.set(__self__, 'address_prefix', address_prefix)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if next_hop_ip_address is not None:
            pulumi.set(__self__, 'next_hop_ip_address', next_hop_ip_address)
        if provisioning_state is not None:
            pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if route_name is not None:
            pulumi.set(__self__, 'route_name', route_name)

    @property
    @pulumi.getter(name='nextHopType')
    def next_hop_type(self) -> pulumi.Input[Union[str, 'RouteNextHopType']]:
        """
        The type of Azure hop the packet should be sent to. Possible values are: 'VirtualNetworkGateway', 'VnetLocal', 'Internet', 'VirtualAppliance', and 'None'
        """
        return pulumi.get(self, 'next_hop_type')

    @next_hop_type.setter
    def next_hop_type(self, value: pulumi.Input[Union[str, 'RouteNextHopType']]):
        pulumi.set(self, 'next_hop_type', value)

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
    @pulumi.getter(name='routeTableName')
    def route_table_name(self) -> pulumi.Input[str]:
        """
        The name of the route table.
        """
        return pulumi.get(self, 'route_table_name')

    @route_table_name.setter
    def route_table_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'route_table_name', value)

    @property
    @pulumi.getter(name='addressPrefix')
    def address_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The destination CIDR to which the route applies.
        """
        return pulumi.get(self, 'address_prefix')

    @address_prefix.setter
    def address_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'address_prefix', value)

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
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='nextHopIpAddress')
    def next_hop_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
        """
        return pulumi.get(self, 'next_hop_ip_address')

    @next_hop_ip_address.setter
    def next_hop_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'next_hop_ip_address', value)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, 'provisioning_state')

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'provisioning_state', value)

    @property
    @pulumi.getter(name='routeName')
    def route_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the route.
        """
        return pulumi.get(self, 'route_name')

    @route_name.setter
    def route_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'route_name', value)
warnings.warn('Version 2016-12-01 will be removed in v2 of the provider.', DeprecationWarning)

class Route(pulumi.CustomResource):
    warnings.warn('Version 2016-12-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, address_prefix: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, next_hop_ip_address: Optional[pulumi.Input[str]]=None, next_hop_type: Optional[pulumi.Input[Union[str, 'RouteNextHopType']]]=None, provisioning_state: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, route_name: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Route resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_prefix: The destination CIDR to which the route applies.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] next_hop_ip_address: The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
        :param pulumi.Input[Union[str, 'RouteNextHopType']] next_hop_type: The type of Azure hop the packet should be sent to. Possible values are: 'VirtualNetworkGateway', 'VnetLocal', 'Internet', 'VirtualAppliance', and 'None'
        :param pulumi.Input[str] provisioning_state: The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] route_name: The name of the route.
        :param pulumi.Input[str] route_table_name: The name of the route table.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: RouteInitArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Route resource

        :param str resource_name: The name of the resource.
        :param RouteInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouteInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, address_prefix: Optional[pulumi.Input[str]]=None, id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, next_hop_ip_address: Optional[pulumi.Input[str]]=None, next_hop_type: Optional[pulumi.Input[Union[str, 'RouteNextHopType']]]=None, provisioning_state: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, route_name: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, __props__=None):
        pulumi.log.warn('Route is deprecated: Version 2016-12-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouteInitArgs.__new__(RouteInitArgs)
            __props__.__dict__['address_prefix'] = address_prefix
            __props__.__dict__['id'] = id
            __props__.__dict__['name'] = name
            __props__.__dict__['next_hop_ip_address'] = next_hop_ip_address
            if next_hop_type is None and (not opts.urn):
                raise TypeError("Missing required property 'next_hop_type'")
            __props__.__dict__['next_hop_type'] = next_hop_type
            __props__.__dict__['provisioning_state'] = provisioning_state
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['route_name'] = route_name
            if route_table_name is None and (not opts.urn):
                raise TypeError("Missing required property 'route_table_name'")
            __props__.__dict__['route_table_name'] = route_table_name
            __props__.__dict__['etag'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network:Route'), pulumi.Alias(type_='azure-native:network/v20150501preview:Route'), pulumi.Alias(type_='azure-native:network/v20150615:Route'), pulumi.Alias(type_='azure-native:network/v20160330:Route'), pulumi.Alias(type_='azure-native:network/v20160601:Route'), pulumi.Alias(type_='azure-native:network/v20160901:Route'), pulumi.Alias(type_='azure-native:network/v20170301:Route'), pulumi.Alias(type_='azure-native:network/v20170601:Route'), pulumi.Alias(type_='azure-native:network/v20170801:Route'), pulumi.Alias(type_='azure-native:network/v20170901:Route'), pulumi.Alias(type_='azure-native:network/v20171001:Route'), pulumi.Alias(type_='azure-native:network/v20171101:Route'), pulumi.Alias(type_='azure-native:network/v20180101:Route'), pulumi.Alias(type_='azure-native:network/v20180201:Route'), pulumi.Alias(type_='azure-native:network/v20180401:Route'), pulumi.Alias(type_='azure-native:network/v20180601:Route'), pulumi.Alias(type_='azure-native:network/v20180701:Route'), pulumi.Alias(type_='azure-native:network/v20180801:Route'), pulumi.Alias(type_='azure-native:network/v20181001:Route'), pulumi.Alias(type_='azure-native:network/v20181101:Route'), pulumi.Alias(type_='azure-native:network/v20181201:Route'), pulumi.Alias(type_='azure-native:network/v20190201:Route'), pulumi.Alias(type_='azure-native:network/v20190401:Route'), pulumi.Alias(type_='azure-native:network/v20190601:Route'), pulumi.Alias(type_='azure-native:network/v20190701:Route'), pulumi.Alias(type_='azure-native:network/v20190801:Route'), pulumi.Alias(type_='azure-native:network/v20190901:Route'), pulumi.Alias(type_='azure-native:network/v20191101:Route'), pulumi.Alias(type_='azure-native:network/v20191201:Route'), pulumi.Alias(type_='azure-native:network/v20200301:Route'), pulumi.Alias(type_='azure-native:network/v20200401:Route'), pulumi.Alias(type_='azure-native:network/v20200501:Route'), pulumi.Alias(type_='azure-native:network/v20200601:Route'), pulumi.Alias(type_='azure-native:network/v20200701:Route'), pulumi.Alias(type_='azure-native:network/v20200801:Route'), pulumi.Alias(type_='azure-native:network/v20201101:Route'), pulumi.Alias(type_='azure-native:network/v20210201:Route'), pulumi.Alias(type_='azure-native:network/v20210301:Route'), pulumi.Alias(type_='azure-native:network/v20210501:Route'), pulumi.Alias(type_='azure-native:network/v20210801:Route'), pulumi.Alias(type_='azure-native:network/v20220101:Route'), pulumi.Alias(type_='azure-native:network/v20220501:Route'), pulumi.Alias(type_='azure-native:network/v20220701:Route')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Route, __self__).__init__('azure-native:network/v20161201:Route', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Route':
        """
        Get an existing Route resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = RouteInitArgs.__new__(RouteInitArgs)
        __props__.__dict__['address_prefix'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['next_hop_ip_address'] = None
        __props__.__dict__['next_hop_type'] = None
        __props__.__dict__['provisioning_state'] = None
        return Route(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='addressPrefix')
    def address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The destination CIDR to which the route applies.
        """
        return pulumi.get(self, 'address_prefix')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='nextHopIpAddress')
    def next_hop_ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
        """
        return pulumi.get(self, 'next_hop_ip_address')

    @property
    @pulumi.getter(name='nextHopType')
    def next_hop_type(self) -> pulumi.Output[str]:
        """
        The type of Azure hop the packet should be sent to. Possible values are: 'VirtualNetworkGateway', 'VnetLocal', 'Internet', 'VirtualAppliance', and 'None'
        """
        return pulumi.get(self, 'next_hop_type')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, 'provisioning_state')
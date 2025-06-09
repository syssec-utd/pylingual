import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['RouteTableInitArgs', 'RouteTable']

@pulumi.input_type
class RouteTableInitArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], disable_bgp_route_propagation: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, routes: Optional[pulumi.Input[Sequence[pulumi.Input['RouteArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a RouteTable resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[bool] disable_bgp_route_propagation: Whether to disable the routes learned by BGP on that route table. True means disable.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] route_table_name: The name of the route table.
        :param pulumi.Input[Sequence[pulumi.Input['RouteArgs']]] routes: Collection of routes contained within a route table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if disable_bgp_route_propagation is not None:
            pulumi.set(__self__, 'disable_bgp_route_propagation', disable_bgp_route_propagation)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if route_table_name is not None:
            pulumi.set(__self__, 'route_table_name', route_table_name)
        if routes is not None:
            pulumi.set(__self__, 'routes', routes)
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
    @pulumi.getter(name='disableBgpRoutePropagation')
    def disable_bgp_route_propagation(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to disable the routes learned by BGP on that route table. True means disable.
        """
        return pulumi.get(self, 'disable_bgp_route_propagation')

    @disable_bgp_route_propagation.setter
    def disable_bgp_route_propagation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'disable_bgp_route_propagation', value)

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
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='routeTableName')
    def route_table_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the route table.
        """
        return pulumi.get(self, 'route_table_name')

    @route_table_name.setter
    def route_table_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'route_table_name', value)

    @property
    @pulumi.getter
    def routes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RouteArgs']]]]:
        """
        Collection of routes contained within a route table.
        """
        return pulumi.get(self, 'routes')

    @routes.setter
    def routes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RouteArgs']]]]):
        pulumi.set(self, 'routes', value)

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

class RouteTable(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, disable_bgp_route_propagation: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, routes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RouteArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Route table resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] disable_bgp_route_propagation: Whether to disable the routes learned by BGP on that route table. True means disable.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] route_table_name: The name of the route table.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RouteArgs']]]] routes: Collection of routes contained within a route table.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: RouteTableInitArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Route table resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param RouteTableInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(RouteTableInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, disable_bgp_route_propagation: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, routes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RouteArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouteTableInitArgs.__new__(RouteTableInitArgs)
            __props__.__dict__['disable_bgp_route_propagation'] = disable_bgp_route_propagation
            __props__.__dict__['id'] = id
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['route_table_name'] = route_table_name
            __props__.__dict__['routes'] = routes
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['resource_guid'] = None
            __props__.__dict__['subnets'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network/v20150501preview:RouteTable'), pulumi.Alias(type_='azure-native:network/v20150615:RouteTable'), pulumi.Alias(type_='azure-native:network/v20160330:RouteTable'), pulumi.Alias(type_='azure-native:network/v20160601:RouteTable'), pulumi.Alias(type_='azure-native:network/v20160901:RouteTable'), pulumi.Alias(type_='azure-native:network/v20161201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20170301:RouteTable'), pulumi.Alias(type_='azure-native:network/v20170601:RouteTable'), pulumi.Alias(type_='azure-native:network/v20170801:RouteTable'), pulumi.Alias(type_='azure-native:network/v20170901:RouteTable'), pulumi.Alias(type_='azure-native:network/v20171001:RouteTable'), pulumi.Alias(type_='azure-native:network/v20171101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180401:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180601:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180701:RouteTable'), pulumi.Alias(type_='azure-native:network/v20180801:RouteTable'), pulumi.Alias(type_='azure-native:network/v20181001:RouteTable'), pulumi.Alias(type_='azure-native:network/v20181101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20181201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190401:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190601:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190701:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190801:RouteTable'), pulumi.Alias(type_='azure-native:network/v20190901:RouteTable'), pulumi.Alias(type_='azure-native:network/v20191101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20191201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200301:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200401:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200501:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200601:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200701:RouteTable'), pulumi.Alias(type_='azure-native:network/v20200801:RouteTable'), pulumi.Alias(type_='azure-native:network/v20201101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20210201:RouteTable'), pulumi.Alias(type_='azure-native:network/v20210301:RouteTable'), pulumi.Alias(type_='azure-native:network/v20210501:RouteTable'), pulumi.Alias(type_='azure-native:network/v20210801:RouteTable'), pulumi.Alias(type_='azure-native:network/v20220101:RouteTable'), pulumi.Alias(type_='azure-native:network/v20220501:RouteTable'), pulumi.Alias(type_='azure-native:network/v20220701:RouteTable'), pulumi.Alias(type_='azure-native:network/v20220901:RouteTable')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RouteTable, __self__).__init__('azure-native:network:RouteTable', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'RouteTable':
        """
        Get an existing RouteTable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = RouteTableInitArgs.__new__(RouteTableInitArgs)
        __props__.__dict__['disable_bgp_route_propagation'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['resource_guid'] = None
        __props__.__dict__['routes'] = None
        __props__.__dict__['subnets'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return RouteTable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='disableBgpRoutePropagation')
    def disable_bgp_route_propagation(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to disable the routes learned by BGP on that route table. True means disable.
        """
        return pulumi.get(self, 'disable_bgp_route_propagation')

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
        The provisioning state of the route table resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the route table.
        """
        return pulumi.get(self, 'resource_guid')

    @property
    @pulumi.getter
    def routes(self) -> pulumi.Output[Optional[Sequence['outputs.RouteResponse']]]:
        """
        Collection of routes contained within a route table.
        """
        return pulumi.get(self, 'routes')

    @property
    @pulumi.getter
    def subnets(self) -> pulumi.Output[Sequence['outputs.SubnetResponse']]:
        """
        A collection of references to subnets.
        """
        return pulumi.get(self, 'subnets')

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
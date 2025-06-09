import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['GraphResourceGraphArgs', 'GraphResourceGraph']

@pulumi.input_type
class GraphResourceGraphArgs:

    def __init__(__self__, *, account_name: pulumi.Input[str], resource: pulumi.Input['GraphResourceArgs'], resource_group_name: pulumi.Input[str], graph_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input['CreateUpdateOptionsArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a GraphResourceGraph resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input['GraphResourceArgs'] resource: The standard JSON format of a Graph resource
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] graph_name: Cosmos DB graph resource name.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: Identity for the resource.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input['CreateUpdateOptionsArgs'] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        pulumi.set(__self__, 'account_name', account_name)
        pulumi.set(__self__, 'resource', resource)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if graph_name is not None:
            pulumi.set(__self__, 'graph_name', graph_name)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if options is not None:
            pulumi.set(__self__, 'options', options)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='accountName')
    def account_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB database account name.
        """
        return pulumi.get(self, 'account_name')

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'account_name', value)

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Input['GraphResourceArgs']:
        """
        The standard JSON format of a Graph resource
        """
        return pulumi.get(self, 'resource')

    @resource.setter
    def resource(self, value: pulumi.Input['GraphResourceArgs']):
        pulumi.set(self, 'resource', value)

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
    @pulumi.getter(name='graphName')
    def graph_name(self) -> Optional[pulumi.Input[str]]:
        """
        Cosmos DB graph resource name.
        """
        return pulumi.get(self, 'graph_name')

    @graph_name.setter
    def graph_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'graph_name', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def options(self) -> Optional[pulumi.Input['CreateUpdateOptionsArgs']]:
        """
        A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        """
        return pulumi.get(self, 'options')

    @options.setter
    def options(self, value: Optional[pulumi.Input['CreateUpdateOptionsArgs']]):
        pulumi.set(self, 'options', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class GraphResourceGraph(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, graph_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']]]=None, resource: Optional[pulumi.Input[pulumi.InputType['GraphResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        An Azure Cosmos DB Graph resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] graph_name: Cosmos DB graph resource name.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: Identity for the resource.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input[pulumi.InputType['GraphResourceArgs']] resource: The standard JSON format of a Graph resource
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: GraphResourceGraphArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        An Azure Cosmos DB Graph resource.

        :param str resource_name: The name of the resource.
        :param GraphResourceGraphArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(GraphResourceGraphArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, graph_name: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']]]=None, resource: Optional[pulumi.Input[pulumi.InputType['GraphResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GraphResourceGraphArgs.__new__(GraphResourceGraphArgs)
            if account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__['account_name'] = account_name
            __props__.__dict__['graph_name'] = graph_name
            __props__.__dict__['identity'] = identity
            __props__.__dict__['location'] = location
            __props__.__dict__['options'] = options
            if resource is None and (not opts.urn):
                raise TypeError("Missing required property 'resource'")
            __props__.__dict__['resource'] = resource
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:documentdb:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20210701preview:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20211015preview:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20211115preview:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20220215preview:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20220815preview:GraphResourceGraph'), pulumi.Alias(type_='azure-native:documentdb/v20221115preview:GraphResourceGraph')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GraphResourceGraph, __self__).__init__('azure-native:documentdb/v20220515preview:GraphResourceGraph', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'GraphResourceGraph':
        """
        Get an existing GraphResourceGraph resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = GraphResourceGraphArgs.__new__(GraphResourceGraphArgs)
        __props__.__dict__['identity'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['options'] = None
        __props__.__dict__['resource'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return GraphResourceGraph(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        Identity for the resource.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the ARM resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def options(self) -> pulumi.Output[Optional['outputs.GraphResourceGetPropertiesResponseOptions']]:
        return pulumi.get(self, 'options')

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Output[Optional['outputs.GraphResourceGetPropertiesResponseResource']]:
        return pulumi.get(self, 'resource')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, 'type')
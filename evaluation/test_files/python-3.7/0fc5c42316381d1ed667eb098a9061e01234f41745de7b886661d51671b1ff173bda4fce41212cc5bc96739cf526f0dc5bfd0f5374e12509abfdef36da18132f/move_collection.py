import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['MoveCollectionArgs', 'MoveCollection']

@pulumi.input_type
class MoveCollectionArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], identity: Optional[pulumi.Input['IdentityArgs']]=None, location: Optional[pulumi.Input[str]]=None, move_collection_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input['MoveCollectionPropertiesArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a MoveCollection resource.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param pulumi.Input['IdentityArgs'] identity: Defines the MSI properties of the Move Collection.
        :param pulumi.Input[str] location: The geo-location where the resource lives.
        :param pulumi.Input[str] move_collection_name: The Move Collection Name.
        :param pulumi.Input['MoveCollectionPropertiesArgs'] properties: Defines the move collection properties.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if move_collection_name is not None:
            pulumi.set(__self__, 'move_collection_name', move_collection_name)
        if properties is not None:
            pulumi.set(__self__, 'properties', properties)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The Resource Group Name.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityArgs']]:
        """
        Defines the MSI properties of the Move Collection.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='moveCollectionName')
    def move_collection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Move Collection Name.
        """
        return pulumi.get(self, 'move_collection_name')

    @move_collection_name.setter
    def move_collection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'move_collection_name', value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['MoveCollectionPropertiesArgs']]:
        """
        Defines the move collection properties.
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['MoveCollectionPropertiesArgs']]):
        pulumi.set(self, 'properties', value)

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

class MoveCollection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, move_collection_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['MoveCollectionPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Define the move collection.
        API Version: 2021-01-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: Defines the MSI properties of the Move Collection.
        :param pulumi.Input[str] location: The geo-location where the resource lives.
        :param pulumi.Input[str] move_collection_name: The Move Collection Name.
        :param pulumi.Input[pulumi.InputType['MoveCollectionPropertiesArgs']] properties: Defines the move collection properties.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: MoveCollectionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Define the move collection.
        API Version: 2021-01-01.

        :param str resource_name: The name of the resource.
        :param MoveCollectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(MoveCollectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, move_collection_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['MoveCollectionPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MoveCollectionArgs.__new__(MoveCollectionArgs)
            __props__.__dict__['identity'] = identity
            __props__.__dict__['location'] = location
            __props__.__dict__['move_collection_name'] = move_collection_name
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:migrate/v20191001preview:MoveCollection'), pulumi.Alias(type_='azure-native:migrate/v20210101:MoveCollection'), pulumi.Alias(type_='azure-native:migrate/v20210801:MoveCollection')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MoveCollection, __self__).__init__('azure-native:migrate:MoveCollection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'MoveCollection':
        """
        Get an existing MoveCollection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = MoveCollectionArgs.__new__(MoveCollectionArgs)
        __props__.__dict__['etag'] = None
        __props__.__dict__['identity'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return MoveCollection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The etag of the resource.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        Defines the MSI properties of the Move Collection.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The geo-location where the resource lives.
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
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.MoveCollectionPropertiesResponse']:
        """
        Defines the move collection properties.
        """
        return pulumi.get(self, 'properties')

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
        The type of the resource.
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['SqlManagedInstanceArgs', 'SqlManagedInstance']

@pulumi.input_type
class SqlManagedInstanceArgs:

    def __init__(__self__, *, properties: pulumi.Input['SqlManagedInstancePropertiesArgs'], resource_group_name: pulumi.Input[str], extended_location: Optional[pulumi.Input['ExtendedLocationArgs']]=None, location: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input['SqlManagedInstanceSkuArgs']]=None, sql_managed_instance_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a SqlManagedInstance resource.
        :param pulumi.Input['SqlManagedInstancePropertiesArgs'] properties: null
        :param pulumi.Input[str] resource_group_name: The name of the Azure resource group
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: The extendedLocation of the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input['SqlManagedInstanceSkuArgs'] sku: Resource sku.
        :param pulumi.Input[str] sql_managed_instance_name: The name of SQL Managed Instances
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, 'properties', properties)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if extended_location is not None:
            pulumi.set(__self__, 'extended_location', extended_location)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if sql_managed_instance_name is not None:
            pulumi.set(__self__, 'sql_managed_instance_name', sql_managed_instance_name)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['SqlManagedInstancePropertiesArgs']:
        """
        null
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: pulumi.Input['SqlManagedInstancePropertiesArgs']):
        pulumi.set(self, 'properties', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Azure resource group
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> Optional[pulumi.Input['ExtendedLocationArgs']]:
        """
        The extendedLocation of the resource.
        """
        return pulumi.get(self, 'extended_location')

    @extended_location.setter
    def extended_location(self, value: Optional[pulumi.Input['ExtendedLocationArgs']]):
        pulumi.set(self, 'extended_location', value)

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
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SqlManagedInstanceSkuArgs']]:
        """
        Resource sku.
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SqlManagedInstanceSkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter(name='sqlManagedInstanceName')
    def sql_managed_instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of SQL Managed Instances
        """
        return pulumi.get(self, 'sql_managed_instance_name')

    @sql_managed_instance_name.setter
    def sql_managed_instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sql_managed_instance_name', value)

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

class SqlManagedInstance(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]]=None, location: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['SqlManagedInstancePropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SqlManagedInstanceSkuArgs']]]=None, sql_managed_instance_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        A SqlManagedInstance.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: The extendedLocation of the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[pulumi.InputType['SqlManagedInstancePropertiesArgs']] properties: null
        :param pulumi.Input[str] resource_group_name: The name of the Azure resource group
        :param pulumi.Input[pulumi.InputType['SqlManagedInstanceSkuArgs']] sku: Resource sku.
        :param pulumi.Input[str] sql_managed_instance_name: The name of SQL Managed Instances
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: SqlManagedInstanceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A SqlManagedInstance.

        :param str resource_name: The name of the resource.
        :param SqlManagedInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlManagedInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]]=None, location: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['SqlManagedInstancePropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SqlManagedInstanceSkuArgs']]]=None, sql_managed_instance_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SqlManagedInstanceArgs.__new__(SqlManagedInstanceArgs)
            __props__.__dict__['extended_location'] = extended_location
            __props__.__dict__['location'] = location
            if properties is None and (not opts.urn):
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['sql_managed_instance_name'] = sql_managed_instance_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:azurearcdata:SqlManagedInstance'), pulumi.Alias(type_='azure-native:azurearcdata/v20210701preview:SqlManagedInstance'), pulumi.Alias(type_='azure-native:azurearcdata/v20210801:SqlManagedInstance'), pulumi.Alias(type_='azure-native:azurearcdata/v20211101:SqlManagedInstance'), pulumi.Alias(type_='azure-native:azurearcdata/v20220301preview:SqlManagedInstance'), pulumi.Alias(type_='azure-native:azurearcdata/v20220615preview:SqlManagedInstance')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlManagedInstance, __self__).__init__('azure-native:azurearcdata/v20210601preview:SqlManagedInstance', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'SqlManagedInstance':
        """
        Get an existing SqlManagedInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = SqlManagedInstanceArgs.__new__(SqlManagedInstanceArgs)
        __props__.__dict__['extended_location'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return SqlManagedInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> pulumi.Output[Optional['outputs.ExtendedLocationResponse']]:
        """
        The extendedLocation of the resource.
        """
        return pulumi.get(self, 'extended_location')

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
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.SqlManagedInstancePropertiesResponse']:
        """
        null
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SqlManagedInstanceSkuResponse']]:
        """
        Resource sku.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Read only system data
        """
        return pulumi.get(self, 'system_data')

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
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, 'type')
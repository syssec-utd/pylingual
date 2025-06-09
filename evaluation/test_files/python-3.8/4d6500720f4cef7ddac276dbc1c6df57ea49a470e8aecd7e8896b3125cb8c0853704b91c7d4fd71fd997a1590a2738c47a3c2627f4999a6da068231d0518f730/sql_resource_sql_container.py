import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['SqlResourceSqlContainerArgs', 'SqlResourceSqlContainer']

@pulumi.input_type
class SqlResourceSqlContainerArgs:

    def __init__(__self__, *, account_name: pulumi.Input[str], database_name: pulumi.Input[str], options: pulumi.Input['CreateUpdateOptionsArgs'], resource: pulumi.Input['SqlContainerResourceArgs'], resource_group_name: pulumi.Input[str], container_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a SqlResourceSqlContainer resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] database_name: Cosmos DB database name.
        :param pulumi.Input['CreateUpdateOptionsArgs'] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input['SqlContainerResourceArgs'] resource: The standard JSON format of a container
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[str] container_name: Cosmos DB container name.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        pulumi.set(__self__, 'account_name', account_name)
        pulumi.set(__self__, 'database_name', database_name)
        pulumi.set(__self__, 'options', options)
        pulumi.set(__self__, 'resource', resource)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if container_name is not None:
            pulumi.set(__self__, 'container_name', container_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
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
    @pulumi.getter(name='databaseName')
    def database_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB database name.
        """
        return pulumi.get(self, 'database_name')

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'database_name', value)

    @property
    @pulumi.getter
    def options(self) -> pulumi.Input['CreateUpdateOptionsArgs']:
        """
        A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        """
        return pulumi.get(self, 'options')

    @options.setter
    def options(self, value: pulumi.Input['CreateUpdateOptionsArgs']):
        pulumi.set(self, 'options', value)

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Input['SqlContainerResourceArgs']:
        """
        The standard JSON format of a container
        """
        return pulumi.get(self, 'resource')

    @resource.setter
    def resource(self, value: pulumi.Input['SqlContainerResourceArgs']):
        pulumi.set(self, 'resource', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='containerName')
    def container_name(self) -> Optional[pulumi.Input[str]]:
        """
        Cosmos DB container name.
        """
        return pulumi.get(self, 'container_name')

    @container_name.setter
    def container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'container_name', value)

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
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)
warnings.warn('Version 2019-12-12 will be removed in v2 of the provider.', DeprecationWarning)

class SqlResourceSqlContainer(pulumi.CustomResource):
    warnings.warn('Version 2019-12-12 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, container_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']]]=None, resource: Optional[pulumi.Input[pulumi.InputType['SqlContainerResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        An Azure Cosmos DB container.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] container_name: Cosmos DB container name.
        :param pulumi.Input[str] database_name: Cosmos DB database name.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input[pulumi.InputType['SqlContainerResourceArgs']] resource: The standard JSON format of a container
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: SqlResourceSqlContainerArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        An Azure Cosmos DB container.

        :param str resource_name: The name of the resource.
        :param SqlResourceSqlContainerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(SqlResourceSqlContainerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, container_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, options: Optional[pulumi.Input[pulumi.InputType['CreateUpdateOptionsArgs']]]=None, resource: Optional[pulumi.Input[pulumi.InputType['SqlContainerResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        pulumi.log.warn('SqlResourceSqlContainer is deprecated: Version 2019-12-12 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SqlResourceSqlContainerArgs.__new__(SqlResourceSqlContainerArgs)
            if account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__['account_name'] = account_name
            __props__.__dict__['container_name'] = container_name
            if database_name is None and (not opts.urn):
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__['database_name'] = database_name
            __props__.__dict__['location'] = location
            if options is None and (not opts.urn):
                raise TypeError("Missing required property 'options'")
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
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:documentdb:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20150401:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20150408:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20151106:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20160319:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20160331:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20190801:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20200301:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20200401:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20200601preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20200901:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210115:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210301preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210315:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210401preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210415:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210515:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210615:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20210701preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20211015:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20211015preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20211115preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20220215preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20220515:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20220515preview:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20220815:SqlResourceSqlContainer'), pulumi.Alias(type_='azure-native:documentdb/v20220815preview:SqlResourceSqlContainer')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlResourceSqlContainer, __self__).__init__('azure-native:documentdb/v20191212:SqlResourceSqlContainer', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'SqlResourceSqlContainer':
        """
        Get an existing SqlResourceSqlContainer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = SqlResourceSqlContainerArgs.__new__(SqlResourceSqlContainerArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['resource'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return SqlResourceSqlContainer(resource_name, opts=opts, __props__=__props__)

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
    def resource(self) -> pulumi.Output[Optional['outputs.SqlContainerGetPropertiesResponseResource']]:
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
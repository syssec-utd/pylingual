import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *
__all__ = ['PoolArgs', 'Pool']

@pulumi.input_type
class PoolArgs:

    def __init__(__self__, *, account_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_level: pulumi.Input[Union[str, 'ServiceLevel']], size: pulumi.Input[float], location: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, qos_type: Optional[pulumi.Input[Union[str, 'QosType']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Pool resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ServiceLevel']] service_level: The service level of the file system
        :param pulumi.Input[float] size: Provisioned size of the pool (in bytes). Allowed values are in 4TiB chunks (value must be multiply of 4398046511104).
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[Union[str, 'QosType']] qos_type: The qos type of the pool
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, 'account_name', account_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if service_level is None:
            service_level = 'Premium'
        pulumi.set(__self__, 'service_level', service_level)
        pulumi.set(__self__, 'size', size)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if pool_name is not None:
            pulumi.set(__self__, 'pool_name', pool_name)
        if qos_type is None:
            qos_type = 'Auto'
        if qos_type is not None:
            pulumi.set(__self__, 'qos_type', qos_type)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='accountName')
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp account
        """
        return pulumi.get(self, 'account_name')

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'account_name', value)

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
    @pulumi.getter(name='serviceLevel')
    def service_level(self) -> pulumi.Input[Union[str, 'ServiceLevel']]:
        """
        The service level of the file system
        """
        return pulumi.get(self, 'service_level')

    @service_level.setter
    def service_level(self, value: pulumi.Input[Union[str, 'ServiceLevel']]):
        pulumi.set(self, 'service_level', value)

    @property
    @pulumi.getter
    def size(self) -> pulumi.Input[float]:
        """
        Provisioned size of the pool (in bytes). Allowed values are in 4TiB chunks (value must be multiply of 4398046511104).
        """
        return pulumi.get(self, 'size')

    @size.setter
    def size(self, value: pulumi.Input[float]):
        pulumi.set(self, 'size', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='poolName')
    def pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the capacity pool
        """
        return pulumi.get(self, 'pool_name')

    @pool_name.setter
    def pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'pool_name', value)

    @property
    @pulumi.getter(name='qosType')
    def qos_type(self) -> Optional[pulumi.Input[Union[str, 'QosType']]]:
        """
        The qos type of the pool
        """
        return pulumi.get(self, 'qos_type')

    @qos_type.setter
    def qos_type(self, value: Optional[pulumi.Input[Union[str, 'QosType']]]):
        pulumi.set(self, 'qos_type', value)

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

class Pool(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, qos_type: Optional[pulumi.Input[Union[str, 'QosType']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_level: Optional[pulumi.Input[Union[str, 'ServiceLevel']]]=None, size: Optional[pulumi.Input[float]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Capacity pool resource
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[Union[str, 'QosType']] qos_type: The qos type of the pool
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ServiceLevel']] service_level: The service level of the file system
        :param pulumi.Input[float] size: Provisioned size of the pool (in bytes). Allowed values are in 4TiB chunks (value must be multiply of 4398046511104).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PoolArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Capacity pool resource
        API Version: 2020-12-01.

        :param str resource_name: The name of the resource.
        :param PoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, qos_type: Optional[pulumi.Input[Union[str, 'QosType']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_level: Optional[pulumi.Input[Union[str, 'ServiceLevel']]]=None, size: Optional[pulumi.Input[float]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PoolArgs.__new__(PoolArgs)
            if account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__['account_name'] = account_name
            __props__.__dict__['location'] = location
            __props__.__dict__['pool_name'] = pool_name
            if qos_type is None:
                qos_type = 'Auto'
            __props__.__dict__['qos_type'] = qos_type
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_level is None:
                service_level = 'Premium'
            if service_level is None and (not opts.urn):
                raise TypeError("Missing required property 'service_level'")
            __props__.__dict__['service_level'] = service_level
            if size is None and (not opts.urn):
                raise TypeError("Missing required property 'size'")
            __props__.__dict__['size'] = size
            __props__.__dict__['tags'] = tags
            __props__.__dict__['name'] = None
            __props__.__dict__['pool_id'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['total_throughput_mibps'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['utilized_throughput_mibps'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:netapp/v20170815:Pool'), pulumi.Alias(type_='azure-native:netapp/v20190501:Pool'), pulumi.Alias(type_='azure-native:netapp/v20190601:Pool'), pulumi.Alias(type_='azure-native:netapp/v20190701:Pool'), pulumi.Alias(type_='azure-native:netapp/v20190801:Pool'), pulumi.Alias(type_='azure-native:netapp/v20191001:Pool'), pulumi.Alias(type_='azure-native:netapp/v20191101:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200201:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200301:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200501:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200601:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200701:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200801:Pool'), pulumi.Alias(type_='azure-native:netapp/v20200901:Pool'), pulumi.Alias(type_='azure-native:netapp/v20201101:Pool'), pulumi.Alias(type_='azure-native:netapp/v20201201:Pool'), pulumi.Alias(type_='azure-native:netapp/v20210201:Pool'), pulumi.Alias(type_='azure-native:netapp/v20210401:Pool'), pulumi.Alias(type_='azure-native:netapp/v20210401preview:Pool'), pulumi.Alias(type_='azure-native:netapp/v20210601:Pool'), pulumi.Alias(type_='azure-native:netapp/v20210801:Pool'), pulumi.Alias(type_='azure-native:netapp/v20211001:Pool'), pulumi.Alias(type_='azure-native:netapp/v20220101:Pool'), pulumi.Alias(type_='azure-native:netapp/v20220301:Pool'), pulumi.Alias(type_='azure-native:netapp/v20220501:Pool')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Pool, __self__).__init__('azure-native:netapp:Pool', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Pool':
        """
        Get an existing Pool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = PoolArgs.__new__(PoolArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['pool_id'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['qos_type'] = None
        __props__.__dict__['service_level'] = None
        __props__.__dict__['size'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['total_throughput_mibps'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['utilized_throughput_mibps'] = None
        return Pool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='poolId')
    def pool_id(self) -> pulumi.Output[str]:
        """
        UUID v4 used to identify the Pool
        """
        return pulumi.get(self, 'pool_id')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='qosType')
    def qos_type(self) -> pulumi.Output[Optional[str]]:
        """
        The qos type of the pool
        """
        return pulumi.get(self, 'qos_type')

    @property
    @pulumi.getter(name='serviceLevel')
    def service_level(self) -> pulumi.Output[str]:
        """
        The service level of the file system
        """
        return pulumi.get(self, 'service_level')

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[float]:
        """
        Provisioned size of the pool (in bytes). Allowed values are in 4TiB chunks (value must be multiply of 4398046511104).
        """
        return pulumi.get(self, 'size')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='totalThroughputMibps')
    def total_throughput_mibps(self) -> pulumi.Output[float]:
        """
        Total throughput of pool in Mibps
        """
        return pulumi.get(self, 'total_throughput_mibps')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='utilizedThroughputMibps')
    def utilized_throughput_mibps(self) -> pulumi.Output[float]:
        """
        Utilized throughput of pool in Mibps
        """
        return pulumi.get(self, 'utilized_throughput_mibps')
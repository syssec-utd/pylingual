import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['SnapshotArgs', 'Snapshot']

@pulumi.input_type
class SnapshotArgs:

    def __init__(__self__, *, account_name: pulumi.Input[str], pool_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], volume_name: pulumi.Input[str], location: Optional[pulumi.Input[str]]=None, snapshot_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Snapshot resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] volume_name: The name of the volume
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] snapshot_name: The name of the snapshot
        """
        pulumi.set(__self__, 'account_name', account_name)
        pulumi.set(__self__, 'pool_name', pool_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'volume_name', volume_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if snapshot_name is not None:
            pulumi.set(__self__, 'snapshot_name', snapshot_name)

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
    @pulumi.getter(name='poolName')
    def pool_name(self) -> pulumi.Input[str]:
        """
        The name of the capacity pool
        """
        return pulumi.get(self, 'pool_name')

    @pool_name.setter
    def pool_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'pool_name', value)

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
    @pulumi.getter(name='volumeName')
    def volume_name(self) -> pulumi.Input[str]:
        """
        The name of the volume
        """
        return pulumi.get(self, 'volume_name')

    @volume_name.setter
    def volume_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'volume_name', value)

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
    @pulumi.getter(name='snapshotName')
    def snapshot_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the snapshot
        """
        return pulumi.get(self, 'snapshot_name')

    @snapshot_name.setter
    def snapshot_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'snapshot_name', value)

class Snapshot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, snapshot_name: Optional[pulumi.Input[str]]=None, volume_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Snapshot of a Volume

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] snapshot_name: The name of the snapshot
        :param pulumi.Input[str] volume_name: The name of the volume
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: SnapshotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Snapshot of a Volume

        :param str resource_name: The name of the resource.
        :param SnapshotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(SnapshotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, snapshot_name: Optional[pulumi.Input[str]]=None, volume_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SnapshotArgs.__new__(SnapshotArgs)
            if account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__['account_name'] = account_name
            __props__.__dict__['location'] = location
            if pool_name is None and (not opts.urn):
                raise TypeError("Missing required property 'pool_name'")
            __props__.__dict__['pool_name'] = pool_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['snapshot_name'] = snapshot_name
            if volume_name is None and (not opts.urn):
                raise TypeError("Missing required property 'volume_name'")
            __props__.__dict__['volume_name'] = volume_name
            __props__.__dict__['created'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['snapshot_id'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:netapp:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20170815:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20190501:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20190601:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20190701:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20190801:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20191001:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20191101:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200201:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200301:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200501:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200601:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200701:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200801:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20200901:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20201101:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20201201:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20210201:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20210401:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20210401preview:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20210601:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20210801:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20211001:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20220101:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20220301:Snapshot'), pulumi.Alias(type_='azure-native:netapp/v20220901:Snapshot')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Snapshot, __self__).__init__('azure-native:netapp/v20220501:Snapshot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Snapshot':
        """
        Get an existing Snapshot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = SnapshotArgs.__new__(SnapshotArgs)
        __props__.__dict__['created'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['snapshot_id'] = None
        __props__.__dict__['type'] = None
        return Snapshot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The creation date of the snapshot
        """
        return pulumi.get(self, 'created')

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
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='snapshotId')
    def snapshot_id(self) -> pulumi.Output[str]:
        """
        UUID v4 used to identify the Snapshot
        """
        return pulumi.get(self, 'snapshot_id')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')
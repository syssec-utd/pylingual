import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetSnapshotResult', 'AwaitableGetSnapshotResult', 'get_snapshot', 'get_snapshot_output']

@pulumi.output_type
class GetSnapshotResult:
    """
    Snapshot of a Volume
    """

    def __init__(__self__, created=None, id=None, location=None, name=None, provisioning_state=None, snapshot_id=None, type=None):
        if created and (not isinstance(created, str)):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, 'created', created)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if snapshot_id and (not isinstance(snapshot_id, str)):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, 'snapshot_id', snapshot_id)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The creation date of the snapshot
        """
        return pulumi.get(self, 'created')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='snapshotId')
    def snapshot_id(self) -> str:
        """
        UUID v4 used to identify the Snapshot
        """
        return pulumi.get(self, 'snapshot_id')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

class AwaitableGetSnapshotResult(GetSnapshotResult):

    def __await__(self):
        if False:
            yield self
        return GetSnapshotResult(created=self.created, id=self.id, location=self.location, name=self.name, provisioning_state=self.provisioning_state, snapshot_id=self.snapshot_id, type=self.type)

def get_snapshot(account_name: Optional[str]=None, pool_name: Optional[str]=None, resource_group_name: Optional[str]=None, snapshot_name: Optional[str]=None, volume_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSnapshotResult:
    """
    Snapshot of a Volume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str snapshot_name: The name of the snapshot
    :param str volume_name: The name of the volume
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['poolName'] = pool_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['snapshotName'] = snapshot_name
    __args__['volumeName'] = volume_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:netapp/v20210601:getSnapshot', __args__, opts=opts, typ=GetSnapshotResult).value
    return AwaitableGetSnapshotResult(created=__ret__.created, id=__ret__.id, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, snapshot_id=__ret__.snapshot_id, type=__ret__.type)

@_utilities.lift_output_func(get_snapshot)
def get_snapshot_output(account_name: Optional[pulumi.Input[str]]=None, pool_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, snapshot_name: Optional[pulumi.Input[str]]=None, volume_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSnapshotResult]:
    """
    Snapshot of a Volume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str snapshot_name: The name of the snapshot
    :param str volume_name: The name of the volume
    """
    ...
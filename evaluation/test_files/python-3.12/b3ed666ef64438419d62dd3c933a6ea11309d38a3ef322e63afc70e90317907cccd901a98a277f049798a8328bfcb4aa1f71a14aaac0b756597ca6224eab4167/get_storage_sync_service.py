import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetStorageSyncServiceResult', 'AwaitableGetStorageSyncServiceResult', 'get_storage_sync_service', 'get_storage_sync_service_output']
warnings.warn('Version 2019-03-01 will be removed in v2 of the provider.', DeprecationWarning)

@pulumi.output_type
class GetStorageSyncServiceResult:
    """
    Storage Sync Service object.
    """

    def __init__(__self__, id=None, location=None, name=None, storage_sync_service_status=None, storage_sync_service_uid=None, tags=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if storage_sync_service_status and (not isinstance(storage_sync_service_status, int)):
            raise TypeError("Expected argument 'storage_sync_service_status' to be a int")
        pulumi.set(__self__, 'storage_sync_service_status', storage_sync_service_status)
        if storage_sync_service_uid and (not isinstance(storage_sync_service_uid, str)):
            raise TypeError("Expected argument 'storage_sync_service_uid' to be a str")
        pulumi.set(__self__, 'storage_sync_service_uid', storage_sync_service_uid)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='storageSyncServiceStatus')
    def storage_sync_service_status(self) -> int:
        """
        Storage Sync service status.
        """
        return pulumi.get(self, 'storage_sync_service_status')

    @property
    @pulumi.getter(name='storageSyncServiceUid')
    def storage_sync_service_uid(self) -> str:
        """
        Storage Sync service Uid
        """
        return pulumi.get(self, 'storage_sync_service_uid')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetStorageSyncServiceResult(GetStorageSyncServiceResult):

    def __await__(self):
        if False:
            yield self
        return GetStorageSyncServiceResult(id=self.id, location=self.location, name=self.name, storage_sync_service_status=self.storage_sync_service_status, storage_sync_service_uid=self.storage_sync_service_uid, tags=self.tags, type=self.type)

def get_storage_sync_service(resource_group_name: Optional[str]=None, storage_sync_service_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetStorageSyncServiceResult:
    """
    Storage Sync Service object.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str storage_sync_service_name: Name of Storage Sync Service resource.
    """
    pulumi.log.warn('get_storage_sync_service is deprecated: Version 2019-03-01 will be removed in v2 of the provider.')
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['storageSyncServiceName'] = storage_sync_service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storagesync/v20190301:getStorageSyncService', __args__, opts=opts, typ=GetStorageSyncServiceResult).value
    return AwaitableGetStorageSyncServiceResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, storage_sync_service_status=__ret__.storage_sync_service_status, storage_sync_service_uid=__ret__.storage_sync_service_uid, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_storage_sync_service)
def get_storage_sync_service_output(resource_group_name: Optional[pulumi.Input[str]]=None, storage_sync_service_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetStorageSyncServiceResult]:
    """
    Storage Sync Service object.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str storage_sync_service_name: Name of Storage Sync Service resource.
    """
    pulumi.log.warn('get_storage_sync_service is deprecated: Version 2019-03-01 will be removed in v2 of the provider.')
    ...
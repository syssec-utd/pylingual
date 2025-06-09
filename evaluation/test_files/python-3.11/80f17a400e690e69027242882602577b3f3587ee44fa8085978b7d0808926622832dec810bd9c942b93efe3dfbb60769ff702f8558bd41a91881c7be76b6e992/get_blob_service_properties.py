import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetBlobServicePropertiesResult', 'AwaitableGetBlobServicePropertiesResult', 'get_blob_service_properties', 'get_blob_service_properties_output']

@pulumi.output_type
class GetBlobServicePropertiesResult:
    """
    The properties of a storage account’s Blob service.
    """

    def __init__(__self__, automatic_snapshot_policy_enabled=None, change_feed=None, container_delete_retention_policy=None, cors=None, default_service_version=None, delete_retention_policy=None, id=None, is_versioning_enabled=None, last_access_time_tracking_policy=None, name=None, restore_policy=None, sku=None, type=None):
        if automatic_snapshot_policy_enabled and (not isinstance(automatic_snapshot_policy_enabled, bool)):
            raise TypeError("Expected argument 'automatic_snapshot_policy_enabled' to be a bool")
        pulumi.set(__self__, 'automatic_snapshot_policy_enabled', automatic_snapshot_policy_enabled)
        if change_feed and (not isinstance(change_feed, dict)):
            raise TypeError("Expected argument 'change_feed' to be a dict")
        pulumi.set(__self__, 'change_feed', change_feed)
        if container_delete_retention_policy and (not isinstance(container_delete_retention_policy, dict)):
            raise TypeError("Expected argument 'container_delete_retention_policy' to be a dict")
        pulumi.set(__self__, 'container_delete_retention_policy', container_delete_retention_policy)
        if cors and (not isinstance(cors, dict)):
            raise TypeError("Expected argument 'cors' to be a dict")
        pulumi.set(__self__, 'cors', cors)
        if default_service_version and (not isinstance(default_service_version, str)):
            raise TypeError("Expected argument 'default_service_version' to be a str")
        pulumi.set(__self__, 'default_service_version', default_service_version)
        if delete_retention_policy and (not isinstance(delete_retention_policy, dict)):
            raise TypeError("Expected argument 'delete_retention_policy' to be a dict")
        pulumi.set(__self__, 'delete_retention_policy', delete_retention_policy)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if is_versioning_enabled and (not isinstance(is_versioning_enabled, bool)):
            raise TypeError("Expected argument 'is_versioning_enabled' to be a bool")
        pulumi.set(__self__, 'is_versioning_enabled', is_versioning_enabled)
        if last_access_time_tracking_policy and (not isinstance(last_access_time_tracking_policy, dict)):
            raise TypeError("Expected argument 'last_access_time_tracking_policy' to be a dict")
        pulumi.set(__self__, 'last_access_time_tracking_policy', last_access_time_tracking_policy)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if restore_policy and (not isinstance(restore_policy, dict)):
            raise TypeError("Expected argument 'restore_policy' to be a dict")
        pulumi.set(__self__, 'restore_policy', restore_policy)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='automaticSnapshotPolicyEnabled')
    def automatic_snapshot_policy_enabled(self) -> Optional[bool]:
        """
        Deprecated in favor of isVersioningEnabled property.
        """
        return pulumi.get(self, 'automatic_snapshot_policy_enabled')

    @property
    @pulumi.getter(name='changeFeed')
    def change_feed(self) -> Optional['outputs.ChangeFeedResponse']:
        """
        The blob service properties for change feed events.
        """
        return pulumi.get(self, 'change_feed')

    @property
    @pulumi.getter(name='containerDeleteRetentionPolicy')
    def container_delete_retention_policy(self) -> Optional['outputs.DeleteRetentionPolicyResponse']:
        """
        The blob service properties for container soft delete.
        """
        return pulumi.get(self, 'container_delete_retention_policy')

    @property
    @pulumi.getter
    def cors(self) -> Optional['outputs.CorsRulesResponse']:
        """
        Specifies CORS rules for the Blob service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the Blob service.
        """
        return pulumi.get(self, 'cors')

    @property
    @pulumi.getter(name='defaultServiceVersion')
    def default_service_version(self) -> Optional[str]:
        """
        DefaultServiceVersion indicates the default version to use for requests to the Blob service if an incoming request’s version is not specified. Possible values include version 2008-10-27 and all more recent versions.
        """
        return pulumi.get(self, 'default_service_version')

    @property
    @pulumi.getter(name='deleteRetentionPolicy')
    def delete_retention_policy(self) -> Optional['outputs.DeleteRetentionPolicyResponse']:
        """
        The blob service properties for blob soft delete.
        """
        return pulumi.get(self, 'delete_retention_policy')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='isVersioningEnabled')
    def is_versioning_enabled(self) -> Optional[bool]:
        """
        Versioning is enabled if set to true.
        """
        return pulumi.get(self, 'is_versioning_enabled')

    @property
    @pulumi.getter(name='lastAccessTimeTrackingPolicy')
    def last_access_time_tracking_policy(self) -> Optional['outputs.LastAccessTimeTrackingPolicyResponse']:
        """
        The blob service property to configure last access time based tracking policy.
        """
        return pulumi.get(self, 'last_access_time_tracking_policy')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='restorePolicy')
    def restore_policy(self) -> Optional['outputs.RestorePolicyPropertiesResponse']:
        """
        The blob service properties for blob restore policy.
        """
        return pulumi.get(self, 'restore_policy')

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        Sku name and tier.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetBlobServicePropertiesResult(GetBlobServicePropertiesResult):

    def __await__(self):
        if False:
            yield self
        return GetBlobServicePropertiesResult(automatic_snapshot_policy_enabled=self.automatic_snapshot_policy_enabled, change_feed=self.change_feed, container_delete_retention_policy=self.container_delete_retention_policy, cors=self.cors, default_service_version=self.default_service_version, delete_retention_policy=self.delete_retention_policy, id=self.id, is_versioning_enabled=self.is_versioning_enabled, last_access_time_tracking_policy=self.last_access_time_tracking_policy, name=self.name, restore_policy=self.restore_policy, sku=self.sku, type=self.type)

def get_blob_service_properties(account_name: Optional[str]=None, blob_services_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetBlobServicePropertiesResult:
    """
    The properties of a storage account’s Blob service.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str blob_services_name: The name of the blob Service within the specified storage account. Blob Service Name must be 'default'
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['blobServicesName'] = blob_services_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storage/v20220501:getBlobServiceProperties', __args__, opts=opts, typ=GetBlobServicePropertiesResult).value
    return AwaitableGetBlobServicePropertiesResult(automatic_snapshot_policy_enabled=__ret__.automatic_snapshot_policy_enabled, change_feed=__ret__.change_feed, container_delete_retention_policy=__ret__.container_delete_retention_policy, cors=__ret__.cors, default_service_version=__ret__.default_service_version, delete_retention_policy=__ret__.delete_retention_policy, id=__ret__.id, is_versioning_enabled=__ret__.is_versioning_enabled, last_access_time_tracking_policy=__ret__.last_access_time_tracking_policy, name=__ret__.name, restore_policy=__ret__.restore_policy, sku=__ret__.sku, type=__ret__.type)

@_utilities.lift_output_func(get_blob_service_properties)
def get_blob_service_properties_output(account_name: Optional[pulumi.Input[str]]=None, blob_services_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetBlobServicePropertiesResult]:
    """
    The properties of a storage account’s Blob service.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str blob_services_name: The name of the blob Service within the specified storage account. Blob Service Name must be 'default'
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
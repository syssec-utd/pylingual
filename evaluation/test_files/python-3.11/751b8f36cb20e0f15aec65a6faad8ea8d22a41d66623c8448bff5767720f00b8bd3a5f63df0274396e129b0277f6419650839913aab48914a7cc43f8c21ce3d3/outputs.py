import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['CommunityGalleryInfoResponse', 'DataDiskImageEncryptionResponse', 'DisallowedResponse', 'EncryptionImagesResponse', 'GalleryApplicationVersionPublishingProfileResponse', 'GalleryArtifactVersionSourceResponse', 'GalleryDataDiskImageResponse', 'GalleryExtendedLocationResponse', 'GalleryIdentifierResponse', 'GalleryImageFeatureResponse', 'GalleryImageIdentifierResponse', 'GalleryImageVersionPublishingProfileResponse', 'GalleryImageVersionStorageProfileResponse', 'GalleryOSDiskImageResponse', 'GalleryTargetExtendedLocationResponse', 'ImagePurchasePlanResponse', 'OSDiskImageEncryptionResponse', 'OSDiskImageSecurityProfileResponse', 'RecommendedMachineConfigurationResponse', 'RegionalReplicationStatusResponse', 'RegionalSharingStatusResponse', 'ReplicationStatusResponse', 'ResourceRangeResponse', 'SharingProfileGroupResponse', 'SharingProfileResponse', 'SharingStatusResponse', 'SoftDeletePolicyResponse', 'TargetRegionResponse', 'UserArtifactManageResponse', 'UserArtifactSourceResponse']

@pulumi.output_type
class CommunityGalleryInfoResponse(dict):
    """
    Information of community gallery if current gallery is shared to community
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'communityGalleryEnabled':
            suggest = 'community_gallery_enabled'
        elif key == 'publicNames':
            suggest = 'public_names'
        elif key == 'publicNamePrefix':
            suggest = 'public_name_prefix'
        elif key == 'publisherContact':
            suggest = 'publisher_contact'
        elif key == 'publisherUri':
            suggest = 'publisher_uri'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CommunityGalleryInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CommunityGalleryInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CommunityGalleryInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, community_gallery_enabled: bool, public_names: Sequence[str], eula: Optional[str]=None, public_name_prefix: Optional[str]=None, publisher_contact: Optional[str]=None, publisher_uri: Optional[str]=None):
        """
        Information of community gallery if current gallery is shared to community
        :param bool community_gallery_enabled: Contains info about whether community gallery sharing is enabled.
        :param Sequence[str] public_names: Community gallery public name list.
        :param str eula: Community gallery publisher eula
        :param str public_name_prefix: Community gallery public name prefix
        :param str publisher_contact: Community gallery publisher contact email
        :param str publisher_uri: Community gallery publisher uri
        """
        pulumi.set(__self__, 'community_gallery_enabled', community_gallery_enabled)
        pulumi.set(__self__, 'public_names', public_names)
        if eula is not None:
            pulumi.set(__self__, 'eula', eula)
        if public_name_prefix is not None:
            pulumi.set(__self__, 'public_name_prefix', public_name_prefix)
        if publisher_contact is not None:
            pulumi.set(__self__, 'publisher_contact', publisher_contact)
        if publisher_uri is not None:
            pulumi.set(__self__, 'publisher_uri', publisher_uri)

    @property
    @pulumi.getter(name='communityGalleryEnabled')
    def community_gallery_enabled(self) -> bool:
        """
        Contains info about whether community gallery sharing is enabled.
        """
        return pulumi.get(self, 'community_gallery_enabled')

    @property
    @pulumi.getter(name='publicNames')
    def public_names(self) -> Sequence[str]:
        """
        Community gallery public name list.
        """
        return pulumi.get(self, 'public_names')

    @property
    @pulumi.getter
    def eula(self) -> Optional[str]:
        """
        Community gallery publisher eula
        """
        return pulumi.get(self, 'eula')

    @property
    @pulumi.getter(name='publicNamePrefix')
    def public_name_prefix(self) -> Optional[str]:
        """
        Community gallery public name prefix
        """
        return pulumi.get(self, 'public_name_prefix')

    @property
    @pulumi.getter(name='publisherContact')
    def publisher_contact(self) -> Optional[str]:
        """
        Community gallery publisher contact email
        """
        return pulumi.get(self, 'publisher_contact')

    @property
    @pulumi.getter(name='publisherUri')
    def publisher_uri(self) -> Optional[str]:
        """
        Community gallery publisher uri
        """
        return pulumi.get(self, 'publisher_uri')

@pulumi.output_type
class DataDiskImageEncryptionResponse(dict):
    """
    Contains encryption settings for a data disk image.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'diskEncryptionSetId':
            suggest = 'disk_encryption_set_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DataDiskImageEncryptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DataDiskImageEncryptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        DataDiskImageEncryptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, lun: int, disk_encryption_set_id: Optional[str]=None):
        """
        Contains encryption settings for a data disk image.
        :param int lun: This property specifies the logical unit number of the data disk. This value is used to identify data disks within the Virtual Machine and therefore must be unique for each data disk attached to the Virtual Machine.
        :param str disk_encryption_set_id: A relative URI containing the resource ID of the disk encryption set.
        """
        pulumi.set(__self__, 'lun', lun)
        if disk_encryption_set_id is not None:
            pulumi.set(__self__, 'disk_encryption_set_id', disk_encryption_set_id)

    @property
    @pulumi.getter
    def lun(self) -> int:
        """
        This property specifies the logical unit number of the data disk. This value is used to identify data disks within the Virtual Machine and therefore must be unique for each data disk attached to the Virtual Machine.
        """
        return pulumi.get(self, 'lun')

    @property
    @pulumi.getter(name='diskEncryptionSetId')
    def disk_encryption_set_id(self) -> Optional[str]:
        """
        A relative URI containing the resource ID of the disk encryption set.
        """
        return pulumi.get(self, 'disk_encryption_set_id')

@pulumi.output_type
class DisallowedResponse(dict):
    """
    Describes the disallowed disk types.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'diskTypes':
            suggest = 'disk_types'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DisallowedResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DisallowedResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        DisallowedResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, disk_types: Optional[Sequence[str]]=None):
        """
        Describes the disallowed disk types.
        :param Sequence[str] disk_types: A list of disk types.
        """
        if disk_types is not None:
            pulumi.set(__self__, 'disk_types', disk_types)

    @property
    @pulumi.getter(name='diskTypes')
    def disk_types(self) -> Optional[Sequence[str]]:
        """
        A list of disk types.
        """
        return pulumi.get(self, 'disk_types')

@pulumi.output_type
class EncryptionImagesResponse(dict):
    """
    Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'dataDiskImages':
            suggest = 'data_disk_images'
        elif key == 'osDiskImage':
            suggest = 'os_disk_image'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionImagesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionImagesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        EncryptionImagesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, data_disk_images: Optional[Sequence['outputs.DataDiskImageEncryptionResponse']]=None, os_disk_image: Optional['outputs.OSDiskImageEncryptionResponse']=None):
        """
        Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
        :param Sequence['DataDiskImageEncryptionResponse'] data_disk_images: A list of encryption specifications for data disk images.
        :param 'OSDiskImageEncryptionResponse' os_disk_image: Contains encryption settings for an OS disk image.
        """
        if data_disk_images is not None:
            pulumi.set(__self__, 'data_disk_images', data_disk_images)
        if os_disk_image is not None:
            pulumi.set(__self__, 'os_disk_image', os_disk_image)

    @property
    @pulumi.getter(name='dataDiskImages')
    def data_disk_images(self) -> Optional[Sequence['outputs.DataDiskImageEncryptionResponse']]:
        """
        A list of encryption specifications for data disk images.
        """
        return pulumi.get(self, 'data_disk_images')

    @property
    @pulumi.getter(name='osDiskImage')
    def os_disk_image(self) -> Optional['outputs.OSDiskImageEncryptionResponse']:
        """
        Contains encryption settings for an OS disk image.
        """
        return pulumi.get(self, 'os_disk_image')

@pulumi.output_type
class GalleryApplicationVersionPublishingProfileResponse(dict):
    """
    The publishing profile of a gallery image version.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publishedDate':
            suggest = 'published_date'
        elif key == 'enableHealthCheck':
            suggest = 'enable_health_check'
        elif key == 'endOfLifeDate':
            suggest = 'end_of_life_date'
        elif key == 'excludeFromLatest':
            suggest = 'exclude_from_latest'
        elif key == 'manageActions':
            suggest = 'manage_actions'
        elif key == 'replicaCount':
            suggest = 'replica_count'
        elif key == 'replicationMode':
            suggest = 'replication_mode'
        elif key == 'storageAccountType':
            suggest = 'storage_account_type'
        elif key == 'targetExtendedLocations':
            suggest = 'target_extended_locations'
        elif key == 'targetRegions':
            suggest = 'target_regions'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryApplicationVersionPublishingProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryApplicationVersionPublishingProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryApplicationVersionPublishingProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, published_date: str, source: 'outputs.UserArtifactSourceResponse', enable_health_check: Optional[bool]=None, end_of_life_date: Optional[str]=None, exclude_from_latest: Optional[bool]=None, manage_actions: Optional['outputs.UserArtifactManageResponse']=None, replica_count: Optional[int]=None, replication_mode: Optional[str]=None, storage_account_type: Optional[str]=None, target_extended_locations: Optional[Sequence['outputs.GalleryTargetExtendedLocationResponse']]=None, target_regions: Optional[Sequence['outputs.TargetRegionResponse']]=None):
        """
        The publishing profile of a gallery image version.
        :param str published_date: The timestamp for when the gallery image version is published.
        :param 'UserArtifactSourceResponse' source: The source image from which the Image Version is going to be created.
        :param bool enable_health_check: Optional. Whether or not this application reports health.
        :param str end_of_life_date: The end of life date of the gallery image version. This property can be used for decommissioning purposes. This property is updatable.
        :param bool exclude_from_latest: If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version.
        :param int replica_count: The number of replicas of the Image Version to be created per region. This property would take effect for a region when regionalReplicaCount is not specified. This property is updatable.
        :param str replication_mode: Optional parameter which specifies the mode to be used for replication. This property is not updatable.
        :param str storage_account_type: Specifies the storage account type to be used to store the image. This property is not updatable.
        :param Sequence['GalleryTargetExtendedLocationResponse'] target_extended_locations: The target extended locations where the Image Version is going to be replicated to. This property is updatable.
        :param Sequence['TargetRegionResponse'] target_regions: The target regions where the Image Version is going to be replicated to. This property is updatable.
        """
        pulumi.set(__self__, 'published_date', published_date)
        pulumi.set(__self__, 'source', source)
        if enable_health_check is not None:
            pulumi.set(__self__, 'enable_health_check', enable_health_check)
        if end_of_life_date is not None:
            pulumi.set(__self__, 'end_of_life_date', end_of_life_date)
        if exclude_from_latest is not None:
            pulumi.set(__self__, 'exclude_from_latest', exclude_from_latest)
        if manage_actions is not None:
            pulumi.set(__self__, 'manage_actions', manage_actions)
        if replica_count is not None:
            pulumi.set(__self__, 'replica_count', replica_count)
        if replication_mode is not None:
            pulumi.set(__self__, 'replication_mode', replication_mode)
        if storage_account_type is not None:
            pulumi.set(__self__, 'storage_account_type', storage_account_type)
        if target_extended_locations is not None:
            pulumi.set(__self__, 'target_extended_locations', target_extended_locations)
        if target_regions is not None:
            pulumi.set(__self__, 'target_regions', target_regions)

    @property
    @pulumi.getter(name='publishedDate')
    def published_date(self) -> str:
        """
        The timestamp for when the gallery image version is published.
        """
        return pulumi.get(self, 'published_date')

    @property
    @pulumi.getter
    def source(self) -> 'outputs.UserArtifactSourceResponse':
        """
        The source image from which the Image Version is going to be created.
        """
        return pulumi.get(self, 'source')

    @property
    @pulumi.getter(name='enableHealthCheck')
    def enable_health_check(self) -> Optional[bool]:
        """
        Optional. Whether or not this application reports health.
        """
        return pulumi.get(self, 'enable_health_check')

    @property
    @pulumi.getter(name='endOfLifeDate')
    def end_of_life_date(self) -> Optional[str]:
        """
        The end of life date of the gallery image version. This property can be used for decommissioning purposes. This property is updatable.
        """
        return pulumi.get(self, 'end_of_life_date')

    @property
    @pulumi.getter(name='excludeFromLatest')
    def exclude_from_latest(self) -> Optional[bool]:
        """
        If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version.
        """
        return pulumi.get(self, 'exclude_from_latest')

    @property
    @pulumi.getter(name='manageActions')
    def manage_actions(self) -> Optional['outputs.UserArtifactManageResponse']:
        return pulumi.get(self, 'manage_actions')

    @property
    @pulumi.getter(name='replicaCount')
    def replica_count(self) -> Optional[int]:
        """
        The number of replicas of the Image Version to be created per region. This property would take effect for a region when regionalReplicaCount is not specified. This property is updatable.
        """
        return pulumi.get(self, 'replica_count')

    @property
    @pulumi.getter(name='replicationMode')
    def replication_mode(self) -> Optional[str]:
        """
        Optional parameter which specifies the mode to be used for replication. This property is not updatable.
        """
        return pulumi.get(self, 'replication_mode')

    @property
    @pulumi.getter(name='storageAccountType')
    def storage_account_type(self) -> Optional[str]:
        """
        Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        return pulumi.get(self, 'storage_account_type')

    @property
    @pulumi.getter(name='targetExtendedLocations')
    def target_extended_locations(self) -> Optional[Sequence['outputs.GalleryTargetExtendedLocationResponse']]:
        """
        The target extended locations where the Image Version is going to be replicated to. This property is updatable.
        """
        return pulumi.get(self, 'target_extended_locations')

    @property
    @pulumi.getter(name='targetRegions')
    def target_regions(self) -> Optional[Sequence['outputs.TargetRegionResponse']]:
        """
        The target regions where the Image Version is going to be replicated to. This property is updatable.
        """
        return pulumi.get(self, 'target_regions')

@pulumi.output_type
class GalleryArtifactVersionSourceResponse(dict):
    """
    The gallery artifact version source.
    """

    def __init__(__self__, *, id: Optional[str]=None, uri: Optional[str]=None):
        """
        The gallery artifact version source.
        :param str id: The id of the gallery artifact version source. Can specify a disk uri, snapshot uri, user image or storage account resource.
        :param str uri: The uri of the gallery artifact version source. Currently used to specify vhd/blob source.
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if uri is not None:
            pulumi.set(__self__, 'uri', uri)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The id of the gallery artifact version source. Can specify a disk uri, snapshot uri, user image or storage account resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def uri(self) -> Optional[str]:
        """
        The uri of the gallery artifact version source. Currently used to specify vhd/blob source.
        """
        return pulumi.get(self, 'uri')

@pulumi.output_type
class GalleryDataDiskImageResponse(dict):
    """
    This is the data disk image.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'sizeInGB':
            suggest = 'size_in_gb'
        elif key == 'hostCaching':
            suggest = 'host_caching'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryDataDiskImageResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryDataDiskImageResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryDataDiskImageResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, lun: int, size_in_gb: int, host_caching: Optional[str]=None, source: Optional['outputs.GalleryArtifactVersionSourceResponse']=None):
        """
        This is the data disk image.
        :param int lun: This property specifies the logical unit number of the data disk. This value is used to identify data disks within the Virtual Machine and therefore must be unique for each data disk attached to the Virtual Machine.
        :param int size_in_gb: This property indicates the size of the VHD to be created.
        :param str host_caching: The host caching of the disk. Valid values are 'None', 'ReadOnly', and 'ReadWrite'
        :param 'GalleryArtifactVersionSourceResponse' source: The gallery artifact version source.
        """
        pulumi.set(__self__, 'lun', lun)
        pulumi.set(__self__, 'size_in_gb', size_in_gb)
        if host_caching is not None:
            pulumi.set(__self__, 'host_caching', host_caching)
        if source is not None:
            pulumi.set(__self__, 'source', source)

    @property
    @pulumi.getter
    def lun(self) -> int:
        """
        This property specifies the logical unit number of the data disk. This value is used to identify data disks within the Virtual Machine and therefore must be unique for each data disk attached to the Virtual Machine.
        """
        return pulumi.get(self, 'lun')

    @property
    @pulumi.getter(name='sizeInGB')
    def size_in_gb(self) -> int:
        """
        This property indicates the size of the VHD to be created.
        """
        return pulumi.get(self, 'size_in_gb')

    @property
    @pulumi.getter(name='hostCaching')
    def host_caching(self) -> Optional[str]:
        """
        The host caching of the disk. Valid values are 'None', 'ReadOnly', and 'ReadWrite'
        """
        return pulumi.get(self, 'host_caching')

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.GalleryArtifactVersionSourceResponse']:
        """
        The gallery artifact version source.
        """
        return pulumi.get(self, 'source')

@pulumi.output_type
class GalleryExtendedLocationResponse(dict):
    """
    The name of the extended location.
    """

    def __init__(__self__, *, name: Optional[str]=None, type: Optional[str]=None):
        """
        The name of the extended location.
        :param str type: It is type of the extended location.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        It is type of the extended location.
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class GalleryIdentifierResponse(dict):
    """
    Describes the gallery unique name.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'uniqueName':
            suggest = 'unique_name'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryIdentifierResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryIdentifierResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryIdentifierResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, unique_name: str):
        """
        Describes the gallery unique name.
        :param str unique_name: The unique name of the Shared Image Gallery. This name is generated automatically by Azure.
        """
        pulumi.set(__self__, 'unique_name', unique_name)

    @property
    @pulumi.getter(name='uniqueName')
    def unique_name(self) -> str:
        """
        The unique name of the Shared Image Gallery. This name is generated automatically by Azure.
        """
        return pulumi.get(self, 'unique_name')

@pulumi.output_type
class GalleryImageFeatureResponse(dict):
    """
    A feature for gallery image.
    """

    def __init__(__self__, *, name: Optional[str]=None, value: Optional[str]=None):
        """
        A feature for gallery image.
        :param str name: The name of the gallery image feature.
        :param str value: The value of the gallery image feature.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if value is not None:
            pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the gallery image feature.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        The value of the gallery image feature.
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class GalleryImageIdentifierResponse(dict):
    """
    This is the gallery image definition identifier.
    """

    def __init__(__self__, *, offer: str, publisher: str, sku: str):
        """
        This is the gallery image definition identifier.
        :param str offer: The name of the gallery image definition offer.
        :param str publisher: The name of the gallery image definition publisher.
        :param str sku: The name of the gallery image definition SKU.
        """
        pulumi.set(__self__, 'offer', offer)
        pulumi.set(__self__, 'publisher', publisher)
        pulumi.set(__self__, 'sku', sku)

    @property
    @pulumi.getter
    def offer(self) -> str:
        """
        The name of the gallery image definition offer.
        """
        return pulumi.get(self, 'offer')

    @property
    @pulumi.getter
    def publisher(self) -> str:
        """
        The name of the gallery image definition publisher.
        """
        return pulumi.get(self, 'publisher')

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        The name of the gallery image definition SKU.
        """
        return pulumi.get(self, 'sku')

@pulumi.output_type
class GalleryImageVersionPublishingProfileResponse(dict):
    """
    The publishing profile of a gallery image Version.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'publishedDate':
            suggest = 'published_date'
        elif key == 'endOfLifeDate':
            suggest = 'end_of_life_date'
        elif key == 'excludeFromLatest':
            suggest = 'exclude_from_latest'
        elif key == 'replicaCount':
            suggest = 'replica_count'
        elif key == 'replicationMode':
            suggest = 'replication_mode'
        elif key == 'storageAccountType':
            suggest = 'storage_account_type'
        elif key == 'targetExtendedLocations':
            suggest = 'target_extended_locations'
        elif key == 'targetRegions':
            suggest = 'target_regions'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryImageVersionPublishingProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryImageVersionPublishingProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryImageVersionPublishingProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, published_date: str, end_of_life_date: Optional[str]=None, exclude_from_latest: Optional[bool]=None, replica_count: Optional[int]=None, replication_mode: Optional[str]=None, storage_account_type: Optional[str]=None, target_extended_locations: Optional[Sequence['outputs.GalleryTargetExtendedLocationResponse']]=None, target_regions: Optional[Sequence['outputs.TargetRegionResponse']]=None):
        """
        The publishing profile of a gallery image Version.
        :param str published_date: The timestamp for when the gallery image version is published.
        :param str end_of_life_date: The end of life date of the gallery image version. This property can be used for decommissioning purposes. This property is updatable.
        :param bool exclude_from_latest: If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version.
        :param int replica_count: The number of replicas of the Image Version to be created per region. This property would take effect for a region when regionalReplicaCount is not specified. This property is updatable.
        :param str replication_mode: Optional parameter which specifies the mode to be used for replication. This property is not updatable.
        :param str storage_account_type: Specifies the storage account type to be used to store the image. This property is not updatable.
        :param Sequence['GalleryTargetExtendedLocationResponse'] target_extended_locations: The target extended locations where the Image Version is going to be replicated to. This property is updatable.
        :param Sequence['TargetRegionResponse'] target_regions: The target regions where the Image Version is going to be replicated to. This property is updatable.
        """
        pulumi.set(__self__, 'published_date', published_date)
        if end_of_life_date is not None:
            pulumi.set(__self__, 'end_of_life_date', end_of_life_date)
        if exclude_from_latest is not None:
            pulumi.set(__self__, 'exclude_from_latest', exclude_from_latest)
        if replica_count is not None:
            pulumi.set(__self__, 'replica_count', replica_count)
        if replication_mode is not None:
            pulumi.set(__self__, 'replication_mode', replication_mode)
        if storage_account_type is not None:
            pulumi.set(__self__, 'storage_account_type', storage_account_type)
        if target_extended_locations is not None:
            pulumi.set(__self__, 'target_extended_locations', target_extended_locations)
        if target_regions is not None:
            pulumi.set(__self__, 'target_regions', target_regions)

    @property
    @pulumi.getter(name='publishedDate')
    def published_date(self) -> str:
        """
        The timestamp for when the gallery image version is published.
        """
        return pulumi.get(self, 'published_date')

    @property
    @pulumi.getter(name='endOfLifeDate')
    def end_of_life_date(self) -> Optional[str]:
        """
        The end of life date of the gallery image version. This property can be used for decommissioning purposes. This property is updatable.
        """
        return pulumi.get(self, 'end_of_life_date')

    @property
    @pulumi.getter(name='excludeFromLatest')
    def exclude_from_latest(self) -> Optional[bool]:
        """
        If set to true, Virtual Machines deployed from the latest version of the Image Definition won't use this Image Version.
        """
        return pulumi.get(self, 'exclude_from_latest')

    @property
    @pulumi.getter(name='replicaCount')
    def replica_count(self) -> Optional[int]:
        """
        The number of replicas of the Image Version to be created per region. This property would take effect for a region when regionalReplicaCount is not specified. This property is updatable.
        """
        return pulumi.get(self, 'replica_count')

    @property
    @pulumi.getter(name='replicationMode')
    def replication_mode(self) -> Optional[str]:
        """
        Optional parameter which specifies the mode to be used for replication. This property is not updatable.
        """
        return pulumi.get(self, 'replication_mode')

    @property
    @pulumi.getter(name='storageAccountType')
    def storage_account_type(self) -> Optional[str]:
        """
        Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        return pulumi.get(self, 'storage_account_type')

    @property
    @pulumi.getter(name='targetExtendedLocations')
    def target_extended_locations(self) -> Optional[Sequence['outputs.GalleryTargetExtendedLocationResponse']]:
        """
        The target extended locations where the Image Version is going to be replicated to. This property is updatable.
        """
        return pulumi.get(self, 'target_extended_locations')

    @property
    @pulumi.getter(name='targetRegions')
    def target_regions(self) -> Optional[Sequence['outputs.TargetRegionResponse']]:
        """
        The target regions where the Image Version is going to be replicated to. This property is updatable.
        """
        return pulumi.get(self, 'target_regions')

@pulumi.output_type
class GalleryImageVersionStorageProfileResponse(dict):
    """
    This is the storage profile of a Gallery Image Version.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'dataDiskImages':
            suggest = 'data_disk_images'
        elif key == 'osDiskImage':
            suggest = 'os_disk_image'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryImageVersionStorageProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryImageVersionStorageProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryImageVersionStorageProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, data_disk_images: Optional[Sequence['outputs.GalleryDataDiskImageResponse']]=None, os_disk_image: Optional['outputs.GalleryOSDiskImageResponse']=None, source: Optional['outputs.GalleryArtifactVersionSourceResponse']=None):
        """
        This is the storage profile of a Gallery Image Version.
        :param Sequence['GalleryDataDiskImageResponse'] data_disk_images: A list of data disk images.
        :param 'GalleryOSDiskImageResponse' os_disk_image: This is the OS disk image.
        :param 'GalleryArtifactVersionSourceResponse' source: The gallery artifact version source.
        """
        if data_disk_images is not None:
            pulumi.set(__self__, 'data_disk_images', data_disk_images)
        if os_disk_image is not None:
            pulumi.set(__self__, 'os_disk_image', os_disk_image)
        if source is not None:
            pulumi.set(__self__, 'source', source)

    @property
    @pulumi.getter(name='dataDiskImages')
    def data_disk_images(self) -> Optional[Sequence['outputs.GalleryDataDiskImageResponse']]:
        """
        A list of data disk images.
        """
        return pulumi.get(self, 'data_disk_images')

    @property
    @pulumi.getter(name='osDiskImage')
    def os_disk_image(self) -> Optional['outputs.GalleryOSDiskImageResponse']:
        """
        This is the OS disk image.
        """
        return pulumi.get(self, 'os_disk_image')

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.GalleryArtifactVersionSourceResponse']:
        """
        The gallery artifact version source.
        """
        return pulumi.get(self, 'source')

@pulumi.output_type
class GalleryOSDiskImageResponse(dict):
    """
    This is the OS disk image.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'sizeInGB':
            suggest = 'size_in_gb'
        elif key == 'hostCaching':
            suggest = 'host_caching'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryOSDiskImageResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryOSDiskImageResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryOSDiskImageResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, size_in_gb: int, host_caching: Optional[str]=None, source: Optional['outputs.GalleryArtifactVersionSourceResponse']=None):
        """
        This is the OS disk image.
        :param int size_in_gb: This property indicates the size of the VHD to be created.
        :param str host_caching: The host caching of the disk. Valid values are 'None', 'ReadOnly', and 'ReadWrite'
        :param 'GalleryArtifactVersionSourceResponse' source: The gallery artifact version source.
        """
        pulumi.set(__self__, 'size_in_gb', size_in_gb)
        if host_caching is not None:
            pulumi.set(__self__, 'host_caching', host_caching)
        if source is not None:
            pulumi.set(__self__, 'source', source)

    @property
    @pulumi.getter(name='sizeInGB')
    def size_in_gb(self) -> int:
        """
        This property indicates the size of the VHD to be created.
        """
        return pulumi.get(self, 'size_in_gb')

    @property
    @pulumi.getter(name='hostCaching')
    def host_caching(self) -> Optional[str]:
        """
        The host caching of the disk. Valid values are 'None', 'ReadOnly', and 'ReadWrite'
        """
        return pulumi.get(self, 'host_caching')

    @property
    @pulumi.getter
    def source(self) -> Optional['outputs.GalleryArtifactVersionSourceResponse']:
        """
        The gallery artifact version source.
        """
        return pulumi.get(self, 'source')

@pulumi.output_type
class GalleryTargetExtendedLocationResponse(dict):

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'extendedLocation':
            suggest = 'extended_location'
        elif key == 'extendedLocationReplicaCount':
            suggest = 'extended_location_replica_count'
        elif key == 'storageAccountType':
            suggest = 'storage_account_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GalleryTargetExtendedLocationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GalleryTargetExtendedLocationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GalleryTargetExtendedLocationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, encryption: Optional['outputs.EncryptionImagesResponse']=None, extended_location: Optional['outputs.GalleryExtendedLocationResponse']=None, extended_location_replica_count: Optional[int]=None, name: Optional[str]=None, storage_account_type: Optional[str]=None):
        """
        :param 'EncryptionImagesResponse' encryption: Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
        :param 'GalleryExtendedLocationResponse' extended_location: The name of the extended location.
        :param int extended_location_replica_count: The number of replicas of the Image Version to be created per extended location. This property is updatable.
        :param str name: The name of the region.
        :param str storage_account_type: Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        if encryption is not None:
            pulumi.set(__self__, 'encryption', encryption)
        if extended_location is not None:
            pulumi.set(__self__, 'extended_location', extended_location)
        if extended_location_replica_count is not None:
            pulumi.set(__self__, 'extended_location_replica_count', extended_location_replica_count)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if storage_account_type is not None:
            pulumi.set(__self__, 'storage_account_type', storage_account_type)

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionImagesResponse']:
        """
        Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
        """
        return pulumi.get(self, 'encryption')

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> Optional['outputs.GalleryExtendedLocationResponse']:
        """
        The name of the extended location.
        """
        return pulumi.get(self, 'extended_location')

    @property
    @pulumi.getter(name='extendedLocationReplicaCount')
    def extended_location_replica_count(self) -> Optional[int]:
        """
        The number of replicas of the Image Version to be created per extended location. This property is updatable.
        """
        return pulumi.get(self, 'extended_location_replica_count')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the region.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='storageAccountType')
    def storage_account_type(self) -> Optional[str]:
        """
        Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        return pulumi.get(self, 'storage_account_type')

@pulumi.output_type
class ImagePurchasePlanResponse(dict):
    """
    Describes the gallery image definition purchase plan. This is used by marketplace images.
    """

    def __init__(__self__, *, name: Optional[str]=None, product: Optional[str]=None, publisher: Optional[str]=None):
        """
        Describes the gallery image definition purchase plan. This is used by marketplace images.
        :param str name: The plan ID.
        :param str product: The product ID.
        :param str publisher: The publisher ID.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if product is not None:
            pulumi.set(__self__, 'product', product)
        if publisher is not None:
            pulumi.set(__self__, 'publisher', publisher)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The plan ID.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def product(self) -> Optional[str]:
        """
        The product ID.
        """
        return pulumi.get(self, 'product')

    @property
    @pulumi.getter
    def publisher(self) -> Optional[str]:
        """
        The publisher ID.
        """
        return pulumi.get(self, 'publisher')

@pulumi.output_type
class OSDiskImageEncryptionResponse(dict):
    """
    Contains encryption settings for an OS disk image.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'diskEncryptionSetId':
            suggest = 'disk_encryption_set_id'
        elif key == 'securityProfile':
            suggest = 'security_profile'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OSDiskImageEncryptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OSDiskImageEncryptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        OSDiskImageEncryptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, disk_encryption_set_id: Optional[str]=None, security_profile: Optional['outputs.OSDiskImageSecurityProfileResponse']=None):
        """
        Contains encryption settings for an OS disk image.
        :param str disk_encryption_set_id: A relative URI containing the resource ID of the disk encryption set.
        :param 'OSDiskImageSecurityProfileResponse' security_profile: This property specifies the security profile of an OS disk image.
        """
        if disk_encryption_set_id is not None:
            pulumi.set(__self__, 'disk_encryption_set_id', disk_encryption_set_id)
        if security_profile is not None:
            pulumi.set(__self__, 'security_profile', security_profile)

    @property
    @pulumi.getter(name='diskEncryptionSetId')
    def disk_encryption_set_id(self) -> Optional[str]:
        """
        A relative URI containing the resource ID of the disk encryption set.
        """
        return pulumi.get(self, 'disk_encryption_set_id')

    @property
    @pulumi.getter(name='securityProfile')
    def security_profile(self) -> Optional['outputs.OSDiskImageSecurityProfileResponse']:
        """
        This property specifies the security profile of an OS disk image.
        """
        return pulumi.get(self, 'security_profile')

@pulumi.output_type
class OSDiskImageSecurityProfileResponse(dict):
    """
    Contains security profile for an OS disk image.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'confidentialVMEncryptionType':
            suggest = 'confidential_vm_encryption_type'
        elif key == 'secureVMDiskEncryptionSetId':
            suggest = 'secure_vm_disk_encryption_set_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OSDiskImageSecurityProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OSDiskImageSecurityProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        OSDiskImageSecurityProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, confidential_vm_encryption_type: Optional[str]=None, secure_vm_disk_encryption_set_id: Optional[str]=None):
        """
        Contains security profile for an OS disk image.
        :param str confidential_vm_encryption_type: confidential VM encryption types
        :param str secure_vm_disk_encryption_set_id: secure VM disk encryption set id
        """
        if confidential_vm_encryption_type is not None:
            pulumi.set(__self__, 'confidential_vm_encryption_type', confidential_vm_encryption_type)
        if secure_vm_disk_encryption_set_id is not None:
            pulumi.set(__self__, 'secure_vm_disk_encryption_set_id', secure_vm_disk_encryption_set_id)

    @property
    @pulumi.getter(name='confidentialVMEncryptionType')
    def confidential_vm_encryption_type(self) -> Optional[str]:
        """
        confidential VM encryption types
        """
        return pulumi.get(self, 'confidential_vm_encryption_type')

    @property
    @pulumi.getter(name='secureVMDiskEncryptionSetId')
    def secure_vm_disk_encryption_set_id(self) -> Optional[str]:
        """
        secure VM disk encryption set id
        """
        return pulumi.get(self, 'secure_vm_disk_encryption_set_id')

@pulumi.output_type
class RecommendedMachineConfigurationResponse(dict):
    """
    The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'vCPUs':
            suggest = 'v_cpus'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RecommendedMachineConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RecommendedMachineConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        RecommendedMachineConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, memory: Optional['outputs.ResourceRangeResponse']=None, v_cpus: Optional['outputs.ResourceRangeResponse']=None):
        """
        The properties describe the recommended machine configuration for this Image Definition. These properties are updatable.
        :param 'ResourceRangeResponse' memory: Describes the resource range.
        :param 'ResourceRangeResponse' v_cpus: Describes the resource range.
        """
        if memory is not None:
            pulumi.set(__self__, 'memory', memory)
        if v_cpus is not None:
            pulumi.set(__self__, 'v_cpus', v_cpus)

    @property
    @pulumi.getter
    def memory(self) -> Optional['outputs.ResourceRangeResponse']:
        """
        Describes the resource range.
        """
        return pulumi.get(self, 'memory')

    @property
    @pulumi.getter(name='vCPUs')
    def v_cpus(self) -> Optional['outputs.ResourceRangeResponse']:
        """
        Describes the resource range.
        """
        return pulumi.get(self, 'v_cpus')

@pulumi.output_type
class RegionalReplicationStatusResponse(dict):
    """
    This is the regional replication status.
    """

    def __init__(__self__, *, details: str, progress: int, region: str, state: str):
        """
        This is the regional replication status.
        :param str details: The details of the replication status.
        :param int progress: It indicates progress of the replication job.
        :param str region: The region to which the gallery image version is being replicated to.
        :param str state: This is the regional replication state.
        """
        pulumi.set(__self__, 'details', details)
        pulumi.set(__self__, 'progress', progress)
        pulumi.set(__self__, 'region', region)
        pulumi.set(__self__, 'state', state)

    @property
    @pulumi.getter
    def details(self) -> str:
        """
        The details of the replication status.
        """
        return pulumi.get(self, 'details')

    @property
    @pulumi.getter
    def progress(self) -> int:
        """
        It indicates progress of the replication job.
        """
        return pulumi.get(self, 'progress')

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        The region to which the gallery image version is being replicated to.
        """
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        This is the regional replication state.
        """
        return pulumi.get(self, 'state')

@pulumi.output_type
class RegionalSharingStatusResponse(dict):
    """
    Gallery regional sharing status
    """

    def __init__(__self__, *, state: str, details: Optional[str]=None, region: Optional[str]=None):
        """
        Gallery regional sharing status
        :param str state: Gallery sharing state in current region
        :param str details: Details of gallery regional sharing failure.
        :param str region: Region name
        """
        pulumi.set(__self__, 'state', state)
        if details is not None:
            pulumi.set(__self__, 'details', details)
        if region is not None:
            pulumi.set(__self__, 'region', region)

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Gallery sharing state in current region
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter
    def details(self) -> Optional[str]:
        """
        Details of gallery regional sharing failure.
        """
        return pulumi.get(self, 'details')

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        """
        Region name
        """
        return pulumi.get(self, 'region')

@pulumi.output_type
class ReplicationStatusResponse(dict):
    """
    This is the replication status of the gallery image version.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'aggregatedState':
            suggest = 'aggregated_state'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationStatusResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationStatusResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ReplicationStatusResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, aggregated_state: str, summary: Sequence['outputs.RegionalReplicationStatusResponse']):
        """
        This is the replication status of the gallery image version.
        :param str aggregated_state: This is the aggregated replication status based on all the regional replication status flags.
        :param Sequence['RegionalReplicationStatusResponse'] summary: This is a summary of replication status for each region.
        """
        pulumi.set(__self__, 'aggregated_state', aggregated_state)
        pulumi.set(__self__, 'summary', summary)

    @property
    @pulumi.getter(name='aggregatedState')
    def aggregated_state(self) -> str:
        """
        This is the aggregated replication status based on all the regional replication status flags.
        """
        return pulumi.get(self, 'aggregated_state')

    @property
    @pulumi.getter
    def summary(self) -> Sequence['outputs.RegionalReplicationStatusResponse']:
        """
        This is a summary of replication status for each region.
        """
        return pulumi.get(self, 'summary')

@pulumi.output_type
class ResourceRangeResponse(dict):
    """
    Describes the resource range.
    """

    def __init__(__self__, *, max: Optional[int]=None, min: Optional[int]=None):
        """
        Describes the resource range.
        :param int max: The maximum number of the resource.
        :param int min: The minimum number of the resource.
        """
        if max is not None:
            pulumi.set(__self__, 'max', max)
        if min is not None:
            pulumi.set(__self__, 'min', min)

    @property
    @pulumi.getter
    def max(self) -> Optional[int]:
        """
        The maximum number of the resource.
        """
        return pulumi.get(self, 'max')

    @property
    @pulumi.getter
    def min(self) -> Optional[int]:
        """
        The minimum number of the resource.
        """
        return pulumi.get(self, 'min')

@pulumi.output_type
class SharingProfileGroupResponse(dict):
    """
    Group of the gallery sharing profile
    """

    def __init__(__self__, *, ids: Optional[Sequence[str]]=None, type: Optional[str]=None):
        """
        Group of the gallery sharing profile
        :param Sequence[str] ids: A list of subscription/tenant ids the gallery is aimed to be shared to.
        :param str type: This property allows you to specify the type of sharing group. <br><br> Possible values are: <br><br> **Subscriptions** <br><br> **AADTenants** <br><br> **Community**
        """
        if ids is not None:
            pulumi.set(__self__, 'ids', ids)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def ids(self) -> Optional[Sequence[str]]:
        """
        A list of subscription/tenant ids the gallery is aimed to be shared to.
        """
        return pulumi.get(self, 'ids')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        This property allows you to specify the type of sharing group. <br><br> Possible values are: <br><br> **Subscriptions** <br><br> **AADTenants** <br><br> **Community**
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class SharingProfileResponse(dict):
    """
    Profile for gallery sharing to subscription or tenant
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'communityGalleryInfo':
            suggest = 'community_gallery_info'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SharingProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SharingProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SharingProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, groups: Sequence['outputs.SharingProfileGroupResponse'], community_gallery_info: Optional['outputs.CommunityGalleryInfoResponse']=None, permissions: Optional[str]=None):
        """
        Profile for gallery sharing to subscription or tenant
        :param Sequence['SharingProfileGroupResponse'] groups: A list of sharing profile groups.
        :param 'CommunityGalleryInfoResponse' community_gallery_info: Information of community gallery if current gallery is shared to community.
        :param str permissions: This property allows you to specify the permission of sharing gallery. <br><br> Possible values are: <br><br> **Private** <br><br> **Groups**
        """
        pulumi.set(__self__, 'groups', groups)
        if community_gallery_info is not None:
            pulumi.set(__self__, 'community_gallery_info', community_gallery_info)
        if permissions is not None:
            pulumi.set(__self__, 'permissions', permissions)

    @property
    @pulumi.getter
    def groups(self) -> Sequence['outputs.SharingProfileGroupResponse']:
        """
        A list of sharing profile groups.
        """
        return pulumi.get(self, 'groups')

    @property
    @pulumi.getter(name='communityGalleryInfo')
    def community_gallery_info(self) -> Optional['outputs.CommunityGalleryInfoResponse']:
        """
        Information of community gallery if current gallery is shared to community.
        """
        return pulumi.get(self, 'community_gallery_info')

    @property
    @pulumi.getter
    def permissions(self) -> Optional[str]:
        """
        This property allows you to specify the permission of sharing gallery. <br><br> Possible values are: <br><br> **Private** <br><br> **Groups**
        """
        return pulumi.get(self, 'permissions')

@pulumi.output_type
class SharingStatusResponse(dict):
    """
    Sharing status of current gallery.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'aggregatedState':
            suggest = 'aggregated_state'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SharingStatusResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SharingStatusResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SharingStatusResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, aggregated_state: str, summary: Optional[Sequence['outputs.RegionalSharingStatusResponse']]=None):
        """
        Sharing status of current gallery.
        :param str aggregated_state: Aggregated sharing state of current gallery.
        :param Sequence['RegionalSharingStatusResponse'] summary: Summary of all regional sharing status.
        """
        pulumi.set(__self__, 'aggregated_state', aggregated_state)
        if summary is not None:
            pulumi.set(__self__, 'summary', summary)

    @property
    @pulumi.getter(name='aggregatedState')
    def aggregated_state(self) -> str:
        """
        Aggregated sharing state of current gallery.
        """
        return pulumi.get(self, 'aggregated_state')

    @property
    @pulumi.getter
    def summary(self) -> Optional[Sequence['outputs.RegionalSharingStatusResponse']]:
        """
        Summary of all regional sharing status.
        """
        return pulumi.get(self, 'summary')

@pulumi.output_type
class SoftDeletePolicyResponse(dict):
    """
    Contains information about the soft deletion policy of the gallery.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'isSoftDeleteEnabled':
            suggest = 'is_soft_delete_enabled'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SoftDeletePolicyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SoftDeletePolicyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SoftDeletePolicyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, is_soft_delete_enabled: Optional[bool]=None):
        """
        Contains information about the soft deletion policy of the gallery.
        :param bool is_soft_delete_enabled: Enables soft-deletion for resources in this gallery, allowing them to be recovered within retention time.
        """
        if is_soft_delete_enabled is not None:
            pulumi.set(__self__, 'is_soft_delete_enabled', is_soft_delete_enabled)

    @property
    @pulumi.getter(name='isSoftDeleteEnabled')
    def is_soft_delete_enabled(self) -> Optional[bool]:
        """
        Enables soft-deletion for resources in this gallery, allowing them to be recovered within retention time.
        """
        return pulumi.get(self, 'is_soft_delete_enabled')

@pulumi.output_type
class TargetRegionResponse(dict):
    """
    Describes the target region information.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'regionalReplicaCount':
            suggest = 'regional_replica_count'
        elif key == 'storageAccountType':
            suggest = 'storage_account_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TargetRegionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TargetRegionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        TargetRegionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, name: str, encryption: Optional['outputs.EncryptionImagesResponse']=None, regional_replica_count: Optional[int]=None, storage_account_type: Optional[str]=None):
        """
        Describes the target region information.
        :param str name: The name of the region.
        :param 'EncryptionImagesResponse' encryption: Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
        :param int regional_replica_count: The number of replicas of the Image Version to be created per region. This property is updatable.
        :param str storage_account_type: Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        pulumi.set(__self__, 'name', name)
        if encryption is not None:
            pulumi.set(__self__, 'encryption', encryption)
        if regional_replica_count is not None:
            pulumi.set(__self__, 'regional_replica_count', regional_replica_count)
        if storage_account_type is not None:
            pulumi.set(__self__, 'storage_account_type', storage_account_type)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the region.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.EncryptionImagesResponse']:
        """
        Optional. Allows users to provide customer managed keys for encrypting the OS and data disks in the gallery artifact.
        """
        return pulumi.get(self, 'encryption')

    @property
    @pulumi.getter(name='regionalReplicaCount')
    def regional_replica_count(self) -> Optional[int]:
        """
        The number of replicas of the Image Version to be created per region. This property is updatable.
        """
        return pulumi.get(self, 'regional_replica_count')

    @property
    @pulumi.getter(name='storageAccountType')
    def storage_account_type(self) -> Optional[str]:
        """
        Specifies the storage account type to be used to store the image. This property is not updatable.
        """
        return pulumi.get(self, 'storage_account_type')

@pulumi.output_type
class UserArtifactManageResponse(dict):

    def __init__(__self__, *, install: str, remove: str, update: Optional[str]=None):
        """
        :param str install: Required. The path and arguments to install the gallery application. This is limited to 4096 characters.
        :param str remove: Required. The path and arguments to remove the gallery application. This is limited to 4096 characters.
        :param str update: Optional. The path and arguments to update the gallery application. If not present, then update operation will invoke remove command on the previous version and install command on the current version of the gallery application. This is limited to 4096 characters.
        """
        pulumi.set(__self__, 'install', install)
        pulumi.set(__self__, 'remove', remove)
        if update is not None:
            pulumi.set(__self__, 'update', update)

    @property
    @pulumi.getter
    def install(self) -> str:
        """
        Required. The path and arguments to install the gallery application. This is limited to 4096 characters.
        """
        return pulumi.get(self, 'install')

    @property
    @pulumi.getter
    def remove(self) -> str:
        """
        Required. The path and arguments to remove the gallery application. This is limited to 4096 characters.
        """
        return pulumi.get(self, 'remove')

    @property
    @pulumi.getter
    def update(self) -> Optional[str]:
        """
        Optional. The path and arguments to update the gallery application. If not present, then update operation will invoke remove command on the previous version and install command on the current version of the gallery application. This is limited to 4096 characters.
        """
        return pulumi.get(self, 'update')

@pulumi.output_type
class UserArtifactSourceResponse(dict):
    """
    The source image from which the Image Version is going to be created.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'mediaLink':
            suggest = 'media_link'
        elif key == 'defaultConfigurationLink':
            suggest = 'default_configuration_link'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserArtifactSourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserArtifactSourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UserArtifactSourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, media_link: str, default_configuration_link: Optional[str]=None):
        """
        The source image from which the Image Version is going to be created.
        :param str media_link: Required. The mediaLink of the artifact, must be a readable storage page blob.
        :param str default_configuration_link: Optional. The defaultConfigurationLink of the artifact, must be a readable storage page blob.
        """
        pulumi.set(__self__, 'media_link', media_link)
        if default_configuration_link is not None:
            pulumi.set(__self__, 'default_configuration_link', default_configuration_link)

    @property
    @pulumi.getter(name='mediaLink')
    def media_link(self) -> str:
        """
        Required. The mediaLink of the artifact, must be a readable storage page blob.
        """
        return pulumi.get(self, 'media_link')

    @property
    @pulumi.getter(name='defaultConfigurationLink')
    def default_configuration_link(self) -> Optional[str]:
        """
        Optional. The defaultConfigurationLink of the artifact, must be a readable storage page blob.
        """
        return pulumi.get(self, 'default_configuration_link')
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['VirtualMachineArgs', 'VirtualMachine']

@pulumi.input_type
class VirtualMachineArgs:

    def __init__(__self__, *, network_interface_ids: pulumi.Input[Sequence[pulumi.Input[str]]], resource_group_name: pulumi.Input[str], storage_os_disk: pulumi.Input['VirtualMachineStorageOsDiskArgs'], vm_size: pulumi.Input[str], additional_capabilities: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]=None, availability_set_id: Optional[pulumi.Input[str]]=None, boot_diagnostics: Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]=None, delete_data_disks_on_termination: Optional[pulumi.Input[bool]]=None, delete_os_disk_on_termination: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['VirtualMachineIdentityArgs']]=None, license_type: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, os_profile: Optional[pulumi.Input['VirtualMachineOsProfileArgs']]=None, os_profile_linux_config: Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]=None, os_profile_secrets: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]=None, os_profile_windows_config: Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]=None, plan: Optional[pulumi.Input['VirtualMachinePlanArgs']]=None, primary_network_interface_id: Optional[pulumi.Input[str]]=None, proximity_placement_group_id: Optional[pulumi.Input[str]]=None, storage_data_disks: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]=None, storage_image_reference: Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zones: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a VirtualMachine resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_ids: A list of Network Interface IDs which should be associated with the Virtual Machine.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualMachineStorageOsDiskArgs'] storage_os_disk: A `storage_os_disk` block as defined below.
        :param pulumi.Input[str] vm_size: Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        :param pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs'] additional_capabilities: An `additional_capabilities` block as defined below.
        :param pulumi.Input[str] availability_set_id: The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualMachineBootDiagnosticsArgs'] boot_diagnostics: A `boot_diagnostics` block as defined below.
        :param pulumi.Input[bool] delete_data_disks_on_termination: Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[bool] delete_os_disk_on_termination: Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input['VirtualMachineIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualMachineOsProfileArgs'] os_profile: An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        :param pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs'] os_profile_linux_config: An `os_profile_linux_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]] os_profile_secrets: One or more `os_profile_secrets` blocks.
        :param pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs'] os_profile_windows_config: An `os_profile_windows_config` block as defined below.
        :param pulumi.Input['VirtualMachinePlanArgs'] plan: A `plan` block as defined below.
        :param pulumi.Input[str] primary_network_interface_id: The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        :param pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]] storage_data_disks: One or more `storage_data_disk` blocks.
        :param pulumi.Input['VirtualMachineStorageImageReferenceArgs'] storage_image_reference: A `storage_image_reference` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Virtual Machine.
        :param pulumi.Input[str] zones: A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        pulumi.set(__self__, 'network_interface_ids', network_interface_ids)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'storage_os_disk', storage_os_disk)
        pulumi.set(__self__, 'vm_size', vm_size)
        if additional_capabilities is not None:
            pulumi.set(__self__, 'additional_capabilities', additional_capabilities)
        if availability_set_id is not None:
            pulumi.set(__self__, 'availability_set_id', availability_set_id)
        if boot_diagnostics is not None:
            pulumi.set(__self__, 'boot_diagnostics', boot_diagnostics)
        if delete_data_disks_on_termination is not None:
            pulumi.set(__self__, 'delete_data_disks_on_termination', delete_data_disks_on_termination)
        if delete_os_disk_on_termination is not None:
            pulumi.set(__self__, 'delete_os_disk_on_termination', delete_os_disk_on_termination)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if license_type is not None:
            pulumi.set(__self__, 'license_type', license_type)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if os_profile is not None:
            pulumi.set(__self__, 'os_profile', os_profile)
        if os_profile_linux_config is not None:
            pulumi.set(__self__, 'os_profile_linux_config', os_profile_linux_config)
        if os_profile_secrets is not None:
            pulumi.set(__self__, 'os_profile_secrets', os_profile_secrets)
        if os_profile_windows_config is not None:
            pulumi.set(__self__, 'os_profile_windows_config', os_profile_windows_config)
        if plan is not None:
            pulumi.set(__self__, 'plan', plan)
        if primary_network_interface_id is not None:
            pulumi.set(__self__, 'primary_network_interface_id', primary_network_interface_id)
        if proximity_placement_group_id is not None:
            pulumi.set(__self__, 'proximity_placement_group_id', proximity_placement_group_id)
        if storage_data_disks is not None:
            pulumi.set(__self__, 'storage_data_disks', storage_data_disks)
        if storage_image_reference is not None:
            pulumi.set(__self__, 'storage_image_reference', storage_image_reference)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zones is not None:
            pulumi.set(__self__, 'zones', zones)

    @property
    @pulumi.getter(name='networkInterfaceIds')
    def network_interface_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of Network Interface IDs which should be associated with the Virtual Machine.
        """
        return pulumi.get(self, 'network_interface_ids')

    @network_interface_ids.setter
    def network_interface_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'network_interface_ids', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='storageOsDisk')
    def storage_os_disk(self) -> pulumi.Input['VirtualMachineStorageOsDiskArgs']:
        """
        A `storage_os_disk` block as defined below.
        """
        return pulumi.get(self, 'storage_os_disk')

    @storage_os_disk.setter
    def storage_os_disk(self, value: pulumi.Input['VirtualMachineStorageOsDiskArgs']):
        pulumi.set(self, 'storage_os_disk', value)

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> pulumi.Input[str]:
        """
        Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        """
        return pulumi.get(self, 'vm_size')

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[str]):
        pulumi.set(self, 'vm_size', value)

    @property
    @pulumi.getter(name='additionalCapabilities')
    def additional_capabilities(self) -> Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]:
        """
        An `additional_capabilities` block as defined below.
        """
        return pulumi.get(self, 'additional_capabilities')

    @additional_capabilities.setter
    def additional_capabilities(self, value: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]):
        pulumi.set(self, 'additional_capabilities', value)

    @property
    @pulumi.getter(name='availabilitySetId')
    def availability_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'availability_set_id')

    @availability_set_id.setter
    def availability_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'availability_set_id', value)

    @property
    @pulumi.getter(name='bootDiagnostics')
    def boot_diagnostics(self) -> Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]:
        """
        A `boot_diagnostics` block as defined below.
        """
        return pulumi.get(self, 'boot_diagnostics')

    @boot_diagnostics.setter
    def boot_diagnostics(self, value: Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]):
        pulumi.set(self, 'boot_diagnostics', value)

    @property
    @pulumi.getter(name='deleteDataDisksOnTermination')
    def delete_data_disks_on_termination(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_data_disks_on_termination')

    @delete_data_disks_on_termination.setter
    def delete_data_disks_on_termination(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'delete_data_disks_on_termination', value)

    @property
    @pulumi.getter(name='deleteOsDiskOnTermination')
    def delete_os_disk_on_termination(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_os_disk_on_termination')

    @delete_os_disk_on_termination.setter
    def delete_os_disk_on_termination(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'delete_os_disk_on_termination', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['VirtualMachineIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['VirtualMachineIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='licenseType')
    def license_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        """
        return pulumi.get(self, 'license_type')

    @license_type.setter
    def license_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'license_type', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='osProfile')
    def os_profile(self) -> Optional[pulumi.Input['VirtualMachineOsProfileArgs']]:
        """
        An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        """
        return pulumi.get(self, 'os_profile')

    @os_profile.setter
    def os_profile(self, value: Optional[pulumi.Input['VirtualMachineOsProfileArgs']]):
        pulumi.set(self, 'os_profile', value)

    @property
    @pulumi.getter(name='osProfileLinuxConfig')
    def os_profile_linux_config(self) -> Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]:
        """
        An `os_profile_linux_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_linux_config')

    @os_profile_linux_config.setter
    def os_profile_linux_config(self, value: Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]):
        pulumi.set(self, 'os_profile_linux_config', value)

    @property
    @pulumi.getter(name='osProfileSecrets')
    def os_profile_secrets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]:
        """
        One or more `os_profile_secrets` blocks.
        """
        return pulumi.get(self, 'os_profile_secrets')

    @os_profile_secrets.setter
    def os_profile_secrets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]):
        pulumi.set(self, 'os_profile_secrets', value)

    @property
    @pulumi.getter(name='osProfileWindowsConfig')
    def os_profile_windows_config(self) -> Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]:
        """
        An `os_profile_windows_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_windows_config')

    @os_profile_windows_config.setter
    def os_profile_windows_config(self, value: Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]):
        pulumi.set(self, 'os_profile_windows_config', value)

    @property
    @pulumi.getter
    def plan(self) -> Optional[pulumi.Input['VirtualMachinePlanArgs']]:
        """
        A `plan` block as defined below.
        """
        return pulumi.get(self, 'plan')

    @plan.setter
    def plan(self, value: Optional[pulumi.Input['VirtualMachinePlanArgs']]):
        pulumi.set(self, 'plan', value)

    @property
    @pulumi.getter(name='primaryNetworkInterfaceId')
    def primary_network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        """
        return pulumi.get(self, 'primary_network_interface_id')

    @primary_network_interface_id.setter
    def primary_network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'primary_network_interface_id', value)

    @property
    @pulumi.getter(name='proximityPlacementGroupId')
    def proximity_placement_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        """
        return pulumi.get(self, 'proximity_placement_group_id')

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'proximity_placement_group_id', value)

    @property
    @pulumi.getter(name='storageDataDisks')
    def storage_data_disks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]:
        """
        One or more `storage_data_disk` blocks.
        """
        return pulumi.get(self, 'storage_data_disks')

    @storage_data_disks.setter
    def storage_data_disks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]):
        pulumi.set(self, 'storage_data_disks', value)

    @property
    @pulumi.getter(name='storageImageReference')
    def storage_image_reference(self) -> Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]:
        """
        A `storage_image_reference` block as defined below.
        """
        return pulumi.get(self, 'storage_image_reference')

    @storage_image_reference.setter
    def storage_image_reference(self, value: Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]):
        pulumi.set(self, 'storage_image_reference', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Virtual Machine.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[str]]:
        """
        A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        return pulumi.get(self, 'zones')

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zones', value)

@pulumi.input_type
class _VirtualMachineState:

    def __init__(__self__, *, additional_capabilities: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]=None, availability_set_id: Optional[pulumi.Input[str]]=None, boot_diagnostics: Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]=None, delete_data_disks_on_termination: Optional[pulumi.Input[bool]]=None, delete_os_disk_on_termination: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['VirtualMachineIdentityArgs']]=None, license_type: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_interface_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, os_profile: Optional[pulumi.Input['VirtualMachineOsProfileArgs']]=None, os_profile_linux_config: Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]=None, os_profile_secrets: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]=None, os_profile_windows_config: Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]=None, plan: Optional[pulumi.Input['VirtualMachinePlanArgs']]=None, primary_network_interface_id: Optional[pulumi.Input[str]]=None, proximity_placement_group_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_data_disks: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]=None, storage_image_reference: Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]=None, storage_os_disk: Optional[pulumi.Input['VirtualMachineStorageOsDiskArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vm_size: Optional[pulumi.Input[str]]=None, zones: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering VirtualMachine resources.
        :param pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs'] additional_capabilities: An `additional_capabilities` block as defined below.
        :param pulumi.Input[str] availability_set_id: The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input['VirtualMachineBootDiagnosticsArgs'] boot_diagnostics: A `boot_diagnostics` block as defined below.
        :param pulumi.Input[bool] delete_data_disks_on_termination: Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[bool] delete_os_disk_on_termination: Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input['VirtualMachineIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_ids: A list of Network Interface IDs which should be associated with the Virtual Machine.
        :param pulumi.Input['VirtualMachineOsProfileArgs'] os_profile: An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        :param pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs'] os_profile_linux_config: An `os_profile_linux_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]] os_profile_secrets: One or more `os_profile_secrets` blocks.
        :param pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs'] os_profile_windows_config: An `os_profile_windows_config` block as defined below.
        :param pulumi.Input['VirtualMachinePlanArgs'] plan: A `plan` block as defined below.
        :param pulumi.Input[str] primary_network_interface_id: The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]] storage_data_disks: One or more `storage_data_disk` blocks.
        :param pulumi.Input['VirtualMachineStorageImageReferenceArgs'] storage_image_reference: A `storage_image_reference` block as defined below.
        :param pulumi.Input['VirtualMachineStorageOsDiskArgs'] storage_os_disk: A `storage_os_disk` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Virtual Machine.
        :param pulumi.Input[str] vm_size: Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        :param pulumi.Input[str] zones: A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        if additional_capabilities is not None:
            pulumi.set(__self__, 'additional_capabilities', additional_capabilities)
        if availability_set_id is not None:
            pulumi.set(__self__, 'availability_set_id', availability_set_id)
        if boot_diagnostics is not None:
            pulumi.set(__self__, 'boot_diagnostics', boot_diagnostics)
        if delete_data_disks_on_termination is not None:
            pulumi.set(__self__, 'delete_data_disks_on_termination', delete_data_disks_on_termination)
        if delete_os_disk_on_termination is not None:
            pulumi.set(__self__, 'delete_os_disk_on_termination', delete_os_disk_on_termination)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if license_type is not None:
            pulumi.set(__self__, 'license_type', license_type)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if network_interface_ids is not None:
            pulumi.set(__self__, 'network_interface_ids', network_interface_ids)
        if os_profile is not None:
            pulumi.set(__self__, 'os_profile', os_profile)
        if os_profile_linux_config is not None:
            pulumi.set(__self__, 'os_profile_linux_config', os_profile_linux_config)
        if os_profile_secrets is not None:
            pulumi.set(__self__, 'os_profile_secrets', os_profile_secrets)
        if os_profile_windows_config is not None:
            pulumi.set(__self__, 'os_profile_windows_config', os_profile_windows_config)
        if plan is not None:
            pulumi.set(__self__, 'plan', plan)
        if primary_network_interface_id is not None:
            pulumi.set(__self__, 'primary_network_interface_id', primary_network_interface_id)
        if proximity_placement_group_id is not None:
            pulumi.set(__self__, 'proximity_placement_group_id', proximity_placement_group_id)
        if resource_group_name is not None:
            pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if storage_data_disks is not None:
            pulumi.set(__self__, 'storage_data_disks', storage_data_disks)
        if storage_image_reference is not None:
            pulumi.set(__self__, 'storage_image_reference', storage_image_reference)
        if storage_os_disk is not None:
            pulumi.set(__self__, 'storage_os_disk', storage_os_disk)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if vm_size is not None:
            pulumi.set(__self__, 'vm_size', vm_size)
        if zones is not None:
            pulumi.set(__self__, 'zones', zones)

    @property
    @pulumi.getter(name='additionalCapabilities')
    def additional_capabilities(self) -> Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]:
        """
        An `additional_capabilities` block as defined below.
        """
        return pulumi.get(self, 'additional_capabilities')

    @additional_capabilities.setter
    def additional_capabilities(self, value: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]):
        pulumi.set(self, 'additional_capabilities', value)

    @property
    @pulumi.getter(name='availabilitySetId')
    def availability_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'availability_set_id')

    @availability_set_id.setter
    def availability_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'availability_set_id', value)

    @property
    @pulumi.getter(name='bootDiagnostics')
    def boot_diagnostics(self) -> Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]:
        """
        A `boot_diagnostics` block as defined below.
        """
        return pulumi.get(self, 'boot_diagnostics')

    @boot_diagnostics.setter
    def boot_diagnostics(self, value: Optional[pulumi.Input['VirtualMachineBootDiagnosticsArgs']]):
        pulumi.set(self, 'boot_diagnostics', value)

    @property
    @pulumi.getter(name='deleteDataDisksOnTermination')
    def delete_data_disks_on_termination(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_data_disks_on_termination')

    @delete_data_disks_on_termination.setter
    def delete_data_disks_on_termination(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'delete_data_disks_on_termination', value)

    @property
    @pulumi.getter(name='deleteOsDiskOnTermination')
    def delete_os_disk_on_termination(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_os_disk_on_termination')

    @delete_os_disk_on_termination.setter
    def delete_os_disk_on_termination(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'delete_os_disk_on_termination', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['VirtualMachineIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['VirtualMachineIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='licenseType')
    def license_type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        """
        return pulumi.get(self, 'license_type')

    @license_type.setter
    def license_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'license_type', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='networkInterfaceIds')
    def network_interface_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of Network Interface IDs which should be associated with the Virtual Machine.
        """
        return pulumi.get(self, 'network_interface_ids')

    @network_interface_ids.setter
    def network_interface_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'network_interface_ids', value)

    @property
    @pulumi.getter(name='osProfile')
    def os_profile(self) -> Optional[pulumi.Input['VirtualMachineOsProfileArgs']]:
        """
        An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        """
        return pulumi.get(self, 'os_profile')

    @os_profile.setter
    def os_profile(self, value: Optional[pulumi.Input['VirtualMachineOsProfileArgs']]):
        pulumi.set(self, 'os_profile', value)

    @property
    @pulumi.getter(name='osProfileLinuxConfig')
    def os_profile_linux_config(self) -> Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]:
        """
        An `os_profile_linux_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_linux_config')

    @os_profile_linux_config.setter
    def os_profile_linux_config(self, value: Optional[pulumi.Input['VirtualMachineOsProfileLinuxConfigArgs']]):
        pulumi.set(self, 'os_profile_linux_config', value)

    @property
    @pulumi.getter(name='osProfileSecrets')
    def os_profile_secrets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]:
        """
        One or more `os_profile_secrets` blocks.
        """
        return pulumi.get(self, 'os_profile_secrets')

    @os_profile_secrets.setter
    def os_profile_secrets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineOsProfileSecretArgs']]]]):
        pulumi.set(self, 'os_profile_secrets', value)

    @property
    @pulumi.getter(name='osProfileWindowsConfig')
    def os_profile_windows_config(self) -> Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]:
        """
        An `os_profile_windows_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_windows_config')

    @os_profile_windows_config.setter
    def os_profile_windows_config(self, value: Optional[pulumi.Input['VirtualMachineOsProfileWindowsConfigArgs']]):
        pulumi.set(self, 'os_profile_windows_config', value)

    @property
    @pulumi.getter
    def plan(self) -> Optional[pulumi.Input['VirtualMachinePlanArgs']]:
        """
        A `plan` block as defined below.
        """
        return pulumi.get(self, 'plan')

    @plan.setter
    def plan(self, value: Optional[pulumi.Input['VirtualMachinePlanArgs']]):
        pulumi.set(self, 'plan', value)

    @property
    @pulumi.getter(name='primaryNetworkInterfaceId')
    def primary_network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        """
        return pulumi.get(self, 'primary_network_interface_id')

    @primary_network_interface_id.setter
    def primary_network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'primary_network_interface_id', value)

    @property
    @pulumi.getter(name='proximityPlacementGroupId')
    def proximity_placement_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        """
        return pulumi.get(self, 'proximity_placement_group_id')

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'proximity_placement_group_id', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='storageDataDisks')
    def storage_data_disks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]:
        """
        One or more `storage_data_disk` blocks.
        """
        return pulumi.get(self, 'storage_data_disks')

    @storage_data_disks.setter
    def storage_data_disks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualMachineStorageDataDiskArgs']]]]):
        pulumi.set(self, 'storage_data_disks', value)

    @property
    @pulumi.getter(name='storageImageReference')
    def storage_image_reference(self) -> Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]:
        """
        A `storage_image_reference` block as defined below.
        """
        return pulumi.get(self, 'storage_image_reference')

    @storage_image_reference.setter
    def storage_image_reference(self, value: Optional[pulumi.Input['VirtualMachineStorageImageReferenceArgs']]):
        pulumi.set(self, 'storage_image_reference', value)

    @property
    @pulumi.getter(name='storageOsDisk')
    def storage_os_disk(self) -> Optional[pulumi.Input['VirtualMachineStorageOsDiskArgs']]:
        """
        A `storage_os_disk` block as defined below.
        """
        return pulumi.get(self, 'storage_os_disk')

    @storage_os_disk.setter
    def storage_os_disk(self, value: Optional[pulumi.Input['VirtualMachineStorageOsDiskArgs']]):
        pulumi.set(self, 'storage_os_disk', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the Virtual Machine.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        """
        return pulumi.get(self, 'vm_size')

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vm_size', value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[str]]:
        """
        A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        return pulumi.get(self, 'zones')

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zones', value)

class VirtualMachine(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, additional_capabilities: Optional[pulumi.Input[pulumi.InputType['VirtualMachineAdditionalCapabilitiesArgs']]]=None, availability_set_id: Optional[pulumi.Input[str]]=None, boot_diagnostics: Optional[pulumi.Input[pulumi.InputType['VirtualMachineBootDiagnosticsArgs']]]=None, delete_data_disks_on_termination: Optional[pulumi.Input[bool]]=None, delete_os_disk_on_termination: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['VirtualMachineIdentityArgs']]]=None, license_type: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_interface_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, os_profile: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileArgs']]]=None, os_profile_linux_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileLinuxConfigArgs']]]=None, os_profile_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileSecretArgs']]]]]=None, os_profile_windows_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileWindowsConfigArgs']]]=None, plan: Optional[pulumi.Input[pulumi.InputType['VirtualMachinePlanArgs']]]=None, primary_network_interface_id: Optional[pulumi.Input[str]]=None, proximity_placement_group_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_data_disks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineStorageDataDiskArgs']]]]]=None, storage_image_reference: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageImageReferenceArgs']]]=None, storage_os_disk: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageOsDiskArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vm_size: Optional[pulumi.Input[str]]=None, zones: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Manages a Virtual Machine.

        ## Disclaimers

        > **Note:** The `compute.VirtualMachine` resource has been superseded by the `compute.LinuxVirtualMachine` and `compute.WindowsVirtualMachine` resources. The existing `compute.VirtualMachine` resource will continue to be available throughout the 2.x releases however is in a feature-frozen state to maintain compatibility - new functionality will instead be added to the `compute.LinuxVirtualMachine` and `compute.WindowsVirtualMachine` resources.

        > **Note:** Data Disks can be attached either directly on the `compute.VirtualMachine` resource, or using the `compute.DataDiskAttachment` resource - but the two cannot be used together. If both are used against the same Virtual Machine, spurious changes will occur.

        ## Example Usage
        ### From An Azure Platform Image)

        This example provisions a Virtual Machine with Managed Disks.

        ```python
        import pulumi
        import pulumi_azure as azure

        config = pulumi.Config()
        prefix = config.get("prefix")
        if prefix is None:
            prefix = "tfvmex"
        example = azure.core.ResourceGroup("example", location="West Europe")
        main_virtual_network = azure.network.VirtualNetwork("mainVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example.location,
            resource_group_name=example.name)
        internal = azure.network.Subnet("internal",
            resource_group_name=example.name,
            virtual_network_name=azurerm_virtual_network["example"]["name"],
            address_prefixes=["10.0.2.0/24"])
        main_network_interface = azure.network.NetworkInterface("mainNetworkInterface",
            location=example.location,
            resource_group_name=example.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=internal.id,
                private_ip_address_allocation="Dynamic",
            )])
        main_virtual_machine = azure.compute.VirtualMachine("mainVirtualMachine",
            location=example.location,
            resource_group_name=example.name,
            network_interface_ids=[main_network_interface.id],
            vm_size="Standard_DS1_v2",
            storage_image_reference=azure.compute.VirtualMachineStorageImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            storage_os_disk=azure.compute.VirtualMachineStorageOsDiskArgs(
                name="myosdisk1",
                caching="ReadWrite",
                create_option="FromImage",
                managed_disk_type="Standard_LRS",
            ),
            os_profile=azure.compute.VirtualMachineOsProfileArgs(
                computer_name="hostname",
                admin_username="testadmin",
                admin_password="Password1234!",
            ),
            os_profile_linux_config=azure.compute.VirtualMachineOsProfileLinuxConfigArgs(
                disable_password_authentication=False,
            ),
            tags={
                "environment": "staging",
            })
        ```

        ## Import

        Virtual Machines can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:compute/virtualMachine:VirtualMachine example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Compute/virtualMachines/machine1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['VirtualMachineAdditionalCapabilitiesArgs']] additional_capabilities: An `additional_capabilities` block as defined below.
        :param pulumi.Input[str] availability_set_id: The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['VirtualMachineBootDiagnosticsArgs']] boot_diagnostics: A `boot_diagnostics` block as defined below.
        :param pulumi.Input[bool] delete_data_disks_on_termination: Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[bool] delete_os_disk_on_termination: Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[pulumi.InputType['VirtualMachineIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_ids: A list of Network Interface IDs which should be associated with the Virtual Machine.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileArgs']] os_profile: An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileLinuxConfigArgs']] os_profile_linux_config: An `os_profile_linux_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileSecretArgs']]]] os_profile_secrets: One or more `os_profile_secrets` blocks.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileWindowsConfigArgs']] os_profile_windows_config: An `os_profile_windows_config` block as defined below.
        :param pulumi.Input[pulumi.InputType['VirtualMachinePlanArgs']] plan: A `plan` block as defined below.
        :param pulumi.Input[str] primary_network_interface_id: The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineStorageDataDiskArgs']]]] storage_data_disks: One or more `storage_data_disk` blocks.
        :param pulumi.Input[pulumi.InputType['VirtualMachineStorageImageReferenceArgs']] storage_image_reference: A `storage_image_reference` block as defined below.
        :param pulumi.Input[pulumi.InputType['VirtualMachineStorageOsDiskArgs']] storage_os_disk: A `storage_os_disk` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Virtual Machine.
        :param pulumi.Input[str] vm_size: Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        :param pulumi.Input[str] zones: A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: VirtualMachineArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages a Virtual Machine.

        ## Disclaimers

        > **Note:** The `compute.VirtualMachine` resource has been superseded by the `compute.LinuxVirtualMachine` and `compute.WindowsVirtualMachine` resources. The existing `compute.VirtualMachine` resource will continue to be available throughout the 2.x releases however is in a feature-frozen state to maintain compatibility - new functionality will instead be added to the `compute.LinuxVirtualMachine` and `compute.WindowsVirtualMachine` resources.

        > **Note:** Data Disks can be attached either directly on the `compute.VirtualMachine` resource, or using the `compute.DataDiskAttachment` resource - but the two cannot be used together. If both are used against the same Virtual Machine, spurious changes will occur.

        ## Example Usage
        ### From An Azure Platform Image)

        This example provisions a Virtual Machine with Managed Disks.

        ```python
        import pulumi
        import pulumi_azure as azure

        config = pulumi.Config()
        prefix = config.get("prefix")
        if prefix is None:
            prefix = "tfvmex"
        example = azure.core.ResourceGroup("example", location="West Europe")
        main_virtual_network = azure.network.VirtualNetwork("mainVirtualNetwork",
            address_spaces=["10.0.0.0/16"],
            location=example.location,
            resource_group_name=example.name)
        internal = azure.network.Subnet("internal",
            resource_group_name=example.name,
            virtual_network_name=azurerm_virtual_network["example"]["name"],
            address_prefixes=["10.0.2.0/24"])
        main_network_interface = azure.network.NetworkInterface("mainNetworkInterface",
            location=example.location,
            resource_group_name=example.name,
            ip_configurations=[azure.network.NetworkInterfaceIpConfigurationArgs(
                name="testconfiguration1",
                subnet_id=internal.id,
                private_ip_address_allocation="Dynamic",
            )])
        main_virtual_machine = azure.compute.VirtualMachine("mainVirtualMachine",
            location=example.location,
            resource_group_name=example.name,
            network_interface_ids=[main_network_interface.id],
            vm_size="Standard_DS1_v2",
            storage_image_reference=azure.compute.VirtualMachineStorageImageReferenceArgs(
                publisher="Canonical",
                offer="UbuntuServer",
                sku="16.04-LTS",
                version="latest",
            ),
            storage_os_disk=azure.compute.VirtualMachineStorageOsDiskArgs(
                name="myosdisk1",
                caching="ReadWrite",
                create_option="FromImage",
                managed_disk_type="Standard_LRS",
            ),
            os_profile=azure.compute.VirtualMachineOsProfileArgs(
                computer_name="hostname",
                admin_username="testadmin",
                admin_password="Password1234!",
            ),
            os_profile_linux_config=azure.compute.VirtualMachineOsProfileLinuxConfigArgs(
                disable_password_authentication=False,
            ),
            tags={
                "environment": "staging",
            })
        ```

        ## Import

        Virtual Machines can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:compute/virtualMachine:VirtualMachine example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Compute/virtualMachines/machine1
        ```

        :param str resource_name: The name of the resource.
        :param VirtualMachineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualMachineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, additional_capabilities: Optional[pulumi.Input[pulumi.InputType['VirtualMachineAdditionalCapabilitiesArgs']]]=None, availability_set_id: Optional[pulumi.Input[str]]=None, boot_diagnostics: Optional[pulumi.Input[pulumi.InputType['VirtualMachineBootDiagnosticsArgs']]]=None, delete_data_disks_on_termination: Optional[pulumi.Input[bool]]=None, delete_os_disk_on_termination: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['VirtualMachineIdentityArgs']]]=None, license_type: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_interface_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, os_profile: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileArgs']]]=None, os_profile_linux_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileLinuxConfigArgs']]]=None, os_profile_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileSecretArgs']]]]]=None, os_profile_windows_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileWindowsConfigArgs']]]=None, plan: Optional[pulumi.Input[pulumi.InputType['VirtualMachinePlanArgs']]]=None, primary_network_interface_id: Optional[pulumi.Input[str]]=None, proximity_placement_group_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_data_disks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineStorageDataDiskArgs']]]]]=None, storage_image_reference: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageImageReferenceArgs']]]=None, storage_os_disk: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageOsDiskArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vm_size: Optional[pulumi.Input[str]]=None, zones: Optional[pulumi.Input[str]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualMachineArgs.__new__(VirtualMachineArgs)
            __props__.__dict__['additional_capabilities'] = additional_capabilities
            __props__.__dict__['availability_set_id'] = availability_set_id
            __props__.__dict__['boot_diagnostics'] = boot_diagnostics
            __props__.__dict__['delete_data_disks_on_termination'] = delete_data_disks_on_termination
            __props__.__dict__['delete_os_disk_on_termination'] = delete_os_disk_on_termination
            __props__.__dict__['identity'] = identity
            __props__.__dict__['license_type'] = license_type
            __props__.__dict__['location'] = location
            __props__.__dict__['name'] = name
            if network_interface_ids is None and (not opts.urn):
                raise TypeError("Missing required property 'network_interface_ids'")
            __props__.__dict__['network_interface_ids'] = network_interface_ids
            __props__.__dict__['os_profile'] = os_profile
            __props__.__dict__['os_profile_linux_config'] = os_profile_linux_config
            __props__.__dict__['os_profile_secrets'] = os_profile_secrets
            __props__.__dict__['os_profile_windows_config'] = os_profile_windows_config
            __props__.__dict__['plan'] = plan
            __props__.__dict__['primary_network_interface_id'] = primary_network_interface_id
            __props__.__dict__['proximity_placement_group_id'] = proximity_placement_group_id
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['storage_data_disks'] = storage_data_disks
            __props__.__dict__['storage_image_reference'] = storage_image_reference
            if storage_os_disk is None and (not opts.urn):
                raise TypeError("Missing required property 'storage_os_disk'")
            __props__.__dict__['storage_os_disk'] = storage_os_disk
            __props__.__dict__['tags'] = tags
            if vm_size is None and (not opts.urn):
                raise TypeError("Missing required property 'vm_size'")
            __props__.__dict__['vm_size'] = vm_size
            __props__.__dict__['zones'] = zones
        super(VirtualMachine, __self__).__init__('azure:compute/virtualMachine:VirtualMachine', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, additional_capabilities: Optional[pulumi.Input[pulumi.InputType['VirtualMachineAdditionalCapabilitiesArgs']]]=None, availability_set_id: Optional[pulumi.Input[str]]=None, boot_diagnostics: Optional[pulumi.Input[pulumi.InputType['VirtualMachineBootDiagnosticsArgs']]]=None, delete_data_disks_on_termination: Optional[pulumi.Input[bool]]=None, delete_os_disk_on_termination: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['VirtualMachineIdentityArgs']]]=None, license_type: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_interface_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, os_profile: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileArgs']]]=None, os_profile_linux_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileLinuxConfigArgs']]]=None, os_profile_secrets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileSecretArgs']]]]]=None, os_profile_windows_config: Optional[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileWindowsConfigArgs']]]=None, plan: Optional[pulumi.Input[pulumi.InputType['VirtualMachinePlanArgs']]]=None, primary_network_interface_id: Optional[pulumi.Input[str]]=None, proximity_placement_group_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, storage_data_disks: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineStorageDataDiskArgs']]]]]=None, storage_image_reference: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageImageReferenceArgs']]]=None, storage_os_disk: Optional[pulumi.Input[pulumi.InputType['VirtualMachineStorageOsDiskArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vm_size: Optional[pulumi.Input[str]]=None, zones: Optional[pulumi.Input[str]]=None) -> 'VirtualMachine':
        """
        Get an existing VirtualMachine resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['VirtualMachineAdditionalCapabilitiesArgs']] additional_capabilities: An `additional_capabilities` block as defined below.
        :param pulumi.Input[str] availability_set_id: The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['VirtualMachineBootDiagnosticsArgs']] boot_diagnostics: A `boot_diagnostics` block as defined below.
        :param pulumi.Input[bool] delete_data_disks_on_termination: Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[bool] delete_os_disk_on_termination: Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        :param pulumi.Input[pulumi.InputType['VirtualMachineIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] license_type: Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        :param pulumi.Input[str] location: Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] network_interface_ids: A list of Network Interface IDs which should be associated with the Virtual Machine.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileArgs']] os_profile: An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileLinuxConfigArgs']] os_profile_linux_config: An `os_profile_linux_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineOsProfileSecretArgs']]]] os_profile_secrets: One or more `os_profile_secrets` blocks.
        :param pulumi.Input[pulumi.InputType['VirtualMachineOsProfileWindowsConfigArgs']] os_profile_windows_config: An `os_profile_windows_config` block as defined below.
        :param pulumi.Input[pulumi.InputType['VirtualMachinePlanArgs']] plan: A `plan` block as defined below.
        :param pulumi.Input[str] primary_network_interface_id: The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        :param pulumi.Input[str] proximity_placement_group_id: The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualMachineStorageDataDiskArgs']]]] storage_data_disks: One or more `storage_data_disk` blocks.
        :param pulumi.Input[pulumi.InputType['VirtualMachineStorageImageReferenceArgs']] storage_image_reference: A `storage_image_reference` block as defined below.
        :param pulumi.Input[pulumi.InputType['VirtualMachineStorageOsDiskArgs']] storage_os_disk: A `storage_os_disk` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the Virtual Machine.
        :param pulumi.Input[str] vm_size: Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        :param pulumi.Input[str] zones: A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _VirtualMachineState.__new__(_VirtualMachineState)
        __props__.__dict__['additional_capabilities'] = additional_capabilities
        __props__.__dict__['availability_set_id'] = availability_set_id
        __props__.__dict__['boot_diagnostics'] = boot_diagnostics
        __props__.__dict__['delete_data_disks_on_termination'] = delete_data_disks_on_termination
        __props__.__dict__['delete_os_disk_on_termination'] = delete_os_disk_on_termination
        __props__.__dict__['identity'] = identity
        __props__.__dict__['license_type'] = license_type
        __props__.__dict__['location'] = location
        __props__.__dict__['name'] = name
        __props__.__dict__['network_interface_ids'] = network_interface_ids
        __props__.__dict__['os_profile'] = os_profile
        __props__.__dict__['os_profile_linux_config'] = os_profile_linux_config
        __props__.__dict__['os_profile_secrets'] = os_profile_secrets
        __props__.__dict__['os_profile_windows_config'] = os_profile_windows_config
        __props__.__dict__['plan'] = plan
        __props__.__dict__['primary_network_interface_id'] = primary_network_interface_id
        __props__.__dict__['proximity_placement_group_id'] = proximity_placement_group_id
        __props__.__dict__['resource_group_name'] = resource_group_name
        __props__.__dict__['storage_data_disks'] = storage_data_disks
        __props__.__dict__['storage_image_reference'] = storage_image_reference
        __props__.__dict__['storage_os_disk'] = storage_os_disk
        __props__.__dict__['tags'] = tags
        __props__.__dict__['vm_size'] = vm_size
        __props__.__dict__['zones'] = zones
        return VirtualMachine(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='additionalCapabilities')
    def additional_capabilities(self) -> pulumi.Output[Optional['outputs.VirtualMachineAdditionalCapabilities']]:
        """
        An `additional_capabilities` block as defined below.
        """
        return pulumi.get(self, 'additional_capabilities')

    @property
    @pulumi.getter(name='availabilitySetId')
    def availability_set_id(self) -> pulumi.Output[str]:
        """
        The ID of the Availability Set in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'availability_set_id')

    @property
    @pulumi.getter(name='bootDiagnostics')
    def boot_diagnostics(self) -> pulumi.Output[Optional['outputs.VirtualMachineBootDiagnostics']]:
        """
        A `boot_diagnostics` block as defined below.
        """
        return pulumi.get(self, 'boot_diagnostics')

    @property
    @pulumi.getter(name='deleteDataDisksOnTermination')
    def delete_data_disks_on_termination(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Data Disks (either the Managed Disks / VHD Blobs) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_data_disks_on_termination')

    @property
    @pulumi.getter(name='deleteOsDiskOnTermination')
    def delete_os_disk_on_termination(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the OS Disk (either the Managed Disk / VHD Blob) be deleted when the Virtual Machine is destroyed? Defaults to `false`.
        """
        return pulumi.get(self, 'delete_os_disk_on_termination')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.VirtualMachineIdentity']:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='licenseType')
    def license_type(self) -> pulumi.Output[str]:
        """
        Specifies the BYOL Type for this Virtual Machine. This is only applicable to Windows Virtual Machines. Possible values are `Windows_Client` and `Windows_Server`.
        """
        return pulumi.get(self, 'license_type')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the Azure Region where the Virtual Machine exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Virtual Machine. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='networkInterfaceIds')
    def network_interface_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of Network Interface IDs which should be associated with the Virtual Machine.
        """
        return pulumi.get(self, 'network_interface_ids')

    @property
    @pulumi.getter(name='osProfile')
    def os_profile(self) -> pulumi.Output[Optional['outputs.VirtualMachineOsProfile']]:
        """
        An `os_profile` block as defined below. Required when `create_option` in the `storage_os_disk` block is set to `FromImage`.
        """
        return pulumi.get(self, 'os_profile')

    @property
    @pulumi.getter(name='osProfileLinuxConfig')
    def os_profile_linux_config(self) -> pulumi.Output[Optional['outputs.VirtualMachineOsProfileLinuxConfig']]:
        """
        An `os_profile_linux_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_linux_config')

    @property
    @pulumi.getter(name='osProfileSecrets')
    def os_profile_secrets(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualMachineOsProfileSecret']]]:
        """
        One or more `os_profile_secrets` blocks.
        """
        return pulumi.get(self, 'os_profile_secrets')

    @property
    @pulumi.getter(name='osProfileWindowsConfig')
    def os_profile_windows_config(self) -> pulumi.Output[Optional['outputs.VirtualMachineOsProfileWindowsConfig']]:
        """
        An `os_profile_windows_config` block as defined below.
        """
        return pulumi.get(self, 'os_profile_windows_config')

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output[Optional['outputs.VirtualMachinePlan']]:
        """
        A `plan` block as defined below.
        """
        return pulumi.get(self, 'plan')

    @property
    @pulumi.getter(name='primaryNetworkInterfaceId')
    def primary_network_interface_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Network Interface (which must be attached to the Virtual Machine) which should be the Primary Network Interface for this Virtual Machine.
        """
        return pulumi.get(self, 'primary_network_interface_id')

    @property
    @pulumi.getter(name='proximityPlacementGroupId')
    def proximity_placement_group_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the Proximity Placement Group to which this Virtual Machine should be assigned. Changing this forces a new resource to be created
        """
        return pulumi.get(self, 'proximity_placement_group_id')

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Resource Group in which the Virtual Machine should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @property
    @pulumi.getter(name='storageDataDisks')
    def storage_data_disks(self) -> pulumi.Output[Sequence['outputs.VirtualMachineStorageDataDisk']]:
        """
        One or more `storage_data_disk` blocks.
        """
        return pulumi.get(self, 'storage_data_disks')

    @property
    @pulumi.getter(name='storageImageReference')
    def storage_image_reference(self) -> pulumi.Output['outputs.VirtualMachineStorageImageReference']:
        """
        A `storage_image_reference` block as defined below.
        """
        return pulumi.get(self, 'storage_image_reference')

    @property
    @pulumi.getter(name='storageOsDisk')
    def storage_os_disk(self) -> pulumi.Output['outputs.VirtualMachineStorageOsDisk']:
        """
        A `storage_os_disk` block as defined below.
        """
        return pulumi.get(self, 'storage_os_disk')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the Virtual Machine.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='vmSize')
    def vm_size(self) -> pulumi.Output[str]:
        """
        Specifies the [size of the Virtual Machine](https://docs.microsoft.com/azure/virtual-machines/sizes-general). See also [Azure VM Naming Conventions](https://docs.microsoft.com/azure/virtual-machines/vm-naming-conventions).
        """
        return pulumi.get(self, 'vm_size')

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[str]]:
        """
        A list of a single item of the Availability Zone which the Virtual Machine should be allocated in.
        """
        return pulumi.get(self, 'zones')
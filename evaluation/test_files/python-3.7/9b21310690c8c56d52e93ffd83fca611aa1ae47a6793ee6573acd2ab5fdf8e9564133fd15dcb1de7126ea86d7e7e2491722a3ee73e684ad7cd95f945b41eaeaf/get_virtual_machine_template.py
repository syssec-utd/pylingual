import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetVirtualMachineTemplateResult', 'AwaitableGetVirtualMachineTemplateResult', 'get_virtual_machine_template', 'get_virtual_machine_template_output']

@pulumi.output_type
class GetVirtualMachineTemplateResult:
    """
    The VirtualMachineTemplates resource definition.
    """

    def __init__(__self__, computer_name=None, cpu_count=None, disks=None, dynamic_memory_enabled=None, dynamic_memory_max_mb=None, dynamic_memory_min_mb=None, extended_location=None, generation=None, id=None, inventory_item_id=None, is_customizable=None, is_highly_available=None, limit_cpu_for_migration=None, location=None, memory_mb=None, name=None, network_interfaces=None, os_name=None, os_type=None, provisioning_state=None, system_data=None, tags=None, type=None, uuid=None, vmm_server_id=None):
        if computer_name and (not isinstance(computer_name, str)):
            raise TypeError("Expected argument 'computer_name' to be a str")
        pulumi.set(__self__, 'computer_name', computer_name)
        if cpu_count and (not isinstance(cpu_count, int)):
            raise TypeError("Expected argument 'cpu_count' to be a int")
        pulumi.set(__self__, 'cpu_count', cpu_count)
        if disks and (not isinstance(disks, list)):
            raise TypeError("Expected argument 'disks' to be a list")
        pulumi.set(__self__, 'disks', disks)
        if dynamic_memory_enabled and (not isinstance(dynamic_memory_enabled, str)):
            raise TypeError("Expected argument 'dynamic_memory_enabled' to be a str")
        pulumi.set(__self__, 'dynamic_memory_enabled', dynamic_memory_enabled)
        if dynamic_memory_max_mb and (not isinstance(dynamic_memory_max_mb, int)):
            raise TypeError("Expected argument 'dynamic_memory_max_mb' to be a int")
        pulumi.set(__self__, 'dynamic_memory_max_mb', dynamic_memory_max_mb)
        if dynamic_memory_min_mb and (not isinstance(dynamic_memory_min_mb, int)):
            raise TypeError("Expected argument 'dynamic_memory_min_mb' to be a int")
        pulumi.set(__self__, 'dynamic_memory_min_mb', dynamic_memory_min_mb)
        if extended_location and (not isinstance(extended_location, dict)):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, 'extended_location', extended_location)
        if generation and (not isinstance(generation, int)):
            raise TypeError("Expected argument 'generation' to be a int")
        pulumi.set(__self__, 'generation', generation)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if inventory_item_id and (not isinstance(inventory_item_id, str)):
            raise TypeError("Expected argument 'inventory_item_id' to be a str")
        pulumi.set(__self__, 'inventory_item_id', inventory_item_id)
        if is_customizable and (not isinstance(is_customizable, str)):
            raise TypeError("Expected argument 'is_customizable' to be a str")
        pulumi.set(__self__, 'is_customizable', is_customizable)
        if is_highly_available and (not isinstance(is_highly_available, str)):
            raise TypeError("Expected argument 'is_highly_available' to be a str")
        pulumi.set(__self__, 'is_highly_available', is_highly_available)
        if limit_cpu_for_migration and (not isinstance(limit_cpu_for_migration, str)):
            raise TypeError("Expected argument 'limit_cpu_for_migration' to be a str")
        pulumi.set(__self__, 'limit_cpu_for_migration', limit_cpu_for_migration)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if memory_mb and (not isinstance(memory_mb, int)):
            raise TypeError("Expected argument 'memory_mb' to be a int")
        pulumi.set(__self__, 'memory_mb', memory_mb)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if network_interfaces and (not isinstance(network_interfaces, list)):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, 'network_interfaces', network_interfaces)
        if os_name and (not isinstance(os_name, str)):
            raise TypeError("Expected argument 'os_name' to be a str")
        pulumi.set(__self__, 'os_name', os_name)
        if os_type and (not isinstance(os_type, str)):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, 'os_type', os_type)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if uuid and (not isinstance(uuid, str)):
            raise TypeError("Expected argument 'uuid' to be a str")
        pulumi.set(__self__, 'uuid', uuid)
        if vmm_server_id and (not isinstance(vmm_server_id, str)):
            raise TypeError("Expected argument 'vmm_server_id' to be a str")
        pulumi.set(__self__, 'vmm_server_id', vmm_server_id)

    @property
    @pulumi.getter(name='computerName')
    def computer_name(self) -> str:
        """
        Gets or sets computer name.
        """
        return pulumi.get(self, 'computer_name')

    @property
    @pulumi.getter(name='cpuCount')
    def cpu_count(self) -> int:
        """
        Gets or sets the desired number of vCPUs for the vm.
        """
        return pulumi.get(self, 'cpu_count')

    @property
    @pulumi.getter
    def disks(self) -> Sequence['outputs.VirtualDiskResponse']:
        """
        Gets or sets the disks of the template.
        """
        return pulumi.get(self, 'disks')

    @property
    @pulumi.getter(name='dynamicMemoryEnabled')
    def dynamic_memory_enabled(self) -> str:
        """
        Gets or sets a value indicating whether to enable dynamic memory or not.
        """
        return pulumi.get(self, 'dynamic_memory_enabled')

    @property
    @pulumi.getter(name='dynamicMemoryMaxMB')
    def dynamic_memory_max_mb(self) -> int:
        """
        Gets or sets the max dynamic memory for the vm.
        """
        return pulumi.get(self, 'dynamic_memory_max_mb')

    @property
    @pulumi.getter(name='dynamicMemoryMinMB')
    def dynamic_memory_min_mb(self) -> int:
        """
        Gets or sets the min dynamic memory for the vm.
        """
        return pulumi.get(self, 'dynamic_memory_min_mb')

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> 'outputs.ExtendedLocationResponse':
        """
        The extended location.
        """
        return pulumi.get(self, 'extended_location')

    @property
    @pulumi.getter
    def generation(self) -> int:
        """
        Gets or sets the generation for the vm.
        """
        return pulumi.get(self, 'generation')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='inventoryItemId')
    def inventory_item_id(self) -> Optional[str]:
        """
        Gets or sets the inventory Item ID for the resource.
        """
        return pulumi.get(self, 'inventory_item_id')

    @property
    @pulumi.getter(name='isCustomizable')
    def is_customizable(self) -> str:
        """
        Gets or sets a value indicating whether the vm template is customizable or not.
        """
        return pulumi.get(self, 'is_customizable')

    @property
    @pulumi.getter(name='isHighlyAvailable')
    def is_highly_available(self) -> str:
        """
        Gets highly available property.
        """
        return pulumi.get(self, 'is_highly_available')

    @property
    @pulumi.getter(name='limitCpuForMigration')
    def limit_cpu_for_migration(self) -> str:
        """
        Gets or sets a value indicating whether to enable processor compatibility mode for live migration of VMs.
        """
        return pulumi.get(self, 'limit_cpu_for_migration')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='memoryMB')
    def memory_mb(self) -> int:
        """
        MemoryMB is the desired size of a virtual machine's memory, in MB.
        """
        return pulumi.get(self, 'memory_mb')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='networkInterfaces')
    def network_interfaces(self) -> Sequence['outputs.NetworkInterfacesResponse']:
        """
        Gets or sets the network interfaces of the template.
        """
        return pulumi.get(self, 'network_interfaces')

    @property
    @pulumi.getter(name='osName')
    def os_name(self) -> str:
        """
        Gets or sets os name.
        """
        return pulumi.get(self, 'os_name')

    @property
    @pulumi.getter(name='osType')
    def os_type(self) -> str:
        """
        Gets or sets the type of the os.
        """
        return pulumi.get(self, 'os_type')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Gets or sets the provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system data.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def uuid(self) -> Optional[str]:
        """
        Unique ID of the virtual machine template.
        """
        return pulumi.get(self, 'uuid')

    @property
    @pulumi.getter(name='vmmServerId')
    def vmm_server_id(self) -> Optional[str]:
        """
        ARM Id of the vmmServer resource in which this resource resides.
        """
        return pulumi.get(self, 'vmm_server_id')

class AwaitableGetVirtualMachineTemplateResult(GetVirtualMachineTemplateResult):

    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineTemplateResult(computer_name=self.computer_name, cpu_count=self.cpu_count, disks=self.disks, dynamic_memory_enabled=self.dynamic_memory_enabled, dynamic_memory_max_mb=self.dynamic_memory_max_mb, dynamic_memory_min_mb=self.dynamic_memory_min_mb, extended_location=self.extended_location, generation=self.generation, id=self.id, inventory_item_id=self.inventory_item_id, is_customizable=self.is_customizable, is_highly_available=self.is_highly_available, limit_cpu_for_migration=self.limit_cpu_for_migration, location=self.location, memory_mb=self.memory_mb, name=self.name, network_interfaces=self.network_interfaces, os_name=self.os_name, os_type=self.os_type, provisioning_state=self.provisioning_state, system_data=self.system_data, tags=self.tags, type=self.type, uuid=self.uuid, vmm_server_id=self.vmm_server_id)

def get_virtual_machine_template(resource_group_name: Optional[str]=None, virtual_machine_template_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVirtualMachineTemplateResult:
    """
    Implements VirtualMachineTemplate GET method.
    API Version: 2020-06-05-preview.


    :param str resource_group_name: The name of the resource group.
    :param str virtual_machine_template_name: Name of the VirtualMachineTemplate.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualMachineTemplateName'] = virtual_machine_template_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:scvmm:getVirtualMachineTemplate', __args__, opts=opts, typ=GetVirtualMachineTemplateResult).value
    return AwaitableGetVirtualMachineTemplateResult(computer_name=__ret__.computer_name, cpu_count=__ret__.cpu_count, disks=__ret__.disks, dynamic_memory_enabled=__ret__.dynamic_memory_enabled, dynamic_memory_max_mb=__ret__.dynamic_memory_max_mb, dynamic_memory_min_mb=__ret__.dynamic_memory_min_mb, extended_location=__ret__.extended_location, generation=__ret__.generation, id=__ret__.id, inventory_item_id=__ret__.inventory_item_id, is_customizable=__ret__.is_customizable, is_highly_available=__ret__.is_highly_available, limit_cpu_for_migration=__ret__.limit_cpu_for_migration, location=__ret__.location, memory_mb=__ret__.memory_mb, name=__ret__.name, network_interfaces=__ret__.network_interfaces, os_name=__ret__.os_name, os_type=__ret__.os_type, provisioning_state=__ret__.provisioning_state, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type, uuid=__ret__.uuid, vmm_server_id=__ret__.vmm_server_id)

@_utilities.lift_output_func(get_virtual_machine_template)
def get_virtual_machine_template_output(resource_group_name: Optional[pulumi.Input[str]]=None, virtual_machine_template_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVirtualMachineTemplateResult]:
    """
    Implements VirtualMachineTemplate GET method.
    API Version: 2020-06-05-preview.


    :param str resource_group_name: The name of the resource group.
    :param str virtual_machine_template_name: Name of the VirtualMachineTemplate.
    """
    ...
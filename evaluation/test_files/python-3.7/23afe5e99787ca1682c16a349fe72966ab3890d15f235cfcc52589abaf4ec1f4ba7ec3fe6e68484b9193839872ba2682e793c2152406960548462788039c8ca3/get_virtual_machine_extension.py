import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetVirtualMachineExtensionResult', 'AwaitableGetVirtualMachineExtensionResult', 'get_virtual_machine_extension', 'get_virtual_machine_extension_output']

@pulumi.output_type
class GetVirtualMachineExtensionResult:
    """
    Describes a Virtual Machine Extension.
    """

    def __init__(__self__, auto_upgrade_minor_version=None, enable_automatic_upgrade=None, force_update_tag=None, id=None, instance_view=None, location=None, name=None, protected_settings=None, provisioning_state=None, publisher=None, settings=None, tags=None, type=None, type_handler_version=None):
        if auto_upgrade_minor_version and (not isinstance(auto_upgrade_minor_version, bool)):
            raise TypeError("Expected argument 'auto_upgrade_minor_version' to be a bool")
        pulumi.set(__self__, 'auto_upgrade_minor_version', auto_upgrade_minor_version)
        if enable_automatic_upgrade and (not isinstance(enable_automatic_upgrade, bool)):
            raise TypeError("Expected argument 'enable_automatic_upgrade' to be a bool")
        pulumi.set(__self__, 'enable_automatic_upgrade', enable_automatic_upgrade)
        if force_update_tag and (not isinstance(force_update_tag, str)):
            raise TypeError("Expected argument 'force_update_tag' to be a str")
        pulumi.set(__self__, 'force_update_tag', force_update_tag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if instance_view and (not isinstance(instance_view, dict)):
            raise TypeError("Expected argument 'instance_view' to be a dict")
        pulumi.set(__self__, 'instance_view', instance_view)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if protected_settings and (not isinstance(protected_settings, dict)):
            raise TypeError("Expected argument 'protected_settings' to be a dict")
        pulumi.set(__self__, 'protected_settings', protected_settings)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if publisher and (not isinstance(publisher, str)):
            raise TypeError("Expected argument 'publisher' to be a str")
        pulumi.set(__self__, 'publisher', publisher)
        if settings and (not isinstance(settings, dict)):
            raise TypeError("Expected argument 'settings' to be a dict")
        pulumi.set(__self__, 'settings', settings)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if type_handler_version and (not isinstance(type_handler_version, str)):
            raise TypeError("Expected argument 'type_handler_version' to be a str")
        pulumi.set(__self__, 'type_handler_version', type_handler_version)

    @property
    @pulumi.getter(name='autoUpgradeMinorVersion')
    def auto_upgrade_minor_version(self) -> Optional[bool]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        """
        return pulumi.get(self, 'auto_upgrade_minor_version')

    @property
    @pulumi.getter(name='enableAutomaticUpgrade')
    def enable_automatic_upgrade(self) -> Optional[bool]:
        """
        Indicates whether the extension should be automatically upgraded by the platform if there is a newer version of the extension available.
        """
        return pulumi.get(self, 'enable_automatic_upgrade')

    @property
    @pulumi.getter(name='forceUpdateTag')
    def force_update_tag(self) -> Optional[str]:
        """
        How the extension handler should be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, 'force_update_tag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='instanceView')
    def instance_view(self) -> Optional['outputs.VirtualMachineExtensionInstanceViewResponse']:
        """
        The virtual machine extension instance view.
        """
        return pulumi.get(self, 'instance_view')

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
    @pulumi.getter(name='protectedSettings')
    def protected_settings(self) -> Optional[Any]:
        """
        The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        """
        return pulumi.get(self, 'protected_settings')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def publisher(self) -> Optional[str]:
        """
        The name of the extension handler publisher.
        """
        return pulumi.get(self, 'publisher')

    @property
    @pulumi.getter
    def settings(self) -> Optional[Any]:
        """
        Json formatted public settings for the extension.
        """
        return pulumi.get(self, 'settings')

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
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='typeHandlerVersion')
    def type_handler_version(self) -> Optional[str]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, 'type_handler_version')

class AwaitableGetVirtualMachineExtensionResult(GetVirtualMachineExtensionResult):

    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineExtensionResult(auto_upgrade_minor_version=self.auto_upgrade_minor_version, enable_automatic_upgrade=self.enable_automatic_upgrade, force_update_tag=self.force_update_tag, id=self.id, instance_view=self.instance_view, location=self.location, name=self.name, protected_settings=self.protected_settings, provisioning_state=self.provisioning_state, publisher=self.publisher, settings=self.settings, tags=self.tags, type=self.type, type_handler_version=self.type_handler_version)

def get_virtual_machine_extension(expand: Optional[str]=None, resource_group_name: Optional[str]=None, vm_extension_name: Optional[str]=None, vm_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVirtualMachineExtensionResult:
    """
    Describes a Virtual Machine Extension.


    :param str expand: The expand expression to apply on the operation.
    :param str resource_group_name: The name of the resource group.
    :param str vm_extension_name: The name of the virtual machine extension.
    :param str vm_name: The name of the virtual machine containing the extension.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['vmExtensionName'] = vm_extension_name
    __args__['vmName'] = vm_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20201201:getVirtualMachineExtension', __args__, opts=opts, typ=GetVirtualMachineExtensionResult).value
    return AwaitableGetVirtualMachineExtensionResult(auto_upgrade_minor_version=__ret__.auto_upgrade_minor_version, enable_automatic_upgrade=__ret__.enable_automatic_upgrade, force_update_tag=__ret__.force_update_tag, id=__ret__.id, instance_view=__ret__.instance_view, location=__ret__.location, name=__ret__.name, protected_settings=__ret__.protected_settings, provisioning_state=__ret__.provisioning_state, publisher=__ret__.publisher, settings=__ret__.settings, tags=__ret__.tags, type=__ret__.type, type_handler_version=__ret__.type_handler_version)

@_utilities.lift_output_func(get_virtual_machine_extension)
def get_virtual_machine_extension_output(expand: Optional[pulumi.Input[Optional[str]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, vm_extension_name: Optional[pulumi.Input[str]]=None, vm_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVirtualMachineExtensionResult]:
    """
    Describes a Virtual Machine Extension.


    :param str expand: The expand expression to apply on the operation.
    :param str resource_group_name: The name of the resource group.
    :param str vm_extension_name: The name of the virtual machine extension.
    :param str vm_name: The name of the virtual machine containing the extension.
    """
    ...
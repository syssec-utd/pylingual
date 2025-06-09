import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetMachineExtensionResult', 'AwaitableGetMachineExtensionResult', 'get_machine_extension', 'get_machine_extension_output']

@pulumi.output_type
class GetMachineExtensionResult:
    """
    Describes a Machine Extension.
    """

    def __init__(__self__, id=None, location=None, name=None, properties=None, system_data=None, tags=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
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
    @pulumi.getter
    def properties(self) -> 'outputs.MachineExtensionPropertiesResponse':
        """
        Describes Machine Extension Properties.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, 'system_data')

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

class AwaitableGetMachineExtensionResult(GetMachineExtensionResult):

    def __await__(self):
        if False:
            yield self
        return GetMachineExtensionResult(id=self.id, location=self.location, name=self.name, properties=self.properties, system_data=self.system_data, tags=self.tags, type=self.type)

def get_machine_extension(extension_name: Optional[str]=None, machine_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetMachineExtensionResult:
    """
    The operation to get the extension.


    :param str extension_name: The name of the machine extension.
    :param str machine_name: The name of the machine containing the extension.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['extensionName'] = extension_name
    __args__['machineName'] = machine_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:hybridcompute/v20210517preview:getMachineExtension', __args__, opts=opts, typ=GetMachineExtensionResult).value
    return AwaitableGetMachineExtensionResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_machine_extension)
def get_machine_extension_output(extension_name: Optional[pulumi.Input[str]]=None, machine_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetMachineExtensionResult]:
    """
    The operation to get the extension.


    :param str extension_name: The name of the machine extension.
    :param str machine_name: The name of the machine containing the extension.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
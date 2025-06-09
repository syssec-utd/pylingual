import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetRegistryComponentContainerResult', 'AwaitableGetRegistryComponentContainerResult', 'get_registry_component_container', 'get_registry_component_container_output']

@pulumi.output_type
class GetRegistryComponentContainerResult:
    """
    Azure Resource Manager resource envelope.
    """

    def __init__(__self__, component_container_properties=None, id=None, name=None, system_data=None, type=None):
        if component_container_properties and (not isinstance(component_container_properties, dict)):
            raise TypeError("Expected argument 'component_container_properties' to be a dict")
        pulumi.set(__self__, 'component_container_properties', component_container_properties)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='componentContainerProperties')
    def component_container_properties(self) -> 'outputs.ComponentContainerResponse':
        """
        [Required] Additional attributes of the entity.
        """
        return pulumi.get(self, 'component_container_properties')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetRegistryComponentContainerResult(GetRegistryComponentContainerResult):

    def __await__(self):
        if False:
            yield self
        return GetRegistryComponentContainerResult(component_container_properties=self.component_container_properties, id=self.id, name=self.name, system_data=self.system_data, type=self.type)

def get_registry_component_container(component_name: Optional[str]=None, registry_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetRegistryComponentContainerResult:
    """
    Azure Resource Manager resource envelope.


    :param str component_name: Container name.
    :param str registry_name: Name of Azure Machine Learning registry.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['componentName'] = component_name
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearningservices/v20230201preview:getRegistryComponentContainer', __args__, opts=opts, typ=GetRegistryComponentContainerResult).value
    return AwaitableGetRegistryComponentContainerResult(component_container_properties=__ret__.component_container_properties, id=__ret__.id, name=__ret__.name, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_registry_component_container)
def get_registry_component_container_output(component_name: Optional[pulumi.Input[str]]=None, registry_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetRegistryComponentContainerResult]:
    """
    Azure Resource Manager resource envelope.


    :param str component_name: Container name.
    :param str registry_name: Name of Azure Machine Learning registry.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
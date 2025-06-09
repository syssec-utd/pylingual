import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetIntegrationRuntimeResult', 'AwaitableGetIntegrationRuntimeResult', 'get_integration_runtime', 'get_integration_runtime_output']
warnings.warn('Version 2020-12-01 will be removed in v2 of the provider.', DeprecationWarning)

@pulumi.output_type
class GetIntegrationRuntimeResult:
    """
    Integration runtime resource type.
    """

    def __init__(__self__, etag=None, id=None, name=None, properties=None, type=None):
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        Resource Etag.
        """
        return pulumi.get(self, 'etag')

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
    @pulumi.getter
    def properties(self) -> Any:
        """
        Integration runtime properties.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetIntegrationRuntimeResult(GetIntegrationRuntimeResult):

    def __await__(self):
        if False:
            yield self
        return GetIntegrationRuntimeResult(etag=self.etag, id=self.id, name=self.name, properties=self.properties, type=self.type)

def get_integration_runtime(integration_runtime_name: Optional[str]=None, resource_group_name: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetIntegrationRuntimeResult:
    """
    Integration runtime resource type.


    :param str integration_runtime_name: Integration runtime name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn('get_integration_runtime is deprecated: Version 2020-12-01 will be removed in v2 of the provider.')
    __args__ = dict()
    __args__['integrationRuntimeName'] = integration_runtime_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20201201:getIntegrationRuntime', __args__, opts=opts, typ=GetIntegrationRuntimeResult).value
    return AwaitableGetIntegrationRuntimeResult(etag=__ret__.etag, id=__ret__.id, name=__ret__.name, properties=__ret__.properties, type=__ret__.type)

@_utilities.lift_output_func(get_integration_runtime)
def get_integration_runtime_output(integration_runtime_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetIntegrationRuntimeResult]:
    """
    Integration runtime resource type.


    :param str integration_runtime_name: Integration runtime name
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn('get_integration_runtime is deprecated: Version 2020-12-01 will be removed in v2 of the provider.')
    ...
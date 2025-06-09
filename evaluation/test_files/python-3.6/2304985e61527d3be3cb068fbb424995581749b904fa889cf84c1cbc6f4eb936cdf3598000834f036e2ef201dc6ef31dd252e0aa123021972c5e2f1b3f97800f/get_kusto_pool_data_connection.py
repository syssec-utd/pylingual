import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetKustoPoolDataConnectionResult', 'AwaitableGetKustoPoolDataConnectionResult', 'get_kusto_pool_data_connection', 'get_kusto_pool_data_connection_output']
warnings.warn('Please use one of the variants: EventGridDataConnection, EventHubDataConnection, IotHubDataConnection.', DeprecationWarning)

@pulumi.output_type
class GetKustoPoolDataConnectionResult:
    """
    Class representing a data connection.
    """

    def __init__(__self__, id=None, kind=None, location=None, name=None, system_data=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
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
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of the endpoint for the data connection
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
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

class AwaitableGetKustoPoolDataConnectionResult(GetKustoPoolDataConnectionResult):

    def __await__(self):
        if False:
            yield self
        return GetKustoPoolDataConnectionResult(id=self.id, kind=self.kind, location=self.location, name=self.name, system_data=self.system_data, type=self.type)

def get_kusto_pool_data_connection(data_connection_name: Optional[str]=None, database_name: Optional[str]=None, kusto_pool_name: Optional[str]=None, resource_group_name: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetKustoPoolDataConnectionResult:
    """
    Returns a data connection.


    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto pool.
    :param str kusto_pool_name: The name of the Kusto pool.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn('get_kusto_pool_data_connection is deprecated: Please use one of the variants: EventGridDataConnection, EventHubDataConnection, IotHubDataConnection.')
    __args__ = dict()
    __args__['dataConnectionName'] = data_connection_name
    __args__['databaseName'] = database_name
    __args__['kustoPoolName'] = kusto_pool_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20210601preview:getKustoPoolDataConnection', __args__, opts=opts, typ=GetKustoPoolDataConnectionResult).value
    return AwaitableGetKustoPoolDataConnectionResult(id=__ret__.id, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_kusto_pool_data_connection)
def get_kusto_pool_data_connection_output(data_connection_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, kusto_pool_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetKustoPoolDataConnectionResult]:
    """
    Returns a data connection.


    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto pool.
    :param str kusto_pool_name: The name of the Kusto pool.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    pulumi.log.warn('get_kusto_pool_data_connection is deprecated: Please use one of the variants: EventGridDataConnection, EventHubDataConnection, IotHubDataConnection.')
    ...
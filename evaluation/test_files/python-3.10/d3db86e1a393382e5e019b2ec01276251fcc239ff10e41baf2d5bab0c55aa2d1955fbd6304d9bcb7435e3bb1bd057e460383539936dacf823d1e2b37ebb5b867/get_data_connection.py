import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetDataConnectionResult', 'AwaitableGetDataConnectionResult', 'get_data_connection', 'get_data_connection_output']
warnings.warn('Please use one of the variants: EventGridDataConnection, EventHubDataConnection.', DeprecationWarning)

@pulumi.output_type
class GetDataConnectionResult:
    """
    Class representing an data connection.
    """

    def __init__(__self__, id=None, kind=None, location=None, name=None, type=None):
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
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetDataConnectionResult(GetDataConnectionResult):

    def __await__(self):
        if False:
            yield self
        return GetDataConnectionResult(id=self.id, kind=self.kind, location=self.location, name=self.name, type=self.type)

def get_data_connection(cluster_name: Optional[str]=None, data_connection_name: Optional[str]=None, database_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDataConnectionResult:
    """
    Returns a data connection.


    :param str cluster_name: The name of the Kusto cluster.
    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    pulumi.log.warn('get_data_connection is deprecated: Please use one of the variants: EventGridDataConnection, EventHubDataConnection.')
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['dataConnectionName'] = data_connection_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:kusto/v20190121:getDataConnection', __args__, opts=opts, typ=GetDataConnectionResult).value
    return AwaitableGetDataConnectionResult(id=__ret__.id, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, type=__ret__.type)

@_utilities.lift_output_func(get_data_connection)
def get_data_connection_output(cluster_name: Optional[pulumi.Input[str]]=None, data_connection_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDataConnectionResult]:
    """
    Returns a data connection.


    :param str cluster_name: The name of the Kusto cluster.
    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    pulumi.log.warn('get_data_connection is deprecated: Please use one of the variants: EventGridDataConnection, EventHubDataConnection.')
    ...
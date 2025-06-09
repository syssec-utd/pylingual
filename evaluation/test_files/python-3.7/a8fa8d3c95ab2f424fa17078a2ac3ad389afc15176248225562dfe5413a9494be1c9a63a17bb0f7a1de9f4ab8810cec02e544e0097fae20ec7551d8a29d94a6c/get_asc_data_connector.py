import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetASCDataConnectorResult', 'AwaitableGetASCDataConnectorResult', 'get_asc_data_connector', 'get_asc_data_connector_output']

@pulumi.output_type
class GetASCDataConnectorResult:
    """
    Represents ASC (Azure Security Center) data connector.
    """

    def __init__(__self__, data_types=None, etag=None, id=None, kind=None, name=None, subscription_id=None, system_data=None, type=None):
        if data_types and (not isinstance(data_types, dict)):
            raise TypeError("Expected argument 'data_types' to be a dict")
        pulumi.set(__self__, 'data_types', data_types)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if subscription_id and (not isinstance(subscription_id, str)):
            raise TypeError("Expected argument 'subscription_id' to be a str")
        pulumi.set(__self__, 'subscription_id', subscription_id)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='dataTypes')
    def data_types(self) -> Optional['outputs.AlertsDataTypeOfDataConnectorResponse']:
        """
        The available data types for the connector.
        """
        return pulumi.get(self, 'data_types')

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
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
    def kind(self) -> str:
        """
        The kind of the data connector
        Expected value is 'AzureSecurityCenter'.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='subscriptionId')
    def subscription_id(self) -> Optional[str]:
        """
        The subscription id to connect to, and get the data from.
        """
        return pulumi.get(self, 'subscription_id')

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

class AwaitableGetASCDataConnectorResult(GetASCDataConnectorResult):

    def __await__(self):
        if False:
            yield self
        return GetASCDataConnectorResult(data_types=self.data_types, etag=self.etag, id=self.id, kind=self.kind, name=self.name, subscription_id=self.subscription_id, system_data=self.system_data, type=self.type)

def get_asc_data_connector(data_connector_id: Optional[str]=None, resource_group_name: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetASCDataConnectorResult:
    """
    Represents ASC (Azure Security Center) data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['dataConnectorId'] = data_connector_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20210901preview:getASCDataConnector', __args__, opts=opts, typ=GetASCDataConnectorResult).value
    return AwaitableGetASCDataConnectorResult(data_types=__ret__.data_types, etag=__ret__.etag, id=__ret__.id, kind=__ret__.kind, name=__ret__.name, subscription_id=__ret__.subscription_id, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_asc_data_connector)
def get_asc_data_connector_output(data_connector_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetASCDataConnectorResult]:
    """
    Represents ASC (Azure Security Center) data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
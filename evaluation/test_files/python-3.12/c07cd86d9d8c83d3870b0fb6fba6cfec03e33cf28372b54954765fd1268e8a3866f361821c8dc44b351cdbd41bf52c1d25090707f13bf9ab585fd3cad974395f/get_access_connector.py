import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetAccessConnectorResult', 'AwaitableGetAccessConnectorResult', 'get_access_connector', 'get_access_connector_output']

@pulumi.output_type
class GetAccessConnectorResult:
    """
    Information about azure databricks accessConnector.
    """

    def __init__(__self__, id=None, identity=None, location=None, name=None, properties=None, tags=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
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
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityDataResponse']:
        """
        Identity for the resource.
        """
        return pulumi.get(self, 'identity')

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
    def properties(self) -> 'outputs.AccessConnectorPropertiesResponse':
        """
        Azure Databricks accessConnector properties
        """
        return pulumi.get(self, 'properties')

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
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, 'type')

class AwaitableGetAccessConnectorResult(GetAccessConnectorResult):

    def __await__(self):
        if False:
            yield self
        return GetAccessConnectorResult(id=self.id, identity=self.identity, location=self.location, name=self.name, properties=self.properties, tags=self.tags, type=self.type)

def get_access_connector(connector_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetAccessConnectorResult:
    """
    Information about azure databricks accessConnector.


    :param str connector_name: The name of the azure databricks accessConnector.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['connectorName'] = connector_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databricks/v20220401preview:getAccessConnector', __args__, opts=opts, typ=GetAccessConnectorResult).value
    return AwaitableGetAccessConnectorResult(id=__ret__.id, identity=__ret__.identity, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_access_connector)
def get_access_connector_output(connector_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetAccessConnectorResult]:
    """
    Information about azure databricks accessConnector.


    :param str connector_name: The name of the azure databricks accessConnector.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
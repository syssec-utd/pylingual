import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPrivateEndpointConnectionsForEDMResult', 'AwaitableGetPrivateEndpointConnectionsForEDMResult', 'get_private_endpoint_connections_for_edm', 'get_private_endpoint_connections_for_edm_output']

@pulumi.output_type
class GetPrivateEndpointConnectionsForEDMResult:
    """
    The Private Endpoint Connection resource.
    """

    def __init__(__self__, id=None, name=None, private_endpoint=None, private_link_service_connection_state=None, provisioning_state=None, system_data=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if private_endpoint and (not isinstance(private_endpoint, dict)):
            raise TypeError("Expected argument 'private_endpoint' to be a dict")
        pulumi.set(__self__, 'private_endpoint', private_endpoint)
        if private_link_service_connection_state and (not isinstance(private_link_service_connection_state, dict)):
            raise TypeError("Expected argument 'private_link_service_connection_state' to be a dict")
        pulumi.set(__self__, 'private_link_service_connection_state', private_link_service_connection_state)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
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
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        The resource of private end point.
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> 'outputs.PrivateLinkServiceConnectionStateResponse':
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the private endpoint connection resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Required property for system data
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetPrivateEndpointConnectionsForEDMResult(GetPrivateEndpointConnectionsForEDMResult):

    def __await__(self):
        if False:
            yield self
        return GetPrivateEndpointConnectionsForEDMResult(id=self.id, name=self.name, private_endpoint=self.private_endpoint, private_link_service_connection_state=self.private_link_service_connection_state, provisioning_state=self.provisioning_state, system_data=self.system_data, type=self.type)

def get_private_endpoint_connections_for_edm(private_endpoint_connection_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPrivateEndpointConnectionsForEDMResult:
    """
    Gets the specified private endpoint connection associated with the service.


    :param str private_endpoint_connection_name: The name of the private endpoint connection associated with the Azure resource
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str resource_name: The name of the service instance.
    """
    __args__ = dict()
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityandcompliance/v20210308:getPrivateEndpointConnectionsForEDM', __args__, opts=opts, typ=GetPrivateEndpointConnectionsForEDMResult).value
    return AwaitableGetPrivateEndpointConnectionsForEDMResult(id=__ret__.id, name=__ret__.name, private_endpoint=__ret__.private_endpoint, private_link_service_connection_state=__ret__.private_link_service_connection_state, provisioning_state=__ret__.provisioning_state, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_private_endpoint_connections_for_edm)
def get_private_endpoint_connections_for_edm_output(private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPrivateEndpointConnectionsForEDMResult]:
    """
    Gets the specified private endpoint connection associated with the service.


    :param str private_endpoint_connection_name: The name of the private endpoint connection associated with the Azure resource
    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str resource_name: The name of the service instance.
    """
    ...
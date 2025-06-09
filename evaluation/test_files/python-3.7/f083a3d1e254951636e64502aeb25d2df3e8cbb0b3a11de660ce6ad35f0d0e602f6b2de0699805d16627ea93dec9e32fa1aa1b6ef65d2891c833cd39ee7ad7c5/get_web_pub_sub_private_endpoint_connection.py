import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetWebPubSubPrivateEndpointConnectionResult', 'AwaitableGetWebPubSubPrivateEndpointConnectionResult', 'get_web_pub_sub_private_endpoint_connection', 'get_web_pub_sub_private_endpoint_connection_output']

@pulumi.output_type
class GetWebPubSubPrivateEndpointConnectionResult:
    """
    A private endpoint connection to an azure resource
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
        Fully qualified resource Id for the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        Private endpoint associated with the private endpoint connection
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkServiceConnectionStateResponse']:
        """
        Connection state
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the private endpoint connection
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, 'type')

class AwaitableGetWebPubSubPrivateEndpointConnectionResult(GetWebPubSubPrivateEndpointConnectionResult):

    def __await__(self):
        if False:
            yield self
        return GetWebPubSubPrivateEndpointConnectionResult(id=self.id, name=self.name, private_endpoint=self.private_endpoint, private_link_service_connection_state=self.private_link_service_connection_state, provisioning_state=self.provisioning_state, system_data=self.system_data, type=self.type)

def get_web_pub_sub_private_endpoint_connection(private_endpoint_connection_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWebPubSubPrivateEndpointConnectionResult:
    """
    Get the specified private endpoint connection


    :param str private_endpoint_connection_name: The name of the private endpoint connection
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str resource_name: The name of the resource.
    """
    __args__ = dict()
    __args__['privateEndpointConnectionName'] = private_endpoint_connection_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:webpubsub/v20210901preview:getWebPubSubPrivateEndpointConnection', __args__, opts=opts, typ=GetWebPubSubPrivateEndpointConnectionResult).value
    return AwaitableGetWebPubSubPrivateEndpointConnectionResult(id=__ret__.id, name=__ret__.name, private_endpoint=__ret__.private_endpoint, private_link_service_connection_state=__ret__.private_link_service_connection_state, provisioning_state=__ret__.provisioning_state, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_web_pub_sub_private_endpoint_connection)
def get_web_pub_sub_private_endpoint_connection_output(private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWebPubSubPrivateEndpointConnectionResult]:
    """
    Get the specified private endpoint connection


    :param str private_endpoint_connection_name: The name of the private endpoint connection
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str resource_name: The name of the resource.
    """
    ...
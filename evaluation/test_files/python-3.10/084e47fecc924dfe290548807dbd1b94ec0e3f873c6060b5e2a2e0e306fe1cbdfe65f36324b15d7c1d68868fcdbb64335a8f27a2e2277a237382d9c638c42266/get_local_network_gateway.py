import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetLocalNetworkGatewayResult', 'AwaitableGetLocalNetworkGatewayResult', 'get_local_network_gateway', 'get_local_network_gateway_output']

@pulumi.output_type
class GetLocalNetworkGatewayResult:
    """
    A common class for general resource information.
    """

    def __init__(__self__, bgp_settings=None, etag=None, fqdn=None, gateway_ip_address=None, id=None, local_network_address_space=None, location=None, name=None, provisioning_state=None, resource_guid=None, tags=None, type=None):
        if bgp_settings and (not isinstance(bgp_settings, dict)):
            raise TypeError("Expected argument 'bgp_settings' to be a dict")
        pulumi.set(__self__, 'bgp_settings', bgp_settings)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if fqdn and (not isinstance(fqdn, str)):
            raise TypeError("Expected argument 'fqdn' to be a str")
        pulumi.set(__self__, 'fqdn', fqdn)
        if gateway_ip_address and (not isinstance(gateway_ip_address, str)):
            raise TypeError("Expected argument 'gateway_ip_address' to be a str")
        pulumi.set(__self__, 'gateway_ip_address', gateway_ip_address)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if local_network_address_space and (not isinstance(local_network_address_space, dict)):
            raise TypeError("Expected argument 'local_network_address_space' to be a dict")
        pulumi.set(__self__, 'local_network_address_space', local_network_address_space)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if resource_guid and (not isinstance(resource_guid, str)):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, 'resource_guid', resource_guid)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='bgpSettings')
    def bgp_settings(self) -> Optional['outputs.BgpSettingsResponse']:
        """
        Local network gateway's BGP speaker settings.
        """
        return pulumi.get(self, 'bgp_settings')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[str]:
        """
        FQDN of local network gateway.
        """
        return pulumi.get(self, 'fqdn')

    @property
    @pulumi.getter(name='gatewayIpAddress')
    def gateway_ip_address(self) -> Optional[str]:
        """
        IP address of local network gateway.
        """
        return pulumi.get(self, 'gateway_ip_address')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='localNetworkAddressSpace')
    def local_network_address_space(self) -> Optional['outputs.AddressSpaceResponse']:
        """
        Local network site address space.
        """
        return pulumi.get(self, 'local_network_address_space')

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
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the local network gateway resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> str:
        """
        The resource GUID property of the local network gateway resource.
        """
        return pulumi.get(self, 'resource_guid')

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
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetLocalNetworkGatewayResult(GetLocalNetworkGatewayResult):

    def __await__(self):
        if False:
            yield self
        return GetLocalNetworkGatewayResult(bgp_settings=self.bgp_settings, etag=self.etag, fqdn=self.fqdn, gateway_ip_address=self.gateway_ip_address, id=self.id, local_network_address_space=self.local_network_address_space, location=self.location, name=self.name, provisioning_state=self.provisioning_state, resource_guid=self.resource_guid, tags=self.tags, type=self.type)

def get_local_network_gateway(local_network_gateway_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetLocalNetworkGatewayResult:
    """
    Gets the specified local network gateway in a resource group.


    :param str local_network_gateway_name: The name of the local network gateway.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['localNetworkGatewayName'] = local_network_gateway_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220901:getLocalNetworkGateway', __args__, opts=opts, typ=GetLocalNetworkGatewayResult).value
    return AwaitableGetLocalNetworkGatewayResult(bgp_settings=__ret__.bgp_settings, etag=__ret__.etag, fqdn=__ret__.fqdn, gateway_ip_address=__ret__.gateway_ip_address, id=__ret__.id, local_network_address_space=__ret__.local_network_address_space, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, resource_guid=__ret__.resource_guid, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_local_network_gateway)
def get_local_network_gateway_output(local_network_gateway_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetLocalNetworkGatewayResult]:
    """
    Gets the specified local network gateway in a resource group.


    :param str local_network_gateway_name: The name of the local network gateway.
    :param str resource_group_name: The name of the resource group.
    """
    ...
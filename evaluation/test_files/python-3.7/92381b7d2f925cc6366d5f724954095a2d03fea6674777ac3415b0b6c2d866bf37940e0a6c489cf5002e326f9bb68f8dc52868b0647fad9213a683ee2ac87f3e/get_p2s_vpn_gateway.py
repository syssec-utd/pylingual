import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetP2sVpnGatewayResult', 'AwaitableGetP2sVpnGatewayResult', 'get_p2s_vpn_gateway', 'get_p2s_vpn_gateway_output']

@pulumi.output_type
class GetP2sVpnGatewayResult:
    """
    P2SVpnGateway Resource.
    """

    def __init__(__self__, custom_dns_servers=None, etag=None, id=None, is_routing_preference_internet=None, location=None, name=None, p2_s_connection_configurations=None, provisioning_state=None, tags=None, type=None, virtual_hub=None, vpn_client_connection_health=None, vpn_gateway_scale_unit=None, vpn_server_configuration=None):
        if custom_dns_servers and (not isinstance(custom_dns_servers, list)):
            raise TypeError("Expected argument 'custom_dns_servers' to be a list")
        pulumi.set(__self__, 'custom_dns_servers', custom_dns_servers)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if is_routing_preference_internet and (not isinstance(is_routing_preference_internet, bool)):
            raise TypeError("Expected argument 'is_routing_preference_internet' to be a bool")
        pulumi.set(__self__, 'is_routing_preference_internet', is_routing_preference_internet)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if p2_s_connection_configurations and (not isinstance(p2_s_connection_configurations, list)):
            raise TypeError("Expected argument 'p2_s_connection_configurations' to be a list")
        pulumi.set(__self__, 'p2_s_connection_configurations', p2_s_connection_configurations)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if virtual_hub and (not isinstance(virtual_hub, dict)):
            raise TypeError("Expected argument 'virtual_hub' to be a dict")
        pulumi.set(__self__, 'virtual_hub', virtual_hub)
        if vpn_client_connection_health and (not isinstance(vpn_client_connection_health, dict)):
            raise TypeError("Expected argument 'vpn_client_connection_health' to be a dict")
        pulumi.set(__self__, 'vpn_client_connection_health', vpn_client_connection_health)
        if vpn_gateway_scale_unit and (not isinstance(vpn_gateway_scale_unit, int)):
            raise TypeError("Expected argument 'vpn_gateway_scale_unit' to be a int")
        pulumi.set(__self__, 'vpn_gateway_scale_unit', vpn_gateway_scale_unit)
        if vpn_server_configuration and (not isinstance(vpn_server_configuration, dict)):
            raise TypeError("Expected argument 'vpn_server_configuration' to be a dict")
        pulumi.set(__self__, 'vpn_server_configuration', vpn_server_configuration)

    @property
    @pulumi.getter(name='customDnsServers')
    def custom_dns_servers(self) -> Optional[Sequence[str]]:
        """
        List of all customer specified DNS servers IP addresses.
        """
        return pulumi.get(self, 'custom_dns_servers')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='isRoutingPreferenceInternet')
    def is_routing_preference_internet(self) -> Optional[bool]:
        """
        Enable Routing Preference property for the Public IP Interface of the P2SVpnGateway.
        """
        return pulumi.get(self, 'is_routing_preference_internet')

    @property
    @pulumi.getter
    def location(self) -> str:
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
    @pulumi.getter(name='p2SConnectionConfigurations')
    def p2_s_connection_configurations(self) -> Optional[Sequence['outputs.P2SConnectionConfigurationResponse']]:
        """
        List of all p2s connection configurations of the gateway.
        """
        return pulumi.get(self, 'p2_s_connection_configurations')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the P2S VPN gateway resource.
        """
        return pulumi.get(self, 'provisioning_state')

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

    @property
    @pulumi.getter(name='virtualHub')
    def virtual_hub(self) -> Optional['outputs.SubResourceResponse']:
        """
        The VirtualHub to which the gateway belongs.
        """
        return pulumi.get(self, 'virtual_hub')

    @property
    @pulumi.getter(name='vpnClientConnectionHealth')
    def vpn_client_connection_health(self) -> 'outputs.VpnClientConnectionHealthResponse':
        """
        All P2S VPN clients' connection health status.
        """
        return pulumi.get(self, 'vpn_client_connection_health')

    @property
    @pulumi.getter(name='vpnGatewayScaleUnit')
    def vpn_gateway_scale_unit(self) -> Optional[int]:
        """
        The scale unit for this p2s vpn gateway.
        """
        return pulumi.get(self, 'vpn_gateway_scale_unit')

    @property
    @pulumi.getter(name='vpnServerConfiguration')
    def vpn_server_configuration(self) -> Optional['outputs.SubResourceResponse']:
        """
        The VpnServerConfiguration to which the p2sVpnGateway is attached to.
        """
        return pulumi.get(self, 'vpn_server_configuration')

class AwaitableGetP2sVpnGatewayResult(GetP2sVpnGatewayResult):

    def __await__(self):
        if False:
            yield self
        return GetP2sVpnGatewayResult(custom_dns_servers=self.custom_dns_servers, etag=self.etag, id=self.id, is_routing_preference_internet=self.is_routing_preference_internet, location=self.location, name=self.name, p2_s_connection_configurations=self.p2_s_connection_configurations, provisioning_state=self.provisioning_state, tags=self.tags, type=self.type, virtual_hub=self.virtual_hub, vpn_client_connection_health=self.vpn_client_connection_health, vpn_gateway_scale_unit=self.vpn_gateway_scale_unit, vpn_server_configuration=self.vpn_server_configuration)

def get_p2s_vpn_gateway(gateway_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetP2sVpnGatewayResult:
    """
    Retrieves the details of a virtual wan p2s vpn gateway.


    :param str gateway_name: The name of the gateway.
    :param str resource_group_name: The resource group name of the P2SVpnGateway.
    """
    __args__ = dict()
    __args__['gatewayName'] = gateway_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20210201:getP2sVpnGateway', __args__, opts=opts, typ=GetP2sVpnGatewayResult).value
    return AwaitableGetP2sVpnGatewayResult(custom_dns_servers=__ret__.custom_dns_servers, etag=__ret__.etag, id=__ret__.id, is_routing_preference_internet=__ret__.is_routing_preference_internet, location=__ret__.location, name=__ret__.name, p2_s_connection_configurations=__ret__.p2_s_connection_configurations, provisioning_state=__ret__.provisioning_state, tags=__ret__.tags, type=__ret__.type, virtual_hub=__ret__.virtual_hub, vpn_client_connection_health=__ret__.vpn_client_connection_health, vpn_gateway_scale_unit=__ret__.vpn_gateway_scale_unit, vpn_server_configuration=__ret__.vpn_server_configuration)

@_utilities.lift_output_func(get_p2s_vpn_gateway)
def get_p2s_vpn_gateway_output(gateway_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetP2sVpnGatewayResult]:
    """
    Retrieves the details of a virtual wan p2s vpn gateway.


    :param str gateway_name: The name of the gateway.
    :param str resource_group_name: The resource group name of the P2SVpnGateway.
    """
    ...
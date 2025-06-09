import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetVirtualNetworkGatewayLearnedRoutesResult', 'AwaitableGetVirtualNetworkGatewayLearnedRoutesResult', 'get_virtual_network_gateway_learned_routes', 'get_virtual_network_gateway_learned_routes_output']

@pulumi.output_type
class GetVirtualNetworkGatewayLearnedRoutesResult:
    """
    List of virtual network gateway routes
    """

    def __init__(__self__, value=None):
        if value and (not isinstance(value, list)):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.GatewayRouteResponse']]:
        """
        List of gateway routes
        """
        return pulumi.get(self, 'value')

class AwaitableGetVirtualNetworkGatewayLearnedRoutesResult(GetVirtualNetworkGatewayLearnedRoutesResult):

    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkGatewayLearnedRoutesResult(value=self.value)

def get_virtual_network_gateway_learned_routes(resource_group_name: Optional[str]=None, virtual_network_gateway_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVirtualNetworkGatewayLearnedRoutesResult:
    """
    List of virtual network gateway routes


    :param str resource_group_name: The name of the resource group.
    :param str virtual_network_gateway_name: The name of the virtual network gateway.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualNetworkGatewayName'] = virtual_network_gateway_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20181201:getVirtualNetworkGatewayLearnedRoutes', __args__, opts=opts, typ=GetVirtualNetworkGatewayLearnedRoutesResult).value
    return AwaitableGetVirtualNetworkGatewayLearnedRoutesResult(value=__ret__.value)

@_utilities.lift_output_func(get_virtual_network_gateway_learned_routes)
def get_virtual_network_gateway_learned_routes_output(resource_group_name: Optional[pulumi.Input[str]]=None, virtual_network_gateway_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVirtualNetworkGatewayLearnedRoutesResult]:
    """
    List of virtual network gateway routes


    :param str resource_group_name: The name of the resource group.
    :param str virtual_network_gateway_name: The name of the virtual network gateway.
    """
    ...
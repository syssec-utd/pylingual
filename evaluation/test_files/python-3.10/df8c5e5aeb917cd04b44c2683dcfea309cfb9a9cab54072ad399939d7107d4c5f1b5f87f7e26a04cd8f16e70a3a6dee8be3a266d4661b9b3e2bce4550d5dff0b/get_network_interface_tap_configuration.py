import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetNetworkInterfaceTapConfigurationResult', 'AwaitableGetNetworkInterfaceTapConfigurationResult', 'get_network_interface_tap_configuration', 'get_network_interface_tap_configuration_output']

@pulumi.output_type
class GetNetworkInterfaceTapConfigurationResult:
    """
    Tap configuration in a Network Interface.
    """

    def __init__(__self__, etag=None, id=None, name=None, provisioning_state=None, type=None, virtual_network_tap=None):
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if virtual_network_tap and (not isinstance(virtual_network_tap, dict)):
            raise TypeError("Expected argument 'virtual_network_tap' to be a dict")
        pulumi.set(__self__, 'virtual_network_tap', virtual_network_tap)

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
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the network interface tap configuration resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Sub Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='virtualNetworkTap')
    def virtual_network_tap(self) -> Optional['outputs.VirtualNetworkTapResponse']:
        """
        The reference to the Virtual Network Tap resource.
        """
        return pulumi.get(self, 'virtual_network_tap')

class AwaitableGetNetworkInterfaceTapConfigurationResult(GetNetworkInterfaceTapConfigurationResult):

    def __await__(self):
        if False:
            yield self
        return GetNetworkInterfaceTapConfigurationResult(etag=self.etag, id=self.id, name=self.name, provisioning_state=self.provisioning_state, type=self.type, virtual_network_tap=self.virtual_network_tap)

def get_network_interface_tap_configuration(network_interface_name: Optional[str]=None, resource_group_name: Optional[str]=None, tap_configuration_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetNetworkInterfaceTapConfigurationResult:
    """
    Get the specified tap configuration on a network interface.


    :param str network_interface_name: The name of the network interface.
    :param str resource_group_name: The name of the resource group.
    :param str tap_configuration_name: The name of the tap configuration.
    """
    __args__ = dict()
    __args__['networkInterfaceName'] = network_interface_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tapConfigurationName'] = tap_configuration_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200801:getNetworkInterfaceTapConfiguration', __args__, opts=opts, typ=GetNetworkInterfaceTapConfigurationResult).value
    return AwaitableGetNetworkInterfaceTapConfigurationResult(etag=__ret__.etag, id=__ret__.id, name=__ret__.name, provisioning_state=__ret__.provisioning_state, type=__ret__.type, virtual_network_tap=__ret__.virtual_network_tap)

@_utilities.lift_output_func(get_network_interface_tap_configuration)
def get_network_interface_tap_configuration_output(network_interface_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tap_configuration_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetNetworkInterfaceTapConfigurationResult]:
    """
    Get the specified tap configuration on a network interface.


    :param str network_interface_name: The name of the network interface.
    :param str resource_group_name: The name of the resource group.
    :param str tap_configuration_name: The name of the tap configuration.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetRouteResult', 'AwaitableGetRouteResult', 'get_route', 'get_route_output']

@pulumi.output_type
class GetRouteResult:
    """
    Route resource.
    """

    def __init__(__self__, address_prefix=None, etag=None, id=None, name=None, next_hop_ip_address=None, next_hop_type=None, provisioning_state=None):
        if address_prefix and (not isinstance(address_prefix, str)):
            raise TypeError("Expected argument 'address_prefix' to be a str")
        pulumi.set(__self__, 'address_prefix', address_prefix)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if next_hop_ip_address and (not isinstance(next_hop_ip_address, str)):
            raise TypeError("Expected argument 'next_hop_ip_address' to be a str")
        pulumi.set(__self__, 'next_hop_ip_address', next_hop_ip_address)
        if next_hop_type and (not isinstance(next_hop_type, str)):
            raise TypeError("Expected argument 'next_hop_type' to be a str")
        pulumi.set(__self__, 'next_hop_type', next_hop_type)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)

    @property
    @pulumi.getter(name='addressPrefix')
    def address_prefix(self) -> Optional[str]:
        """
        The destination CIDR to which the route applies.
        """
        return pulumi.get(self, 'address_prefix')

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
    @pulumi.getter(name='nextHopIpAddress')
    def next_hop_ip_address(self) -> Optional[str]:
        """
        The IP address packets should be forwarded to. Next hop values are only allowed in routes where the next hop type is VirtualAppliance.
        """
        return pulumi.get(self, 'next_hop_ip_address')

    @property
    @pulumi.getter(name='nextHopType')
    def next_hop_type(self) -> str:
        """
        The type of Azure hop the packet should be sent to.
        """
        return pulumi.get(self, 'next_hop_type')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the route resource.
        """
        return pulumi.get(self, 'provisioning_state')

class AwaitableGetRouteResult(GetRouteResult):

    def __await__(self):
        if False:
            yield self
        return GetRouteResult(address_prefix=self.address_prefix, etag=self.etag, id=self.id, name=self.name, next_hop_ip_address=self.next_hop_ip_address, next_hop_type=self.next_hop_type, provisioning_state=self.provisioning_state)

def get_route(resource_group_name: Optional[str]=None, route_name: Optional[str]=None, route_table_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetRouteResult:
    """
    Gets the specified route from a route table.


    :param str resource_group_name: The name of the resource group.
    :param str route_name: The name of the route.
    :param str route_table_name: The name of the route table.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['routeName'] = route_name
    __args__['routeTableName'] = route_table_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200701:getRoute', __args__, opts=opts, typ=GetRouteResult).value
    return AwaitableGetRouteResult(address_prefix=__ret__.address_prefix, etag=__ret__.etag, id=__ret__.id, name=__ret__.name, next_hop_ip_address=__ret__.next_hop_ip_address, next_hop_type=__ret__.next_hop_type, provisioning_state=__ret__.provisioning_state)

@_utilities.lift_output_func(get_route)
def get_route_output(resource_group_name: Optional[pulumi.Input[str]]=None, route_name: Optional[pulumi.Input[str]]=None, route_table_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetRouteResult]:
    """
    Gets the specified route from a route table.


    :param str resource_group_name: The name of the resource group.
    :param str route_name: The name of the route.
    :param str route_table_name: The name of the route table.
    """
    ...
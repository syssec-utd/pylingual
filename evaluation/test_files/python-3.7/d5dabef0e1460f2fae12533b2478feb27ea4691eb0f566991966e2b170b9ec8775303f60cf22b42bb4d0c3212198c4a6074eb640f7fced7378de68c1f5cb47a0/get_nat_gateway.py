import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetNatGatewayResult', 'AwaitableGetNatGatewayResult', 'get_nat_gateway', 'get_nat_gateway_output']

@pulumi.output_type
class GetNatGatewayResult:
    """
    Nat Gateway resource.
    """

    def __init__(__self__, etag=None, id=None, idle_timeout_in_minutes=None, location=None, name=None, provisioning_state=None, public_ip_addresses=None, public_ip_prefixes=None, resource_guid=None, sku=None, subnets=None, tags=None, type=None, zones=None):
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if idle_timeout_in_minutes and (not isinstance(idle_timeout_in_minutes, int)):
            raise TypeError("Expected argument 'idle_timeout_in_minutes' to be a int")
        pulumi.set(__self__, 'idle_timeout_in_minutes', idle_timeout_in_minutes)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if public_ip_addresses and (not isinstance(public_ip_addresses, list)):
            raise TypeError("Expected argument 'public_ip_addresses' to be a list")
        pulumi.set(__self__, 'public_ip_addresses', public_ip_addresses)
        if public_ip_prefixes and (not isinstance(public_ip_prefixes, list)):
            raise TypeError("Expected argument 'public_ip_prefixes' to be a list")
        pulumi.set(__self__, 'public_ip_prefixes', public_ip_prefixes)
        if resource_guid and (not isinstance(resource_guid, str)):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, 'resource_guid', resource_guid)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if subnets and (not isinstance(subnets, list)):
            raise TypeError("Expected argument 'subnets' to be a list")
        pulumi.set(__self__, 'subnets', subnets)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if zones and (not isinstance(zones, list)):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, 'zones', zones)

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
    @pulumi.getter(name='idleTimeoutInMinutes')
    def idle_timeout_in_minutes(self) -> Optional[int]:
        """
        The idle timeout of the nat gateway.
        """
        return pulumi.get(self, 'idle_timeout_in_minutes')

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
        The provisioning state of the NAT gateway resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publicIpAddresses')
    def public_ip_addresses(self) -> Optional[Sequence['outputs.SubResourceResponse']]:
        """
        An array of public ip addresses associated with the nat gateway resource.
        """
        return pulumi.get(self, 'public_ip_addresses')

    @property
    @pulumi.getter(name='publicIpPrefixes')
    def public_ip_prefixes(self) -> Optional[Sequence['outputs.SubResourceResponse']]:
        """
        An array of public ip prefixes associated with the nat gateway resource.
        """
        return pulumi.get(self, 'public_ip_prefixes')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> str:
        """
        The resource GUID property of the NAT gateway resource.
        """
        return pulumi.get(self, 'resource_guid')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.NatGatewaySkuResponse']:
        """
        The nat gateway SKU.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def subnets(self) -> Sequence['outputs.SubResourceResponse']:
        """
        An array of references to the subnets using this nat gateway resource.
        """
        return pulumi.get(self, 'subnets')

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
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        A list of availability zones denoting the zone in which Nat Gateway should be deployed.
        """
        return pulumi.get(self, 'zones')

class AwaitableGetNatGatewayResult(GetNatGatewayResult):

    def __await__(self):
        if False:
            yield self
        return GetNatGatewayResult(etag=self.etag, id=self.id, idle_timeout_in_minutes=self.idle_timeout_in_minutes, location=self.location, name=self.name, provisioning_state=self.provisioning_state, public_ip_addresses=self.public_ip_addresses, public_ip_prefixes=self.public_ip_prefixes, resource_guid=self.resource_guid, sku=self.sku, subnets=self.subnets, tags=self.tags, type=self.type, zones=self.zones)

def get_nat_gateway(expand: Optional[str]=None, nat_gateway_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetNatGatewayResult:
    """
    Gets the specified nat gateway in a specified resource group.
    API Version: 2020-11-01.


    :param str expand: Expands referenced resources.
    :param str nat_gateway_name: The name of the nat gateway.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['natGatewayName'] = nat_gateway_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network:getNatGateway', __args__, opts=opts, typ=GetNatGatewayResult).value
    return AwaitableGetNatGatewayResult(etag=__ret__.etag, id=__ret__.id, idle_timeout_in_minutes=__ret__.idle_timeout_in_minutes, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, public_ip_addresses=__ret__.public_ip_addresses, public_ip_prefixes=__ret__.public_ip_prefixes, resource_guid=__ret__.resource_guid, sku=__ret__.sku, subnets=__ret__.subnets, tags=__ret__.tags, type=__ret__.type, zones=__ret__.zones)

@_utilities.lift_output_func(get_nat_gateway)
def get_nat_gateway_output(expand: Optional[pulumi.Input[Optional[str]]]=None, nat_gateway_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetNatGatewayResult]:
    """
    Gets the specified nat gateway in a specified resource group.
    API Version: 2020-11-01.


    :param str expand: Expands referenced resources.
    :param str nat_gateway_name: The name of the nat gateway.
    :param str resource_group_name: The name of the resource group.
    """
    ...
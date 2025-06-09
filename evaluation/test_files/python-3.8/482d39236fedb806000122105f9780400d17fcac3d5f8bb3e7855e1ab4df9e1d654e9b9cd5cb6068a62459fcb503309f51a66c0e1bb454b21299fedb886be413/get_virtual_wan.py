import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetVirtualWanResult', 'AwaitableGetVirtualWanResult', 'get_virtual_wan', 'get_virtual_wan_output']

@pulumi.output_type
class GetVirtualWanResult:
    """
    VirtualWAN Resource.
    """

    def __init__(__self__, allow_branch_to_branch_traffic=None, allow_vnet_to_vnet_traffic=None, disable_vpn_encryption=None, etag=None, id=None, location=None, name=None, office365_local_breakout_category=None, provisioning_state=None, tags=None, type=None, virtual_hubs=None, vpn_sites=None):
        if allow_branch_to_branch_traffic and (not isinstance(allow_branch_to_branch_traffic, bool)):
            raise TypeError("Expected argument 'allow_branch_to_branch_traffic' to be a bool")
        pulumi.set(__self__, 'allow_branch_to_branch_traffic', allow_branch_to_branch_traffic)
        if allow_vnet_to_vnet_traffic and (not isinstance(allow_vnet_to_vnet_traffic, bool)):
            raise TypeError("Expected argument 'allow_vnet_to_vnet_traffic' to be a bool")
        pulumi.set(__self__, 'allow_vnet_to_vnet_traffic', allow_vnet_to_vnet_traffic)
        if disable_vpn_encryption and (not isinstance(disable_vpn_encryption, bool)):
            raise TypeError("Expected argument 'disable_vpn_encryption' to be a bool")
        pulumi.set(__self__, 'disable_vpn_encryption', disable_vpn_encryption)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if office365_local_breakout_category and (not isinstance(office365_local_breakout_category, str)):
            raise TypeError("Expected argument 'office365_local_breakout_category' to be a str")
        pulumi.set(__self__, 'office365_local_breakout_category', office365_local_breakout_category)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if virtual_hubs and (not isinstance(virtual_hubs, list)):
            raise TypeError("Expected argument 'virtual_hubs' to be a list")
        pulumi.set(__self__, 'virtual_hubs', virtual_hubs)
        if vpn_sites and (not isinstance(vpn_sites, list)):
            raise TypeError("Expected argument 'vpn_sites' to be a list")
        pulumi.set(__self__, 'vpn_sites', vpn_sites)

    @property
    @pulumi.getter(name='allowBranchToBranchTraffic')
    def allow_branch_to_branch_traffic(self) -> Optional[bool]:
        """
        True if branch to branch traffic is allowed.
        """
        return pulumi.get(self, 'allow_branch_to_branch_traffic')

    @property
    @pulumi.getter(name='allowVnetToVnetTraffic')
    def allow_vnet_to_vnet_traffic(self) -> Optional[bool]:
        """
        True if Vnet to Vnet traffic is allowed.
        """
        return pulumi.get(self, 'allow_vnet_to_vnet_traffic')

    @property
    @pulumi.getter(name='disableVpnEncryption')
    def disable_vpn_encryption(self) -> Optional[bool]:
        """
        Vpn encryption to be disabled or not.
        """
        return pulumi.get(self, 'disable_vpn_encryption')

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
    @pulumi.getter(name='office365LocalBreakoutCategory')
    def office365_local_breakout_category(self) -> str:
        """
        The office local breakout category.
        """
        return pulumi.get(self, 'office365_local_breakout_category')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the virtual WAN resource.
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
    @pulumi.getter(name='virtualHubs')
    def virtual_hubs(self) -> Sequence['outputs.SubResourceResponse']:
        """
        List of VirtualHubs in the VirtualWAN.
        """
        return pulumi.get(self, 'virtual_hubs')

    @property
    @pulumi.getter(name='vpnSites')
    def vpn_sites(self) -> Sequence['outputs.SubResourceResponse']:
        """
        List of VpnSites in the VirtualWAN.
        """
        return pulumi.get(self, 'vpn_sites')

class AwaitableGetVirtualWanResult(GetVirtualWanResult):

    def __await__(self):
        if False:
            yield self
        return GetVirtualWanResult(allow_branch_to_branch_traffic=self.allow_branch_to_branch_traffic, allow_vnet_to_vnet_traffic=self.allow_vnet_to_vnet_traffic, disable_vpn_encryption=self.disable_vpn_encryption, etag=self.etag, id=self.id, location=self.location, name=self.name, office365_local_breakout_category=self.office365_local_breakout_category, provisioning_state=self.provisioning_state, tags=self.tags, type=self.type, virtual_hubs=self.virtual_hubs, vpn_sites=self.vpn_sites)

def get_virtual_wan(resource_group_name: Optional[str]=None, virtual_wan_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVirtualWanResult:
    """
    Retrieves the details of a VirtualWAN.


    :param str resource_group_name: The resource group name of the VirtualWan.
    :param str virtual_wan_name: The name of the VirtualWAN being retrieved.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualWANName'] = virtual_wan_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20191201:getVirtualWan', __args__, opts=opts, typ=GetVirtualWanResult).value
    return AwaitableGetVirtualWanResult(allow_branch_to_branch_traffic=__ret__.allow_branch_to_branch_traffic, allow_vnet_to_vnet_traffic=__ret__.allow_vnet_to_vnet_traffic, disable_vpn_encryption=__ret__.disable_vpn_encryption, etag=__ret__.etag, id=__ret__.id, location=__ret__.location, name=__ret__.name, office365_local_breakout_category=__ret__.office365_local_breakout_category, provisioning_state=__ret__.provisioning_state, tags=__ret__.tags, type=__ret__.type, virtual_hubs=__ret__.virtual_hubs, vpn_sites=__ret__.vpn_sites)

@_utilities.lift_output_func(get_virtual_wan)
def get_virtual_wan_output(resource_group_name: Optional[pulumi.Input[str]]=None, virtual_wan_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVirtualWanResult]:
    """
    Retrieves the details of a VirtualWAN.


    :param str resource_group_name: The resource group name of the VirtualWan.
    :param str virtual_wan_name: The name of the VirtualWAN being retrieved.
    """
    ...
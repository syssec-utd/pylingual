import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetNatRuleResult', 'AwaitableGetNatRuleResult', 'get_nat_rule', 'get_nat_rule_output']

@pulumi.output_type
class GetNatRuleResult:
    """
    VpnGatewayNatRule Resource.
    """

    def __init__(__self__, egress_vpn_site_link_connections=None, etag=None, external_mappings=None, id=None, ingress_vpn_site_link_connections=None, internal_mappings=None, ip_configuration_id=None, mode=None, name=None, provisioning_state=None, type=None):
        if egress_vpn_site_link_connections and (not isinstance(egress_vpn_site_link_connections, list)):
            raise TypeError("Expected argument 'egress_vpn_site_link_connections' to be a list")
        pulumi.set(__self__, 'egress_vpn_site_link_connections', egress_vpn_site_link_connections)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if external_mappings and (not isinstance(external_mappings, list)):
            raise TypeError("Expected argument 'external_mappings' to be a list")
        pulumi.set(__self__, 'external_mappings', external_mappings)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if ingress_vpn_site_link_connections and (not isinstance(ingress_vpn_site_link_connections, list)):
            raise TypeError("Expected argument 'ingress_vpn_site_link_connections' to be a list")
        pulumi.set(__self__, 'ingress_vpn_site_link_connections', ingress_vpn_site_link_connections)
        if internal_mappings and (not isinstance(internal_mappings, list)):
            raise TypeError("Expected argument 'internal_mappings' to be a list")
        pulumi.set(__self__, 'internal_mappings', internal_mappings)
        if ip_configuration_id and (not isinstance(ip_configuration_id, str)):
            raise TypeError("Expected argument 'ip_configuration_id' to be a str")
        pulumi.set(__self__, 'ip_configuration_id', ip_configuration_id)
        if mode and (not isinstance(mode, str)):
            raise TypeError("Expected argument 'mode' to be a str")
        pulumi.set(__self__, 'mode', mode)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='egressVpnSiteLinkConnections')
    def egress_vpn_site_link_connections(self) -> Sequence['outputs.SubResourceResponse']:
        """
        List of egress VpnSiteLinkConnections.
        """
        return pulumi.get(self, 'egress_vpn_site_link_connections')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='externalMappings')
    def external_mappings(self) -> Optional[Sequence['outputs.VpnNatRuleMappingResponse']]:
        """
        The private IP address external mapping for NAT.
        """
        return pulumi.get(self, 'external_mappings')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='ingressVpnSiteLinkConnections')
    def ingress_vpn_site_link_connections(self) -> Sequence['outputs.SubResourceResponse']:
        """
        List of ingress VpnSiteLinkConnections.
        """
        return pulumi.get(self, 'ingress_vpn_site_link_connections')

    @property
    @pulumi.getter(name='internalMappings')
    def internal_mappings(self) -> Optional[Sequence['outputs.VpnNatRuleMappingResponse']]:
        """
        The private IP address internal mapping for NAT.
        """
        return pulumi.get(self, 'internal_mappings')

    @property
    @pulumi.getter(name='ipConfigurationId')
    def ip_configuration_id(self) -> Optional[str]:
        """
        The IP Configuration ID this NAT rule applies to.
        """
        return pulumi.get(self, 'ip_configuration_id')

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        The Source NAT direction of a VPN NAT.
        """
        return pulumi.get(self, 'mode')

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
        The provisioning state of the NAT Rule resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetNatRuleResult(GetNatRuleResult):

    def __await__(self):
        if False:
            yield self
        return GetNatRuleResult(egress_vpn_site_link_connections=self.egress_vpn_site_link_connections, etag=self.etag, external_mappings=self.external_mappings, id=self.id, ingress_vpn_site_link_connections=self.ingress_vpn_site_link_connections, internal_mappings=self.internal_mappings, ip_configuration_id=self.ip_configuration_id, mode=self.mode, name=self.name, provisioning_state=self.provisioning_state, type=self.type)

def get_nat_rule(gateway_name: Optional[str]=None, nat_rule_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetNatRuleResult:
    """
    VpnGatewayNatRule Resource.


    :param str gateway_name: The name of the gateway.
    :param str nat_rule_name: The name of the nat rule.
    :param str resource_group_name: The resource group name of the VpnGateway.
    """
    __args__ = dict()
    __args__['gatewayName'] = gateway_name
    __args__['natRuleName'] = nat_rule_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200801:getNatRule', __args__, opts=opts, typ=GetNatRuleResult).value
    return AwaitableGetNatRuleResult(egress_vpn_site_link_connections=__ret__.egress_vpn_site_link_connections, etag=__ret__.etag, external_mappings=__ret__.external_mappings, id=__ret__.id, ingress_vpn_site_link_connections=__ret__.ingress_vpn_site_link_connections, internal_mappings=__ret__.internal_mappings, ip_configuration_id=__ret__.ip_configuration_id, mode=__ret__.mode, name=__ret__.name, provisioning_state=__ret__.provisioning_state, type=__ret__.type)

@_utilities.lift_output_func(get_nat_rule)
def get_nat_rule_output(gateway_name: Optional[pulumi.Input[str]]=None, nat_rule_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetNatRuleResult]:
    """
    VpnGatewayNatRule Resource.


    :param str gateway_name: The name of the gateway.
    :param str nat_rule_name: The name of the nat rule.
    :param str resource_group_name: The resource group name of the VpnGateway.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetExpressRouteCircuitPeeringResult', 'AwaitableGetExpressRouteCircuitPeeringResult', 'get_express_route_circuit_peering', 'get_express_route_circuit_peering_output']
warnings.warn('Version 2015-06-15 will be removed in v2 of the provider.', DeprecationWarning)

@pulumi.output_type
class GetExpressRouteCircuitPeeringResult:
    """
    Peering in an ExpressRouteCircuit resource.
    """

    def __init__(__self__, azure_asn=None, etag=None, id=None, microsoft_peering_config=None, name=None, peer_asn=None, peering_type=None, primary_azure_port=None, primary_peer_address_prefix=None, provisioning_state=None, secondary_azure_port=None, secondary_peer_address_prefix=None, shared_key=None, state=None, stats=None, vlan_id=None):
        if azure_asn and (not isinstance(azure_asn, int)):
            raise TypeError("Expected argument 'azure_asn' to be a int")
        pulumi.set(__self__, 'azure_asn', azure_asn)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if microsoft_peering_config and (not isinstance(microsoft_peering_config, dict)):
            raise TypeError("Expected argument 'microsoft_peering_config' to be a dict")
        pulumi.set(__self__, 'microsoft_peering_config', microsoft_peering_config)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if peer_asn and (not isinstance(peer_asn, int)):
            raise TypeError("Expected argument 'peer_asn' to be a int")
        pulumi.set(__self__, 'peer_asn', peer_asn)
        if peering_type and (not isinstance(peering_type, str)):
            raise TypeError("Expected argument 'peering_type' to be a str")
        pulumi.set(__self__, 'peering_type', peering_type)
        if primary_azure_port and (not isinstance(primary_azure_port, str)):
            raise TypeError("Expected argument 'primary_azure_port' to be a str")
        pulumi.set(__self__, 'primary_azure_port', primary_azure_port)
        if primary_peer_address_prefix and (not isinstance(primary_peer_address_prefix, str)):
            raise TypeError("Expected argument 'primary_peer_address_prefix' to be a str")
        pulumi.set(__self__, 'primary_peer_address_prefix', primary_peer_address_prefix)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if secondary_azure_port and (not isinstance(secondary_azure_port, str)):
            raise TypeError("Expected argument 'secondary_azure_port' to be a str")
        pulumi.set(__self__, 'secondary_azure_port', secondary_azure_port)
        if secondary_peer_address_prefix and (not isinstance(secondary_peer_address_prefix, str)):
            raise TypeError("Expected argument 'secondary_peer_address_prefix' to be a str")
        pulumi.set(__self__, 'secondary_peer_address_prefix', secondary_peer_address_prefix)
        if shared_key and (not isinstance(shared_key, str)):
            raise TypeError("Expected argument 'shared_key' to be a str")
        pulumi.set(__self__, 'shared_key', shared_key)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if stats and (not isinstance(stats, dict)):
            raise TypeError("Expected argument 'stats' to be a dict")
        pulumi.set(__self__, 'stats', stats)
        if vlan_id and (not isinstance(vlan_id, int)):
            raise TypeError("Expected argument 'vlan_id' to be a int")
        pulumi.set(__self__, 'vlan_id', vlan_id)

    @property
    @pulumi.getter(name='azureASN')
    def azure_asn(self) -> Optional[int]:
        """
        The Azure ASN.
        """
        return pulumi.get(self, 'azure_asn')

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource Identifier.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='microsoftPeeringConfig')
    def microsoft_peering_config(self) -> Optional['outputs.ExpressRouteCircuitPeeringConfigResponse']:
        """
        The Microsoft peering configuration.
        """
        return pulumi.get(self, 'microsoft_peering_config')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='peerASN')
    def peer_asn(self) -> Optional[int]:
        """
        The peer ASN.
        """
        return pulumi.get(self, 'peer_asn')

    @property
    @pulumi.getter(name='peeringType')
    def peering_type(self) -> Optional[str]:
        """
        The PeeringType. Possible values are: 'AzurePublicPeering', 'AzurePrivatePeering', and 'MicrosoftPeering'.
        """
        return pulumi.get(self, 'peering_type')

    @property
    @pulumi.getter(name='primaryAzurePort')
    def primary_azure_port(self) -> Optional[str]:
        """
        The primary port.
        """
        return pulumi.get(self, 'primary_azure_port')

    @property
    @pulumi.getter(name='primaryPeerAddressPrefix')
    def primary_peer_address_prefix(self) -> Optional[str]:
        """
        The primary address prefix.
        """
        return pulumi.get(self, 'primary_peer_address_prefix')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[str]:
        """
        Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='secondaryAzurePort')
    def secondary_azure_port(self) -> Optional[str]:
        """
        The secondary port.
        """
        return pulumi.get(self, 'secondary_azure_port')

    @property
    @pulumi.getter(name='secondaryPeerAddressPrefix')
    def secondary_peer_address_prefix(self) -> Optional[str]:
        """
        The secondary address prefix.
        """
        return pulumi.get(self, 'secondary_peer_address_prefix')

    @property
    @pulumi.getter(name='sharedKey')
    def shared_key(self) -> Optional[str]:
        """
        The shared key.
        """
        return pulumi.get(self, 'shared_key')

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of peering. Possible values are: 'Disabled' and 'Enabled'
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter
    def stats(self) -> Optional['outputs.ExpressRouteCircuitStatsResponse']:
        """
        Gets peering stats.
        """
        return pulumi.get(self, 'stats')

    @property
    @pulumi.getter(name='vlanId')
    def vlan_id(self) -> Optional[int]:
        """
        The VLAN ID.
        """
        return pulumi.get(self, 'vlan_id')

class AwaitableGetExpressRouteCircuitPeeringResult(GetExpressRouteCircuitPeeringResult):

    def __await__(self):
        if False:
            yield self
        return GetExpressRouteCircuitPeeringResult(azure_asn=self.azure_asn, etag=self.etag, id=self.id, microsoft_peering_config=self.microsoft_peering_config, name=self.name, peer_asn=self.peer_asn, peering_type=self.peering_type, primary_azure_port=self.primary_azure_port, primary_peer_address_prefix=self.primary_peer_address_prefix, provisioning_state=self.provisioning_state, secondary_azure_port=self.secondary_azure_port, secondary_peer_address_prefix=self.secondary_peer_address_prefix, shared_key=self.shared_key, state=self.state, stats=self.stats, vlan_id=self.vlan_id)

def get_express_route_circuit_peering(circuit_name: Optional[str]=None, peering_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetExpressRouteCircuitPeeringResult:
    """
    Gets the specified authorization from the specified express route circuit.


    :param str circuit_name: The name of the express route circuit.
    :param str peering_name: The name of the peering.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn('get_express_route_circuit_peering is deprecated: Version 2015-06-15 will be removed in v2 of the provider.')
    __args__ = dict()
    __args__['circuitName'] = circuit_name
    __args__['peeringName'] = peering_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20150615:getExpressRouteCircuitPeering', __args__, opts=opts, typ=GetExpressRouteCircuitPeeringResult).value
    return AwaitableGetExpressRouteCircuitPeeringResult(azure_asn=__ret__.azure_asn, etag=__ret__.etag, id=__ret__.id, microsoft_peering_config=__ret__.microsoft_peering_config, name=__ret__.name, peer_asn=__ret__.peer_asn, peering_type=__ret__.peering_type, primary_azure_port=__ret__.primary_azure_port, primary_peer_address_prefix=__ret__.primary_peer_address_prefix, provisioning_state=__ret__.provisioning_state, secondary_azure_port=__ret__.secondary_azure_port, secondary_peer_address_prefix=__ret__.secondary_peer_address_prefix, shared_key=__ret__.shared_key, state=__ret__.state, stats=__ret__.stats, vlan_id=__ret__.vlan_id)

@_utilities.lift_output_func(get_express_route_circuit_peering)
def get_express_route_circuit_peering_output(circuit_name: Optional[pulumi.Input[str]]=None, peering_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetExpressRouteCircuitPeeringResult]:
    """
    Gets the specified authorization from the specified express route circuit.


    :param str circuit_name: The name of the express route circuit.
    :param str peering_name: The name of the peering.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn('get_express_route_circuit_peering is deprecated: Version 2015-06-15 will be removed in v2 of the provider.')
    ...
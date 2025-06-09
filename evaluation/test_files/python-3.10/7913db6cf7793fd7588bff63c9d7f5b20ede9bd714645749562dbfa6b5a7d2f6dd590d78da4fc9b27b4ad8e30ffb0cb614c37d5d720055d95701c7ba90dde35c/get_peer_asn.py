import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPeerAsnResult', 'AwaitableGetPeerAsnResult', 'get_peer_asn', 'get_peer_asn_output']

@pulumi.output_type
class GetPeerAsnResult:
    """
    The essential information related to the peer's ASN.
    """

    def __init__(__self__, error_message=None, id=None, name=None, peer_asn=None, peer_contact_detail=None, peer_name=None, type=None, validation_state=None):
        if error_message and (not isinstance(error_message, str)):
            raise TypeError("Expected argument 'error_message' to be a str")
        pulumi.set(__self__, 'error_message', error_message)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if peer_asn and (not isinstance(peer_asn, int)):
            raise TypeError("Expected argument 'peer_asn' to be a int")
        pulumi.set(__self__, 'peer_asn', peer_asn)
        if peer_contact_detail and (not isinstance(peer_contact_detail, list)):
            raise TypeError("Expected argument 'peer_contact_detail' to be a list")
        pulumi.set(__self__, 'peer_contact_detail', peer_contact_detail)
        if peer_name and (not isinstance(peer_name, str)):
            raise TypeError("Expected argument 'peer_name' to be a str")
        pulumi.set(__self__, 'peer_name', peer_name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if validation_state and (not isinstance(validation_state, str)):
            raise TypeError("Expected argument 'validation_state' to be a str")
        pulumi.set(__self__, 'validation_state', validation_state)

    @property
    @pulumi.getter(name='errorMessage')
    def error_message(self) -> str:
        """
        The error message for the validation state
        """
        return pulumi.get(self, 'error_message')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource.
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
    @pulumi.getter(name='peerAsn')
    def peer_asn(self) -> Optional[int]:
        """
        The Autonomous System Number (ASN) of the peer.
        """
        return pulumi.get(self, 'peer_asn')

    @property
    @pulumi.getter(name='peerContactDetail')
    def peer_contact_detail(self) -> Optional[Sequence['outputs.ContactDetailResponse']]:
        """
        The contact details of the peer.
        """
        return pulumi.get(self, 'peer_contact_detail')

    @property
    @pulumi.getter(name='peerName')
    def peer_name(self) -> Optional[str]:
        """
        The name of the peer.
        """
        return pulumi.get(self, 'peer_name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='validationState')
    def validation_state(self) -> Optional[str]:
        """
        The validation state of the ASN associated with the peer.
        """
        return pulumi.get(self, 'validation_state')

class AwaitableGetPeerAsnResult(GetPeerAsnResult):

    def __await__(self):
        if False:
            yield self
        return GetPeerAsnResult(error_message=self.error_message, id=self.id, name=self.name, peer_asn=self.peer_asn, peer_contact_detail=self.peer_contact_detail, peer_name=self.peer_name, type=self.type, validation_state=self.validation_state)

def get_peer_asn(peer_asn_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPeerAsnResult:
    """
    Gets the peer ASN with the specified name under the given subscription.


    :param str peer_asn_name: The peer ASN name.
    """
    __args__ = dict()
    __args__['peerAsnName'] = peer_asn_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:peering/v20210101:getPeerAsn', __args__, opts=opts, typ=GetPeerAsnResult).value
    return AwaitableGetPeerAsnResult(error_message=__ret__.error_message, id=__ret__.id, name=__ret__.name, peer_asn=__ret__.peer_asn, peer_contact_detail=__ret__.peer_contact_detail, peer_name=__ret__.peer_name, type=__ret__.type, validation_state=__ret__.validation_state)

@_utilities.lift_output_func(get_peer_asn)
def get_peer_asn_output(peer_asn_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPeerAsnResult]:
    """
    Gets the peer ASN with the specified name under the given subscription.


    :param str peer_asn_name: The peer ASN name.
    """
    ...
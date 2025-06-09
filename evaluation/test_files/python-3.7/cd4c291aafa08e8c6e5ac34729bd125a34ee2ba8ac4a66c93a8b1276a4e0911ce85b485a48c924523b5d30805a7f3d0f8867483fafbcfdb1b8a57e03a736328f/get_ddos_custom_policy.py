import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetDdosCustomPolicyResult', 'AwaitableGetDdosCustomPolicyResult', 'get_ddos_custom_policy', 'get_ddos_custom_policy_output']

@pulumi.output_type
class GetDdosCustomPolicyResult:
    """
    A DDoS custom policy in a resource group.
    """

    def __init__(__self__, etag=None, id=None, location=None, name=None, protocol_custom_settings=None, provisioning_state=None, public_ip_addresses=None, resource_guid=None, tags=None, type=None):
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
        if protocol_custom_settings and (not isinstance(protocol_custom_settings, list)):
            raise TypeError("Expected argument 'protocol_custom_settings' to be a list")
        pulumi.set(__self__, 'protocol_custom_settings', protocol_custom_settings)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if public_ip_addresses and (not isinstance(public_ip_addresses, list)):
            raise TypeError("Expected argument 'public_ip_addresses' to be a list")
        pulumi.set(__self__, 'public_ip_addresses', public_ip_addresses)
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
    @pulumi.getter(name='protocolCustomSettings')
    def protocol_custom_settings(self) -> Optional[Sequence['outputs.ProtocolCustomSettingsFormatResponse']]:
        """
        The protocol-specific DDoS policy customization parameters.
        """
        return pulumi.get(self, 'protocol_custom_settings')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the DDoS custom policy resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publicIPAddresses')
    def public_ip_addresses(self) -> Sequence['outputs.SubResourceResponse']:
        """
        The list of public IPs associated with the DDoS custom policy resource. This list is read-only.
        """
        return pulumi.get(self, 'public_ip_addresses')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> str:
        """
        The resource GUID property of the DDoS custom policy resource. It uniquely identifies the resource, even if the user changes its name or migrate the resource across subscriptions or resource groups.
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

class AwaitableGetDdosCustomPolicyResult(GetDdosCustomPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetDdosCustomPolicyResult(etag=self.etag, id=self.id, location=self.location, name=self.name, protocol_custom_settings=self.protocol_custom_settings, provisioning_state=self.provisioning_state, public_ip_addresses=self.public_ip_addresses, resource_guid=self.resource_guid, tags=self.tags, type=self.type)

def get_ddos_custom_policy(ddos_custom_policy_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDdosCustomPolicyResult:
    """
    A DDoS custom policy in a resource group.


    :param str ddos_custom_policy_name: The name of the DDoS custom policy.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['ddosCustomPolicyName'] = ddos_custom_policy_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20210301:getDdosCustomPolicy', __args__, opts=opts, typ=GetDdosCustomPolicyResult).value
    return AwaitableGetDdosCustomPolicyResult(etag=__ret__.etag, id=__ret__.id, location=__ret__.location, name=__ret__.name, protocol_custom_settings=__ret__.protocol_custom_settings, provisioning_state=__ret__.provisioning_state, public_ip_addresses=__ret__.public_ip_addresses, resource_guid=__ret__.resource_guid, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_ddos_custom_policy)
def get_ddos_custom_policy_output(ddos_custom_policy_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDdosCustomPolicyResult]:
    """
    A DDoS custom policy in a resource group.


    :param str ddos_custom_policy_name: The name of the DDoS custom policy.
    :param str resource_group_name: The name of the resource group.
    """
    ...
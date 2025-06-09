import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetStreamingPolicyResult', 'AwaitableGetStreamingPolicyResult', 'get_streaming_policy', 'get_streaming_policy_output']

@pulumi.output_type
class GetStreamingPolicyResult:
    """
    A Streaming Policy resource
    """

    def __init__(__self__, common_encryption_cbcs=None, common_encryption_cenc=None, created=None, default_content_key_policy_name=None, envelope_encryption=None, id=None, name=None, no_encryption=None, system_data=None, type=None):
        if common_encryption_cbcs and (not isinstance(common_encryption_cbcs, dict)):
            raise TypeError("Expected argument 'common_encryption_cbcs' to be a dict")
        pulumi.set(__self__, 'common_encryption_cbcs', common_encryption_cbcs)
        if common_encryption_cenc and (not isinstance(common_encryption_cenc, dict)):
            raise TypeError("Expected argument 'common_encryption_cenc' to be a dict")
        pulumi.set(__self__, 'common_encryption_cenc', common_encryption_cenc)
        if created and (not isinstance(created, str)):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, 'created', created)
        if default_content_key_policy_name and (not isinstance(default_content_key_policy_name, str)):
            raise TypeError("Expected argument 'default_content_key_policy_name' to be a str")
        pulumi.set(__self__, 'default_content_key_policy_name', default_content_key_policy_name)
        if envelope_encryption and (not isinstance(envelope_encryption, dict)):
            raise TypeError("Expected argument 'envelope_encryption' to be a dict")
        pulumi.set(__self__, 'envelope_encryption', envelope_encryption)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if no_encryption and (not isinstance(no_encryption, dict)):
            raise TypeError("Expected argument 'no_encryption' to be a dict")
        pulumi.set(__self__, 'no_encryption', no_encryption)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='commonEncryptionCbcs')
    def common_encryption_cbcs(self) -> Optional['outputs.CommonEncryptionCbcsResponse']:
        """
        Configuration of CommonEncryptionCbcs
        """
        return pulumi.get(self, 'common_encryption_cbcs')

    @property
    @pulumi.getter(name='commonEncryptionCenc')
    def common_encryption_cenc(self) -> Optional['outputs.CommonEncryptionCencResponse']:
        """
        Configuration of CommonEncryptionCenc
        """
        return pulumi.get(self, 'common_encryption_cenc')

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        Creation time of Streaming Policy
        """
        return pulumi.get(self, 'created')

    @property
    @pulumi.getter(name='defaultContentKeyPolicyName')
    def default_content_key_policy_name(self) -> Optional[str]:
        """
        Default ContentKey used by current Streaming Policy
        """
        return pulumi.get(self, 'default_content_key_policy_name')

    @property
    @pulumi.getter(name='envelopeEncryption')
    def envelope_encryption(self) -> Optional['outputs.EnvelopeEncryptionResponse']:
        """
        Configuration of EnvelopeEncryption
        """
        return pulumi.get(self, 'envelope_encryption')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='noEncryption')
    def no_encryption(self) -> Optional['outputs.NoEncryptionResponse']:
        """
        Configurations of NoEncryption
        """
        return pulumi.get(self, 'no_encryption')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetStreamingPolicyResult(GetStreamingPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetStreamingPolicyResult(common_encryption_cbcs=self.common_encryption_cbcs, common_encryption_cenc=self.common_encryption_cenc, created=self.created, default_content_key_policy_name=self.default_content_key_policy_name, envelope_encryption=self.envelope_encryption, id=self.id, name=self.name, no_encryption=self.no_encryption, system_data=self.system_data, type=self.type)

def get_streaming_policy(account_name: Optional[str]=None, resource_group_name: Optional[str]=None, streaming_policy_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetStreamingPolicyResult:
    """
    Get the details of a Streaming Policy in the Media Services account


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_policy_name: The Streaming Policy name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['streamingPolicyName'] = streaming_policy_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:media/v20211101:getStreamingPolicy', __args__, opts=opts, typ=GetStreamingPolicyResult).value
    return AwaitableGetStreamingPolicyResult(common_encryption_cbcs=__ret__.common_encryption_cbcs, common_encryption_cenc=__ret__.common_encryption_cenc, created=__ret__.created, default_content_key_policy_name=__ret__.default_content_key_policy_name, envelope_encryption=__ret__.envelope_encryption, id=__ret__.id, name=__ret__.name, no_encryption=__ret__.no_encryption, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_streaming_policy)
def get_streaming_policy_output(account_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, streaming_policy_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetStreamingPolicyResult]:
    """
    Get the details of a Streaming Policy in the Media Services account


    :param str account_name: The Media Services account name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    :param str streaming_policy_name: The Streaming Policy name.
    """
    ...
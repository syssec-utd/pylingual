import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetRegisteredPrefixResult', 'AwaitableGetRegisteredPrefixResult', 'get_registered_prefix', 'get_registered_prefix_output']

@pulumi.output_type
class GetRegisteredPrefixResult:
    """
    The customer's prefix that is registered by the peering service provider.
    """

    def __init__(__self__, error_message=None, id=None, name=None, peering_service_prefix_key=None, prefix=None, prefix_validation_state=None, provisioning_state=None, type=None):
        if error_message and (not isinstance(error_message, str)):
            raise TypeError("Expected argument 'error_message' to be a str")
        pulumi.set(__self__, 'error_message', error_message)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if peering_service_prefix_key and (not isinstance(peering_service_prefix_key, str)):
            raise TypeError("Expected argument 'peering_service_prefix_key' to be a str")
        pulumi.set(__self__, 'peering_service_prefix_key', peering_service_prefix_key)
        if prefix and (not isinstance(prefix, str)):
            raise TypeError("Expected argument 'prefix' to be a str")
        pulumi.set(__self__, 'prefix', prefix)
        if prefix_validation_state and (not isinstance(prefix_validation_state, str)):
            raise TypeError("Expected argument 'prefix_validation_state' to be a str")
        pulumi.set(__self__, 'prefix_validation_state', prefix_validation_state)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='errorMessage')
    def error_message(self) -> str:
        """
        The error message associated with the validation state, if any.
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
    @pulumi.getter(name='peeringServicePrefixKey')
    def peering_service_prefix_key(self) -> str:
        """
        The peering service prefix key that is to be shared with the customer.
        """
        return pulumi.get(self, 'peering_service_prefix_key')

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        """
        The customer's prefix from which traffic originates.
        """
        return pulumi.get(self, 'prefix')

    @property
    @pulumi.getter(name='prefixValidationState')
    def prefix_validation_state(self) -> str:
        """
        The prefix validation state.
        """
        return pulumi.get(self, 'prefix_validation_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')

class AwaitableGetRegisteredPrefixResult(GetRegisteredPrefixResult):

    def __await__(self):
        if False:
            yield self
        return GetRegisteredPrefixResult(error_message=self.error_message, id=self.id, name=self.name, peering_service_prefix_key=self.peering_service_prefix_key, prefix=self.prefix, prefix_validation_state=self.prefix_validation_state, provisioning_state=self.provisioning_state, type=self.type)

def get_registered_prefix(peering_name: Optional[str]=None, registered_prefix_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetRegisteredPrefixResult:
    """
    The customer's prefix that is registered by the peering service provider.


    :param str peering_name: The name of the peering.
    :param str registered_prefix_name: The name of the registered prefix.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['peeringName'] = peering_name
    __args__['registeredPrefixName'] = registered_prefix_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:peering/v20210101:getRegisteredPrefix', __args__, opts=opts, typ=GetRegisteredPrefixResult).value
    return AwaitableGetRegisteredPrefixResult(error_message=__ret__.error_message, id=__ret__.id, name=__ret__.name, peering_service_prefix_key=__ret__.peering_service_prefix_key, prefix=__ret__.prefix, prefix_validation_state=__ret__.prefix_validation_state, provisioning_state=__ret__.provisioning_state, type=__ret__.type)

@_utilities.lift_output_func(get_registered_prefix)
def get_registered_prefix_output(peering_name: Optional[pulumi.Input[str]]=None, registered_prefix_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetRegisteredPrefixResult]:
    """
    The customer's prefix that is registered by the peering service provider.


    :param str peering_name: The name of the peering.
    :param str registered_prefix_name: The name of the registered prefix.
    :param str resource_group_name: The name of the resource group.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['ListWebAppHostKeysSlotResult', 'AwaitableListWebAppHostKeysSlotResult', 'list_web_app_host_keys_slot', 'list_web_app_host_keys_slot_output']

@pulumi.output_type
class ListWebAppHostKeysSlotResult:
    """
    Functions host level keys.
    """

    def __init__(__self__, function_keys=None, master_key=None, system_keys=None):
        if function_keys and (not isinstance(function_keys, dict)):
            raise TypeError("Expected argument 'function_keys' to be a dict")
        pulumi.set(__self__, 'function_keys', function_keys)
        if master_key and (not isinstance(master_key, str)):
            raise TypeError("Expected argument 'master_key' to be a str")
        pulumi.set(__self__, 'master_key', master_key)
        if system_keys and (not isinstance(system_keys, dict)):
            raise TypeError("Expected argument 'system_keys' to be a dict")
        pulumi.set(__self__, 'system_keys', system_keys)

    @property
    @pulumi.getter(name='functionKeys')
    def function_keys(self) -> Optional[Mapping[str, str]]:
        """
        Host level function keys.
        """
        return pulumi.get(self, 'function_keys')

    @property
    @pulumi.getter(name='masterKey')
    def master_key(self) -> Optional[str]:
        """
        Secret key.
        """
        return pulumi.get(self, 'master_key')

    @property
    @pulumi.getter(name='systemKeys')
    def system_keys(self) -> Optional[Mapping[str, str]]:
        """
        System keys.
        """
        return pulumi.get(self, 'system_keys')

class AwaitableListWebAppHostKeysSlotResult(ListWebAppHostKeysSlotResult):

    def __await__(self):
        if False:
            yield self
        return ListWebAppHostKeysSlotResult(function_keys=self.function_keys, master_key=self.master_key, system_keys=self.system_keys)

def list_web_app_host_keys_slot(name: Optional[str]=None, resource_group_name: Optional[str]=None, slot: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListWebAppHostKeysSlotResult:
    """
    Functions host level keys.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20201001:listWebAppHostKeysSlot', __args__, opts=opts, typ=ListWebAppHostKeysSlotResult).value
    return AwaitableListWebAppHostKeysSlotResult(function_keys=__ret__.function_keys, master_key=__ret__.master_key, system_keys=__ret__.system_keys)

@_utilities.lift_output_func(list_web_app_host_keys_slot)
def list_web_app_host_keys_slot_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListWebAppHostKeysSlotResult]:
    """
    Functions host level keys.


    :param str name: Site name.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot.
    """
    ...
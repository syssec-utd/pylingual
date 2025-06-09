import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['ListIotHubResourceKeysForKeyNameResult', 'AwaitableListIotHubResourceKeysForKeyNameResult', 'list_iot_hub_resource_keys_for_key_name', 'list_iot_hub_resource_keys_for_key_name_output']

@pulumi.output_type
class ListIotHubResourceKeysForKeyNameResult:
    """
    The properties of an IoT hub shared access policy.
    """

    def __init__(__self__, key_name=None, primary_key=None, rights=None, secondary_key=None):
        if key_name and (not isinstance(key_name, str)):
            raise TypeError("Expected argument 'key_name' to be a str")
        pulumi.set(__self__, 'key_name', key_name)
        if primary_key and (not isinstance(primary_key, str)):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, 'primary_key', primary_key)
        if rights and (not isinstance(rights, str)):
            raise TypeError("Expected argument 'rights' to be a str")
        pulumi.set(__self__, 'rights', rights)
        if secondary_key and (not isinstance(secondary_key, str)):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, 'secondary_key', secondary_key)

    @property
    @pulumi.getter(name='keyName')
    def key_name(self) -> str:
        """
        The name of the shared access policy.
        """
        return pulumi.get(self, 'key_name')

    @property
    @pulumi.getter(name='primaryKey')
    def primary_key(self) -> Optional[str]:
        """
        The primary key.
        """
        return pulumi.get(self, 'primary_key')

    @property
    @pulumi.getter
    def rights(self) -> str:
        """
        The permissions assigned to the shared access policy.
        """
        return pulumi.get(self, 'rights')

    @property
    @pulumi.getter(name='secondaryKey')
    def secondary_key(self) -> Optional[str]:
        """
        The secondary key.
        """
        return pulumi.get(self, 'secondary_key')

class AwaitableListIotHubResourceKeysForKeyNameResult(ListIotHubResourceKeysForKeyNameResult):

    def __await__(self):
        if False:
            yield self
        return ListIotHubResourceKeysForKeyNameResult(key_name=self.key_name, primary_key=self.primary_key, rights=self.rights, secondary_key=self.secondary_key)

def list_iot_hub_resource_keys_for_key_name(key_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListIotHubResourceKeysForKeyNameResult:
    """
    The properties of an IoT hub shared access policy.


    :param str key_name: The name of the shared access policy.
    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    __args__ = dict()
    __args__['keyName'] = key_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:devices/v20190701preview:listIotHubResourceKeysForKeyName', __args__, opts=opts, typ=ListIotHubResourceKeysForKeyNameResult).value
    return AwaitableListIotHubResourceKeysForKeyNameResult(key_name=__ret__.key_name, primary_key=__ret__.primary_key, rights=__ret__.rights, secondary_key=__ret__.secondary_key)

@_utilities.lift_output_func(list_iot_hub_resource_keys_for_key_name)
def list_iot_hub_resource_keys_for_key_name_output(key_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListIotHubResourceKeysForKeyNameResult]:
    """
    The properties of an IoT hub shared access policy.


    :param str key_name: The name of the shared access policy.
    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    ...
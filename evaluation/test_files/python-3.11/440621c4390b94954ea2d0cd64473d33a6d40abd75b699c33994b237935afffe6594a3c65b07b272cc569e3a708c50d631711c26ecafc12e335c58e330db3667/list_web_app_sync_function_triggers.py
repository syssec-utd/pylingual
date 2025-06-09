import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['ListWebAppSyncFunctionTriggersResult', 'AwaitableListWebAppSyncFunctionTriggersResult', 'list_web_app_sync_function_triggers', 'list_web_app_sync_function_triggers_output']

@pulumi.output_type
class ListWebAppSyncFunctionTriggersResult:
    """
    Function secrets.
    """

    def __init__(__self__, id=None, key=None, kind=None, name=None, trigger_url=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if key and (not isinstance(key, str)):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, 'key', key)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if trigger_url and (not isinstance(trigger_url, str)):
            raise TypeError("Expected argument 'trigger_url' to be a str")
        pulumi.set(__self__, 'trigger_url', trigger_url)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        Secret key.
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='triggerUrl')
    def trigger_url(self) -> Optional[str]:
        """
        Trigger URL.
        """
        return pulumi.get(self, 'trigger_url')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableListWebAppSyncFunctionTriggersResult(ListWebAppSyncFunctionTriggersResult):

    def __await__(self):
        if False:
            yield self
        return ListWebAppSyncFunctionTriggersResult(id=self.id, key=self.key, kind=self.kind, name=self.name, trigger_url=self.trigger_url, type=self.type)

def list_web_app_sync_function_triggers(name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListWebAppSyncFunctionTriggersResult:
    """
    Function secrets.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20190801:listWebAppSyncFunctionTriggers', __args__, opts=opts, typ=ListWebAppSyncFunctionTriggersResult).value
    return AwaitableListWebAppSyncFunctionTriggersResult(id=__ret__.id, key=__ret__.key, kind=__ret__.kind, name=__ret__.name, trigger_url=__ret__.trigger_url, type=__ret__.type)

@_utilities.lift_output_func(list_web_app_sync_function_triggers)
def list_web_app_sync_function_triggers_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListWebAppSyncFunctionTriggersResult]:
    """
    Function secrets.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
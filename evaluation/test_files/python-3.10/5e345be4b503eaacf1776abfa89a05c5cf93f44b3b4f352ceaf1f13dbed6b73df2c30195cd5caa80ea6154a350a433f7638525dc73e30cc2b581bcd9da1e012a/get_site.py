import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetSiteResult', 'AwaitableGetSiteResult', 'get_site', 'get_site_output']

@pulumi.output_type
class GetSiteResult:
    """
    IoT site model
    """

    def __init__(__self__, display_name=None, id=None, name=None, system_data=None, tags=None, type=None):
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        Display name of the IoT site
        """
        return pulumi.get(self, 'display_name')

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
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags of the IoT site
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetSiteResult(GetSiteResult):

    def __await__(self):
        if False:
            yield self
        return GetSiteResult(display_name=self.display_name, id=self.id, name=self.name, system_data=self.system_data, tags=self.tags, type=self.type)

def get_site(scope: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSiteResult:
    """
    Get IoT site


    :param str scope: Scope of the query (IoT Hub, /providers/Microsoft.Devices/iotHubs/myHub)
    """
    __args__ = dict()
    __args__['scope'] = scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:iotsecurity/v20210201preview:getSite', __args__, opts=opts, typ=GetSiteResult).value
    return AwaitableGetSiteResult(display_name=__ret__.display_name, id=__ret__.id, name=__ret__.name, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_site)
def get_site_output(scope: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSiteResult]:
    """
    Get IoT site


    :param str scope: Scope of the query (IoT Hub, /providers/Microsoft.Devices/iotHubs/myHub)
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPrivateLinkScopeResult', 'AwaitableGetPrivateLinkScopeResult', 'get_private_link_scope', 'get_private_link_scope_output']

@pulumi.output_type
class GetPrivateLinkScopeResult:
    """
    An Azure Arc PrivateLinkScope definition.
    """

    def __init__(__self__, id=None, location=None, name=None, properties=None, system_data=None, tags=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
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
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.HybridComputePrivateLinkScopePropertiesResponse':
        """
        Properties that define a Azure Arc PrivateLinkScope resource.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, 'type')

class AwaitableGetPrivateLinkScopeResult(GetPrivateLinkScopeResult):

    def __await__(self):
        if False:
            yield self
        return GetPrivateLinkScopeResult(id=self.id, location=self.location, name=self.name, properties=self.properties, system_data=self.system_data, tags=self.tags, type=self.type)

def get_private_link_scope(resource_group_name: Optional[str]=None, scope_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPrivateLinkScopeResult:
    """
    An Azure Arc PrivateLinkScope definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str scope_name: The name of the Azure Arc PrivateLinkScope resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['scopeName'] = scope_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:hybridcompute/v20210128preview:getPrivateLinkScope', __args__, opts=opts, typ=GetPrivateLinkScopeResult).value
    return AwaitableGetPrivateLinkScopeResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_private_link_scope)
def get_private_link_scope_output(resource_group_name: Optional[pulumi.Input[str]]=None, scope_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPrivateLinkScopeResult]:
    """
    An Azure Arc PrivateLinkScope definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str scope_name: The name of the Azure Arc PrivateLinkScope resource.
    """
    ...
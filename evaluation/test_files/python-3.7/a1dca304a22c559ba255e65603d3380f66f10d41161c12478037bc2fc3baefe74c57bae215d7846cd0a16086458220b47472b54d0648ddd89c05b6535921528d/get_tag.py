import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetTagResult', 'AwaitableGetTagResult', 'get_tag', 'get_tag_output']

@pulumi.output_type
class GetTagResult:
    """
    Tag Contract details.
    """

    def __init__(__self__, display_name=None, id=None, name=None, type=None):
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        Tag name.
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
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetTagResult(GetTagResult):

    def __await__(self):
        if False:
            yield self
        return GetTagResult(display_name=self.display_name, id=self.id, name=self.name, type=self.type)

def get_tag(resource_group_name: Optional[str]=None, service_name: Optional[str]=None, tag_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetTagResult:
    """
    Gets the details of the tag specified by its identifier.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str service_name: The name of the API Management service.
    :param str tag_id: Tag identifier. Must be unique in the current API Management service instance.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    __args__['tagId'] = tag_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20220801:getTag', __args__, opts=opts, typ=GetTagResult).value
    return AwaitableGetTagResult(display_name=__ret__.display_name, id=__ret__.id, name=__ret__.name, type=__ret__.type)

@_utilities.lift_output_func(get_tag)
def get_tag_output(resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, tag_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetTagResult]:
    """
    Gets the details of the tag specified by its identifier.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str service_name: The name of the API Management service.
    :param str tag_id: Tag identifier. Must be unique in the current API Management service instance.
    """
    ...
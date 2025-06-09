import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetProfileResult', 'AwaitableGetProfileResult', 'get_profile', 'get_profile_output']
warnings.warn('Version 2019-12-31 will be removed in v2 of the provider.', DeprecationWarning)

@pulumi.output_type
class GetProfileResult:
    """
    CDN profile is a logical grouping of endpoints that share the same settings, such as CDN provider and pricing tier.
    """

    def __init__(__self__, id=None, location=None, name=None, provisioning_state=None, resource_state=None, sku=None, tags=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if resource_state and (not isinstance(resource_state, str)):
            raise TypeError("Expected argument 'resource_state' to be a str")
        pulumi.set(__self__, 'resource_state', resource_state)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
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
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
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
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning status of the profile.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceState')
    def resource_state(self) -> str:
        """
        Resource status of the profile.
        """
        return pulumi.get(self, 'resource_state')

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The pricing tier (defines a CDN provider, feature list and rate) of the CDN profile.
        """
        return pulumi.get(self, 'sku')

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

class AwaitableGetProfileResult(GetProfileResult):

    def __await__(self):
        if False:
            yield self
        return GetProfileResult(id=self.id, location=self.location, name=self.name, provisioning_state=self.provisioning_state, resource_state=self.resource_state, sku=self.sku, tags=self.tags, type=self.type)

def get_profile(profile_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetProfileResult:
    """
    Gets a CDN profile with the specified profile name under the specified subscription and resource group.


    :param str profile_name: Name of the CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    pulumi.log.warn('get_profile is deprecated: Version 2019-12-31 will be removed in v2 of the provider.')
    __args__ = dict()
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20191231:getProfile', __args__, opts=opts, typ=GetProfileResult).value
    return AwaitableGetProfileResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, resource_state=__ret__.resource_state, sku=__ret__.sku, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_profile)
def get_profile_output(profile_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetProfileResult]:
    """
    Gets a CDN profile with the specified profile name under the specified subscription and resource group.


    :param str profile_name: Name of the CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    pulumi.log.warn('get_profile is deprecated: Version 2019-12-31 will be removed in v2 of the provider.')
    ...
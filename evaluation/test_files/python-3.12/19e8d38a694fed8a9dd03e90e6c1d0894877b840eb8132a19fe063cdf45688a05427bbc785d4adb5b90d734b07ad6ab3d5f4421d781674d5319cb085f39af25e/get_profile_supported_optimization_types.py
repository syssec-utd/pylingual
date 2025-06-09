import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetProfileSupportedOptimizationTypesResult', 'AwaitableGetProfileSupportedOptimizationTypesResult', 'get_profile_supported_optimization_types', 'get_profile_supported_optimization_types_output']

@pulumi.output_type
class GetProfileSupportedOptimizationTypesResult:
    """
    The result of the GetSupportedOptimizationTypes API
    """

    def __init__(__self__, supported_optimization_types=None):
        if supported_optimization_types and (not isinstance(supported_optimization_types, list)):
            raise TypeError("Expected argument 'supported_optimization_types' to be a list")
        pulumi.set(__self__, 'supported_optimization_types', supported_optimization_types)

    @property
    @pulumi.getter(name='supportedOptimizationTypes')
    def supported_optimization_types(self) -> Sequence[str]:
        """
        Supported optimization types for a profile.
        """
        return pulumi.get(self, 'supported_optimization_types')

class AwaitableGetProfileSupportedOptimizationTypesResult(GetProfileSupportedOptimizationTypesResult):

    def __await__(self):
        if False:
            yield self
        return GetProfileSupportedOptimizationTypesResult(supported_optimization_types=self.supported_optimization_types)

def get_profile_supported_optimization_types(profile_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetProfileSupportedOptimizationTypesResult:
    """
    The result of the GetSupportedOptimizationTypes API


    :param str profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium or CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20210601:getProfileSupportedOptimizationTypes', __args__, opts=opts, typ=GetProfileSupportedOptimizationTypesResult).value
    return AwaitableGetProfileSupportedOptimizationTypesResult(supported_optimization_types=__ret__.supported_optimization_types)

@_utilities.lift_output_func(get_profile_supported_optimization_types)
def get_profile_supported_optimization_types_output(profile_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetProfileSupportedOptimizationTypesResult]:
    """
    The result of the GetSupportedOptimizationTypes API


    :param str profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium or CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    ...
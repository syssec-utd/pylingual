import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetManagedHsmResult', 'AwaitableGetManagedHsmResult', 'get_managed_hsm', 'get_managed_hsm_output']

@pulumi.output_type
class GetManagedHsmResult:
    """
    Resource information with extended details.
    """

    def __init__(__self__, id=None, location=None, name=None, properties=None, sku=None, system_data=None, tags=None, type=None):
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
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
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
        The Azure Resource Manager resource ID for the managed HSM Pool.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The supported Azure location where the managed HSM Pool should be created.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the managed HSM Pool.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ManagedHsmPropertiesResponse':
        """
        Properties of the managed HSM
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ManagedHsmSkuResponse']:
        """
        SKU details
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the key vault resource.
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
        The resource type of the managed HSM Pool.
        """
        return pulumi.get(self, 'type')

class AwaitableGetManagedHsmResult(GetManagedHsmResult):

    def __await__(self):
        if False:
            yield self
        return GetManagedHsmResult(id=self.id, location=self.location, name=self.name, properties=self.properties, sku=self.sku, system_data=self.system_data, tags=self.tags, type=self.type)

def get_managed_hsm(name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetManagedHsmResult:
    """
    Resource information with extended details.


    :param str name: The name of the managed HSM Pool.
    :param str resource_group_name: Name of the resource group that contains the managed HSM pool.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:keyvault/v20210401preview:getManagedHsm', __args__, opts=opts, typ=GetManagedHsmResult).value
    return AwaitableGetManagedHsmResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, sku=__ret__.sku, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_managed_hsm)
def get_managed_hsm_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetManagedHsmResult]:
    """
    Resource information with extended details.


    :param str name: The name of the managed HSM Pool.
    :param str resource_group_name: Name of the resource group that contains the managed HSM pool.
    """
    ...
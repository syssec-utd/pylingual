import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetIotHubResourceResult', 'AwaitableGetIotHubResourceResult', 'get_iot_hub_resource', 'get_iot_hub_resource_output']

@pulumi.output_type
class GetIotHubResourceResult:
    """
    The description of the IoT hub.
    """

    def __init__(__self__, etag=None, id=None, identity=None, location=None, name=None, properties=None, sku=None, tags=None, type=None):
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
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
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        The Etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal ETag convention.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ArmIdentityResponse']:
        """
        The managed identities for the IotHub.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.IotHubPropertiesResponse':
        """
        IotHub properties
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.IotHubSkuInfoResponse':
        """
        IotHub SKU info
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetIotHubResourceResult(GetIotHubResourceResult):

    def __await__(self):
        if False:
            yield self
        return GetIotHubResourceResult(etag=self.etag, id=self.id, identity=self.identity, location=self.location, name=self.name, properties=self.properties, sku=self.sku, tags=self.tags, type=self.type)

def get_iot_hub_resource(resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetIotHubResourceResult:
    """
    Get the non-security related metadata of an IoT hub.


    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:devices/v20200831preview:getIotHubResource', __args__, opts=opts, typ=GetIotHubResourceResult).value
    return AwaitableGetIotHubResourceResult(etag=__ret__.etag, id=__ret__.id, identity=__ret__.identity, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, sku=__ret__.sku, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_iot_hub_resource)
def get_iot_hub_resource_output(resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetIotHubResourceResult]:
    """
    Get the non-security related metadata of an IoT hub.


    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    ...
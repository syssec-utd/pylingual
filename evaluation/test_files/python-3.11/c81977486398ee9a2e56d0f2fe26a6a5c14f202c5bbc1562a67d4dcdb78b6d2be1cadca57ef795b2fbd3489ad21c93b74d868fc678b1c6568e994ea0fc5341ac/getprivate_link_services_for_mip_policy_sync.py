import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetprivateLinkServicesForMIPPolicySyncResult', 'AwaitableGetprivateLinkServicesForMIPPolicySyncResult', 'getprivate_link_services_for_mip_policy_sync', 'getprivate_link_services_for_mip_policy_sync_output']

@pulumi.output_type
class GetprivateLinkServicesForMIPPolicySyncResult:
    """
    The description of the service.
    """

    def __init__(__self__, etag=None, id=None, identity=None, kind=None, location=None, name=None, properties=None, system_data=None, tags=None, type=None):
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
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
    def etag(self) -> Optional[str]:
        """
        An etag associated with the resource, used for optimistic concurrency when editing it.
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
    def identity(self) -> Optional['outputs.ServicesResourceResponseIdentity']:
        """
        Setting indicating whether the service has a managed identity associated with it.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the service.
        """
        return pulumi.get(self, 'kind')

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
    def properties(self) -> 'outputs.ServicesPropertiesResponse':
        """
        The common properties of a service.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Required property for system data
        """
        return pulumi.get(self, 'system_data')

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

class AwaitableGetprivateLinkServicesForMIPPolicySyncResult(GetprivateLinkServicesForMIPPolicySyncResult):

    def __await__(self):
        if False:
            yield self
        return GetprivateLinkServicesForMIPPolicySyncResult(etag=self.etag, id=self.id, identity=self.identity, kind=self.kind, location=self.location, name=self.name, properties=self.properties, system_data=self.system_data, tags=self.tags, type=self.type)

def getprivate_link_services_for_mip_policy_sync(resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetprivateLinkServicesForMIPPolicySyncResult:
    """
    Get the metadata of a privateLinkServicesForMIPPolicySync resource.


    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str resource_name: The name of the service instance.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:m365securityandcompliance/v20210325preview:getprivateLinkServicesForMIPPolicySync', __args__, opts=opts, typ=GetprivateLinkServicesForMIPPolicySyncResult).value
    return AwaitableGetprivateLinkServicesForMIPPolicySyncResult(etag=__ret__.etag, id=__ret__.id, identity=__ret__.identity, kind=__ret__.kind, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(getprivate_link_services_for_mip_policy_sync)
def getprivate_link_services_for_mip_policy_sync_output(resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetprivateLinkServicesForMIPPolicySyncResult]:
    """
    Get the metadata of a privateLinkServicesForMIPPolicySync resource.


    :param str resource_group_name: The name of the resource group that contains the service instance.
    :param str resource_name: The name of the service instance.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetProtectionPolicyResult', 'AwaitableGetProtectionPolicyResult', 'get_protection_policy', 'get_protection_policy_output']

@pulumi.output_type
class GetProtectionPolicyResult:
    """
    Base class for backup policy. Workload-specific backup policies are derived from this class.
    """

    def __init__(__self__, e_tag=None, id=None, location=None, name=None, properties=None, tags=None, type=None):
        if e_tag and (not isinstance(e_tag, str)):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, 'e_tag', e_tag)
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
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='eTag')
    def e_tag(self) -> Optional[str]:
        """
        Optional ETag.
        """
        return pulumi.get(self, 'e_tag')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id represents the complete path to the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name associated with the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> Any:
        """
        ProtectionPolicyResource properties
        """
        return pulumi.get(self, 'properties')

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
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, 'type')

class AwaitableGetProtectionPolicyResult(GetProtectionPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetProtectionPolicyResult(e_tag=self.e_tag, id=self.id, location=self.location, name=self.name, properties=self.properties, tags=self.tags, type=self.type)

def get_protection_policy(policy_name: Optional[str]=None, resource_group_name: Optional[str]=None, vault_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetProtectionPolicyResult:
    """
    Base class for backup policy. Workload-specific backup policies are derived from this class.


    :param str policy_name: Backup policy information to be fetched.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str vault_name: The name of the recovery services vault.
    """
    __args__ = dict()
    __args__['policyName'] = policy_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vaultName'] = vault_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:recoveryservices/v20210601:getProtectionPolicy', __args__, opts=opts, typ=GetProtectionPolicyResult).value
    return AwaitableGetProtectionPolicyResult(e_tag=__ret__.e_tag, id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_protection_policy)
def get_protection_policy_output(policy_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, vault_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetProtectionPolicyResult]:
    """
    Base class for backup policy. Workload-specific backup policies are derived from this class.


    :param str policy_name: Backup policy information to be fetched.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str vault_name: The name of the recovery services vault.
    """
    ...
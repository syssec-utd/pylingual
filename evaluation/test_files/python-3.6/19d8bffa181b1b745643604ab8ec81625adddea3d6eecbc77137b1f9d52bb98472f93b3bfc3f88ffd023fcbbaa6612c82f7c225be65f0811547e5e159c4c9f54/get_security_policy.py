import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetSecurityPolicyResult', 'AwaitableGetSecurityPolicyResult', 'get_security_policy', 'get_security_policy_output']

@pulumi.output_type
class GetSecurityPolicyResult:
    """
    A collection of values returned by getSecurityPolicy.
    """

    def __init__(__self__, category=None, compartment_id=None, defined_tags=None, description=None, display_name=None, freeform_tags=None, friendly_name=None, id=None, lifecycle_details=None, owner=None, security_policy_id=None, services=None, state=None, system_tags=None, time_created=None, time_updated=None):
        if category and (not isinstance(category, str)):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, 'category', category)
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if defined_tags and (not isinstance(defined_tags, dict)):
            raise TypeError("Expected argument 'defined_tags' to be a dict")
        pulumi.set(__self__, 'defined_tags', defined_tags)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if freeform_tags and (not isinstance(freeform_tags, dict)):
            raise TypeError("Expected argument 'freeform_tags' to be a dict")
        pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if friendly_name and (not isinstance(friendly_name, str)):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, 'friendly_name', friendly_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if lifecycle_details and (not isinstance(lifecycle_details, str)):
            raise TypeError("Expected argument 'lifecycle_details' to be a str")
        pulumi.set(__self__, 'lifecycle_details', lifecycle_details)
        if owner and (not isinstance(owner, str)):
            raise TypeError("Expected argument 'owner' to be a str")
        pulumi.set(__self__, 'owner', owner)
        if security_policy_id and (not isinstance(security_policy_id, str)):
            raise TypeError("Expected argument 'security_policy_id' to be a str")
        pulumi.set(__self__, 'security_policy_id', security_policy_id)
        if services and (not isinstance(services, list)):
            raise TypeError("Expected argument 'services' to be a list")
        pulumi.set(__self__, 'services', services)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if system_tags and (not isinstance(system_tags, dict)):
            raise TypeError("Expected argument 'system_tags' to be a dict")
        pulumi.set(__self__, 'system_tags', system_tags)
        if time_created and (not isinstance(time_created, str)):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, 'time_created', time_created)
        if time_updated and (not isinstance(time_updated, str)):
            raise TypeError("Expected argument 'time_updated' to be a str")
        pulumi.set(__self__, 'time_updated', time_updated)

    @property
    @pulumi.getter
    def category(self) -> str:
        """
        The category of security policy
        """
        return pulumi.get(self, 'category')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        """
        The id of the security policy's compartment
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Mapping[str, Any]:
        """
        Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        """
        return pulumi.get(self, 'defined_tags')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The security policy's description
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        The security policy's full name
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Mapping[str, Any]:
        """
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> str:
        """
        A shorter version of the security policy's name
        """
        return pulumi.get(self, 'friendly_name')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='lifecycleDetails')
    def lifecycle_details(self) -> str:
        """
        A message describing the current state in more detail. For example, this can be used to provide actionable information for a resource in a `Failed` state.
        """
        return pulumi.get(self, 'lifecycle_details')

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        The owner of the security policy
        """
        return pulumi.get(self, 'owner')

    @property
    @pulumi.getter(name='securityPolicyId')
    def security_policy_id(self) -> str:
        return pulumi.get(self, 'security_policy_id')

    @property
    @pulumi.getter
    def services(self) -> Sequence[str]:
        """
        The list of services that the security policy protects
        """
        return pulumi.get(self, 'services')

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the security policy
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='systemTags')
    def system_tags(self) -> Mapping[str, Any]:
        """
        System tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm). System tags can be viewed by users, but can only be created by the system.  Example: `{"orcl-cloud.free-tier-retained": "true"}`
        """
        return pulumi.get(self, 'system_tags')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> str:
        """
        The time the security policy was created. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> str:
        """
        The time the security policy was last updated. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_updated')

class AwaitableGetSecurityPolicyResult(GetSecurityPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetSecurityPolicyResult(category=self.category, compartment_id=self.compartment_id, defined_tags=self.defined_tags, description=self.description, display_name=self.display_name, freeform_tags=self.freeform_tags, friendly_name=self.friendly_name, id=self.id, lifecycle_details=self.lifecycle_details, owner=self.owner, security_policy_id=self.security_policy_id, services=self.services, state=self.state, system_tags=self.system_tags, time_created=self.time_created, time_updated=self.time_updated)

def get_security_policy(security_policy_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSecurityPolicyResult:
    """
    This data source provides details about a specific Security Policy resource in Oracle Cloud Infrastructure Cloud Guard service.

    Gets a security zone policy using its identifier. When a policy is enabled in a security zone, then any action in the zone that attempts to violate that policy is denied.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_security_policy = oci.CloudGuard.get_security_policy(security_policy_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str security_policy_id: The unique identifier of the security zone policy (`SecurityPolicy`)
    """
    __args__ = dict()
    __args__['securityPolicyId'] = security_policy_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:CloudGuard/getSecurityPolicy:getSecurityPolicy', __args__, opts=opts, typ=GetSecurityPolicyResult).value
    return AwaitableGetSecurityPolicyResult(category=__ret__.category, compartment_id=__ret__.compartment_id, defined_tags=__ret__.defined_tags, description=__ret__.description, display_name=__ret__.display_name, freeform_tags=__ret__.freeform_tags, friendly_name=__ret__.friendly_name, id=__ret__.id, lifecycle_details=__ret__.lifecycle_details, owner=__ret__.owner, security_policy_id=__ret__.security_policy_id, services=__ret__.services, state=__ret__.state, system_tags=__ret__.system_tags, time_created=__ret__.time_created, time_updated=__ret__.time_updated)

@_utilities.lift_output_func(get_security_policy)
def get_security_policy_output(security_policy_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSecurityPolicyResult]:
    """
    This data source provides details about a specific Security Policy resource in Oracle Cloud Infrastructure Cloud Guard service.

    Gets a security zone policy using its identifier. When a policy is enabled in a security zone, then any action in the zone that attempts to violate that policy is denied.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_security_policy = oci.CloudGuard.get_security_policy(security_policy_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str security_policy_id: The unique identifier of the security zone policy (`SecurityPolicy`)
    """
    ...
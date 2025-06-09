import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetVolumeGroupsResult', 'AwaitableGetVolumeGroupsResult', 'get_volume_groups', 'get_volume_groups_output']

@pulumi.output_type
class GetVolumeGroupsResult:
    """
    A collection of values returned by getVolumeGroups.
    """

    def __init__(__self__, availability_domain=None, compartment_id=None, display_name=None, filters=None, id=None, state=None, volume_groups=None):
        if availability_domain and (not isinstance(availability_domain, str)):
            raise TypeError("Expected argument 'availability_domain' to be a str")
        pulumi.set(__self__, 'availability_domain', availability_domain)
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if volume_groups and (not isinstance(volume_groups, list)):
            raise TypeError("Expected argument 'volume_groups' to be a list")
        pulumi.set(__self__, 'volume_groups', volume_groups)

    @property
    @pulumi.getter(name='availabilityDomain')
    def availability_domain(self) -> Optional[str]:
        """
        The availability domain of the boot volume replica replica.  Example: `Uocm:PHX-AD-1`
        """
        return pulumi.get(self, 'availability_domain')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        """
        The OCID of the compartment that contains the volume group.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetVolumeGroupsFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The current state of a volume group.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='volumeGroups')
    def volume_groups(self) -> Sequence['outputs.GetVolumeGroupsVolumeGroupResult']:
        """
        The list of volume_groups.
        """
        return pulumi.get(self, 'volume_groups')

class AwaitableGetVolumeGroupsResult(GetVolumeGroupsResult):

    def __await__(self):
        if False:
            yield self
        return GetVolumeGroupsResult(availability_domain=self.availability_domain, compartment_id=self.compartment_id, display_name=self.display_name, filters=self.filters, id=self.id, state=self.state, volume_groups=self.volume_groups)

def get_volume_groups(availability_domain: Optional[str]=None, compartment_id: Optional[str]=None, display_name: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetVolumeGroupsFilterArgs']]]=None, state: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVolumeGroupsResult:
    """
    This data source provides the list of Volume Groups in Oracle Cloud Infrastructure Core service.

    Lists the volume groups in the specified compartment and availability domain.
    For more information, see [Volume Groups](https://docs.cloud.oracle.com/iaas/Content/Block/Concepts/volumegroups.htm).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_volume_groups = oci.Core.get_volume_groups(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        availability_domain=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str availability_domain: The name of the availability domain.  Example: `Uocm:PHX-AD-1`
    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to return only resources that match the given display name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state. The state value is case-insensitive.
    """
    __args__ = dict()
    __args__['availabilityDomain'] = availability_domain
    __args__['compartmentId'] = compartment_id
    __args__['displayName'] = display_name
    __args__['filters'] = filters
    __args__['state'] = state
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:Core/getVolumeGroups:getVolumeGroups', __args__, opts=opts, typ=GetVolumeGroupsResult).value
    return AwaitableGetVolumeGroupsResult(availability_domain=__ret__.availability_domain, compartment_id=__ret__.compartment_id, display_name=__ret__.display_name, filters=__ret__.filters, id=__ret__.id, state=__ret__.state, volume_groups=__ret__.volume_groups)

@_utilities.lift_output_func(get_volume_groups)
def get_volume_groups_output(availability_domain: Optional[pulumi.Input[Optional[str]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVolumeGroupsFilterArgs']]]]]=None, state: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVolumeGroupsResult]:
    """
    This data source provides the list of Volume Groups in Oracle Cloud Infrastructure Core service.

    Lists the volume groups in the specified compartment and availability domain.
    For more information, see [Volume Groups](https://docs.cloud.oracle.com/iaas/Content/Block/Concepts/volumegroups.htm).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_volume_groups = oci.Core.get_volume_groups(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        availability_domain=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str availability_domain: The name of the availability domain.  Example: `Uocm:PHX-AD-1`
    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to return only resources that match the given display name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state. The state value is case-insensitive.
    """
    ...
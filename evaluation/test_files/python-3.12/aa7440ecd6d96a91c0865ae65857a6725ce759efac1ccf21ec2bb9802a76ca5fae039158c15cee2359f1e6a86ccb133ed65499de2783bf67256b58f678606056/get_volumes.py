import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetVolumesResult', 'AwaitableGetVolumesResult', 'get_volumes', 'get_volumes_output']

@pulumi.output_type
class GetVolumesResult:
    """
    A collection of values returned by getVolumes.
    """

    def __init__(__self__, availability_domain=None, compartment_id=None, display_name=None, filters=None, id=None, state=None, volume_group_id=None, volumes=None):
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
        if volume_group_id and (not isinstance(volume_group_id, str)):
            raise TypeError("Expected argument 'volume_group_id' to be a str")
        pulumi.set(__self__, 'volume_group_id', volume_group_id)
        if volumes and (not isinstance(volumes, list)):
            raise TypeError("Expected argument 'volumes' to be a list")
        pulumi.set(__self__, 'volumes', volumes)

    @property
    @pulumi.getter(name='availabilityDomain')
    def availability_domain(self) -> Optional[str]:
        """
        The availability domain of the block volume replica.  Example: `Uocm:PHX-AD-1`
        """
        return pulumi.get(self, 'availability_domain')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[str]:
        """
        The OCID of the compartment that contains the volume.
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
    def filters(self) -> Optional[Sequence['outputs.GetVolumesFilterResult']]:
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
        The current state of a volume.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='volumeGroupId')
    def volume_group_id(self) -> Optional[str]:
        """
        The OCID of the source volume group.
        """
        return pulumi.get(self, 'volume_group_id')

    @property
    @pulumi.getter
    def volumes(self) -> Sequence['outputs.GetVolumesVolumeResult']:
        """
        The list of volumes.
        """
        return pulumi.get(self, 'volumes')

class AwaitableGetVolumesResult(GetVolumesResult):

    def __await__(self):
        if False:
            yield self
        return GetVolumesResult(availability_domain=self.availability_domain, compartment_id=self.compartment_id, display_name=self.display_name, filters=self.filters, id=self.id, state=self.state, volume_group_id=self.volume_group_id, volumes=self.volumes)

def get_volumes(availability_domain: Optional[str]=None, compartment_id: Optional[str]=None, display_name: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetVolumesFilterArgs']]]=None, state: Optional[str]=None, volume_group_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVolumesResult:
    """
    This data source provides the list of Volumes in Oracle Cloud Infrastructure Core service.

    Lists the volumes in the specified compartment and availability domain.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_volumes = oci.Core.get_volumes(availability_domain=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        volume_group_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str availability_domain: The name of the availability domain.  Example: `Uocm:PHX-AD-1`
    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to return only resources that match the given display name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state. The state value is case-insensitive.
    :param str volume_group_id: The OCID of the volume group.
    """
    __args__ = dict()
    __args__['availabilityDomain'] = availability_domain
    __args__['compartmentId'] = compartment_id
    __args__['displayName'] = display_name
    __args__['filters'] = filters
    __args__['state'] = state
    __args__['volumeGroupId'] = volume_group_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:Core/getVolumes:getVolumes', __args__, opts=opts, typ=GetVolumesResult).value
    return AwaitableGetVolumesResult(availability_domain=__ret__.availability_domain, compartment_id=__ret__.compartment_id, display_name=__ret__.display_name, filters=__ret__.filters, id=__ret__.id, state=__ret__.state, volume_group_id=__ret__.volume_group_id, volumes=__ret__.volumes)

@_utilities.lift_output_func(get_volumes)
def get_volumes_output(availability_domain: Optional[pulumi.Input[Optional[str]]]=None, compartment_id: Optional[pulumi.Input[Optional[str]]]=None, display_name: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVolumesFilterArgs']]]]]=None, state: Optional[pulumi.Input[Optional[str]]]=None, volume_group_id: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVolumesResult]:
    """
    This data source provides the list of Volumes in Oracle Cloud Infrastructure Core service.

    Lists the volumes in the specified compartment and availability domain.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_volumes = oci.Core.get_volumes(availability_domain=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        volume_group_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str availability_domain: The name of the availability domain.  Example: `Uocm:PHX-AD-1`
    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to return only resources that match the given display name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state. The state value is case-insensitive.
    :param str volume_group_id: The OCID of the volume group.
    """
    ...
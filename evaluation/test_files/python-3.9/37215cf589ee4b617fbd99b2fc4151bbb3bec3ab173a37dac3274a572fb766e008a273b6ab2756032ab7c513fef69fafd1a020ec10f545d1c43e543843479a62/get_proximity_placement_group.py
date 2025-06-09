import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetProximityPlacementGroupResult', 'AwaitableGetProximityPlacementGroupResult', 'get_proximity_placement_group', 'get_proximity_placement_group_output']

@pulumi.output_type
class GetProximityPlacementGroupResult:
    """
    Specifies information about the proximity placement group.
    """

    def __init__(__self__, availability_sets=None, colocation_status=None, id=None, location=None, name=None, proximity_placement_group_type=None, tags=None, type=None, virtual_machine_scale_sets=None, virtual_machines=None):
        if availability_sets and (not isinstance(availability_sets, list)):
            raise TypeError("Expected argument 'availability_sets' to be a list")
        pulumi.set(__self__, 'availability_sets', availability_sets)
        if colocation_status and (not isinstance(colocation_status, dict)):
            raise TypeError("Expected argument 'colocation_status' to be a dict")
        pulumi.set(__self__, 'colocation_status', colocation_status)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if proximity_placement_group_type and (not isinstance(proximity_placement_group_type, str)):
            raise TypeError("Expected argument 'proximity_placement_group_type' to be a str")
        pulumi.set(__self__, 'proximity_placement_group_type', proximity_placement_group_type)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if virtual_machine_scale_sets and (not isinstance(virtual_machine_scale_sets, list)):
            raise TypeError("Expected argument 'virtual_machine_scale_sets' to be a list")
        pulumi.set(__self__, 'virtual_machine_scale_sets', virtual_machine_scale_sets)
        if virtual_machines and (not isinstance(virtual_machines, list)):
            raise TypeError("Expected argument 'virtual_machines' to be a list")
        pulumi.set(__self__, 'virtual_machines', virtual_machines)

    @property
    @pulumi.getter(name='availabilitySets')
    def availability_sets(self) -> Sequence['outputs.SubResourceWithColocationStatusResponse']:
        """
        A list of references to all availability sets in the proximity placement group.
        """
        return pulumi.get(self, 'availability_sets')

    @property
    @pulumi.getter(name='colocationStatus')
    def colocation_status(self) -> Optional['outputs.InstanceViewStatusResponse']:
        """
        Describes colocation status of the Proximity Placement Group.
        """
        return pulumi.get(self, 'colocation_status')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='proximityPlacementGroupType')
    def proximity_placement_group_type(self) -> Optional[str]:
        """
        Specifies the type of the proximity placement group. <br><br> Possible values are: <br><br> **Standard** : Co-locate resources within an Azure region or Availability Zone. <br><br> **Ultra** : For future use.
        """
        return pulumi.get(self, 'proximity_placement_group_type')

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
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='virtualMachineScaleSets')
    def virtual_machine_scale_sets(self) -> Sequence['outputs.SubResourceWithColocationStatusResponse']:
        """
        A list of references to all virtual machine scale sets in the proximity placement group.
        """
        return pulumi.get(self, 'virtual_machine_scale_sets')

    @property
    @pulumi.getter(name='virtualMachines')
    def virtual_machines(self) -> Sequence['outputs.SubResourceWithColocationStatusResponse']:
        """
        A list of references to all virtual machines in the proximity placement group.
        """
        return pulumi.get(self, 'virtual_machines')

class AwaitableGetProximityPlacementGroupResult(GetProximityPlacementGroupResult):

    def __await__(self):
        if False:
            yield self
        return GetProximityPlacementGroupResult(availability_sets=self.availability_sets, colocation_status=self.colocation_status, id=self.id, location=self.location, name=self.name, proximity_placement_group_type=self.proximity_placement_group_type, tags=self.tags, type=self.type, virtual_machine_scale_sets=self.virtual_machine_scale_sets, virtual_machines=self.virtual_machines)

def get_proximity_placement_group(include_colocation_status: Optional[str]=None, proximity_placement_group_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetProximityPlacementGroupResult:
    """
    Specifies information about the proximity placement group.


    :param str include_colocation_status: includeColocationStatus=true enables fetching the colocation status of all the resources in the proximity placement group.
    :param str proximity_placement_group_name: The name of the proximity placement group.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['includeColocationStatus'] = include_colocation_status
    __args__['proximityPlacementGroupName'] = proximity_placement_group_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20201201:getProximityPlacementGroup', __args__, opts=opts, typ=GetProximityPlacementGroupResult).value
    return AwaitableGetProximityPlacementGroupResult(availability_sets=__ret__.availability_sets, colocation_status=__ret__.colocation_status, id=__ret__.id, location=__ret__.location, name=__ret__.name, proximity_placement_group_type=__ret__.proximity_placement_group_type, tags=__ret__.tags, type=__ret__.type, virtual_machine_scale_sets=__ret__.virtual_machine_scale_sets, virtual_machines=__ret__.virtual_machines)

@_utilities.lift_output_func(get_proximity_placement_group)
def get_proximity_placement_group_output(include_colocation_status: Optional[pulumi.Input[Optional[str]]]=None, proximity_placement_group_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetProximityPlacementGroupResult]:
    """
    Specifies information about the proximity placement group.


    :param str include_colocation_status: includeColocationStatus=true enables fetching the colocation status of all the resources in the proximity placement group.
    :param str proximity_placement_group_name: The name of the proximity placement group.
    :param str resource_group_name: The name of the resource group.
    """
    ...
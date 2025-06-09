import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetReplicationvCenterResult', 'AwaitableGetReplicationvCenterResult', 'get_replicationv_center', 'get_replicationv_center_output']

@pulumi.output_type
class GetReplicationvCenterResult:
    """
    vCenter definition.
    """

    def __init__(__self__, id=None, location=None, name=None, properties=None, type=None):
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
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource Location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.VCenterPropertiesResponse':
        """
        VCenter related data.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, 'type')

class AwaitableGetReplicationvCenterResult(GetReplicationvCenterResult):

    def __await__(self):
        if False:
            yield self
        return GetReplicationvCenterResult(id=self.id, location=self.location, name=self.name, properties=self.properties, type=self.type)

def get_replicationv_center(fabric_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, vcenter_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetReplicationvCenterResult:
    """
    vCenter definition.


    :param str fabric_name: Fabric name.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    :param str vcenter_name: vcenter name.
    """
    __args__ = dict()
    __args__['fabricName'] = fabric_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    __args__['vcenterName'] = vcenter_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:recoveryservices/v20211101:getReplicationvCenter', __args__, opts=opts, typ=GetReplicationvCenterResult).value
    return AwaitableGetReplicationvCenterResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, type=__ret__.type)

@_utilities.lift_output_func(get_replicationv_center)
def get_replicationv_center_output(fabric_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, vcenter_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetReplicationvCenterResult]:
    """
    vCenter definition.


    :param str fabric_name: Fabric name.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    :param str vcenter_name: vcenter name.
    """
    ...
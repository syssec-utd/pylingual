import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetReplicationRecoveryPlanResult', 'AwaitableGetReplicationRecoveryPlanResult', 'get_replication_recovery_plan', 'get_replication_recovery_plan_output']

@pulumi.output_type
class GetReplicationRecoveryPlanResult:
    """
    Recovery plan details.
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
    def properties(self) -> 'outputs.RecoveryPlanPropertiesResponse':
        """
        The custom details.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, 'type')

class AwaitableGetReplicationRecoveryPlanResult(GetReplicationRecoveryPlanResult):

    def __await__(self):
        if False:
            yield self
        return GetReplicationRecoveryPlanResult(id=self.id, location=self.location, name=self.name, properties=self.properties, type=self.type)

def get_replication_recovery_plan(recovery_plan_name: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetReplicationRecoveryPlanResult:
    """
    Recovery plan details.


    :param str recovery_plan_name: Name of the recovery plan.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    """
    __args__ = dict()
    __args__['recoveryPlanName'] = recovery_plan_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:recoveryservices/v20220801:getReplicationRecoveryPlan', __args__, opts=opts, typ=GetReplicationRecoveryPlanResult).value
    return AwaitableGetReplicationRecoveryPlanResult(id=__ret__.id, location=__ret__.location, name=__ret__.name, properties=__ret__.properties, type=__ret__.type)

@_utilities.lift_output_func(get_replication_recovery_plan)
def get_replication_recovery_plan_output(recovery_plan_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetReplicationRecoveryPlanResult]:
    """
    Recovery plan details.


    :param str recovery_plan_name: Name of the recovery plan.
    :param str resource_group_name: The name of the resource group where the recovery services vault is present.
    :param str resource_name: The name of the recovery services vault.
    """
    ...
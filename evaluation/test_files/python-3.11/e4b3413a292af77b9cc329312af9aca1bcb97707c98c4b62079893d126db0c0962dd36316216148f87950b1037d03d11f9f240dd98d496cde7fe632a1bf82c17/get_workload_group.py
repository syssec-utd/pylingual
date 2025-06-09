import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetWorkloadGroupResult', 'AwaitableGetWorkloadGroupResult', 'get_workload_group', 'get_workload_group_output']

@pulumi.output_type
class GetWorkloadGroupResult:
    """
    Workload group operations for a data warehouse
    """

    def __init__(__self__, id=None, importance=None, max_resource_percent=None, max_resource_percent_per_request=None, min_resource_percent=None, min_resource_percent_per_request=None, name=None, query_execution_timeout=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if importance and (not isinstance(importance, str)):
            raise TypeError("Expected argument 'importance' to be a str")
        pulumi.set(__self__, 'importance', importance)
        if max_resource_percent and (not isinstance(max_resource_percent, int)):
            raise TypeError("Expected argument 'max_resource_percent' to be a int")
        pulumi.set(__self__, 'max_resource_percent', max_resource_percent)
        if max_resource_percent_per_request and (not isinstance(max_resource_percent_per_request, float)):
            raise TypeError("Expected argument 'max_resource_percent_per_request' to be a float")
        pulumi.set(__self__, 'max_resource_percent_per_request', max_resource_percent_per_request)
        if min_resource_percent and (not isinstance(min_resource_percent, int)):
            raise TypeError("Expected argument 'min_resource_percent' to be a int")
        pulumi.set(__self__, 'min_resource_percent', min_resource_percent)
        if min_resource_percent_per_request and (not isinstance(min_resource_percent_per_request, float)):
            raise TypeError("Expected argument 'min_resource_percent_per_request' to be a float")
        pulumi.set(__self__, 'min_resource_percent_per_request', min_resource_percent_per_request)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if query_execution_timeout and (not isinstance(query_execution_timeout, int)):
            raise TypeError("Expected argument 'query_execution_timeout' to be a int")
        pulumi.set(__self__, 'query_execution_timeout', query_execution_timeout)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def importance(self) -> Optional[str]:
        """
        The workload group importance level.
        """
        return pulumi.get(self, 'importance')

    @property
    @pulumi.getter(name='maxResourcePercent')
    def max_resource_percent(self) -> int:
        """
        The workload group cap percentage resource.
        """
        return pulumi.get(self, 'max_resource_percent')

    @property
    @pulumi.getter(name='maxResourcePercentPerRequest')
    def max_resource_percent_per_request(self) -> Optional[float]:
        """
        The workload group request maximum grant percentage.
        """
        return pulumi.get(self, 'max_resource_percent_per_request')

    @property
    @pulumi.getter(name='minResourcePercent')
    def min_resource_percent(self) -> int:
        """
        The workload group minimum percentage resource.
        """
        return pulumi.get(self, 'min_resource_percent')

    @property
    @pulumi.getter(name='minResourcePercentPerRequest')
    def min_resource_percent_per_request(self) -> float:
        """
        The workload group request minimum grant percentage.
        """
        return pulumi.get(self, 'min_resource_percent_per_request')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='queryExecutionTimeout')
    def query_execution_timeout(self) -> Optional[int]:
        """
        The workload group query execution timeout.
        """
        return pulumi.get(self, 'query_execution_timeout')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetWorkloadGroupResult(GetWorkloadGroupResult):

    def __await__(self):
        if False:
            yield self
        return GetWorkloadGroupResult(id=self.id, importance=self.importance, max_resource_percent=self.max_resource_percent, max_resource_percent_per_request=self.max_resource_percent_per_request, min_resource_percent=self.min_resource_percent, min_resource_percent_per_request=self.min_resource_percent_per_request, name=self.name, query_execution_timeout=self.query_execution_timeout, type=self.type)

def get_workload_group(database_name: Optional[str]=None, resource_group_name: Optional[str]=None, server_name: Optional[str]=None, workload_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWorkloadGroupResult:
    """
    Gets a workload group
    API Version: 2020-11-01-preview.


    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str workload_group_name: The name of the workload group.
    """
    __args__ = dict()
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    __args__['workloadGroupName'] = workload_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql:getWorkloadGroup', __args__, opts=opts, typ=GetWorkloadGroupResult).value
    return AwaitableGetWorkloadGroupResult(id=__ret__.id, importance=__ret__.importance, max_resource_percent=__ret__.max_resource_percent, max_resource_percent_per_request=__ret__.max_resource_percent_per_request, min_resource_percent=__ret__.min_resource_percent, min_resource_percent_per_request=__ret__.min_resource_percent_per_request, name=__ret__.name, query_execution_timeout=__ret__.query_execution_timeout, type=__ret__.type)

@_utilities.lift_output_func(get_workload_group)
def get_workload_group_output(database_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, workload_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWorkloadGroupResult]:
    """
    Gets a workload group
    API Version: 2020-11-01-preview.


    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str workload_group_name: The name of the workload group.
    """
    ...
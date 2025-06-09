import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetMonitoringConfigResult', 'AwaitableGetMonitoringConfigResult', 'get_monitoring_config', 'get_monitoring_config_output']

@pulumi.output_type
class GetMonitoringConfigResult:
    """
    The metric setting details for the role
    """

    def __init__(__self__, id=None, metric_configurations=None, name=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if metric_configurations and (not isinstance(metric_configurations, list)):
            raise TypeError("Expected argument 'metric_configurations' to be a list")
        pulumi.set(__self__, 'metric_configurations', metric_configurations)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The path ID that uniquely identifies the object.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='metricConfigurations')
    def metric_configurations(self) -> Sequence['outputs.MetricConfigurationResponse']:
        """
        The metrics configuration details
        """
        return pulumi.get(self, 'metric_configurations')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The object name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, 'type')

class AwaitableGetMonitoringConfigResult(GetMonitoringConfigResult):

    def __await__(self):
        if False:
            yield self
        return GetMonitoringConfigResult(id=self.id, metric_configurations=self.metric_configurations, name=self.name, type=self.type)

def get_monitoring_config(device_name: Optional[str]=None, resource_group_name: Optional[str]=None, role_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetMonitoringConfigResult:
    """
    The metric setting details for the role
    API Version: 2020-12-01.


    :param str device_name: The device name.
    :param str resource_group_name: The resource group name.
    :param str role_name: The role name.
    """
    __args__ = dict()
    __args__['deviceName'] = device_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['roleName'] = role_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databoxedge:getMonitoringConfig', __args__, opts=opts, typ=GetMonitoringConfigResult).value
    return AwaitableGetMonitoringConfigResult(id=__ret__.id, metric_configurations=__ret__.metric_configurations, name=__ret__.name, type=__ret__.type)

@_utilities.lift_output_func(get_monitoring_config)
def get_monitoring_config_output(device_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, role_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetMonitoringConfigResult]:
    """
    The metric setting details for the role
    API Version: 2020-12-01.


    :param str device_name: The device name.
    :param str resource_group_name: The resource group name.
    :param str role_name: The role name.
    """
    ...
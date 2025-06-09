import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['GetApplicationGatewayBackendHealthOnDemandResult', 'AwaitableGetApplicationGatewayBackendHealthOnDemandResult', 'get_application_gateway_backend_health_on_demand', 'get_application_gateway_backend_health_on_demand_output']

@pulumi.output_type
class GetApplicationGatewayBackendHealthOnDemandResult:
    """
    Result of on demand test probe.
    """

    def __init__(__self__, backend_address_pool=None, backend_health_http_settings=None):
        if backend_address_pool and (not isinstance(backend_address_pool, dict)):
            raise TypeError("Expected argument 'backend_address_pool' to be a dict")
        pulumi.set(__self__, 'backend_address_pool', backend_address_pool)
        if backend_health_http_settings and (not isinstance(backend_health_http_settings, dict)):
            raise TypeError("Expected argument 'backend_health_http_settings' to be a dict")
        pulumi.set(__self__, 'backend_health_http_settings', backend_health_http_settings)

    @property
    @pulumi.getter(name='backendAddressPool')
    def backend_address_pool(self) -> Optional['outputs.ApplicationGatewayBackendAddressPoolResponse']:
        """
        Reference to an ApplicationGatewayBackendAddressPool resource.
        """
        return pulumi.get(self, 'backend_address_pool')

    @property
    @pulumi.getter(name='backendHealthHttpSettings')
    def backend_health_http_settings(self) -> Optional['outputs.ApplicationGatewayBackendHealthHttpSettingsResponse']:
        """
        Application gateway BackendHealthHttp settings.
        """
        return pulumi.get(self, 'backend_health_http_settings')

class AwaitableGetApplicationGatewayBackendHealthOnDemandResult(GetApplicationGatewayBackendHealthOnDemandResult):

    def __await__(self):
        if False:
            yield self
        return GetApplicationGatewayBackendHealthOnDemandResult(backend_address_pool=self.backend_address_pool, backend_health_http_settings=self.backend_health_http_settings)

def get_application_gateway_backend_health_on_demand(application_gateway_name: Optional[str]=None, backend_address_pool: Optional[pulumi.InputType['SubResource']]=None, backend_http_settings: Optional[pulumi.InputType['SubResource']]=None, expand: Optional[str]=None, host: Optional[str]=None, match: Optional[pulumi.InputType['ApplicationGatewayProbeHealthResponseMatch']]=None, path: Optional[str]=None, pick_host_name_from_backend_http_settings: Optional[bool]=None, protocol: Optional[Union[str, 'ApplicationGatewayProtocol']]=None, resource_group_name: Optional[str]=None, timeout: Optional[int]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetApplicationGatewayBackendHealthOnDemandResult:
    """
    Result of on demand test probe.


    :param str application_gateway_name: The name of the application gateway.
    :param pulumi.InputType['SubResource'] backend_address_pool: Reference to backend pool of application gateway to which probe request will be sent.
    :param pulumi.InputType['SubResource'] backend_http_settings: Reference to backend http setting of application gateway to be used for test probe.
    :param str expand: Expands BackendAddressPool and BackendHttpSettings referenced in backend health.
    :param str host: Host name to send the probe to.
    :param pulumi.InputType['ApplicationGatewayProbeHealthResponseMatch'] match: Criterion for classifying a healthy probe response.
    :param str path: Relative path of probe. Valid path starts from '/'. Probe is sent to <Protocol>://<host>:<port><path>.
    :param bool pick_host_name_from_backend_http_settings: Whether the host header should be picked from the backend http settings. Default value is false.
    :param Union[str, 'ApplicationGatewayProtocol'] protocol: The protocol used for the probe.
    :param str resource_group_name: The name of the resource group.
    :param int timeout: The probe timeout in seconds. Probe marked as failed if valid response is not received with this timeout period. Acceptable values are from 1 second to 86400 seconds.
    """
    __args__ = dict()
    __args__['applicationGatewayName'] = application_gateway_name
    __args__['backendAddressPool'] = backend_address_pool
    __args__['backendHttpSettings'] = backend_http_settings
    __args__['expand'] = expand
    __args__['host'] = host
    __args__['match'] = match
    __args__['path'] = path
    __args__['pickHostNameFromBackendHttpSettings'] = pick_host_name_from_backend_http_settings
    __args__['protocol'] = protocol
    __args__['resourceGroupName'] = resource_group_name
    __args__['timeout'] = timeout
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220701:getApplicationGatewayBackendHealthOnDemand', __args__, opts=opts, typ=GetApplicationGatewayBackendHealthOnDemandResult).value
    return AwaitableGetApplicationGatewayBackendHealthOnDemandResult(backend_address_pool=__ret__.backend_address_pool, backend_health_http_settings=__ret__.backend_health_http_settings)

@_utilities.lift_output_func(get_application_gateway_backend_health_on_demand)
def get_application_gateway_backend_health_on_demand_output(application_gateway_name: Optional[pulumi.Input[str]]=None, backend_address_pool: Optional[pulumi.Input[Optional[pulumi.InputType['SubResource']]]]=None, backend_http_settings: Optional[pulumi.Input[Optional[pulumi.InputType['SubResource']]]]=None, expand: Optional[pulumi.Input[Optional[str]]]=None, host: Optional[pulumi.Input[Optional[str]]]=None, match: Optional[pulumi.Input[Optional[pulumi.InputType['ApplicationGatewayProbeHealthResponseMatch']]]]=None, path: Optional[pulumi.Input[Optional[str]]]=None, pick_host_name_from_backend_http_settings: Optional[pulumi.Input[Optional[bool]]]=None, protocol: Optional[pulumi.Input[Optional[Union[str, 'ApplicationGatewayProtocol']]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, timeout: Optional[pulumi.Input[Optional[int]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetApplicationGatewayBackendHealthOnDemandResult]:
    """
    Result of on demand test probe.


    :param str application_gateway_name: The name of the application gateway.
    :param pulumi.InputType['SubResource'] backend_address_pool: Reference to backend pool of application gateway to which probe request will be sent.
    :param pulumi.InputType['SubResource'] backend_http_settings: Reference to backend http setting of application gateway to be used for test probe.
    :param str expand: Expands BackendAddressPool and BackendHttpSettings referenced in backend health.
    :param str host: Host name to send the probe to.
    :param pulumi.InputType['ApplicationGatewayProbeHealthResponseMatch'] match: Criterion for classifying a healthy probe response.
    :param str path: Relative path of probe. Valid path starts from '/'. Probe is sent to <Protocol>://<host>:<port><path>.
    :param bool pick_host_name_from_backend_http_settings: Whether the host header should be picked from the backend http settings. Default value is false.
    :param Union[str, 'ApplicationGatewayProtocol'] protocol: The protocol used for the probe.
    :param str resource_group_name: The name of the resource group.
    :param int timeout: The probe timeout in seconds. Probe marked as failed if valid response is not received with this timeout period. Acceptable values are from 1 second to 86400 seconds.
    """
    ...
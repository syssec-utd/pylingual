import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetExpressRouteCircuitAuthorizationResult', 'AwaitableGetExpressRouteCircuitAuthorizationResult', 'get_express_route_circuit_authorization', 'get_express_route_circuit_authorization_output']

@pulumi.output_type
class GetExpressRouteCircuitAuthorizationResult:
    """
    Authorization in an ExpressRouteCircuit resource.
    """

    def __init__(__self__, authorization_key=None, authorization_use_status=None, etag=None, id=None, name=None, provisioning_state=None, type=None):
        if authorization_key and (not isinstance(authorization_key, str)):
            raise TypeError("Expected argument 'authorization_key' to be a str")
        pulumi.set(__self__, 'authorization_key', authorization_key)
        if authorization_use_status and (not isinstance(authorization_use_status, str)):
            raise TypeError("Expected argument 'authorization_use_status' to be a str")
        pulumi.set(__self__, 'authorization_use_status', authorization_use_status)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='authorizationKey')
    def authorization_key(self) -> Optional[str]:
        """
        The authorization key.
        """
        return pulumi.get(self, 'authorization_key')

    @property
    @pulumi.getter(name='authorizationUseStatus')
    def authorization_use_status(self) -> Optional[str]:
        """
        The authorization use status.
        """
        return pulumi.get(self, 'authorization_use_status')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the authorization resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, 'type')

class AwaitableGetExpressRouteCircuitAuthorizationResult(GetExpressRouteCircuitAuthorizationResult):

    def __await__(self):
        if False:
            yield self
        return GetExpressRouteCircuitAuthorizationResult(authorization_key=self.authorization_key, authorization_use_status=self.authorization_use_status, etag=self.etag, id=self.id, name=self.name, provisioning_state=self.provisioning_state, type=self.type)

def get_express_route_circuit_authorization(authorization_name: Optional[str]=None, circuit_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetExpressRouteCircuitAuthorizationResult:
    """
    Authorization in an ExpressRouteCircuit resource.


    :param str authorization_name: The name of the authorization.
    :param str circuit_name: The name of the express route circuit.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['authorizationName'] = authorization_name
    __args__['circuitName'] = circuit_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200301:getExpressRouteCircuitAuthorization', __args__, opts=opts, typ=GetExpressRouteCircuitAuthorizationResult).value
    return AwaitableGetExpressRouteCircuitAuthorizationResult(authorization_key=__ret__.authorization_key, authorization_use_status=__ret__.authorization_use_status, etag=__ret__.etag, id=__ret__.id, name=__ret__.name, provisioning_state=__ret__.provisioning_state, type=__ret__.type)

@_utilities.lift_output_func(get_express_route_circuit_authorization)
def get_express_route_circuit_authorization_output(authorization_name: Optional[pulumi.Input[str]]=None, circuit_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetExpressRouteCircuitAuthorizationResult]:
    """
    Authorization in an ExpressRouteCircuit resource.


    :param str authorization_name: The name of the authorization.
    :param str circuit_name: The name of the express route circuit.
    :param str resource_group_name: The name of the resource group.
    """
    ...
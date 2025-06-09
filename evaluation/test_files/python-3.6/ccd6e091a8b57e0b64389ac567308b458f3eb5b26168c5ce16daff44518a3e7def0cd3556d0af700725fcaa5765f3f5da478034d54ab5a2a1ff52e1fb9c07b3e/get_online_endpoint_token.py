import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetOnlineEndpointTokenResult', 'AwaitableGetOnlineEndpointTokenResult', 'get_online_endpoint_token', 'get_online_endpoint_token_output']

@pulumi.output_type
class GetOnlineEndpointTokenResult:
    """
    Service Token
    """

    def __init__(__self__, access_token=None, expiry_time_utc=None, refresh_after_time_utc=None, token_type=None):
        if access_token and (not isinstance(access_token, str)):
            raise TypeError("Expected argument 'access_token' to be a str")
        pulumi.set(__self__, 'access_token', access_token)
        if expiry_time_utc and (not isinstance(expiry_time_utc, float)):
            raise TypeError("Expected argument 'expiry_time_utc' to be a float")
        pulumi.set(__self__, 'expiry_time_utc', expiry_time_utc)
        if refresh_after_time_utc and (not isinstance(refresh_after_time_utc, float)):
            raise TypeError("Expected argument 'refresh_after_time_utc' to be a float")
        pulumi.set(__self__, 'refresh_after_time_utc', refresh_after_time_utc)
        if token_type and (not isinstance(token_type, str)):
            raise TypeError("Expected argument 'token_type' to be a str")
        pulumi.set(__self__, 'token_type', token_type)

    @property
    @pulumi.getter(name='accessToken')
    def access_token(self) -> Optional[str]:
        """
        Access token.
        """
        return pulumi.get(self, 'access_token')

    @property
    @pulumi.getter(name='expiryTimeUtc')
    def expiry_time_utc(self) -> Optional[float]:
        """
        Access token expiry time (UTC).
        """
        return pulumi.get(self, 'expiry_time_utc')

    @property
    @pulumi.getter(name='refreshAfterTimeUtc')
    def refresh_after_time_utc(self) -> Optional[float]:
        """
        Refresh access token after time (UTC).
        """
        return pulumi.get(self, 'refresh_after_time_utc')

    @property
    @pulumi.getter(name='tokenType')
    def token_type(self) -> Optional[str]:
        """
        Access token type.
        """
        return pulumi.get(self, 'token_type')

class AwaitableGetOnlineEndpointTokenResult(GetOnlineEndpointTokenResult):

    def __await__(self):
        if False:
            yield self
        return GetOnlineEndpointTokenResult(access_token=self.access_token, expiry_time_utc=self.expiry_time_utc, refresh_after_time_utc=self.refresh_after_time_utc, token_type=self.token_type)

def get_online_endpoint_token(endpoint_name: Optional[str]=None, resource_group_name: Optional[str]=None, workspace_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetOnlineEndpointTokenResult:
    """
    Service Token


    :param str endpoint_name: Online Endpoint name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    __args__ = dict()
    __args__['endpointName'] = endpoint_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearningservices/v20210301preview:getOnlineEndpointToken', __args__, opts=opts, typ=GetOnlineEndpointTokenResult).value
    return AwaitableGetOnlineEndpointTokenResult(access_token=__ret__.access_token, expiry_time_utc=__ret__.expiry_time_utc, refresh_after_time_utc=__ret__.refresh_after_time_utc, token_type=__ret__.token_type)

@_utilities.lift_output_func(get_online_endpoint_token)
def get_online_endpoint_token_output(endpoint_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, workspace_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetOnlineEndpointTokenResult]:
    """
    Service Token


    :param str endpoint_name: Online Endpoint name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    ...
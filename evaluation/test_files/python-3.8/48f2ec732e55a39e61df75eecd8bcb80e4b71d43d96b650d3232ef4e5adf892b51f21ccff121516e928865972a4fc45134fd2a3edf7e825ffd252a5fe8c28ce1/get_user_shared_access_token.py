import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['GetUserSharedAccessTokenResult', 'AwaitableGetUserSharedAccessTokenResult', 'get_user_shared_access_token', 'get_user_shared_access_token_output']

@pulumi.output_type
class GetUserSharedAccessTokenResult:
    """
    Get User Token response details.
    """

    def __init__(__self__, value=None):
        if value and (not isinstance(value, str)):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Shared Access Authorization token for the User.
        """
        return pulumi.get(self, 'value')

class AwaitableGetUserSharedAccessTokenResult(GetUserSharedAccessTokenResult):

    def __await__(self):
        if False:
            yield self
        return GetUserSharedAccessTokenResult(value=self.value)

def get_user_shared_access_token(expiry: Optional[str]=None, key_type: Optional['KeyType']=None, resource_group_name: Optional[str]=None, service_name: Optional[str]=None, uid: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetUserSharedAccessTokenResult:
    """
    Get User Token response details.


    :param str expiry: The Expiry time of the Token. Maximum token expiry time is set to 30 days. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
    :param 'KeyType' key_type: The Key to be used to generate token for user.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    :param str uid: User identifier. Must be unique in the current API Management service instance.
    """
    __args__ = dict()
    __args__['expiry'] = expiry
    __args__['keyType'] = key_type
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    __args__['uid'] = uid
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20180101:getUserSharedAccessToken', __args__, opts=opts, typ=GetUserSharedAccessTokenResult).value
    return AwaitableGetUserSharedAccessTokenResult(value=__ret__.value)

@_utilities.lift_output_func(get_user_shared_access_token)
def get_user_shared_access_token_output(expiry: Optional[pulumi.Input[str]]=None, key_type: Optional[pulumi.Input['KeyType']]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, uid: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetUserSharedAccessTokenResult]:
    """
    Get User Token response details.


    :param str expiry: The Expiry time of the Token. Maximum token expiry time is set to 30 days. The date conforms to the following format: `yyyy-MM-ddTHH:mm:ssZ` as specified by the ISO 8601 standard.
    :param 'KeyType' key_type: The Key to be used to generate token for user.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    :param str uid: User identifier. Must be unique in the current API Management service instance.
    """
    ...
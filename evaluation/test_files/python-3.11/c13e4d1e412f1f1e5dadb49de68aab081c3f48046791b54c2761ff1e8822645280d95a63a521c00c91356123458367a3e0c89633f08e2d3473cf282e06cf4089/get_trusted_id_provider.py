import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetTrustedIdProviderResult', 'AwaitableGetTrustedIdProviderResult', 'get_trusted_id_provider', 'get_trusted_id_provider_output']

@pulumi.output_type
class GetTrustedIdProviderResult:
    """
    Data Lake Store trusted identity provider information.
    """

    def __init__(__self__, id=None, id_provider=None, name=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if id_provider and (not isinstance(id_provider, str)):
            raise TypeError("Expected argument 'id_provider' to be a str")
        pulumi.set(__self__, 'id_provider', id_provider)
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
        The resource identifier.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='idProvider')
    def id_provider(self) -> str:
        """
        The URL of this trusted identity provider.
        """
        return pulumi.get(self, 'id_provider')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetTrustedIdProviderResult(GetTrustedIdProviderResult):

    def __await__(self):
        if False:
            yield self
        return GetTrustedIdProviderResult(id=self.id, id_provider=self.id_provider, name=self.name, type=self.type)

def get_trusted_id_provider(account_name: Optional[str]=None, resource_group_name: Optional[str]=None, trusted_id_provider_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetTrustedIdProviderResult:
    """
    Gets the specified Data Lake Store trusted identity provider.
    API Version: 2016-11-01.


    :param str account_name: The name of the Data Lake Store account.
    :param str resource_group_name: The name of the Azure resource group.
    :param str trusted_id_provider_name: The name of the trusted identity provider to retrieve.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['trustedIdProviderName'] = trusted_id_provider_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:datalakestore:getTrustedIdProvider', __args__, opts=opts, typ=GetTrustedIdProviderResult).value
    return AwaitableGetTrustedIdProviderResult(id=__ret__.id, id_provider=__ret__.id_provider, name=__ret__.name, type=__ret__.type)

@_utilities.lift_output_func(get_trusted_id_provider)
def get_trusted_id_provider_output(account_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, trusted_id_provider_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetTrustedIdProviderResult]:
    """
    Gets the specified Data Lake Store trusted identity provider.
    API Version: 2016-11-01.


    :param str account_name: The name of the Data Lake Store account.
    :param str resource_group_name: The name of the Azure resource group.
    :param str trusted_id_provider_name: The name of the trusted identity provider to retrieve.
    """
    ...
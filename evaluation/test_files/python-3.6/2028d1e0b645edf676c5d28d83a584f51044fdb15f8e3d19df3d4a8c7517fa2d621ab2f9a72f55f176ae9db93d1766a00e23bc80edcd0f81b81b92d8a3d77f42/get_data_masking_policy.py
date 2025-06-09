import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetDataMaskingPolicyResult', 'AwaitableGetDataMaskingPolicyResult', 'get_data_masking_policy', 'get_data_masking_policy_output']

@pulumi.output_type
class GetDataMaskingPolicyResult:
    """
    A database data masking policy.
    """

    def __init__(__self__, application_principals=None, data_masking_state=None, exempt_principals=None, id=None, kind=None, location=None, masking_level=None, name=None, type=None):
        if application_principals and (not isinstance(application_principals, str)):
            raise TypeError("Expected argument 'application_principals' to be a str")
        pulumi.set(__self__, 'application_principals', application_principals)
        if data_masking_state and (not isinstance(data_masking_state, str)):
            raise TypeError("Expected argument 'data_masking_state' to be a str")
        pulumi.set(__self__, 'data_masking_state', data_masking_state)
        if exempt_principals and (not isinstance(exempt_principals, str)):
            raise TypeError("Expected argument 'exempt_principals' to be a str")
        pulumi.set(__self__, 'exempt_principals', exempt_principals)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if masking_level and (not isinstance(masking_level, str)):
            raise TypeError("Expected argument 'masking_level' to be a str")
        pulumi.set(__self__, 'masking_level', masking_level)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='applicationPrincipals')
    def application_principals(self) -> str:
        """
        The list of the application principals. This is a legacy parameter and is no longer used.
        """
        return pulumi.get(self, 'application_principals')

    @property
    @pulumi.getter(name='dataMaskingState')
    def data_masking_state(self) -> str:
        """
        The state of the data masking policy.
        """
        return pulumi.get(self, 'data_masking_state')

    @property
    @pulumi.getter(name='exemptPrincipals')
    def exempt_principals(self) -> Optional[str]:
        """
        The list of the exempt principals. Specifies the semicolon-separated list of database users for which the data masking policy does not apply. The specified users receive data results without masking for all of the database queries.
        """
        return pulumi.get(self, 'exempt_principals')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of Data Masking Policy. Metadata, used for Azure portal.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the data masking policy.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='maskingLevel')
    def masking_level(self) -> str:
        """
        The masking level. This is a legacy parameter and is no longer used.
        """
        return pulumi.get(self, 'masking_level')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetDataMaskingPolicyResult(GetDataMaskingPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetDataMaskingPolicyResult(application_principals=self.application_principals, data_masking_state=self.data_masking_state, exempt_principals=self.exempt_principals, id=self.id, kind=self.kind, location=self.location, masking_level=self.masking_level, name=self.name, type=self.type)

def get_data_masking_policy(data_masking_policy_name: Optional[str]=None, database_name: Optional[str]=None, resource_group_name: Optional[str]=None, server_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDataMaskingPolicyResult:
    """
    A database data masking policy.


    :param str data_masking_policy_name: The name of the database for which the data masking policy applies.
    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['dataMaskingPolicyName'] = data_masking_policy_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20211101:getDataMaskingPolicy', __args__, opts=opts, typ=GetDataMaskingPolicyResult).value
    return AwaitableGetDataMaskingPolicyResult(application_principals=__ret__.application_principals, data_masking_state=__ret__.data_masking_state, exempt_principals=__ret__.exempt_principals, id=__ret__.id, kind=__ret__.kind, location=__ret__.location, masking_level=__ret__.masking_level, name=__ret__.name, type=__ret__.type)

@_utilities.lift_output_func(get_data_masking_policy)
def get_data_masking_policy_output(data_masking_policy_name: Optional[pulumi.Input[str]]=None, database_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDataMaskingPolicyResult]:
    """
    A database data masking policy.


    :param str data_masking_policy_name: The name of the database for which the data masking policy applies.
    :param str database_name: The name of the database.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    """
    ...
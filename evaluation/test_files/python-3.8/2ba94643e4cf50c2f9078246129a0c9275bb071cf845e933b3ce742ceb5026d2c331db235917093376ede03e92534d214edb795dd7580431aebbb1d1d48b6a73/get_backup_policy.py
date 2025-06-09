import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetBackupPolicyResult', 'AwaitableGetBackupPolicyResult', 'get_backup_policy', 'get_backup_policy_output']

@pulumi.output_type
class GetBackupPolicyResult:
    """
    BaseBackupPolicy resource
    """

    def __init__(__self__, id=None, name=None, properties=None, system_data=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id represents the complete path to the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name associated with the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.BackupPolicyResponse':
        """
        BaseBackupPolicyResource properties
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type represents the complete path of the form Namespace/ResourceType/ResourceType/...
        """
        return pulumi.get(self, 'type')

class AwaitableGetBackupPolicyResult(GetBackupPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetBackupPolicyResult(id=self.id, name=self.name, properties=self.properties, system_data=self.system_data, type=self.type)

def get_backup_policy(backup_policy_name: Optional[str]=None, resource_group_name: Optional[str]=None, vault_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetBackupPolicyResult:
    """
    Gets a backup policy belonging to a backup vault


    :param str resource_group_name: The name of the resource group where the backup vault is present.
    :param str vault_name: The name of the backup vault.
    """
    __args__ = dict()
    __args__['backupPolicyName'] = backup_policy_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vaultName'] = vault_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:dataprotection/v20210701:getBackupPolicy', __args__, opts=opts, typ=GetBackupPolicyResult).value
    return AwaitableGetBackupPolicyResult(id=__ret__.id, name=__ret__.name, properties=__ret__.properties, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_backup_policy)
def get_backup_policy_output(backup_policy_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, vault_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetBackupPolicyResult]:
    """
    Gets a backup policy belonging to a backup vault


    :param str resource_group_name: The name of the resource group where the backup vault is present.
    :param str vault_name: The name of the backup vault.
    """
    ...
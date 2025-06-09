import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ListWebAppBackupConfigurationResult', 'AwaitableListWebAppBackupConfigurationResult', 'list_web_app_backup_configuration', 'list_web_app_backup_configuration_output']

@pulumi.output_type
class ListWebAppBackupConfigurationResult:
    """
    Description of a backup which will be performed.
    """

    def __init__(__self__, backup_name=None, backup_schedule=None, databases=None, enabled=None, id=None, kind=None, name=None, storage_account_url=None, system_data=None, type=None):
        if backup_name and (not isinstance(backup_name, str)):
            raise TypeError("Expected argument 'backup_name' to be a str")
        pulumi.set(__self__, 'backup_name', backup_name)
        if backup_schedule and (not isinstance(backup_schedule, dict)):
            raise TypeError("Expected argument 'backup_schedule' to be a dict")
        pulumi.set(__self__, 'backup_schedule', backup_schedule)
        if databases and (not isinstance(databases, list)):
            raise TypeError("Expected argument 'databases' to be a list")
        pulumi.set(__self__, 'databases', databases)
        if enabled and (not isinstance(enabled, bool)):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, 'enabled', enabled)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if storage_account_url and (not isinstance(storage_account_url, str)):
            raise TypeError("Expected argument 'storage_account_url' to be a str")
        pulumi.set(__self__, 'storage_account_url', storage_account_url)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='backupName')
    def backup_name(self) -> Optional[str]:
        """
        Name of the backup.
        """
        return pulumi.get(self, 'backup_name')

    @property
    @pulumi.getter(name='backupSchedule')
    def backup_schedule(self) -> Optional['outputs.BackupScheduleResponse']:
        """
        Schedule for the backup if it is executed periodically.
        """
        return pulumi.get(self, 'backup_schedule')

    @property
    @pulumi.getter
    def databases(self) -> Optional[Sequence['outputs.DatabaseBackupSettingResponse']]:
        """
        Databases included in the backup.
        """
        return pulumi.get(self, 'databases')

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        True if the backup schedule is enabled (must be included in that case), false if the backup schedule should be disabled.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='storageAccountUrl')
    def storage_account_url(self) -> str:
        """
        SAS URL to the container.
        """
        return pulumi.get(self, 'storage_account_url')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableListWebAppBackupConfigurationResult(ListWebAppBackupConfigurationResult):

    def __await__(self):
        if False:
            yield self
        return ListWebAppBackupConfigurationResult(backup_name=self.backup_name, backup_schedule=self.backup_schedule, databases=self.databases, enabled=self.enabled, id=self.id, kind=self.kind, name=self.name, storage_account_url=self.storage_account_url, system_data=self.system_data, type=self.type)

def list_web_app_backup_configuration(name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListWebAppBackupConfigurationResult:
    """
    Description of a backup which will be performed.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20200901:listWebAppBackupConfiguration', __args__, opts=opts, typ=ListWebAppBackupConfigurationResult).value
    return AwaitableListWebAppBackupConfigurationResult(backup_name=__ret__.backup_name, backup_schedule=__ret__.backup_schedule, databases=__ret__.databases, enabled=__ret__.enabled, id=__ret__.id, kind=__ret__.kind, name=__ret__.name, storage_account_url=__ret__.storage_account_url, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(list_web_app_backup_configuration)
def list_web_app_backup_configuration_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListWebAppBackupConfigurationResult]:
    """
    Description of a backup which will be performed.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
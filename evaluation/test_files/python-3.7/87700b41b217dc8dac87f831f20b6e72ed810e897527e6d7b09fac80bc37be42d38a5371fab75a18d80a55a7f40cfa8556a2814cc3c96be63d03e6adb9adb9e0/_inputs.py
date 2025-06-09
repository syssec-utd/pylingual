import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *
__all__ = ['AbsoluteDeleteOptionArgs', 'AdhocBasedTaggingCriteriaArgs', 'AdhocBasedTriggerContextArgs', 'AzureBackupParamsArgs', 'AzureBackupRuleArgs', 'AzureOperationalStoreParametersArgs', 'AzureRetentionRuleArgs', 'BackupInstanceArgs', 'BackupPolicyArgs', 'BackupScheduleArgs', 'BackupVaultArgs', 'CopyOnExpiryOptionArgs', 'CustomCopyOptionArgs', 'DataStoreInfoBaseArgs', 'DatasourceSetArgs', 'DatasourceArgs', 'DayArgs', 'DppIdentityDetailsArgs', 'ImmediateCopyOptionArgs', 'PolicyInfoArgs', 'PolicyParametersArgs', 'RetentionTagArgs', 'ScheduleBasedBackupCriteriaArgs', 'ScheduleBasedTriggerContextArgs', 'SourceLifeCycleArgs', 'StorageSettingArgs', 'TaggingCriteriaArgs', 'TargetCopySettingArgs']

@pulumi.input_type
class AbsoluteDeleteOptionArgs:

    def __init__(__self__, *, duration: pulumi.Input[str], object_type: pulumi.Input[str]):
        """
        Delete option with duration
        :param pulumi.Input[str] duration: Duration of deletion after given timespan
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'AbsoluteDeleteOption'.
        """
        pulumi.set(__self__, 'duration', duration)
        pulumi.set(__self__, 'object_type', 'AbsoluteDeleteOption')

    @property
    @pulumi.getter
    def duration(self) -> pulumi.Input[str]:
        """
        Duration of deletion after given timespan
        """
        return pulumi.get(self, 'duration')

    @duration.setter
    def duration(self, value: pulumi.Input[str]):
        pulumi.set(self, 'duration', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'AbsoluteDeleteOption'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

@pulumi.input_type
class AdhocBasedTaggingCriteriaArgs:

    def __init__(__self__, *, tag_info: Optional[pulumi.Input['RetentionTagArgs']]=None):
        """
        Adhoc backup tagging criteria
        :param pulumi.Input['RetentionTagArgs'] tag_info: Retention tag information
        """
        if tag_info is not None:
            pulumi.set(__self__, 'tag_info', tag_info)

    @property
    @pulumi.getter(name='tagInfo')
    def tag_info(self) -> Optional[pulumi.Input['RetentionTagArgs']]:
        """
        Retention tag information
        """
        return pulumi.get(self, 'tag_info')

    @tag_info.setter
    def tag_info(self, value: Optional[pulumi.Input['RetentionTagArgs']]):
        pulumi.set(self, 'tag_info', value)

@pulumi.input_type
class AdhocBasedTriggerContextArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str], tagging_criteria: pulumi.Input['AdhocBasedTaggingCriteriaArgs']):
        """
        Adhoc trigger context
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'AdhocBasedTriggerContext'.
        :param pulumi.Input['AdhocBasedTaggingCriteriaArgs'] tagging_criteria: Tagging Criteria containing retention tag for adhoc backup.
        """
        pulumi.set(__self__, 'object_type', 'AdhocBasedTriggerContext')
        pulumi.set(__self__, 'tagging_criteria', tagging_criteria)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'AdhocBasedTriggerContext'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='taggingCriteria')
    def tagging_criteria(self) -> pulumi.Input['AdhocBasedTaggingCriteriaArgs']:
        """
        Tagging Criteria containing retention tag for adhoc backup.
        """
        return pulumi.get(self, 'tagging_criteria')

    @tagging_criteria.setter
    def tagging_criteria(self, value: pulumi.Input['AdhocBasedTaggingCriteriaArgs']):
        pulumi.set(self, 'tagging_criteria', value)

@pulumi.input_type
class AzureBackupParamsArgs:

    def __init__(__self__, *, backup_type: pulumi.Input[str], object_type: pulumi.Input[str]):
        """
        Azure backup parameters
        :param pulumi.Input[str] backup_type: BackupType ; Full/Incremental etc
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'AzureBackupParams'.
        """
        pulumi.set(__self__, 'backup_type', backup_type)
        pulumi.set(__self__, 'object_type', 'AzureBackupParams')

    @property
    @pulumi.getter(name='backupType')
    def backup_type(self) -> pulumi.Input[str]:
        """
        BackupType ; Full/Incremental etc
        """
        return pulumi.get(self, 'backup_type')

    @backup_type.setter
    def backup_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'backup_type', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'AzureBackupParams'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

@pulumi.input_type
class AzureBackupRuleArgs:

    def __init__(__self__, *, data_store: pulumi.Input['DataStoreInfoBaseArgs'], name: pulumi.Input[str], object_type: pulumi.Input[str], trigger: pulumi.Input[Union['AdhocBasedTriggerContextArgs', 'ScheduleBasedTriggerContextArgs']], backup_parameters: Optional[pulumi.Input['AzureBackupParamsArgs']]=None):
        """
        Azure backup rule
        :param pulumi.Input['DataStoreInfoBaseArgs'] data_store: DataStoreInfo base
        :param pulumi.Input[str] object_type: 
               Expected value is 'AzureBackupRule'.
        :param pulumi.Input[Union['AdhocBasedTriggerContextArgs', 'ScheduleBasedTriggerContextArgs']] trigger: Trigger context
        :param pulumi.Input['AzureBackupParamsArgs'] backup_parameters: BackupParameters base
        """
        pulumi.set(__self__, 'data_store', data_store)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'object_type', 'AzureBackupRule')
        pulumi.set(__self__, 'trigger', trigger)
        if backup_parameters is not None:
            pulumi.set(__self__, 'backup_parameters', backup_parameters)

    @property
    @pulumi.getter(name='dataStore')
    def data_store(self) -> pulumi.Input['DataStoreInfoBaseArgs']:
        """
        DataStoreInfo base
        """
        return pulumi.get(self, 'data_store')

    @data_store.setter
    def data_store(self, value: pulumi.Input['DataStoreInfoBaseArgs']):
        pulumi.set(self, 'data_store', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """

        Expected value is 'AzureBackupRule'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter
    def trigger(self) -> pulumi.Input[Union['AdhocBasedTriggerContextArgs', 'ScheduleBasedTriggerContextArgs']]:
        """
        Trigger context
        """
        return pulumi.get(self, 'trigger')

    @trigger.setter
    def trigger(self, value: pulumi.Input[Union['AdhocBasedTriggerContextArgs', 'ScheduleBasedTriggerContextArgs']]):
        pulumi.set(self, 'trigger', value)

    @property
    @pulumi.getter(name='backupParameters')
    def backup_parameters(self) -> Optional[pulumi.Input['AzureBackupParamsArgs']]:
        """
        BackupParameters base
        """
        return pulumi.get(self, 'backup_parameters')

    @backup_parameters.setter
    def backup_parameters(self, value: Optional[pulumi.Input['AzureBackupParamsArgs']]):
        pulumi.set(self, 'backup_parameters', value)

@pulumi.input_type
class AzureOperationalStoreParametersArgs:

    def __init__(__self__, *, data_store_type: pulumi.Input[Union[str, 'DataStoreTypes']], object_type: pulumi.Input[str], resource_group_id: Optional[pulumi.Input[str]]=None):
        """
        Parameters for Operational-Tier DataStore
        :param pulumi.Input[Union[str, 'DataStoreTypes']] data_store_type: type of datastore; Operational/Vault/Archive
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'AzureOperationalStoreParameters'.
        :param pulumi.Input[str] resource_group_id: Gets or sets the Snapshot Resource Group Uri.
        """
        pulumi.set(__self__, 'data_store_type', data_store_type)
        pulumi.set(__self__, 'object_type', 'AzureOperationalStoreParameters')
        if resource_group_id is not None:
            pulumi.set(__self__, 'resource_group_id', resource_group_id)

    @property
    @pulumi.getter(name='dataStoreType')
    def data_store_type(self) -> pulumi.Input[Union[str, 'DataStoreTypes']]:
        """
        type of datastore; Operational/Vault/Archive
        """
        return pulumi.get(self, 'data_store_type')

    @data_store_type.setter
    def data_store_type(self, value: pulumi.Input[Union[str, 'DataStoreTypes']]):
        pulumi.set(self, 'data_store_type', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'AzureOperationalStoreParameters'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the Snapshot Resource Group Uri.
        """
        return pulumi.get(self, 'resource_group_id')

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_id', value)

@pulumi.input_type
class AzureRetentionRuleArgs:

    def __init__(__self__, *, lifecycles: pulumi.Input[Sequence[pulumi.Input['SourceLifeCycleArgs']]], name: pulumi.Input[str], object_type: pulumi.Input[str], is_default: Optional[pulumi.Input[bool]]=None):
        """
        Azure retention rule
        :param pulumi.Input[str] object_type: 
               Expected value is 'AzureRetentionRule'.
        """
        pulumi.set(__self__, 'lifecycles', lifecycles)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'object_type', 'AzureRetentionRule')
        if is_default is not None:
            pulumi.set(__self__, 'is_default', is_default)

    @property
    @pulumi.getter
    def lifecycles(self) -> pulumi.Input[Sequence[pulumi.Input['SourceLifeCycleArgs']]]:
        return pulumi.get(self, 'lifecycles')

    @lifecycles.setter
    def lifecycles(self, value: pulumi.Input[Sequence[pulumi.Input['SourceLifeCycleArgs']]]):
        pulumi.set(self, 'lifecycles', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """

        Expected value is 'AzureRetentionRule'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='isDefault')
    def is_default(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, 'is_default')

    @is_default.setter
    def is_default(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_default', value)

@pulumi.input_type
class BackupInstanceArgs:

    def __init__(__self__, *, data_source_info: pulumi.Input['DatasourceArgs'], object_type: pulumi.Input[str], policy_info: pulumi.Input['PolicyInfoArgs'], data_source_set_info: Optional[pulumi.Input['DatasourceSetArgs']]=None, friendly_name: Optional[pulumi.Input[str]]=None):
        """
        Backup Instance
        :param pulumi.Input['DatasourceArgs'] data_source_info: Gets or sets the data source information.
        :param pulumi.Input['PolicyInfoArgs'] policy_info: Gets or sets the policy information.
        :param pulumi.Input['DatasourceSetArgs'] data_source_set_info: Gets or sets the data source set information.
        :param pulumi.Input[str] friendly_name: Gets or sets the Backup Instance friendly name.
        """
        pulumi.set(__self__, 'data_source_info', data_source_info)
        pulumi.set(__self__, 'object_type', object_type)
        pulumi.set(__self__, 'policy_info', policy_info)
        if data_source_set_info is not None:
            pulumi.set(__self__, 'data_source_set_info', data_source_set_info)
        if friendly_name is not None:
            pulumi.set(__self__, 'friendly_name', friendly_name)

    @property
    @pulumi.getter(name='dataSourceInfo')
    def data_source_info(self) -> pulumi.Input['DatasourceArgs']:
        """
        Gets or sets the data source information.
        """
        return pulumi.get(self, 'data_source_info')

    @data_source_info.setter
    def data_source_info(self, value: pulumi.Input['DatasourceArgs']):
        pulumi.set(self, 'data_source_info', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='policyInfo')
    def policy_info(self) -> pulumi.Input['PolicyInfoArgs']:
        """
        Gets or sets the policy information.
        """
        return pulumi.get(self, 'policy_info')

    @policy_info.setter
    def policy_info(self, value: pulumi.Input['PolicyInfoArgs']):
        pulumi.set(self, 'policy_info', value)

    @property
    @pulumi.getter(name='dataSourceSetInfo')
    def data_source_set_info(self) -> Optional[pulumi.Input['DatasourceSetArgs']]:
        """
        Gets or sets the data source set information.
        """
        return pulumi.get(self, 'data_source_set_info')

    @data_source_set_info.setter
    def data_source_set_info(self, value: Optional[pulumi.Input['DatasourceSetArgs']]):
        pulumi.set(self, 'data_source_set_info', value)

    @property
    @pulumi.getter(name='friendlyName')
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the Backup Instance friendly name.
        """
        return pulumi.get(self, 'friendly_name')

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'friendly_name', value)

@pulumi.input_type
class BackupPolicyArgs:

    def __init__(__self__, *, datasource_types: pulumi.Input[Sequence[pulumi.Input[str]]], object_type: pulumi.Input[str], policy_rules: pulumi.Input[Sequence[pulumi.Input[Union['AzureBackupRuleArgs', 'AzureRetentionRuleArgs']]]]):
        """
        Rule based backup policy
        :param pulumi.Input[Sequence[pulumi.Input[str]]] datasource_types: Type of datasource for the backup management
        :param pulumi.Input[str] object_type: 
               Expected value is 'BackupPolicy'.
        :param pulumi.Input[Sequence[pulumi.Input[Union['AzureBackupRuleArgs', 'AzureRetentionRuleArgs']]]] policy_rules: Policy rule dictionary that contains rules for each backuptype i.e Full/Incremental/Logs etc
        """
        pulumi.set(__self__, 'datasource_types', datasource_types)
        pulumi.set(__self__, 'object_type', 'BackupPolicy')
        pulumi.set(__self__, 'policy_rules', policy_rules)

    @property
    @pulumi.getter(name='datasourceTypes')
    def datasource_types(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Type of datasource for the backup management
        """
        return pulumi.get(self, 'datasource_types')

    @datasource_types.setter
    def datasource_types(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'datasource_types', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """

        Expected value is 'BackupPolicy'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='policyRules')
    def policy_rules(self) -> pulumi.Input[Sequence[pulumi.Input[Union['AzureBackupRuleArgs', 'AzureRetentionRuleArgs']]]]:
        """
        Policy rule dictionary that contains rules for each backuptype i.e Full/Incremental/Logs etc
        """
        return pulumi.get(self, 'policy_rules')

    @policy_rules.setter
    def policy_rules(self, value: pulumi.Input[Sequence[pulumi.Input[Union['AzureBackupRuleArgs', 'AzureRetentionRuleArgs']]]]):
        pulumi.set(self, 'policy_rules', value)

@pulumi.input_type
class BackupScheduleArgs:

    def __init__(__self__, *, repeating_time_intervals: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        Schedule for backup
        :param pulumi.Input[Sequence[pulumi.Input[str]]] repeating_time_intervals: ISO 8601 repeating time interval format
        """
        pulumi.set(__self__, 'repeating_time_intervals', repeating_time_intervals)

    @property
    @pulumi.getter(name='repeatingTimeIntervals')
    def repeating_time_intervals(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        ISO 8601 repeating time interval format
        """
        return pulumi.get(self, 'repeating_time_intervals')

    @repeating_time_intervals.setter
    def repeating_time_intervals(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'repeating_time_intervals', value)

@pulumi.input_type
class BackupVaultArgs:

    def __init__(__self__, *, storage_settings: pulumi.Input[Sequence[pulumi.Input['StorageSettingArgs']]]):
        """
        Backup Vault
        :param pulumi.Input[Sequence[pulumi.Input['StorageSettingArgs']]] storage_settings: Storage Settings
        """
        pulumi.set(__self__, 'storage_settings', storage_settings)

    @property
    @pulumi.getter(name='storageSettings')
    def storage_settings(self) -> pulumi.Input[Sequence[pulumi.Input['StorageSettingArgs']]]:
        """
        Storage Settings
        """
        return pulumi.get(self, 'storage_settings')

    @storage_settings.setter
    def storage_settings(self, value: pulumi.Input[Sequence[pulumi.Input['StorageSettingArgs']]]):
        pulumi.set(self, 'storage_settings', value)

@pulumi.input_type
class CopyOnExpiryOptionArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str]):
        """
        Copy on Expiry Option
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'CopyOnExpiryOption'.
        """
        pulumi.set(__self__, 'object_type', 'CopyOnExpiryOption')

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'CopyOnExpiryOption'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

@pulumi.input_type
class CustomCopyOptionArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str], duration: Optional[pulumi.Input[str]]=None):
        """
        Duration based custom options to copy
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'CustomCopyOption'.
        :param pulumi.Input[str] duration: Data copied after given timespan
        """
        pulumi.set(__self__, 'object_type', 'CustomCopyOption')
        if duration is not None:
            pulumi.set(__self__, 'duration', duration)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'CustomCopyOption'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter
    def duration(self) -> Optional[pulumi.Input[str]]:
        """
        Data copied after given timespan
        """
        return pulumi.get(self, 'duration')

    @duration.setter
    def duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'duration', value)

@pulumi.input_type
class DataStoreInfoBaseArgs:

    def __init__(__self__, *, data_store_type: pulumi.Input[Union[str, 'DataStoreTypes']], object_type: pulumi.Input[str]):
        """
        DataStoreInfo base
        :param pulumi.Input[Union[str, 'DataStoreTypes']] data_store_type: type of datastore; Operational/Vault/Archive
        :param pulumi.Input[str] object_type: Type of Datasource object, used to initialize the right inherited type
        """
        pulumi.set(__self__, 'data_store_type', data_store_type)
        pulumi.set(__self__, 'object_type', object_type)

    @property
    @pulumi.getter(name='dataStoreType')
    def data_store_type(self) -> pulumi.Input[Union[str, 'DataStoreTypes']]:
        """
        type of datastore; Operational/Vault/Archive
        """
        return pulumi.get(self, 'data_store_type')

    @data_store_type.setter
    def data_store_type(self, value: pulumi.Input[Union[str, 'DataStoreTypes']]):
        pulumi.set(self, 'data_store_type', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of Datasource object, used to initialize the right inherited type
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

@pulumi.input_type
class DatasourceSetArgs:

    def __init__(__self__, *, resource_id: pulumi.Input[str], datasource_type: Optional[pulumi.Input[str]]=None, object_type: Optional[pulumi.Input[str]]=None, resource_location: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, resource_type: Optional[pulumi.Input[str]]=None, resource_uri: Optional[pulumi.Input[str]]=None):
        """
        DatasourceSet details of datasource to be backed up
        :param pulumi.Input[str] resource_id: Full ARM ID of the resource. For azure resources, this is ARM ID. For non azure resources, this will be the ID created by backup service via Fabric/Vault.
        :param pulumi.Input[str] datasource_type: DatasourceType of the resource.
        :param pulumi.Input[str] object_type: Type of Datasource object, used to initialize the right inherited type
        :param pulumi.Input[str] resource_location: Location of datasource.
        :param pulumi.Input[str] resource_name: Unique identifier of the resource in the context of parent.
        :param pulumi.Input[str] resource_type: Resource Type of Datasource.
        :param pulumi.Input[str] resource_uri: Uri of the resource.
        """
        pulumi.set(__self__, 'resource_id', resource_id)
        if datasource_type is not None:
            pulumi.set(__self__, 'datasource_type', datasource_type)
        if object_type is not None:
            pulumi.set(__self__, 'object_type', object_type)
        if resource_location is not None:
            pulumi.set(__self__, 'resource_location', resource_location)
        if resource_name is not None:
            pulumi.set(__self__, 'resource_name', resource_name)
        if resource_type is not None:
            pulumi.set(__self__, 'resource_type', resource_type)
        if resource_uri is not None:
            pulumi.set(__self__, 'resource_uri', resource_uri)

    @property
    @pulumi.getter(name='resourceID')
    def resource_id(self) -> pulumi.Input[str]:
        """
        Full ARM ID of the resource. For azure resources, this is ARM ID. For non azure resources, this will be the ID created by backup service via Fabric/Vault.
        """
        return pulumi.get(self, 'resource_id')

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_id', value)

    @property
    @pulumi.getter(name='datasourceType')
    def datasource_type(self) -> Optional[pulumi.Input[str]]:
        """
        DatasourceType of the resource.
        """
        return pulumi.get(self, 'datasource_type')

    @datasource_type.setter
    def datasource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'datasource_type', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Datasource object, used to initialize the right inherited type
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='resourceLocation')
    def resource_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location of datasource.
        """
        return pulumi.get(self, 'resource_location')

    @resource_location.setter
    def resource_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_location', value)

    @property
    @pulumi.getter(name='resourceName')
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the resource in the context of parent.
        """
        return pulumi.get(self, 'resource_name')

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_name', value)

    @property
    @pulumi.getter(name='resourceType')
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Type of Datasource.
        """
        return pulumi.get(self, 'resource_type')

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_type', value)

    @property
    @pulumi.getter(name='resourceUri')
    def resource_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Uri of the resource.
        """
        return pulumi.get(self, 'resource_uri')

    @resource_uri.setter
    def resource_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_uri', value)

@pulumi.input_type
class DatasourceArgs:

    def __init__(__self__, *, resource_id: pulumi.Input[str], datasource_type: Optional[pulumi.Input[str]]=None, object_type: Optional[pulumi.Input[str]]=None, resource_location: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, resource_type: Optional[pulumi.Input[str]]=None, resource_uri: Optional[pulumi.Input[str]]=None):
        """
        Datasource to be backed up
        :param pulumi.Input[str] resource_id: Full ARM ID of the resource. For azure resources, this is ARM ID. For non azure resources, this will be the ID created by backup service via Fabric/Vault.
        :param pulumi.Input[str] datasource_type: DatasourceType of the resource.
        :param pulumi.Input[str] object_type: Type of Datasource object, used to initialize the right inherited type
        :param pulumi.Input[str] resource_location: Location of datasource.
        :param pulumi.Input[str] resource_name: Unique identifier of the resource in the context of parent.
        :param pulumi.Input[str] resource_type: Resource Type of Datasource.
        :param pulumi.Input[str] resource_uri: Uri of the resource.
        """
        pulumi.set(__self__, 'resource_id', resource_id)
        if datasource_type is not None:
            pulumi.set(__self__, 'datasource_type', datasource_type)
        if object_type is not None:
            pulumi.set(__self__, 'object_type', object_type)
        if resource_location is not None:
            pulumi.set(__self__, 'resource_location', resource_location)
        if resource_name is not None:
            pulumi.set(__self__, 'resource_name', resource_name)
        if resource_type is not None:
            pulumi.set(__self__, 'resource_type', resource_type)
        if resource_uri is not None:
            pulumi.set(__self__, 'resource_uri', resource_uri)

    @property
    @pulumi.getter(name='resourceID')
    def resource_id(self) -> pulumi.Input[str]:
        """
        Full ARM ID of the resource. For azure resources, this is ARM ID. For non azure resources, this will be the ID created by backup service via Fabric/Vault.
        """
        return pulumi.get(self, 'resource_id')

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_id', value)

    @property
    @pulumi.getter(name='datasourceType')
    def datasource_type(self) -> Optional[pulumi.Input[str]]:
        """
        DatasourceType of the resource.
        """
        return pulumi.get(self, 'datasource_type')

    @datasource_type.setter
    def datasource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'datasource_type', value)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of Datasource object, used to initialize the right inherited type
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='resourceLocation')
    def resource_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location of datasource.
        """
        return pulumi.get(self, 'resource_location')

    @resource_location.setter
    def resource_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_location', value)

    @property
    @pulumi.getter(name='resourceName')
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier of the resource in the context of parent.
        """
        return pulumi.get(self, 'resource_name')

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_name', value)

    @property
    @pulumi.getter(name='resourceType')
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Type of Datasource.
        """
        return pulumi.get(self, 'resource_type')

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_type', value)

    @property
    @pulumi.getter(name='resourceUri')
    def resource_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Uri of the resource.
        """
        return pulumi.get(self, 'resource_uri')

    @resource_uri.setter
    def resource_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_uri', value)

@pulumi.input_type
class DayArgs:

    def __init__(__self__, *, date: Optional[pulumi.Input[int]]=None, is_last: Optional[pulumi.Input[bool]]=None):
        """
        Day of the week
        :param pulumi.Input[int] date: Date of the month
        :param pulumi.Input[bool] is_last: Whether Date is last date of month
        """
        if date is not None:
            pulumi.set(__self__, 'date', date)
        if is_last is not None:
            pulumi.set(__self__, 'is_last', is_last)

    @property
    @pulumi.getter
    def date(self) -> Optional[pulumi.Input[int]]:
        """
        Date of the month
        """
        return pulumi.get(self, 'date')

    @date.setter
    def date(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'date', value)

    @property
    @pulumi.getter(name='isLast')
    def is_last(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether Date is last date of month
        """
        return pulumi.get(self, 'is_last')

    @is_last.setter
    def is_last(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_last', value)

@pulumi.input_type
class DppIdentityDetailsArgs:

    def __init__(__self__, *, type: Optional[pulumi.Input[str]]=None):
        """
        Identity details
        :param pulumi.Input[str] type: The identityType which can be either SystemAssigned or None
        """
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The identityType which can be either SystemAssigned or None
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class ImmediateCopyOptionArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str]):
        """
        Immediate copy Option
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'ImmediateCopyOption'.
        """
        pulumi.set(__self__, 'object_type', 'ImmediateCopyOption')

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'ImmediateCopyOption'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

@pulumi.input_type
class PolicyInfoArgs:

    def __init__(__self__, *, policy_id: pulumi.Input[str], policy_parameters: Optional[pulumi.Input['PolicyParametersArgs']]=None):
        """
        Policy Info in backupInstance
        :param pulumi.Input['PolicyParametersArgs'] policy_parameters: Policy parameters for the backup instance
        """
        pulumi.set(__self__, 'policy_id', policy_id)
        if policy_parameters is not None:
            pulumi.set(__self__, 'policy_parameters', policy_parameters)

    @property
    @pulumi.getter(name='policyId')
    def policy_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'policy_id')

    @policy_id.setter
    def policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'policy_id', value)

    @property
    @pulumi.getter(name='policyParameters')
    def policy_parameters(self) -> Optional[pulumi.Input['PolicyParametersArgs']]:
        """
        Policy parameters for the backup instance
        """
        return pulumi.get(self, 'policy_parameters')

    @policy_parameters.setter
    def policy_parameters(self, value: Optional[pulumi.Input['PolicyParametersArgs']]):
        pulumi.set(self, 'policy_parameters', value)

@pulumi.input_type
class PolicyParametersArgs:

    def __init__(__self__, *, data_store_parameters_list: Optional[pulumi.Input[Sequence[pulumi.Input['AzureOperationalStoreParametersArgs']]]]=None):
        """
        Parameters in Policy
        :param pulumi.Input[Sequence[pulumi.Input['AzureOperationalStoreParametersArgs']]] data_store_parameters_list: Gets or sets the DataStore Parameters
        """
        if data_store_parameters_list is not None:
            pulumi.set(__self__, 'data_store_parameters_list', data_store_parameters_list)

    @property
    @pulumi.getter(name='dataStoreParametersList')
    def data_store_parameters_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureOperationalStoreParametersArgs']]]]:
        """
        Gets or sets the DataStore Parameters
        """
        return pulumi.get(self, 'data_store_parameters_list')

    @data_store_parameters_list.setter
    def data_store_parameters_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureOperationalStoreParametersArgs']]]]):
        pulumi.set(self, 'data_store_parameters_list', value)

@pulumi.input_type
class RetentionTagArgs:

    def __init__(__self__, *, tag_name: pulumi.Input[str]):
        """
        Retention tag
        :param pulumi.Input[str] tag_name: Retention Tag Name to relate it to retention rule.
        """
        pulumi.set(__self__, 'tag_name', tag_name)

    @property
    @pulumi.getter(name='tagName')
    def tag_name(self) -> pulumi.Input[str]:
        """
        Retention Tag Name to relate it to retention rule.
        """
        return pulumi.get(self, 'tag_name')

    @tag_name.setter
    def tag_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'tag_name', value)

@pulumi.input_type
class ScheduleBasedBackupCriteriaArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str], absolute_criteria: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AbsoluteMarker']]]]]=None, days_of_month: Optional[pulumi.Input[Sequence[pulumi.Input['DayArgs']]]]=None, days_of_the_week: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]]=None, months_of_year: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'Month']]]]]=None, schedule_times: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, weeks_of_the_month: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeekNumber']]]]]=None):
        """
        Schedule based backup criteria
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'ScheduleBasedBackupCriteria'.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AbsoluteMarker']]]] absolute_criteria: it contains absolute values like "AllBackup" / "FirstOfDay" / "FirstOfWeek" / "FirstOfMonth"
               and should be part of AbsoluteMarker enum
        :param pulumi.Input[Sequence[pulumi.Input['DayArgs']]] days_of_month: This is day of the month from 1 to 28 other wise last of month
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]] days_of_the_week: It should be Sunday/Monday/T..../Saturday
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'Month']]]] months_of_year: It should be January/February/....../December
        :param pulumi.Input[Sequence[pulumi.Input[str]]] schedule_times: List of schedule times for backup
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeekNumber']]]] weeks_of_the_month: It should be First/Second/Third/Fourth/Last
        """
        pulumi.set(__self__, 'object_type', 'ScheduleBasedBackupCriteria')
        if absolute_criteria is not None:
            pulumi.set(__self__, 'absolute_criteria', absolute_criteria)
        if days_of_month is not None:
            pulumi.set(__self__, 'days_of_month', days_of_month)
        if days_of_the_week is not None:
            pulumi.set(__self__, 'days_of_the_week', days_of_the_week)
        if months_of_year is not None:
            pulumi.set(__self__, 'months_of_year', months_of_year)
        if schedule_times is not None:
            pulumi.set(__self__, 'schedule_times', schedule_times)
        if weeks_of_the_month is not None:
            pulumi.set(__self__, 'weeks_of_the_month', weeks_of_the_month)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'ScheduleBasedBackupCriteria'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter(name='absoluteCriteria')
    def absolute_criteria(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AbsoluteMarker']]]]]:
        """
        it contains absolute values like "AllBackup" / "FirstOfDay" / "FirstOfWeek" / "FirstOfMonth"
        and should be part of AbsoluteMarker enum
        """
        return pulumi.get(self, 'absolute_criteria')

    @absolute_criteria.setter
    def absolute_criteria(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AbsoluteMarker']]]]]):
        pulumi.set(self, 'absolute_criteria', value)

    @property
    @pulumi.getter(name='daysOfMonth')
    def days_of_month(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DayArgs']]]]:
        """
        This is day of the month from 1 to 28 other wise last of month
        """
        return pulumi.get(self, 'days_of_month')

    @days_of_month.setter
    def days_of_month(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DayArgs']]]]):
        pulumi.set(self, 'days_of_month', value)

    @property
    @pulumi.getter(name='daysOfTheWeek')
    def days_of_the_week(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]]:
        """
        It should be Sunday/Monday/T..../Saturday
        """
        return pulumi.get(self, 'days_of_the_week')

    @days_of_the_week.setter
    def days_of_the_week(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]]):
        pulumi.set(self, 'days_of_the_week', value)

    @property
    @pulumi.getter(name='monthsOfYear')
    def months_of_year(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'Month']]]]]:
        """
        It should be January/February/....../December
        """
        return pulumi.get(self, 'months_of_year')

    @months_of_year.setter
    def months_of_year(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'Month']]]]]):
        pulumi.set(self, 'months_of_year', value)

    @property
    @pulumi.getter(name='scheduleTimes')
    def schedule_times(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of schedule times for backup
        """
        return pulumi.get(self, 'schedule_times')

    @schedule_times.setter
    def schedule_times(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'schedule_times', value)

    @property
    @pulumi.getter(name='weeksOfTheMonth')
    def weeks_of_the_month(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeekNumber']]]]]:
        """
        It should be First/Second/Third/Fourth/Last
        """
        return pulumi.get(self, 'weeks_of_the_month')

    @weeks_of_the_month.setter
    def weeks_of_the_month(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeekNumber']]]]]):
        pulumi.set(self, 'weeks_of_the_month', value)

@pulumi.input_type
class ScheduleBasedTriggerContextArgs:

    def __init__(__self__, *, object_type: pulumi.Input[str], schedule: pulumi.Input['BackupScheduleArgs'], tagging_criteria: pulumi.Input[Sequence[pulumi.Input['TaggingCriteriaArgs']]]):
        """
        Schedule based trigger context
        :param pulumi.Input[str] object_type: Type of the specific object - used for deserializing
               Expected value is 'ScheduleBasedTriggerContext'.
        :param pulumi.Input['BackupScheduleArgs'] schedule: Schedule for this backup
        :param pulumi.Input[Sequence[pulumi.Input['TaggingCriteriaArgs']]] tagging_criteria: List of tags that can be applicable for given schedule.
        """
        pulumi.set(__self__, 'object_type', 'ScheduleBasedTriggerContext')
        pulumi.set(__self__, 'schedule', schedule)
        pulumi.set(__self__, 'tagging_criteria', tagging_criteria)

    @property
    @pulumi.getter(name='objectType')
    def object_type(self) -> pulumi.Input[str]:
        """
        Type of the specific object - used for deserializing
        Expected value is 'ScheduleBasedTriggerContext'.
        """
        return pulumi.get(self, 'object_type')

    @object_type.setter
    def object_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'object_type', value)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input['BackupScheduleArgs']:
        """
        Schedule for this backup
        """
        return pulumi.get(self, 'schedule')

    @schedule.setter
    def schedule(self, value: pulumi.Input['BackupScheduleArgs']):
        pulumi.set(self, 'schedule', value)

    @property
    @pulumi.getter(name='taggingCriteria')
    def tagging_criteria(self) -> pulumi.Input[Sequence[pulumi.Input['TaggingCriteriaArgs']]]:
        """
        List of tags that can be applicable for given schedule.
        """
        return pulumi.get(self, 'tagging_criteria')

    @tagging_criteria.setter
    def tagging_criteria(self, value: pulumi.Input[Sequence[pulumi.Input['TaggingCriteriaArgs']]]):
        pulumi.set(self, 'tagging_criteria', value)

@pulumi.input_type
class SourceLifeCycleArgs:

    def __init__(__self__, *, delete_after: pulumi.Input['AbsoluteDeleteOptionArgs'], source_data_store: pulumi.Input['DataStoreInfoBaseArgs'], target_data_store_copy_settings: Optional[pulumi.Input[Sequence[pulumi.Input['TargetCopySettingArgs']]]]=None):
        """
        Source LifeCycle
        :param pulumi.Input['AbsoluteDeleteOptionArgs'] delete_after: Delete Option
        :param pulumi.Input['DataStoreInfoBaseArgs'] source_data_store: DataStoreInfo base
        """
        pulumi.set(__self__, 'delete_after', delete_after)
        pulumi.set(__self__, 'source_data_store', source_data_store)
        if target_data_store_copy_settings is not None:
            pulumi.set(__self__, 'target_data_store_copy_settings', target_data_store_copy_settings)

    @property
    @pulumi.getter(name='deleteAfter')
    def delete_after(self) -> pulumi.Input['AbsoluteDeleteOptionArgs']:
        """
        Delete Option
        """
        return pulumi.get(self, 'delete_after')

    @delete_after.setter
    def delete_after(self, value: pulumi.Input['AbsoluteDeleteOptionArgs']):
        pulumi.set(self, 'delete_after', value)

    @property
    @pulumi.getter(name='sourceDataStore')
    def source_data_store(self) -> pulumi.Input['DataStoreInfoBaseArgs']:
        """
        DataStoreInfo base
        """
        return pulumi.get(self, 'source_data_store')

    @source_data_store.setter
    def source_data_store(self, value: pulumi.Input['DataStoreInfoBaseArgs']):
        pulumi.set(self, 'source_data_store', value)

    @property
    @pulumi.getter(name='targetDataStoreCopySettings')
    def target_data_store_copy_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TargetCopySettingArgs']]]]:
        return pulumi.get(self, 'target_data_store_copy_settings')

    @target_data_store_copy_settings.setter
    def target_data_store_copy_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TargetCopySettingArgs']]]]):
        pulumi.set(self, 'target_data_store_copy_settings', value)

@pulumi.input_type
class StorageSettingArgs:

    def __init__(__self__, *, datastore_type: Optional[pulumi.Input[Union[str, 'StorageSettingStoreTypes']]]=None, type: Optional[pulumi.Input[Union[str, 'StorageSettingTypes']]]=None):
        """
        Storage setting
        :param pulumi.Input[Union[str, 'StorageSettingStoreTypes']] datastore_type: Gets or sets the type of the datastore.
        :param pulumi.Input[Union[str, 'StorageSettingTypes']] type: Gets or sets the type.
        """
        if datastore_type is not None:
            pulumi.set(__self__, 'datastore_type', datastore_type)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='datastoreType')
    def datastore_type(self) -> Optional[pulumi.Input[Union[str, 'StorageSettingStoreTypes']]]:
        """
        Gets or sets the type of the datastore.
        """
        return pulumi.get(self, 'datastore_type')

    @datastore_type.setter
    def datastore_type(self, value: Optional[pulumi.Input[Union[str, 'StorageSettingStoreTypes']]]):
        pulumi.set(self, 'datastore_type', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'StorageSettingTypes']]]:
        """
        Gets or sets the type.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'StorageSettingTypes']]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class TaggingCriteriaArgs:

    def __init__(__self__, *, is_default: pulumi.Input[bool], tag_info: pulumi.Input['RetentionTagArgs'], tagging_priority: pulumi.Input[float], criteria: Optional[pulumi.Input[Sequence[pulumi.Input['ScheduleBasedBackupCriteriaArgs']]]]=None):
        """
        Tagging criteria
        :param pulumi.Input[bool] is_default: Specifies if tag is default.
        :param pulumi.Input['RetentionTagArgs'] tag_info: Retention tag information
        :param pulumi.Input[float] tagging_priority: Retention Tag priority.
        :param pulumi.Input[Sequence[pulumi.Input['ScheduleBasedBackupCriteriaArgs']]] criteria: Criteria which decides whether the tag can be applied to a triggered backup.
        """
        pulumi.set(__self__, 'is_default', is_default)
        pulumi.set(__self__, 'tag_info', tag_info)
        pulumi.set(__self__, 'tagging_priority', tagging_priority)
        if criteria is not None:
            pulumi.set(__self__, 'criteria', criteria)

    @property
    @pulumi.getter(name='isDefault')
    def is_default(self) -> pulumi.Input[bool]:
        """
        Specifies if tag is default.
        """
        return pulumi.get(self, 'is_default')

    @is_default.setter
    def is_default(self, value: pulumi.Input[bool]):
        pulumi.set(self, 'is_default', value)

    @property
    @pulumi.getter(name='tagInfo')
    def tag_info(self) -> pulumi.Input['RetentionTagArgs']:
        """
        Retention tag information
        """
        return pulumi.get(self, 'tag_info')

    @tag_info.setter
    def tag_info(self, value: pulumi.Input['RetentionTagArgs']):
        pulumi.set(self, 'tag_info', value)

    @property
    @pulumi.getter(name='taggingPriority')
    def tagging_priority(self) -> pulumi.Input[float]:
        """
        Retention Tag priority.
        """
        return pulumi.get(self, 'tagging_priority')

    @tagging_priority.setter
    def tagging_priority(self, value: pulumi.Input[float]):
        pulumi.set(self, 'tagging_priority', value)

    @property
    @pulumi.getter
    def criteria(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ScheduleBasedBackupCriteriaArgs']]]]:
        """
        Criteria which decides whether the tag can be applied to a triggered backup.
        """
        return pulumi.get(self, 'criteria')

    @criteria.setter
    def criteria(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ScheduleBasedBackupCriteriaArgs']]]]):
        pulumi.set(self, 'criteria', value)

@pulumi.input_type
class TargetCopySettingArgs:

    def __init__(__self__, *, copy_after: pulumi.Input[Union['CopyOnExpiryOptionArgs', 'CustomCopyOptionArgs', 'ImmediateCopyOptionArgs']], data_store: pulumi.Input['DataStoreInfoBaseArgs']):
        """
        Target copy settings
        :param pulumi.Input[Union['CopyOnExpiryOptionArgs', 'CustomCopyOptionArgs', 'ImmediateCopyOptionArgs']] copy_after: It can be CustomCopyOption or ImmediateCopyOption.
        :param pulumi.Input['DataStoreInfoBaseArgs'] data_store: Info of target datastore
        """
        pulumi.set(__self__, 'copy_after', copy_after)
        pulumi.set(__self__, 'data_store', data_store)

    @property
    @pulumi.getter(name='copyAfter')
    def copy_after(self) -> pulumi.Input[Union['CopyOnExpiryOptionArgs', 'CustomCopyOptionArgs', 'ImmediateCopyOptionArgs']]:
        """
        It can be CustomCopyOption or ImmediateCopyOption.
        """
        return pulumi.get(self, 'copy_after')

    @copy_after.setter
    def copy_after(self, value: pulumi.Input[Union['CopyOnExpiryOptionArgs', 'CustomCopyOptionArgs', 'ImmediateCopyOptionArgs']]):
        pulumi.set(self, 'copy_after', value)

    @property
    @pulumi.getter(name='dataStore')
    def data_store(self) -> pulumi.Input['DataStoreInfoBaseArgs']:
        """
        Info of target datastore
        """
        return pulumi.get(self, 'data_store')

    @data_store.setter
    def data_store(self, value: pulumi.Input['DataStoreInfoBaseArgs']):
        pulumi.set(self, 'data_store', value)
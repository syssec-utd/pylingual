import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['InstanceArgs', 'Instance']

@pulumi.input_type
class InstanceArgs:

    def __init__(__self__, *, db_instance_class: pulumi.Input[str], db_instance_storage: pulumi.Input[int], engine_version: pulumi.Input[str], account_password: Optional[pulumi.Input[str]]=None, auto_renew: Optional[pulumi.Input[bool]]=None, backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, backup_time: Optional[pulumi.Input[str]]=None, hidden_zone_id: Optional[pulumi.Input[str]]=None, instance_charge_type: Optional[pulumi.Input[str]]=None, kms_encrypted_password: Optional[pulumi.Input[str]]=None, kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]]=None, maintain_end_time: Optional[pulumi.Input[str]]=None, maintain_start_time: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_type: Optional[pulumi.Input[str]]=None, order_type: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]=None, period: Optional[pulumi.Input[int]]=None, readonly_replicas: Optional[pulumi.Input[int]]=None, replication_factor: Optional[pulumi.Input[int]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, secondary_zone_id: Optional[pulumi.Input[str]]=None, security_group_id: Optional[pulumi.Input[str]]=None, security_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ssl_action: Optional[pulumi.Input[str]]=None, storage_engine: Optional[pulumi.Input[str]]=None, storage_type: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, tde_status: Optional[pulumi.Input[str]]=None, vpc_id: Optional[pulumi.Input[str]]=None, vswitch_id: Optional[pulumi.Input[str]]=None, zone_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Instance resource.
        :param pulumi.Input[str] db_instance_class: Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        :param pulumi.Input[int] db_instance_storage: User-defined DB instance storage space.Unit: GB. Value range:
               - Custom storage space.
               - 10-GB increments.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        :param pulumi.Input[str] account_password: Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        :param pulumi.Input[bool] auto_renew: Auto renew for prepaid, true of false. Default is false.
               > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_periods: MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        :param pulumi.Input[str] backup_time: MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        :param pulumi.Input[str] hidden_zone_id: Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[str] network_type: The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        :param pulumi.Input[str] order_type: The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
               * UPGRADE: The specifications are upgraded.
               * DOWNGRADE: The specifications are downgraded.
               Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]] parameters: Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        :param pulumi.Input[int] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        :param pulumi.Input[int] readonly_replicas: The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        :param pulumi.Input[int] replication_factor: Number of replica set nodes. Valid values: [1, 3, 5, 7]
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group.
        :param pulumi.Input[str] secondary_zone_id: Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        :param pulumi.Input[str] security_group_id: The Security Group ID of ECS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_ip_lists: List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        :param pulumi.Input[str] ssl_action: Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        :param pulumi.Input[str] storage_engine: Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        :param pulumi.Input[str] storage_type: The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tde_status: The TDE(Transparent Data Encryption) status.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance. it supports multiple zone.
               If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
               The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        pulumi.set(__self__, 'db_instance_class', db_instance_class)
        pulumi.set(__self__, 'db_instance_storage', db_instance_storage)
        pulumi.set(__self__, 'engine_version', engine_version)
        if account_password is not None:
            pulumi.set(__self__, 'account_password', account_password)
        if auto_renew is not None:
            pulumi.set(__self__, 'auto_renew', auto_renew)
        if backup_periods is not None:
            pulumi.set(__self__, 'backup_periods', backup_periods)
        if backup_time is not None:
            pulumi.set(__self__, 'backup_time', backup_time)
        if hidden_zone_id is not None:
            pulumi.set(__self__, 'hidden_zone_id', hidden_zone_id)
        if instance_charge_type is not None:
            pulumi.set(__self__, 'instance_charge_type', instance_charge_type)
        if kms_encrypted_password is not None:
            pulumi.set(__self__, 'kms_encrypted_password', kms_encrypted_password)
        if kms_encryption_context is not None:
            pulumi.set(__self__, 'kms_encryption_context', kms_encryption_context)
        if maintain_end_time is not None:
            pulumi.set(__self__, 'maintain_end_time', maintain_end_time)
        if maintain_start_time is not None:
            pulumi.set(__self__, 'maintain_start_time', maintain_start_time)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if network_type is not None:
            pulumi.set(__self__, 'network_type', network_type)
        if order_type is not None:
            pulumi.set(__self__, 'order_type', order_type)
        if parameters is not None:
            pulumi.set(__self__, 'parameters', parameters)
        if period is not None:
            pulumi.set(__self__, 'period', period)
        if readonly_replicas is not None:
            pulumi.set(__self__, 'readonly_replicas', readonly_replicas)
        if replication_factor is not None:
            pulumi.set(__self__, 'replication_factor', replication_factor)
        if resource_group_id is not None:
            pulumi.set(__self__, 'resource_group_id', resource_group_id)
        if secondary_zone_id is not None:
            pulumi.set(__self__, 'secondary_zone_id', secondary_zone_id)
        if security_group_id is not None:
            pulumi.set(__self__, 'security_group_id', security_group_id)
        if security_ip_lists is not None:
            pulumi.set(__self__, 'security_ip_lists', security_ip_lists)
        if ssl_action is not None:
            pulumi.set(__self__, 'ssl_action', ssl_action)
        if storage_engine is not None:
            pulumi.set(__self__, 'storage_engine', storage_engine)
        if storage_type is not None:
            pulumi.set(__self__, 'storage_type', storage_type)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if tde_status is not None:
            pulumi.set(__self__, 'tde_status', tde_status)
        if vpc_id is not None:
            pulumi.set(__self__, 'vpc_id', vpc_id)
        if vswitch_id is not None:
            pulumi.set(__self__, 'vswitch_id', vswitch_id)
        if zone_id is not None:
            pulumi.set(__self__, 'zone_id', zone_id)

    @property
    @pulumi.getter(name='dbInstanceClass')
    def db_instance_class(self) -> pulumi.Input[str]:
        """
        Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        """
        return pulumi.get(self, 'db_instance_class')

    @db_instance_class.setter
    def db_instance_class(self, value: pulumi.Input[str]):
        pulumi.set(self, 'db_instance_class', value)

    @property
    @pulumi.getter(name='dbInstanceStorage')
    def db_instance_storage(self) -> pulumi.Input[int]:
        """
        User-defined DB instance storage space.Unit: GB. Value range:
        - Custom storage space.
        - 10-GB increments.
        """
        return pulumi.get(self, 'db_instance_storage')

    @db_instance_storage.setter
    def db_instance_storage(self, value: pulumi.Input[int]):
        pulumi.set(self, 'db_instance_storage', value)

    @property
    @pulumi.getter(name='engineVersion')
    def engine_version(self) -> pulumi.Input[str]:
        """
        Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        """
        return pulumi.get(self, 'engine_version')

    @engine_version.setter
    def engine_version(self, value: pulumi.Input[str]):
        pulumi.set(self, 'engine_version', value)

    @property
    @pulumi.getter(name='accountPassword')
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        """
        return pulumi.get(self, 'account_password')

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'account_password', value)

    @property
    @pulumi.getter(name='autoRenew')
    def auto_renew(self) -> Optional[pulumi.Input[bool]]:
        """
        Auto renew for prepaid, true of false. Default is false.
        > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        """
        return pulumi.get(self, 'auto_renew')

    @auto_renew.setter
    def auto_renew(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_renew', value)

    @property
    @pulumi.getter(name='backupPeriods')
    def backup_periods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        """
        return pulumi.get(self, 'backup_periods')

    @backup_periods.setter
    def backup_periods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'backup_periods', value)

    @property
    @pulumi.getter(name='backupTime')
    def backup_time(self) -> Optional[pulumi.Input[str]]:
        """
        MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        """
        return pulumi.get(self, 'backup_time')

    @backup_time.setter
    def backup_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'backup_time', value)

    @property
    @pulumi.getter(name='hiddenZoneId')
    def hidden_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        """
        return pulumi.get(self, 'hidden_zone_id')

    @hidden_zone_id.setter
    def hidden_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'hidden_zone_id', value)

    @property
    @pulumi.getter(name='instanceChargeType')
    def instance_charge_type(self) -> Optional[pulumi.Input[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        """
        return pulumi.get(self, 'instance_charge_type')

    @instance_charge_type.setter
    def instance_charge_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'instance_charge_type', value)

    @property
    @pulumi.getter(name='kmsEncryptedPassword')
    def kms_encrypted_password(self) -> Optional[pulumi.Input[str]]:
        """
        An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, 'kms_encrypted_password')

    @kms_encrypted_password.setter
    def kms_encrypted_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kms_encrypted_password', value)

    @property
    @pulumi.getter(name='kmsEncryptionContext')
    def kms_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, 'kms_encryption_context')

    @kms_encryption_context.setter
    def kms_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'kms_encryption_context', value)

    @property
    @pulumi.getter(name='maintainEndTime')
    def maintain_end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_end_time')

    @maintain_end_time.setter
    def maintain_end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'maintain_end_time', value)

    @property
    @pulumi.getter(name='maintainStartTime')
    def maintain_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_start_time')

    @maintain_start_time.setter
    def maintain_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'maintain_start_time', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of DB instance. It a string of 2 to 256 characters.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='networkType')
    def network_type(self) -> Optional[pulumi.Input[str]]:
        """
        The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        """
        return pulumi.get(self, 'network_type')

    @network_type.setter
    def network_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'network_type', value)

    @property
    @pulumi.getter(name='orderType')
    def order_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
        * UPGRADE: The specifications are upgraded.
        * DOWNGRADE: The specifications are downgraded.
        Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        """
        return pulumi.get(self, 'order_type')

    @order_type.setter
    def order_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'order_type', value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]:
        """
        Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        """
        return pulumi.get(self, 'parameters')

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]):
        pulumi.set(self, 'parameters', value)

    @property
    @pulumi.getter
    def period(self) -> Optional[pulumi.Input[int]]:
        """
        The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        """
        return pulumi.get(self, 'period')

    @period.setter
    def period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'period', value)

    @property
    @pulumi.getter(name='readonlyReplicas')
    def readonly_replicas(self) -> Optional[pulumi.Input[int]]:
        """
        The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        """
        return pulumi.get(self, 'readonly_replicas')

    @readonly_replicas.setter
    def readonly_replicas(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'readonly_replicas', value)

    @property
    @pulumi.getter(name='replicationFactor')
    def replication_factor(self) -> Optional[pulumi.Input[int]]:
        """
        Number of replica set nodes. Valid values: [1, 3, 5, 7]
        """
        return pulumi.get(self, 'replication_factor')

    @replication_factor.setter
    def replication_factor(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'replication_factor', value)

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Resource Group.
        """
        return pulumi.get(self, 'resource_group_id')

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_id', value)

    @property
    @pulumi.getter(name='secondaryZoneId')
    def secondary_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        """
        return pulumi.get(self, 'secondary_zone_id')

    @secondary_zone_id.setter
    def secondary_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'secondary_zone_id', value)

    @property
    @pulumi.getter(name='securityGroupId')
    def security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Security Group ID of ECS.
        """
        return pulumi.get(self, 'security_group_id')

    @security_group_id.setter
    def security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'security_group_id', value)

    @property
    @pulumi.getter(name='securityIpLists')
    def security_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        """
        return pulumi.get(self, 'security_ip_lists')

    @security_ip_lists.setter
    def security_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'security_ip_lists', value)

    @property
    @pulumi.getter(name='sslAction')
    def ssl_action(self) -> Optional[pulumi.Input[str]]:
        """
        Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        """
        return pulumi.get(self, 'ssl_action')

    @ssl_action.setter
    def ssl_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ssl_action', value)

    @property
    @pulumi.getter(name='storageEngine')
    def storage_engine(self) -> Optional[pulumi.Input[str]]:
        """
        Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        """
        return pulumi.get(self, 'storage_engine')

    @storage_engine.setter
    def storage_engine(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'storage_engine', value)

    @property
    @pulumi.getter(name='storageType')
    def storage_type(self) -> Optional[pulumi.Input[str]]:
        """
        The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        """
        return pulumi.get(self, 'storage_type')

    @storage_type.setter
    def storage_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'storage_type', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='tdeStatus')
    def tde_status(self) -> Optional[pulumi.Input[str]]:
        """
        The TDE(Transparent Data Encryption) status.
        """
        return pulumi.get(self, 'tde_status')

    @tde_status.setter
    def tde_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tde_status', value)

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        """
        return pulumi.get(self, 'vpc_id')

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vpc_id', value)

    @property
    @pulumi.getter(name='vswitchId')
    def vswitch_id(self) -> Optional[pulumi.Input[str]]:
        """
        The virtual switch ID to launch DB instances in one VPC.
        """
        return pulumi.get(self, 'vswitch_id')

    @vswitch_id.setter
    def vswitch_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vswitch_id', value)

    @property
    @pulumi.getter(name='zoneId')
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Zone to launch the DB instance. it supports multiple zone.
        If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
        The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        return pulumi.get(self, 'zone_id')

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zone_id', value)

@pulumi.input_type
class _InstanceState:

    def __init__(__self__, *, account_password: Optional[pulumi.Input[str]]=None, auto_renew: Optional[pulumi.Input[bool]]=None, backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, backup_time: Optional[pulumi.Input[str]]=None, db_instance_class: Optional[pulumi.Input[str]]=None, db_instance_storage: Optional[pulumi.Input[int]]=None, engine_version: Optional[pulumi.Input[str]]=None, hidden_zone_id: Optional[pulumi.Input[str]]=None, instance_charge_type: Optional[pulumi.Input[str]]=None, kms_encrypted_password: Optional[pulumi.Input[str]]=None, kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]]=None, maintain_end_time: Optional[pulumi.Input[str]]=None, maintain_start_time: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_type: Optional[pulumi.Input[str]]=None, order_type: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]=None, period: Optional[pulumi.Input[int]]=None, readonly_replicas: Optional[pulumi.Input[int]]=None, replica_set_name: Optional[pulumi.Input[str]]=None, replica_sets: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceReplicaSetArgs']]]]=None, replication_factor: Optional[pulumi.Input[int]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, retention_period: Optional[pulumi.Input[int]]=None, secondary_zone_id: Optional[pulumi.Input[str]]=None, security_group_id: Optional[pulumi.Input[str]]=None, security_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ssl_action: Optional[pulumi.Input[str]]=None, ssl_status: Optional[pulumi.Input[str]]=None, storage_engine: Optional[pulumi.Input[str]]=None, storage_type: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, tde_status: Optional[pulumi.Input[str]]=None, vpc_id: Optional[pulumi.Input[str]]=None, vswitch_id: Optional[pulumi.Input[str]]=None, zone_id: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering Instance resources.
        :param pulumi.Input[str] account_password: Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        :param pulumi.Input[bool] auto_renew: Auto renew for prepaid, true of false. Default is false.
               > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_periods: MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        :param pulumi.Input[str] backup_time: MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        :param pulumi.Input[str] db_instance_class: Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        :param pulumi.Input[int] db_instance_storage: User-defined DB instance storage space.Unit: GB. Value range:
               - Custom storage space.
               - 10-GB increments.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        :param pulumi.Input[str] hidden_zone_id: Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[str] network_type: The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        :param pulumi.Input[str] order_type: The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
               * UPGRADE: The specifications are upgraded.
               * DOWNGRADE: The specifications are downgraded.
               Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        :param pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]] parameters: Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        :param pulumi.Input[int] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        :param pulumi.Input[int] readonly_replicas: The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        :param pulumi.Input[str] replica_set_name: The name of the mongo replica set
        :param pulumi.Input[Sequence[pulumi.Input['InstanceReplicaSetArgs']]] replica_sets: Replica set instance information. The details see Block replica_sets. **NOTE:** Available in v1.140+.
        :param pulumi.Input[int] replication_factor: Number of replica set nodes. Valid values: [1, 3, 5, 7]
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group.
        :param pulumi.Input[int] retention_period: Instance log backup retention days. Available in 1.42.0+.
        :param pulumi.Input[str] secondary_zone_id: Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        :param pulumi.Input[str] security_group_id: The Security Group ID of ECS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_ip_lists: List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        :param pulumi.Input[str] ssl_action: Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        :param pulumi.Input[str] ssl_status: Status of the SSL feature. `Open`: SSL is turned on; `Closed`: SSL is turned off.
        :param pulumi.Input[str] storage_engine: Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        :param pulumi.Input[str] storage_type: The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tde_status: The TDE(Transparent Data Encryption) status.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance. it supports multiple zone.
               If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
               The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        if account_password is not None:
            pulumi.set(__self__, 'account_password', account_password)
        if auto_renew is not None:
            pulumi.set(__self__, 'auto_renew', auto_renew)
        if backup_periods is not None:
            pulumi.set(__self__, 'backup_periods', backup_periods)
        if backup_time is not None:
            pulumi.set(__self__, 'backup_time', backup_time)
        if db_instance_class is not None:
            pulumi.set(__self__, 'db_instance_class', db_instance_class)
        if db_instance_storage is not None:
            pulumi.set(__self__, 'db_instance_storage', db_instance_storage)
        if engine_version is not None:
            pulumi.set(__self__, 'engine_version', engine_version)
        if hidden_zone_id is not None:
            pulumi.set(__self__, 'hidden_zone_id', hidden_zone_id)
        if instance_charge_type is not None:
            pulumi.set(__self__, 'instance_charge_type', instance_charge_type)
        if kms_encrypted_password is not None:
            pulumi.set(__self__, 'kms_encrypted_password', kms_encrypted_password)
        if kms_encryption_context is not None:
            pulumi.set(__self__, 'kms_encryption_context', kms_encryption_context)
        if maintain_end_time is not None:
            pulumi.set(__self__, 'maintain_end_time', maintain_end_time)
        if maintain_start_time is not None:
            pulumi.set(__self__, 'maintain_start_time', maintain_start_time)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if network_type is not None:
            pulumi.set(__self__, 'network_type', network_type)
        if order_type is not None:
            pulumi.set(__self__, 'order_type', order_type)
        if parameters is not None:
            pulumi.set(__self__, 'parameters', parameters)
        if period is not None:
            pulumi.set(__self__, 'period', period)
        if readonly_replicas is not None:
            pulumi.set(__self__, 'readonly_replicas', readonly_replicas)
        if replica_set_name is not None:
            pulumi.set(__self__, 'replica_set_name', replica_set_name)
        if replica_sets is not None:
            pulumi.set(__self__, 'replica_sets', replica_sets)
        if replication_factor is not None:
            pulumi.set(__self__, 'replication_factor', replication_factor)
        if resource_group_id is not None:
            pulumi.set(__self__, 'resource_group_id', resource_group_id)
        if retention_period is not None:
            pulumi.set(__self__, 'retention_period', retention_period)
        if secondary_zone_id is not None:
            pulumi.set(__self__, 'secondary_zone_id', secondary_zone_id)
        if security_group_id is not None:
            pulumi.set(__self__, 'security_group_id', security_group_id)
        if security_ip_lists is not None:
            pulumi.set(__self__, 'security_ip_lists', security_ip_lists)
        if ssl_action is not None:
            pulumi.set(__self__, 'ssl_action', ssl_action)
        if ssl_status is not None:
            pulumi.set(__self__, 'ssl_status', ssl_status)
        if storage_engine is not None:
            pulumi.set(__self__, 'storage_engine', storage_engine)
        if storage_type is not None:
            pulumi.set(__self__, 'storage_type', storage_type)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if tde_status is not None:
            pulumi.set(__self__, 'tde_status', tde_status)
        if vpc_id is not None:
            pulumi.set(__self__, 'vpc_id', vpc_id)
        if vswitch_id is not None:
            pulumi.set(__self__, 'vswitch_id', vswitch_id)
        if zone_id is not None:
            pulumi.set(__self__, 'zone_id', zone_id)

    @property
    @pulumi.getter(name='accountPassword')
    def account_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        """
        return pulumi.get(self, 'account_password')

    @account_password.setter
    def account_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'account_password', value)

    @property
    @pulumi.getter(name='autoRenew')
    def auto_renew(self) -> Optional[pulumi.Input[bool]]:
        """
        Auto renew for prepaid, true of false. Default is false.
        > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        """
        return pulumi.get(self, 'auto_renew')

    @auto_renew.setter
    def auto_renew(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_renew', value)

    @property
    @pulumi.getter(name='backupPeriods')
    def backup_periods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        """
        return pulumi.get(self, 'backup_periods')

    @backup_periods.setter
    def backup_periods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'backup_periods', value)

    @property
    @pulumi.getter(name='backupTime')
    def backup_time(self) -> Optional[pulumi.Input[str]]:
        """
        MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        """
        return pulumi.get(self, 'backup_time')

    @backup_time.setter
    def backup_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'backup_time', value)

    @property
    @pulumi.getter(name='dbInstanceClass')
    def db_instance_class(self) -> Optional[pulumi.Input[str]]:
        """
        Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        """
        return pulumi.get(self, 'db_instance_class')

    @db_instance_class.setter
    def db_instance_class(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'db_instance_class', value)

    @property
    @pulumi.getter(name='dbInstanceStorage')
    def db_instance_storage(self) -> Optional[pulumi.Input[int]]:
        """
        User-defined DB instance storage space.Unit: GB. Value range:
        - Custom storage space.
        - 10-GB increments.
        """
        return pulumi.get(self, 'db_instance_storage')

    @db_instance_storage.setter
    def db_instance_storage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'db_instance_storage', value)

    @property
    @pulumi.getter(name='engineVersion')
    def engine_version(self) -> Optional[pulumi.Input[str]]:
        """
        Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        """
        return pulumi.get(self, 'engine_version')

    @engine_version.setter
    def engine_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'engine_version', value)

    @property
    @pulumi.getter(name='hiddenZoneId')
    def hidden_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        """
        return pulumi.get(self, 'hidden_zone_id')

    @hidden_zone_id.setter
    def hidden_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'hidden_zone_id', value)

    @property
    @pulumi.getter(name='instanceChargeType')
    def instance_charge_type(self) -> Optional[pulumi.Input[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        """
        return pulumi.get(self, 'instance_charge_type')

    @instance_charge_type.setter
    def instance_charge_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'instance_charge_type', value)

    @property
    @pulumi.getter(name='kmsEncryptedPassword')
    def kms_encrypted_password(self) -> Optional[pulumi.Input[str]]:
        """
        An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, 'kms_encrypted_password')

    @kms_encrypted_password.setter
    def kms_encrypted_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kms_encrypted_password', value)

    @property
    @pulumi.getter(name='kmsEncryptionContext')
    def kms_encryption_context(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, 'kms_encryption_context')

    @kms_encryption_context.setter
    def kms_encryption_context(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'kms_encryption_context', value)

    @property
    @pulumi.getter(name='maintainEndTime')
    def maintain_end_time(self) -> Optional[pulumi.Input[str]]:
        """
        The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_end_time')

    @maintain_end_time.setter
    def maintain_end_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'maintain_end_time', value)

    @property
    @pulumi.getter(name='maintainStartTime')
    def maintain_start_time(self) -> Optional[pulumi.Input[str]]:
        """
        The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_start_time')

    @maintain_start_time.setter
    def maintain_start_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'maintain_start_time', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of DB instance. It a string of 2 to 256 characters.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='networkType')
    def network_type(self) -> Optional[pulumi.Input[str]]:
        """
        The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        """
        return pulumi.get(self, 'network_type')

    @network_type.setter
    def network_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'network_type', value)

    @property
    @pulumi.getter(name='orderType')
    def order_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
        * UPGRADE: The specifications are upgraded.
        * DOWNGRADE: The specifications are downgraded.
        Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        """
        return pulumi.get(self, 'order_type')

    @order_type.setter
    def order_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'order_type', value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]:
        """
        Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        """
        return pulumi.get(self, 'parameters')

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceParameterArgs']]]]):
        pulumi.set(self, 'parameters', value)

    @property
    @pulumi.getter
    def period(self) -> Optional[pulumi.Input[int]]:
        """
        The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        """
        return pulumi.get(self, 'period')

    @period.setter
    def period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'period', value)

    @property
    @pulumi.getter(name='readonlyReplicas')
    def readonly_replicas(self) -> Optional[pulumi.Input[int]]:
        """
        The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        """
        return pulumi.get(self, 'readonly_replicas')

    @readonly_replicas.setter
    def readonly_replicas(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'readonly_replicas', value)

    @property
    @pulumi.getter(name='replicaSetName')
    def replica_set_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the mongo replica set
        """
        return pulumi.get(self, 'replica_set_name')

    @replica_set_name.setter
    def replica_set_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'replica_set_name', value)

    @property
    @pulumi.getter(name='replicaSets')
    def replica_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InstanceReplicaSetArgs']]]]:
        """
        Replica set instance information. The details see Block replica_sets. **NOTE:** Available in v1.140+.
        """
        return pulumi.get(self, 'replica_sets')

    @replica_sets.setter
    def replica_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InstanceReplicaSetArgs']]]]):
        pulumi.set(self, 'replica_sets', value)

    @property
    @pulumi.getter(name='replicationFactor')
    def replication_factor(self) -> Optional[pulumi.Input[int]]:
        """
        Number of replica set nodes. Valid values: [1, 3, 5, 7]
        """
        return pulumi.get(self, 'replication_factor')

    @replication_factor.setter
    def replication_factor(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'replication_factor', value)

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Resource Group.
        """
        return pulumi.get(self, 'resource_group_id')

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_id', value)

    @property
    @pulumi.getter(name='retentionPeriod')
    def retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        Instance log backup retention days. Available in 1.42.0+.
        """
        return pulumi.get(self, 'retention_period')

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'retention_period', value)

    @property
    @pulumi.getter(name='secondaryZoneId')
    def secondary_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        """
        return pulumi.get(self, 'secondary_zone_id')

    @secondary_zone_id.setter
    def secondary_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'secondary_zone_id', value)

    @property
    @pulumi.getter(name='securityGroupId')
    def security_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Security Group ID of ECS.
        """
        return pulumi.get(self, 'security_group_id')

    @security_group_id.setter
    def security_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'security_group_id', value)

    @property
    @pulumi.getter(name='securityIpLists')
    def security_ip_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        """
        return pulumi.get(self, 'security_ip_lists')

    @security_ip_lists.setter
    def security_ip_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'security_ip_lists', value)

    @property
    @pulumi.getter(name='sslAction')
    def ssl_action(self) -> Optional[pulumi.Input[str]]:
        """
        Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        """
        return pulumi.get(self, 'ssl_action')

    @ssl_action.setter
    def ssl_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ssl_action', value)

    @property
    @pulumi.getter(name='sslStatus')
    def ssl_status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the SSL feature. `Open`: SSL is turned on; `Closed`: SSL is turned off.
        """
        return pulumi.get(self, 'ssl_status')

    @ssl_status.setter
    def ssl_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ssl_status', value)

    @property
    @pulumi.getter(name='storageEngine')
    def storage_engine(self) -> Optional[pulumi.Input[str]]:
        """
        Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        """
        return pulumi.get(self, 'storage_engine')

    @storage_engine.setter
    def storage_engine(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'storage_engine', value)

    @property
    @pulumi.getter(name='storageType')
    def storage_type(self) -> Optional[pulumi.Input[str]]:
        """
        The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        """
        return pulumi.get(self, 'storage_type')

    @storage_type.setter
    def storage_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'storage_type', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='tdeStatus')
    def tde_status(self) -> Optional[pulumi.Input[str]]:
        """
        The TDE(Transparent Data Encryption) status.
        """
        return pulumi.get(self, 'tde_status')

    @tde_status.setter
    def tde_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tde_status', value)

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        """
        return pulumi.get(self, 'vpc_id')

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vpc_id', value)

    @property
    @pulumi.getter(name='vswitchId')
    def vswitch_id(self) -> Optional[pulumi.Input[str]]:
        """
        The virtual switch ID to launch DB instances in one VPC.
        """
        return pulumi.get(self, 'vswitch_id')

    @vswitch_id.setter
    def vswitch_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vswitch_id', value)

    @property
    @pulumi.getter(name='zoneId')
    def zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Zone to launch the DB instance. it supports multiple zone.
        If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
        The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        return pulumi.get(self, 'zone_id')

    @zone_id.setter
    def zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zone_id', value)

class Instance(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_password: Optional[pulumi.Input[str]]=None, auto_renew: Optional[pulumi.Input[bool]]=None, backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, backup_time: Optional[pulumi.Input[str]]=None, db_instance_class: Optional[pulumi.Input[str]]=None, db_instance_storage: Optional[pulumi.Input[int]]=None, engine_version: Optional[pulumi.Input[str]]=None, hidden_zone_id: Optional[pulumi.Input[str]]=None, instance_charge_type: Optional[pulumi.Input[str]]=None, kms_encrypted_password: Optional[pulumi.Input[str]]=None, kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]]=None, maintain_end_time: Optional[pulumi.Input[str]]=None, maintain_start_time: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_type: Optional[pulumi.Input[str]]=None, order_type: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceParameterArgs']]]]]=None, period: Optional[pulumi.Input[int]]=None, readonly_replicas: Optional[pulumi.Input[int]]=None, replication_factor: Optional[pulumi.Input[int]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, secondary_zone_id: Optional[pulumi.Input[str]]=None, security_group_id: Optional[pulumi.Input[str]]=None, security_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ssl_action: Optional[pulumi.Input[str]]=None, storage_engine: Optional[pulumi.Input[str]]=None, storage_type: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, tde_status: Optional[pulumi.Input[str]]=None, vpc_id: Optional[pulumi.Input[str]]=None, vswitch_id: Optional[pulumi.Input[str]]=None, zone_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Provides a MongoDB instance resource supports replica set instances only. the MongoDB provides stable, reliable, and automatic scalable database services.
        It offers a full range of database solutions, such as disaster recovery, backup, recovery, monitoring, and alarms.
        You can see detail product introduction [here](https://www.alibabacloud.com/help/doc-detail/26558.htm)

        > **NOTE:**  Available in 1.37.0+

        > **NOTE:**  The following regions don't support create Classic network MongoDB instance.
        [`cn-zhangjiakou`,`cn-huhehaote`,`ap-southeast-2`,`ap-southeast-3`,`ap-southeast-5`,`ap-south-1`,`me-east-1`,`ap-northeast-1`,`eu-west-1`]

        > **NOTE:**  Create MongoDB instance or change instance type and storage would cost 5~10 minutes. Please make full preparation

        ## Example Usage
        ### Create a Mongodb instance

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_zones = alicloud.get_zones(available_resource_creation="MongoDB")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/24",
            zone_id=default_zones.zones[0].id)
        example = alicloud.mongodb.Instance("example",
            engine_version="3.4",
            db_instance_class="dds.mongo.mid",
            db_instance_storage=10,
            vswitch_id=default_switch.id,
            security_ip_lists=[
                "10.168.1.12",
                "100.69.7.112",
            ])
        ```
        ## Module Support

        You can use to the existing mongodb module
        to create a MongoDB instance resource one-click.

        ## Import

        MongoDB can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:mongodb/instance:Instance example dds-bp1291daeda44194
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_password: Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        :param pulumi.Input[bool] auto_renew: Auto renew for prepaid, true of false. Default is false.
               > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_periods: MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        :param pulumi.Input[str] backup_time: MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        :param pulumi.Input[str] db_instance_class: Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        :param pulumi.Input[int] db_instance_storage: User-defined DB instance storage space.Unit: GB. Value range:
               - Custom storage space.
               - 10-GB increments.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        :param pulumi.Input[str] hidden_zone_id: Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[str] network_type: The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        :param pulumi.Input[str] order_type: The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
               * UPGRADE: The specifications are upgraded.
               * DOWNGRADE: The specifications are downgraded.
               Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceParameterArgs']]]] parameters: Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        :param pulumi.Input[int] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        :param pulumi.Input[int] readonly_replicas: The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        :param pulumi.Input[int] replication_factor: Number of replica set nodes. Valid values: [1, 3, 5, 7]
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group.
        :param pulumi.Input[str] secondary_zone_id: Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        :param pulumi.Input[str] security_group_id: The Security Group ID of ECS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_ip_lists: List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        :param pulumi.Input[str] ssl_action: Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        :param pulumi.Input[str] storage_engine: Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        :param pulumi.Input[str] storage_type: The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tde_status: The TDE(Transparent Data Encryption) status.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance. it supports multiple zone.
               If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
               The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: InstanceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a MongoDB instance resource supports replica set instances only. the MongoDB provides stable, reliable, and automatic scalable database services.
        It offers a full range of database solutions, such as disaster recovery, backup, recovery, monitoring, and alarms.
        You can see detail product introduction [here](https://www.alibabacloud.com/help/doc-detail/26558.htm)

        > **NOTE:**  Available in 1.37.0+

        > **NOTE:**  The following regions don't support create Classic network MongoDB instance.
        [`cn-zhangjiakou`,`cn-huhehaote`,`ap-southeast-2`,`ap-southeast-3`,`ap-southeast-5`,`ap-south-1`,`me-east-1`,`ap-northeast-1`,`eu-west-1`]

        > **NOTE:**  Create MongoDB instance or change instance type and storage would cost 5~10 minutes. Please make full preparation

        ## Example Usage
        ### Create a Mongodb instance

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default_zones = alicloud.get_zones(available_resource_creation="MongoDB")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/24",
            zone_id=default_zones.zones[0].id)
        example = alicloud.mongodb.Instance("example",
            engine_version="3.4",
            db_instance_class="dds.mongo.mid",
            db_instance_storage=10,
            vswitch_id=default_switch.id,
            security_ip_lists=[
                "10.168.1.12",
                "100.69.7.112",
            ])
        ```
        ## Module Support

        You can use to the existing mongodb module
        to create a MongoDB instance resource one-click.

        ## Import

        MongoDB can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:mongodb/instance:Instance example dds-bp1291daeda44194
        ```

        :param str resource_name: The name of the resource.
        :param InstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, account_password: Optional[pulumi.Input[str]]=None, auto_renew: Optional[pulumi.Input[bool]]=None, backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, backup_time: Optional[pulumi.Input[str]]=None, db_instance_class: Optional[pulumi.Input[str]]=None, db_instance_storage: Optional[pulumi.Input[int]]=None, engine_version: Optional[pulumi.Input[str]]=None, hidden_zone_id: Optional[pulumi.Input[str]]=None, instance_charge_type: Optional[pulumi.Input[str]]=None, kms_encrypted_password: Optional[pulumi.Input[str]]=None, kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]]=None, maintain_end_time: Optional[pulumi.Input[str]]=None, maintain_start_time: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_type: Optional[pulumi.Input[str]]=None, order_type: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceParameterArgs']]]]]=None, period: Optional[pulumi.Input[int]]=None, readonly_replicas: Optional[pulumi.Input[int]]=None, replication_factor: Optional[pulumi.Input[int]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, secondary_zone_id: Optional[pulumi.Input[str]]=None, security_group_id: Optional[pulumi.Input[str]]=None, security_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ssl_action: Optional[pulumi.Input[str]]=None, storage_engine: Optional[pulumi.Input[str]]=None, storage_type: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, tde_status: Optional[pulumi.Input[str]]=None, vpc_id: Optional[pulumi.Input[str]]=None, vswitch_id: Optional[pulumi.Input[str]]=None, zone_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceArgs.__new__(InstanceArgs)
            __props__.__dict__['account_password'] = None if account_password is None else pulumi.Output.secret(account_password)
            __props__.__dict__['auto_renew'] = auto_renew
            __props__.__dict__['backup_periods'] = backup_periods
            __props__.__dict__['backup_time'] = backup_time
            if db_instance_class is None and (not opts.urn):
                raise TypeError("Missing required property 'db_instance_class'")
            __props__.__dict__['db_instance_class'] = db_instance_class
            if db_instance_storage is None and (not opts.urn):
                raise TypeError("Missing required property 'db_instance_storage'")
            __props__.__dict__['db_instance_storage'] = db_instance_storage
            if engine_version is None and (not opts.urn):
                raise TypeError("Missing required property 'engine_version'")
            __props__.__dict__['engine_version'] = engine_version
            __props__.__dict__['hidden_zone_id'] = hidden_zone_id
            __props__.__dict__['instance_charge_type'] = instance_charge_type
            __props__.__dict__['kms_encrypted_password'] = kms_encrypted_password
            __props__.__dict__['kms_encryption_context'] = kms_encryption_context
            __props__.__dict__['maintain_end_time'] = maintain_end_time
            __props__.__dict__['maintain_start_time'] = maintain_start_time
            __props__.__dict__['name'] = name
            __props__.__dict__['network_type'] = network_type
            __props__.__dict__['order_type'] = order_type
            __props__.__dict__['parameters'] = parameters
            __props__.__dict__['period'] = period
            __props__.__dict__['readonly_replicas'] = readonly_replicas
            __props__.__dict__['replication_factor'] = replication_factor
            __props__.__dict__['resource_group_id'] = resource_group_id
            __props__.__dict__['secondary_zone_id'] = secondary_zone_id
            __props__.__dict__['security_group_id'] = security_group_id
            __props__.__dict__['security_ip_lists'] = security_ip_lists
            __props__.__dict__['ssl_action'] = ssl_action
            __props__.__dict__['storage_engine'] = storage_engine
            __props__.__dict__['storage_type'] = storage_type
            __props__.__dict__['tags'] = tags
            __props__.__dict__['tde_status'] = tde_status
            __props__.__dict__['vpc_id'] = vpc_id
            __props__.__dict__['vswitch_id'] = vswitch_id
            __props__.__dict__['zone_id'] = zone_id
            __props__.__dict__['replica_set_name'] = None
            __props__.__dict__['replica_sets'] = None
            __props__.__dict__['retention_period'] = None
            __props__.__dict__['ssl_status'] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=['accountPassword'])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Instance, __self__).__init__('alicloud:mongodb/instance:Instance', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, account_password: Optional[pulumi.Input[str]]=None, auto_renew: Optional[pulumi.Input[bool]]=None, backup_periods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, backup_time: Optional[pulumi.Input[str]]=None, db_instance_class: Optional[pulumi.Input[str]]=None, db_instance_storage: Optional[pulumi.Input[int]]=None, engine_version: Optional[pulumi.Input[str]]=None, hidden_zone_id: Optional[pulumi.Input[str]]=None, instance_charge_type: Optional[pulumi.Input[str]]=None, kms_encrypted_password: Optional[pulumi.Input[str]]=None, kms_encryption_context: Optional[pulumi.Input[Mapping[str, Any]]]=None, maintain_end_time: Optional[pulumi.Input[str]]=None, maintain_start_time: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, network_type: Optional[pulumi.Input[str]]=None, order_type: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceParameterArgs']]]]]=None, period: Optional[pulumi.Input[int]]=None, readonly_replicas: Optional[pulumi.Input[int]]=None, replica_set_name: Optional[pulumi.Input[str]]=None, replica_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceReplicaSetArgs']]]]]=None, replication_factor: Optional[pulumi.Input[int]]=None, resource_group_id: Optional[pulumi.Input[str]]=None, retention_period: Optional[pulumi.Input[int]]=None, secondary_zone_id: Optional[pulumi.Input[str]]=None, security_group_id: Optional[pulumi.Input[str]]=None, security_ip_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, ssl_action: Optional[pulumi.Input[str]]=None, ssl_status: Optional[pulumi.Input[str]]=None, storage_engine: Optional[pulumi.Input[str]]=None, storage_type: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, Any]]]=None, tde_status: Optional[pulumi.Input[str]]=None, vpc_id: Optional[pulumi.Input[str]]=None, vswitch_id: Optional[pulumi.Input[str]]=None, zone_id: Optional[pulumi.Input[str]]=None) -> 'Instance':
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_password: Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        :param pulumi.Input[bool] auto_renew: Auto renew for prepaid, true of false. Default is false.
               > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] backup_periods: MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        :param pulumi.Input[str] backup_time: MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        :param pulumi.Input[str] db_instance_class: Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        :param pulumi.Input[int] db_instance_storage: User-defined DB instance storage space.Unit: GB. Value range:
               - Custom storage space.
               - 10-GB increments.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        :param pulumi.Input[str] hidden_zone_id: Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        :param pulumi.Input[Mapping[str, Any]] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[str] network_type: The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        :param pulumi.Input[str] order_type: The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
               * UPGRADE: The specifications are upgraded.
               * DOWNGRADE: The specifications are downgraded.
               Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceParameterArgs']]]] parameters: Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        :param pulumi.Input[int] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        :param pulumi.Input[int] readonly_replicas: The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        :param pulumi.Input[str] replica_set_name: The name of the mongo replica set
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InstanceReplicaSetArgs']]]] replica_sets: Replica set instance information. The details see Block replica_sets. **NOTE:** Available in v1.140+.
        :param pulumi.Input[int] replication_factor: Number of replica set nodes. Valid values: [1, 3, 5, 7]
        :param pulumi.Input[str] resource_group_id: The ID of the Resource Group.
        :param pulumi.Input[int] retention_period: Instance log backup retention days. Available in 1.42.0+.
        :param pulumi.Input[str] secondary_zone_id: Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        :param pulumi.Input[str] security_group_id: The Security Group ID of ECS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_ip_lists: List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        :param pulumi.Input[str] ssl_action: Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        :param pulumi.Input[str] ssl_status: Status of the SSL feature. `Open`: SSL is turned on; `Closed`: SSL is turned off.
        :param pulumi.Input[str] storage_engine: Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        :param pulumi.Input[str] storage_type: The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] tde_status: The TDE(Transparent Data Encryption) status.
        :param pulumi.Input[str] vpc_id: The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance. it supports multiple zone.
               If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
               The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _InstanceState.__new__(_InstanceState)
        __props__.__dict__['account_password'] = account_password
        __props__.__dict__['auto_renew'] = auto_renew
        __props__.__dict__['backup_periods'] = backup_periods
        __props__.__dict__['backup_time'] = backup_time
        __props__.__dict__['db_instance_class'] = db_instance_class
        __props__.__dict__['db_instance_storage'] = db_instance_storage
        __props__.__dict__['engine_version'] = engine_version
        __props__.__dict__['hidden_zone_id'] = hidden_zone_id
        __props__.__dict__['instance_charge_type'] = instance_charge_type
        __props__.__dict__['kms_encrypted_password'] = kms_encrypted_password
        __props__.__dict__['kms_encryption_context'] = kms_encryption_context
        __props__.__dict__['maintain_end_time'] = maintain_end_time
        __props__.__dict__['maintain_start_time'] = maintain_start_time
        __props__.__dict__['name'] = name
        __props__.__dict__['network_type'] = network_type
        __props__.__dict__['order_type'] = order_type
        __props__.__dict__['parameters'] = parameters
        __props__.__dict__['period'] = period
        __props__.__dict__['readonly_replicas'] = readonly_replicas
        __props__.__dict__['replica_set_name'] = replica_set_name
        __props__.__dict__['replica_sets'] = replica_sets
        __props__.__dict__['replication_factor'] = replication_factor
        __props__.__dict__['resource_group_id'] = resource_group_id
        __props__.__dict__['retention_period'] = retention_period
        __props__.__dict__['secondary_zone_id'] = secondary_zone_id
        __props__.__dict__['security_group_id'] = security_group_id
        __props__.__dict__['security_ip_lists'] = security_ip_lists
        __props__.__dict__['ssl_action'] = ssl_action
        __props__.__dict__['ssl_status'] = ssl_status
        __props__.__dict__['storage_engine'] = storage_engine
        __props__.__dict__['storage_type'] = storage_type
        __props__.__dict__['tags'] = tags
        __props__.__dict__['tde_status'] = tde_status
        __props__.__dict__['vpc_id'] = vpc_id
        __props__.__dict__['vswitch_id'] = vswitch_id
        __props__.__dict__['zone_id'] = zone_id
        return Instance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='accountPassword')
    def account_password(self) -> pulumi.Output[Optional[str]]:
        """
        Password of the root account. It is a string of 6 to 32 characters and is composed of letters, numbers, and underlines.
        """
        return pulumi.get(self, 'account_password')

    @property
    @pulumi.getter(name='autoRenew')
    def auto_renew(self) -> pulumi.Output[Optional[bool]]:
        """
        Auto renew for prepaid, true of false. Default is false.
        > **NOTE:** The start time to the end time must be 1 hour. For example, the MaintainStartTime is 01:00Z, then the MaintainEndTime must be 02:00Z.
        """
        return pulumi.get(self, 'auto_renew')

    @property
    @pulumi.getter(name='backupPeriods')
    def backup_periods(self) -> pulumi.Output[Sequence[str]]:
        """
        MongoDB Instance backup period. It is required when `backup_time` was existed. Valid values: [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]. Default to [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
        """
        return pulumi.get(self, 'backup_periods')

    @property
    @pulumi.getter(name='backupTime')
    def backup_time(self) -> pulumi.Output[str]:
        """
        MongoDB instance backup time. It is required when `backup_period` was existed. In the format of HH:mmZ- HH:mmZ. Time setting interval is one hour. If not set, the system will return a default, like "23:00Z-24:00Z".
        """
        return pulumi.get(self, 'backup_time')

    @property
    @pulumi.getter(name='dbInstanceClass')
    def db_instance_class(self) -> pulumi.Output[str]:
        """
        Instance specification. see [Instance specifications](https://www.alibabacloud.com/help/doc-detail/57141.htm).
        """
        return pulumi.get(self, 'db_instance_class')

    @property
    @pulumi.getter(name='dbInstanceStorage')
    def db_instance_storage(self) -> pulumi.Output[int]:
        """
        User-defined DB instance storage space.Unit: GB. Value range:
        - Custom storage space.
        - 10-GB increments.
        """
        return pulumi.get(self, 'db_instance_storage')

    @property
    @pulumi.getter(name='engineVersion')
    def engine_version(self) -> pulumi.Output[str]:
        """
        Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/61763.htm) `EngineVersion`.
        """
        return pulumi.get(self, 'engine_version')

    @property
    @pulumi.getter(name='hiddenZoneId')
    def hidden_zone_id(self) -> pulumi.Output[Optional[str]]:
        """
        Configure the zone where the hidden node is located to deploy multiple zones. **NOTE:** This parameter value cannot be the same as `zone_id` and `secondary_zone_id` parameter values.
        """
        return pulumi.get(self, 'hidden_zone_id')

    @property
    @pulumi.getter(name='instanceChargeType')
    def instance_charge_type(self) -> pulumi.Output[Optional[str]]:
        """
        Valid values are `PrePaid`, `PostPaid`, System default to `PostPaid`. **NOTE:** It can be modified from `PostPaid` to `PrePaid` after version 1.63.0.
        """
        return pulumi.get(self, 'instance_charge_type')

    @property
    @pulumi.getter(name='kmsEncryptedPassword')
    def kms_encrypted_password(self) -> pulumi.Output[Optional[str]]:
        """
        An KMS encrypts password used to a instance. If the `account_password` is filled in, this field will be ignored.
        """
        return pulumi.get(self, 'kms_encrypted_password')

    @property
    @pulumi.getter(name='kmsEncryptionContext')
    def kms_encryption_context(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        """
        return pulumi.get(self, 'kms_encryption_context')

    @property
    @pulumi.getter(name='maintainEndTime')
    def maintain_end_time(self) -> pulumi.Output[str]:
        """
        The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_end_time')

    @property
    @pulumi.getter(name='maintainStartTime')
    def maintain_start_time(self) -> pulumi.Output[str]:
        """
        The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        """
        return pulumi.get(self, 'maintain_start_time')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of DB instance. It a string of 2 to 256 characters.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='networkType')
    def network_type(self) -> pulumi.Output[str]:
        """
        The network type of the instance. Valid values:`Classic` or `VPC`. Default value: `Classic`.
        """
        return pulumi.get(self, 'network_type')

    @property
    @pulumi.getter(name='orderType')
    def order_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of configuration changes performed. Default value: DOWNGRADE. Valid values:
        * UPGRADE: The specifications are upgraded.
        * DOWNGRADE: The specifications are downgraded.
        Note: This parameter is only applicable to instances when `instance_charge_type` is PrePaid.
        """
        return pulumi.get(self, 'order_type')

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Sequence['outputs.InstanceParameter']]:
        """
        Set of parameters needs to be set after mongodb instance was launched. See the following `Block parameters`.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter
    def period(self) -> pulumi.Output[int]:
        """
        The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. System default to 1.
        """
        return pulumi.get(self, 'period')

    @property
    @pulumi.getter(name='readonlyReplicas')
    def readonly_replicas(self) -> pulumi.Output[int]:
        """
        The number of read-only nodes in the replica set instance. Default value: 0. Valid values: 0 to 5.
        """
        return pulumi.get(self, 'readonly_replicas')

    @property
    @pulumi.getter(name='replicaSetName')
    def replica_set_name(self) -> pulumi.Output[str]:
        """
        The name of the mongo replica set
        """
        return pulumi.get(self, 'replica_set_name')

    @property
    @pulumi.getter(name='replicaSets')
    def replica_sets(self) -> pulumi.Output[Sequence['outputs.InstanceReplicaSet']]:
        """
        Replica set instance information. The details see Block replica_sets. **NOTE:** Available in v1.140+.
        """
        return pulumi.get(self, 'replica_sets')

    @property
    @pulumi.getter(name='replicationFactor')
    def replication_factor(self) -> pulumi.Output[int]:
        """
        Number of replica set nodes. Valid values: [1, 3, 5, 7]
        """
        return pulumi.get(self, 'replication_factor')

    @property
    @pulumi.getter(name='resourceGroupId')
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The ID of the Resource Group.
        """
        return pulumi.get(self, 'resource_group_id')

    @property
    @pulumi.getter(name='retentionPeriod')
    def retention_period(self) -> pulumi.Output[int]:
        """
        Instance log backup retention days. Available in 1.42.0+.
        """
        return pulumi.get(self, 'retention_period')

    @property
    @pulumi.getter(name='secondaryZoneId')
    def secondary_zone_id(self) -> pulumi.Output[Optional[str]]:
        """
        Configure the available area where the slave node (Secondary node) is located to realize multi-available area deployment. **NOTE:** This parameter value cannot be the same as `zone_id` and `hidden_zone_id` parameter values.
        """
        return pulumi.get(self, 'secondary_zone_id')

    @property
    @pulumi.getter(name='securityGroupId')
    def security_group_id(self) -> pulumi.Output[str]:
        """
        The Security Group ID of ECS.
        """
        return pulumi.get(self, 'security_group_id')

    @property
    @pulumi.getter(name='securityIpLists')
    def security_ip_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        List of IP addresses allowed to access all databases of an instance. The list contains up to 1,000 IP addresses, separated by commas. Supported formats include 0.0.0.0/0, 10.23.12.24 (IP), and 10.23.12.24/24 (Classless Inter-Domain Routing (CIDR) mode. /24 represents the length of the prefix in an IP address. The range of the prefix length is [1,32]).
        """
        return pulumi.get(self, 'security_ip_lists')

    @property
    @pulumi.getter(name='sslAction')
    def ssl_action(self) -> pulumi.Output[str]:
        """
        Actions performed on SSL functions, Valid values: `Open`: turn on SSL encryption; `Close`: turn off SSL encryption; `Update`: update SSL certificate.
        """
        return pulumi.get(self, 'ssl_action')

    @property
    @pulumi.getter(name='sslStatus')
    def ssl_status(self) -> pulumi.Output[str]:
        """
        Status of the SSL feature. `Open`: SSL is turned on; `Closed`: SSL is turned off.
        """
        return pulumi.get(self, 'ssl_status')

    @property
    @pulumi.getter(name='storageEngine')
    def storage_engine(self) -> pulumi.Output[str]:
        """
        Storage engine: WiredTiger or RocksDB. System Default value: WiredTiger.
        """
        return pulumi.get(self, 'storage_engine')

    @property
    @pulumi.getter(name='storageType')
    def storage_type(self) -> pulumi.Output[str]:
        """
        The storage type of the instance. Valid values: `cloud_essd1`, `cloud_essd2`, `cloud_essd3`, `local_ssd`.
        """
        return pulumi.get(self, 'storage_type')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='tdeStatus')
    def tde_status(self) -> pulumi.Output[Optional[str]]:
        """
        The TDE(Transparent Data Encryption) status.
        """
        return pulumi.get(self, 'tde_status')

    @property
    @pulumi.getter(name='vpcId')
    def vpc_id(self) -> pulumi.Output[str]:
        """
        The ID of the VPC. > **NOTE:** This parameter is valid only when NetworkType is set to VPC.
        """
        return pulumi.get(self, 'vpc_id')

    @property
    @pulumi.getter(name='vswitchId')
    def vswitch_id(self) -> pulumi.Output[str]:
        """
        The virtual switch ID to launch DB instances in one VPC.
        """
        return pulumi.get(self, 'vswitch_id')

    @property
    @pulumi.getter(name='zoneId')
    def zone_id(self) -> pulumi.Output[str]:
        """
        The Zone to launch the DB instance. it supports multiple zone.
        If it is a multi-zone and `vswitch_id` is specified, the vswitch must in one of them.
        The multiple zone ID can be retrieved by setting `multi` to "true" in the data source `get_zones`.
        """
        return pulumi.get(self, 'zone_id')
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['ProtectedFileShareArgs', 'ProtectedFileShare']

@pulumi.input_type
class ProtectedFileShareArgs:

    def __init__(__self__, *, backup_policy_id: pulumi.Input[str], recovery_vault_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], source_file_share_name: pulumi.Input[str], source_storage_account_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a ProtectedFileShare resource.
        :param pulumi.Input[str] backup_policy_id: Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_file_share_name: Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_storage_account_id: Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, 'backup_policy_id', backup_policy_id)
        pulumi.set(__self__, 'recovery_vault_name', recovery_vault_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'source_file_share_name', source_file_share_name)
        pulumi.set(__self__, 'source_storage_account_id', source_storage_account_id)

    @property
    @pulumi.getter(name='backupPolicyId')
    def backup_policy_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        """
        return pulumi.get(self, 'backup_policy_id')

    @backup_policy_id.setter
    def backup_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'backup_policy_id', value)

    @property
    @pulumi.getter(name='recoveryVaultName')
    def recovery_vault_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'recovery_vault_name')

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'recovery_vault_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='sourceFileShareName')
    def source_file_share_name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_file_share_name')

    @source_file_share_name.setter
    def source_file_share_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'source_file_share_name', value)

    @property
    @pulumi.getter(name='sourceStorageAccountId')
    def source_storage_account_id(self) -> pulumi.Input[str]:
        """
        Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_storage_account_id')

    @source_storage_account_id.setter
    def source_storage_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'source_storage_account_id', value)

@pulumi.input_type
class _ProtectedFileShareState:

    def __init__(__self__, *, backup_policy_id: Optional[pulumi.Input[str]]=None, recovery_vault_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, source_file_share_name: Optional[pulumi.Input[str]]=None, source_storage_account_id: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering ProtectedFileShare resources.
        :param pulumi.Input[str] backup_policy_id: Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_file_share_name: Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_storage_account_id: Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        if backup_policy_id is not None:
            pulumi.set(__self__, 'backup_policy_id', backup_policy_id)
        if recovery_vault_name is not None:
            pulumi.set(__self__, 'recovery_vault_name', recovery_vault_name)
        if resource_group_name is not None:
            pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if source_file_share_name is not None:
            pulumi.set(__self__, 'source_file_share_name', source_file_share_name)
        if source_storage_account_id is not None:
            pulumi.set(__self__, 'source_storage_account_id', source_storage_account_id)

    @property
    @pulumi.getter(name='backupPolicyId')
    def backup_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        """
        return pulumi.get(self, 'backup_policy_id')

    @backup_policy_id.setter
    def backup_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'backup_policy_id', value)

    @property
    @pulumi.getter(name='recoveryVaultName')
    def recovery_vault_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'recovery_vault_name')

    @recovery_vault_name.setter
    def recovery_vault_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'recovery_vault_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='sourceFileShareName')
    def source_file_share_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_file_share_name')

    @source_file_share_name.setter
    def source_file_share_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'source_file_share_name', value)

    @property
    @pulumi.getter(name='sourceStorageAccountId')
    def source_storage_account_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_storage_account_id')

    @source_storage_account_id.setter
    def source_storage_account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'source_storage_account_id', value)

class ProtectedFileShare(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, backup_policy_id: Optional[pulumi.Input[str]]=None, recovery_vault_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, source_file_share_name: Optional[pulumi.Input[str]]=None, source_storage_account_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Manages an Azure Backup Protected File Share to enable backups for file shares within an Azure Storage Account

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        vault = azure.recoveryservices.Vault("vault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard")
        sa = azure.storage.Account("sa",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            account_tier="Standard",
            account_replication_type="LRS")
        example_share = azure.storage.Share("exampleShare",
            storage_account_name=sa.name,
            quota=1)
        protection_container = azure.backup.ContainerStorageAccount("protection-container",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            storage_account_id=sa.id)
        example_policy_file_share = azure.backup.PolicyFileShare("examplePolicyFileShare",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            backup=azure.backup.PolicyFileShareBackupArgs(
                frequency="Daily",
                time="23:00",
            ),
            retention_daily=azure.backup.PolicyFileShareRetentionDailyArgs(
                count=10,
            ))
        share1 = azure.backup.ProtectedFileShare("share1",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            source_storage_account_id=protection_container.storage_account_id,
            source_file_share_name=example_share.name,
            backup_policy_id=example_policy_file_share.id)
        ```

        ## Import

        Azure Backup Protected File Shares can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:backup/protectedFileShare:ProtectedFileShare item1 "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.RecoveryServices/vaults/example-recovery-vault/backupFabrics/Azure/protectionContainers/StorageContainer;storage;group2;example-storage-account/protectedItems/AzureFileShare;3f6e3108a45793581bcbd1c61c87a3b2ceeb4ff4bc02a95ce9d1022b23722935"
        ```

         -> **NOTE** The ID requires quoting as there are semicolons. This user unfriendly ID can be found in the Deployments of the used resourcegroup, look for an Deployment which starts with `ConfigureAFSProtection-`, click then `Go to resource`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_file_share_name: Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_storage_account_id: Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ProtectedFileShareArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages an Azure Backup Protected File Share to enable backups for file shares within an Azure Storage Account

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        vault = azure.recoveryservices.Vault("vault",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku="Standard")
        sa = azure.storage.Account("sa",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            account_tier="Standard",
            account_replication_type="LRS")
        example_share = azure.storage.Share("exampleShare",
            storage_account_name=sa.name,
            quota=1)
        protection_container = azure.backup.ContainerStorageAccount("protection-container",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            storage_account_id=sa.id)
        example_policy_file_share = azure.backup.PolicyFileShare("examplePolicyFileShare",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            backup=azure.backup.PolicyFileShareBackupArgs(
                frequency="Daily",
                time="23:00",
            ),
            retention_daily=azure.backup.PolicyFileShareRetentionDailyArgs(
                count=10,
            ))
        share1 = azure.backup.ProtectedFileShare("share1",
            resource_group_name=example_resource_group.name,
            recovery_vault_name=vault.name,
            source_storage_account_id=protection_container.storage_account_id,
            source_file_share_name=example_share.name,
            backup_policy_id=example_policy_file_share.id)
        ```

        ## Import

        Azure Backup Protected File Shares can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:backup/protectedFileShare:ProtectedFileShare item1 "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/group1/providers/Microsoft.RecoveryServices/vaults/example-recovery-vault/backupFabrics/Azure/protectionContainers/StorageContainer;storage;group2;example-storage-account/protectedItems/AzureFileShare;3f6e3108a45793581bcbd1c61c87a3b2ceeb4ff4bc02a95ce9d1022b23722935"
        ```

         -> **NOTE** The ID requires quoting as there are semicolons. This user unfriendly ID can be found in the Deployments of the used resourcegroup, look for an Deployment which starts with `ConfigureAFSProtection-`, click then `Go to resource`.

        :param str resource_name: The name of the resource.
        :param ProtectedFileShareArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProtectedFileShareArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, backup_policy_id: Optional[pulumi.Input[str]]=None, recovery_vault_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, source_file_share_name: Optional[pulumi.Input[str]]=None, source_storage_account_id: Optional[pulumi.Input[str]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProtectedFileShareArgs.__new__(ProtectedFileShareArgs)
            if backup_policy_id is None and (not opts.urn):
                raise TypeError("Missing required property 'backup_policy_id'")
            __props__.__dict__['backup_policy_id'] = backup_policy_id
            if recovery_vault_name is None and (not opts.urn):
                raise TypeError("Missing required property 'recovery_vault_name'")
            __props__.__dict__['recovery_vault_name'] = recovery_vault_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if source_file_share_name is None and (not opts.urn):
                raise TypeError("Missing required property 'source_file_share_name'")
            __props__.__dict__['source_file_share_name'] = source_file_share_name
            if source_storage_account_id is None and (not opts.urn):
                raise TypeError("Missing required property 'source_storage_account_id'")
            __props__.__dict__['source_storage_account_id'] = source_storage_account_id
        super(ProtectedFileShare, __self__).__init__('azure:backup/protectedFileShare:ProtectedFileShare', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, backup_policy_id: Optional[pulumi.Input[str]]=None, recovery_vault_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, source_file_share_name: Optional[pulumi.Input[str]]=None, source_storage_account_id: Optional[pulumi.Input[str]]=None) -> 'ProtectedFileShare':
        """
        Get an existing ProtectedFileShare resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_policy_id: Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        :param pulumi.Input[str] recovery_vault_name: Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_file_share_name: Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_storage_account_id: Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ProtectedFileShareState.__new__(_ProtectedFileShareState)
        __props__.__dict__['backup_policy_id'] = backup_policy_id
        __props__.__dict__['recovery_vault_name'] = recovery_vault_name
        __props__.__dict__['resource_group_name'] = resource_group_name
        __props__.__dict__['source_file_share_name'] = source_file_share_name
        __props__.__dict__['source_storage_account_id'] = source_storage_account_id
        return ProtectedFileShare(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='backupPolicyId')
    def backup_policy_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the backup policy to use. The policy must be an Azure File Share backup policy. Other types are not supported.
        """
        return pulumi.get(self, 'backup_policy_id')

    @property
    @pulumi.getter(name='recoveryVaultName')
    def recovery_vault_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Recovery Services Vault to use. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'recovery_vault_name')

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the Azure Backup Protected File Share. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @property
    @pulumi.getter(name='sourceFileShareName')
    def source_file_share_name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_file_share_name')

    @property
    @pulumi.getter(name='sourceStorageAccountId')
    def source_storage_account_id(self) -> pulumi.Output[str]:
        """
        Specifies the ID of the storage account of the file share to backup. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'source_storage_account_id')
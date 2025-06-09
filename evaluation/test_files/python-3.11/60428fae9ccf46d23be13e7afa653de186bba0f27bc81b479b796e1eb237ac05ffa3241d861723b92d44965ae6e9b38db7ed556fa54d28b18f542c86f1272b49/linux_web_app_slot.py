import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['LinuxWebAppSlotArgs', 'LinuxWebAppSlot']

@pulumi.input_type
class LinuxWebAppSlotArgs:

    def __init__(__self__, *, app_service_id: pulumi.Input[str], site_config: pulumi.Input['LinuxWebAppSlotSiteConfigArgs'], app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]=None, backup: Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_mode: Optional[pulumi.Input[str]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]=None, name: Optional[pulumi.Input[str]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zip_deploy_file: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a LinuxWebAppSlot resource.
        :param pulumi.Input[str] app_service_id: The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input['LinuxWebAppSlotSiteConfigArgs'] site_config: A `site_config` block as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A map of key-value pairs of App Settings.
        :param pulumi.Input['LinuxWebAppSlotAuthSettingsArgs'] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input['LinuxWebAppSlotBackupArgs'] backup: A `backup` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should Client Affinity be enabled?
        :param pulumi.Input[bool] client_certificate_enabled: Should Client Certificates be enabled?
        :param pulumi.Input[str] client_certificate_mode: The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        :param pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]] connection_strings: One or more `connection_string` blocks as defined below.
        :param pulumi.Input[bool] enabled: Should the Linux Web App be enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Should the Linux Web App require HTTPS connections.
        :param pulumi.Input['LinuxWebAppSlotIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        :param pulumi.Input['LinuxWebAppSlotLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Linux Web App.
        :param pulumi.Input[str] zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        pulumi.set(__self__, 'app_service_id', app_service_id)
        pulumi.set(__self__, 'site_config', site_config)
        if app_settings is not None:
            pulumi.set(__self__, 'app_settings', app_settings)
        if auth_settings is not None:
            pulumi.set(__self__, 'auth_settings', auth_settings)
        if backup is not None:
            pulumi.set(__self__, 'backup', backup)
        if client_affinity_enabled is not None:
            pulumi.set(__self__, 'client_affinity_enabled', client_affinity_enabled)
        if client_certificate_enabled is not None:
            pulumi.set(__self__, 'client_certificate_enabled', client_certificate_enabled)
        if client_certificate_mode is not None:
            pulumi.set(__self__, 'client_certificate_mode', client_certificate_mode)
        if connection_strings is not None:
            pulumi.set(__self__, 'connection_strings', connection_strings)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if key_vault_reference_identity_id is not None:
            pulumi.set(__self__, 'key_vault_reference_identity_id', key_vault_reference_identity_id)
        if logs is not None:
            pulumi.set(__self__, 'logs', logs)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if storage_accounts is not None:
            pulumi.set(__self__, 'storage_accounts', storage_accounts)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zip_deploy_file is not None:
            pulumi.set(__self__, 'zip_deploy_file', zip_deploy_file)

    @property
    @pulumi.getter(name='appServiceId')
    def app_service_id(self) -> pulumi.Input[str]:
        """
        The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'app_service_id')

    @app_service_id.setter
    def app_service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'app_service_id', value)

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> pulumi.Input['LinuxWebAppSlotSiteConfigArgs']:
        """
        A `site_config` block as defined below.
        """
        return pulumi.get(self, 'site_config')

    @site_config.setter
    def site_config(self, value: pulumi.Input['LinuxWebAppSlotSiteConfigArgs']):
        pulumi.set(self, 'site_config', value)

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of key-value pairs of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @app_settings.setter
    def app_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'app_settings', value)

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @auth_settings.setter
    def auth_settings(self, value: Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]):
        pulumi.set(self, 'auth_settings', value)

    @property
    @pulumi.getter
    def backup(self) -> Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]:
        """
        A `backup` block as defined below.
        """
        return pulumi.get(self, 'backup')

    @backup.setter
    def backup(self, value: Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]):
        pulumi.set(self, 'backup', value)

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Client Affinity be enabled?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @client_affinity_enabled.setter
    def client_affinity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_affinity_enabled', value)

    @property
    @pulumi.getter(name='clientCertificateEnabled')
    def client_certificate_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Client Certificates be enabled?
        """
        return pulumi.get(self, 'client_certificate_enabled')

    @client_certificate_enabled.setter
    def client_certificate_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_certificate_enabled', value)

    @property
    @pulumi.getter(name='clientCertificateMode')
    def client_certificate_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        """
        return pulumi.get(self, 'client_certificate_mode')

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'client_certificate_mode', value)

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]:
        """
        One or more `connection_string` blocks as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @connection_strings.setter
    def connection_strings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]):
        pulumi.set(self, 'connection_strings', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Linux Web App be enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Linux Web App require HTTPS connections.
        """
        return pulumi.get(self, 'https_only')

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'https_only', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_reference_identity_id', value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]):
        pulumi.set(self, 'logs', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]):
        pulumi.set(self, 'storage_accounts', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Linux Web App.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='zipDeployFile')
    def zip_deploy_file(self) -> Optional[pulumi.Input[str]]:
        """
        The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        return pulumi.get(self, 'zip_deploy_file')

    @zip_deploy_file.setter
    def zip_deploy_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zip_deploy_file', value)

@pulumi.input_type
class _LinuxWebAppSlotState:

    def __init__(__self__, *, app_metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, app_service_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]=None, backup: Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_mode: Optional[pulumi.Input[str]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]=None, custom_domain_verification_id: Optional[pulumi.Input[str]]=None, default_hostname: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]=None, name: Optional[pulumi.Input[str]]=None, outbound_ip_address_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, outbound_ip_addresses: Optional[pulumi.Input[str]]=None, possible_outbound_ip_address_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, possible_outbound_ip_addresses: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input['LinuxWebAppSlotSiteConfigArgs']]=None, site_credentials: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotSiteCredentialArgs']]]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zip_deploy_file: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering LinuxWebAppSlot resources.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_metadata: A `app_metadata` block as defined below.
        :param pulumi.Input[str] app_service_id: The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A map of key-value pairs of App Settings.
        :param pulumi.Input['LinuxWebAppSlotAuthSettingsArgs'] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input['LinuxWebAppSlotBackupArgs'] backup: A `backup` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should Client Affinity be enabled?
        :param pulumi.Input[bool] client_certificate_enabled: Should Client Certificates be enabled?
        :param pulumi.Input[str] client_certificate_mode: The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        :param pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]] connection_strings: One or more `connection_string` blocks as defined below.
        :param pulumi.Input[str] custom_domain_verification_id: The identifier used by App Service to perform domain ownership verification via DNS TXT record.
        :param pulumi.Input[str] default_hostname: The default hostname of the Linux Web App.
        :param pulumi.Input[bool] enabled: Should the Linux Web App be enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Should the Linux Web App require HTTPS connections.
        :param pulumi.Input['LinuxWebAppSlotIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        :param pulumi.Input[str] kind: The Kind value for this Linux Web App.
        :param pulumi.Input['LinuxWebAppSlotLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] outbound_ip_address_lists: A list of outbound IP addresses - such as `["52.23.25.3", "52.143.43.12"]`
        :param pulumi.Input[str] outbound_ip_addresses: A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] possible_outbound_ip_address_lists: A `possible_outbound_ip_address_list` block as defined below.
        :param pulumi.Input[str] possible_outbound_ip_addresses: A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12,52.143.43.17` - not all of which are necessarily in use. Superset of `outbound_ip_addresses`.
        :param pulumi.Input['LinuxWebAppSlotSiteConfigArgs'] site_config: A `site_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotSiteCredentialArgs']]] site_credentials: A `site_credential` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Linux Web App.
        :param pulumi.Input[str] zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        if app_metadata is not None:
            pulumi.set(__self__, 'app_metadata', app_metadata)
        if app_service_id is not None:
            pulumi.set(__self__, 'app_service_id', app_service_id)
        if app_settings is not None:
            pulumi.set(__self__, 'app_settings', app_settings)
        if auth_settings is not None:
            pulumi.set(__self__, 'auth_settings', auth_settings)
        if backup is not None:
            pulumi.set(__self__, 'backup', backup)
        if client_affinity_enabled is not None:
            pulumi.set(__self__, 'client_affinity_enabled', client_affinity_enabled)
        if client_certificate_enabled is not None:
            pulumi.set(__self__, 'client_certificate_enabled', client_certificate_enabled)
        if client_certificate_mode is not None:
            pulumi.set(__self__, 'client_certificate_mode', client_certificate_mode)
        if connection_strings is not None:
            pulumi.set(__self__, 'connection_strings', connection_strings)
        if custom_domain_verification_id is not None:
            pulumi.set(__self__, 'custom_domain_verification_id', custom_domain_verification_id)
        if default_hostname is not None:
            pulumi.set(__self__, 'default_hostname', default_hostname)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if key_vault_reference_identity_id is not None:
            pulumi.set(__self__, 'key_vault_reference_identity_id', key_vault_reference_identity_id)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if logs is not None:
            pulumi.set(__self__, 'logs', logs)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if outbound_ip_address_lists is not None:
            pulumi.set(__self__, 'outbound_ip_address_lists', outbound_ip_address_lists)
        if outbound_ip_addresses is not None:
            pulumi.set(__self__, 'outbound_ip_addresses', outbound_ip_addresses)
        if possible_outbound_ip_address_lists is not None:
            pulumi.set(__self__, 'possible_outbound_ip_address_lists', possible_outbound_ip_address_lists)
        if possible_outbound_ip_addresses is not None:
            pulumi.set(__self__, 'possible_outbound_ip_addresses', possible_outbound_ip_addresses)
        if site_config is not None:
            pulumi.set(__self__, 'site_config', site_config)
        if site_credentials is not None:
            pulumi.set(__self__, 'site_credentials', site_credentials)
        if storage_accounts is not None:
            pulumi.set(__self__, 'storage_accounts', storage_accounts)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zip_deploy_file is not None:
            pulumi.set(__self__, 'zip_deploy_file', zip_deploy_file)

    @property
    @pulumi.getter(name='appMetadata')
    def app_metadata(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A `app_metadata` block as defined below.
        """
        return pulumi.get(self, 'app_metadata')

    @app_metadata.setter
    def app_metadata(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'app_metadata', value)

    @property
    @pulumi.getter(name='appServiceId')
    def app_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'app_service_id')

    @app_service_id.setter
    def app_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'app_service_id', value)

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of key-value pairs of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @app_settings.setter
    def app_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'app_settings', value)

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @auth_settings.setter
    def auth_settings(self, value: Optional[pulumi.Input['LinuxWebAppSlotAuthSettingsArgs']]):
        pulumi.set(self, 'auth_settings', value)

    @property
    @pulumi.getter
    def backup(self) -> Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]:
        """
        A `backup` block as defined below.
        """
        return pulumi.get(self, 'backup')

    @backup.setter
    def backup(self, value: Optional[pulumi.Input['LinuxWebAppSlotBackupArgs']]):
        pulumi.set(self, 'backup', value)

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Client Affinity be enabled?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @client_affinity_enabled.setter
    def client_affinity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_affinity_enabled', value)

    @property
    @pulumi.getter(name='clientCertificateEnabled')
    def client_certificate_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should Client Certificates be enabled?
        """
        return pulumi.get(self, 'client_certificate_enabled')

    @client_certificate_enabled.setter
    def client_certificate_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_certificate_enabled', value)

    @property
    @pulumi.getter(name='clientCertificateMode')
    def client_certificate_mode(self) -> Optional[pulumi.Input[str]]:
        """
        The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        """
        return pulumi.get(self, 'client_certificate_mode')

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'client_certificate_mode', value)

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]:
        """
        One or more `connection_string` blocks as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @connection_strings.setter
    def connection_strings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotConnectionStringArgs']]]]):
        pulumi.set(self, 'connection_strings', value)

    @property
    @pulumi.getter(name='customDomainVerificationId')
    def custom_domain_verification_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier used by App Service to perform domain ownership verification via DNS TXT record.
        """
        return pulumi.get(self, 'custom_domain_verification_id')

    @custom_domain_verification_id.setter
    def custom_domain_verification_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'custom_domain_verification_id', value)

    @property
    @pulumi.getter(name='defaultHostname')
    def default_hostname(self) -> Optional[pulumi.Input[str]]:
        """
        The default hostname of the Linux Web App.
        """
        return pulumi.get(self, 'default_hostname')

    @default_hostname.setter
    def default_hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_hostname', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Linux Web App be enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the Linux Web App require HTTPS connections.
        """
        return pulumi.get(self, 'https_only')

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'https_only', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['LinuxWebAppSlotIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_reference_identity_id', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        The Kind value for this Linux Web App.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['LinuxWebAppSlotLogsArgs']]):
        pulumi.set(self, 'logs', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='outboundIpAddressLists')
    def outbound_ip_address_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of outbound IP addresses - such as `["52.23.25.3", "52.143.43.12"]`
        """
        return pulumi.get(self, 'outbound_ip_address_lists')

    @outbound_ip_address_lists.setter
    def outbound_ip_address_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'outbound_ip_address_lists', value)

    @property
    @pulumi.getter(name='outboundIpAddresses')
    def outbound_ip_addresses(self) -> Optional[pulumi.Input[str]]:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12`.
        """
        return pulumi.get(self, 'outbound_ip_addresses')

    @outbound_ip_addresses.setter
    def outbound_ip_addresses(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'outbound_ip_addresses', value)

    @property
    @pulumi.getter(name='possibleOutboundIpAddressLists')
    def possible_outbound_ip_address_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A `possible_outbound_ip_address_list` block as defined below.
        """
        return pulumi.get(self, 'possible_outbound_ip_address_lists')

    @possible_outbound_ip_address_lists.setter
    def possible_outbound_ip_address_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'possible_outbound_ip_address_lists', value)

    @property
    @pulumi.getter(name='possibleOutboundIpAddresses')
    def possible_outbound_ip_addresses(self) -> Optional[pulumi.Input[str]]:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12,52.143.43.17` - not all of which are necessarily in use. Superset of `outbound_ip_addresses`.
        """
        return pulumi.get(self, 'possible_outbound_ip_addresses')

    @possible_outbound_ip_addresses.setter
    def possible_outbound_ip_addresses(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'possible_outbound_ip_addresses', value)

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> Optional[pulumi.Input['LinuxWebAppSlotSiteConfigArgs']]:
        """
        A `site_config` block as defined below.
        """
        return pulumi.get(self, 'site_config')

    @site_config.setter
    def site_config(self, value: Optional[pulumi.Input['LinuxWebAppSlotSiteConfigArgs']]):
        pulumi.set(self, 'site_config', value)

    @property
    @pulumi.getter(name='siteCredentials')
    def site_credentials(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotSiteCredentialArgs']]]]:
        """
        A `site_credential` block as defined below.
        """
        return pulumi.get(self, 'site_credentials')

    @site_credentials.setter
    def site_credentials(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotSiteCredentialArgs']]]]):
        pulumi.set(self, 'site_credentials', value)

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LinuxWebAppSlotStorageAccountArgs']]]]):
        pulumi.set(self, 'storage_accounts', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags which should be assigned to the Linux Web App.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='zipDeployFile')
    def zip_deploy_file(self) -> Optional[pulumi.Input[str]]:
        """
        The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        return pulumi.get(self, 'zip_deploy_file')

    @zip_deploy_file.setter
    def zip_deploy_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'zip_deploy_file', value)

class LinuxWebAppSlot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_service_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotAuthSettingsArgs']]]=None, backup: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotBackupArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_mode: Optional[pulumi.Input[str]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotConnectionStringArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteConfigArgs']]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zip_deploy_file: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Manages a Linux Web App Slot.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service_plan = azure.appservice.ServicePlan("exampleServicePlan",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            os_type="Linux",
            sku_name="P1v2")
        example_linux_web_app = azure.appservice.LinuxWebApp("exampleLinuxWebApp",
            resource_group_name=example_resource_group.name,
            location=example_service_plan.location,
            service_plan_id=example_service_plan.id,
            site_config=azure.appservice.LinuxWebAppSiteConfigArgs())
        example_linux_web_app_slot = azure.appservice.LinuxWebAppSlot("exampleLinuxWebAppSlot",
            app_service_id=example_linux_web_app.id,
            site_config=azure.appservice.LinuxWebAppSlotSiteConfigArgs())
        ```

        ## Import

        Linux Web Apps can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/linuxWebAppSlot:LinuxWebAppSlot example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/resGroup1/providers/Microsoft.Web/sites/site1/slots/slot1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_service_id: The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A map of key-value pairs of App Settings.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotAuthSettingsArgs']] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotBackupArgs']] backup: A `backup` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should Client Affinity be enabled?
        :param pulumi.Input[bool] client_certificate_enabled: Should Client Certificates be enabled?
        :param pulumi.Input[str] client_certificate_mode: The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotConnectionStringArgs']]]] connection_strings: One or more `connection_string` blocks as defined below.
        :param pulumi.Input[bool] enabled: Should the Linux Web App be enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Should the Linux Web App require HTTPS connections.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotLogsArgs']] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteConfigArgs']] site_config: A `site_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotStorageAccountArgs']]]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Linux Web App.
        :param pulumi.Input[str] zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: LinuxWebAppSlotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages a Linux Web App Slot.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service_plan = azure.appservice.ServicePlan("exampleServicePlan",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            os_type="Linux",
            sku_name="P1v2")
        example_linux_web_app = azure.appservice.LinuxWebApp("exampleLinuxWebApp",
            resource_group_name=example_resource_group.name,
            location=example_service_plan.location,
            service_plan_id=example_service_plan.id,
            site_config=azure.appservice.LinuxWebAppSiteConfigArgs())
        example_linux_web_app_slot = azure.appservice.LinuxWebAppSlot("exampleLinuxWebAppSlot",
            app_service_id=example_linux_web_app.id,
            site_config=azure.appservice.LinuxWebAppSlotSiteConfigArgs())
        ```

        ## Import

        Linux Web Apps can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/linuxWebAppSlot:LinuxWebAppSlot example /subscriptions/12345678-1234-9876-4563-123456789012/resourceGroups/resGroup1/providers/Microsoft.Web/sites/site1/slots/slot1
        ```

        :param str resource_name: The name of the resource.
        :param LinuxWebAppSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LinuxWebAppSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_service_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotAuthSettingsArgs']]]=None, backup: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotBackupArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_mode: Optional[pulumi.Input[str]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotConnectionStringArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteConfigArgs']]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zip_deploy_file: Optional[pulumi.Input[str]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LinuxWebAppSlotArgs.__new__(LinuxWebAppSlotArgs)
            if app_service_id is None and (not opts.urn):
                raise TypeError("Missing required property 'app_service_id'")
            __props__.__dict__['app_service_id'] = app_service_id
            __props__.__dict__['app_settings'] = app_settings
            __props__.__dict__['auth_settings'] = auth_settings
            __props__.__dict__['backup'] = backup
            __props__.__dict__['client_affinity_enabled'] = client_affinity_enabled
            __props__.__dict__['client_certificate_enabled'] = client_certificate_enabled
            __props__.__dict__['client_certificate_mode'] = client_certificate_mode
            __props__.__dict__['connection_strings'] = connection_strings
            __props__.__dict__['enabled'] = enabled
            __props__.__dict__['https_only'] = https_only
            __props__.__dict__['identity'] = identity
            __props__.__dict__['key_vault_reference_identity_id'] = key_vault_reference_identity_id
            __props__.__dict__['logs'] = logs
            __props__.__dict__['name'] = name
            if site_config is None and (not opts.urn):
                raise TypeError("Missing required property 'site_config'")
            __props__.__dict__['site_config'] = site_config
            __props__.__dict__['storage_accounts'] = storage_accounts
            __props__.__dict__['tags'] = tags
            __props__.__dict__['zip_deploy_file'] = zip_deploy_file
            __props__.__dict__['app_metadata'] = None
            __props__.__dict__['custom_domain_verification_id'] = None
            __props__.__dict__['default_hostname'] = None
            __props__.__dict__['kind'] = None
            __props__.__dict__['outbound_ip_address_lists'] = None
            __props__.__dict__['outbound_ip_addresses'] = None
            __props__.__dict__['possible_outbound_ip_address_lists'] = None
            __props__.__dict__['possible_outbound_ip_addresses'] = None
            __props__.__dict__['site_credentials'] = None
        super(LinuxWebAppSlot, __self__).__init__('azure:appservice/linuxWebAppSlot:LinuxWebAppSlot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, app_metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, app_service_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotAuthSettingsArgs']]]=None, backup: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotBackupArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_enabled: Optional[pulumi.Input[bool]]=None, client_certificate_mode: Optional[pulumi.Input[str]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotConnectionStringArgs']]]]]=None, custom_domain_verification_id: Optional[pulumi.Input[str]]=None, default_hostname: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, outbound_ip_address_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, outbound_ip_addresses: Optional[pulumi.Input[str]]=None, possible_outbound_ip_address_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, possible_outbound_ip_addresses: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteConfigArgs']]]=None, site_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteCredentialArgs']]]]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zip_deploy_file: Optional[pulumi.Input[str]]=None) -> 'LinuxWebAppSlot':
        """
        Get an existing LinuxWebAppSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_metadata: A `app_metadata` block as defined below.
        :param pulumi.Input[str] app_service_id: The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A map of key-value pairs of App Settings.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotAuthSettingsArgs']] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotBackupArgs']] backup: A `backup` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should Client Affinity be enabled?
        :param pulumi.Input[bool] client_certificate_enabled: Should Client Certificates be enabled?
        :param pulumi.Input[str] client_certificate_mode: The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotConnectionStringArgs']]]] connection_strings: One or more `connection_string` blocks as defined below.
        :param pulumi.Input[str] custom_domain_verification_id: The identifier used by App Service to perform domain ownership verification via DNS TXT record.
        :param pulumi.Input[str] default_hostname: The default hostname of the Linux Web App.
        :param pulumi.Input[bool] enabled: Should the Linux Web App be enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Should the Linux Web App require HTTPS connections.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        :param pulumi.Input[str] kind: The Kind value for this Linux Web App.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotLogsArgs']] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] outbound_ip_address_lists: A list of outbound IP addresses - such as `["52.23.25.3", "52.143.43.12"]`
        :param pulumi.Input[str] outbound_ip_addresses: A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] possible_outbound_ip_address_lists: A `possible_outbound_ip_address_list` block as defined below.
        :param pulumi.Input[str] possible_outbound_ip_addresses: A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12,52.143.43.17` - not all of which are necessarily in use. Superset of `outbound_ip_addresses`.
        :param pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteConfigArgs']] site_config: A `site_config` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotSiteCredentialArgs']]]] site_credentials: A `site_credential` block as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LinuxWebAppSlotStorageAccountArgs']]]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags which should be assigned to the Linux Web App.
        :param pulumi.Input[str] zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _LinuxWebAppSlotState.__new__(_LinuxWebAppSlotState)
        __props__.__dict__['app_metadata'] = app_metadata
        __props__.__dict__['app_service_id'] = app_service_id
        __props__.__dict__['app_settings'] = app_settings
        __props__.__dict__['auth_settings'] = auth_settings
        __props__.__dict__['backup'] = backup
        __props__.__dict__['client_affinity_enabled'] = client_affinity_enabled
        __props__.__dict__['client_certificate_enabled'] = client_certificate_enabled
        __props__.__dict__['client_certificate_mode'] = client_certificate_mode
        __props__.__dict__['connection_strings'] = connection_strings
        __props__.__dict__['custom_domain_verification_id'] = custom_domain_verification_id
        __props__.__dict__['default_hostname'] = default_hostname
        __props__.__dict__['enabled'] = enabled
        __props__.__dict__['https_only'] = https_only
        __props__.__dict__['identity'] = identity
        __props__.__dict__['key_vault_reference_identity_id'] = key_vault_reference_identity_id
        __props__.__dict__['kind'] = kind
        __props__.__dict__['logs'] = logs
        __props__.__dict__['name'] = name
        __props__.__dict__['outbound_ip_address_lists'] = outbound_ip_address_lists
        __props__.__dict__['outbound_ip_addresses'] = outbound_ip_addresses
        __props__.__dict__['possible_outbound_ip_address_lists'] = possible_outbound_ip_address_lists
        __props__.__dict__['possible_outbound_ip_addresses'] = possible_outbound_ip_addresses
        __props__.__dict__['site_config'] = site_config
        __props__.__dict__['site_credentials'] = site_credentials
        __props__.__dict__['storage_accounts'] = storage_accounts
        __props__.__dict__['tags'] = tags
        __props__.__dict__['zip_deploy_file'] = zip_deploy_file
        return LinuxWebAppSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='appMetadata')
    def app_metadata(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A `app_metadata` block as defined below.
        """
        return pulumi.get(self, 'app_metadata')

    @property
    @pulumi.getter(name='appServiceId')
    def app_service_id(self) -> pulumi.Output[str]:
        """
        The ID of the Linux Web App this Deployment Slot will be part of. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'app_service_id')

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of key-value pairs of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> pulumi.Output['outputs.LinuxWebAppSlotAuthSettings']:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @property
    @pulumi.getter
    def backup(self) -> pulumi.Output[Optional['outputs.LinuxWebAppSlotBackup']]:
        """
        A `backup` block as defined below.
        """
        return pulumi.get(self, 'backup')

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Should Client Affinity be enabled?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @property
    @pulumi.getter(name='clientCertificateEnabled')
    def client_certificate_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Should Client Certificates be enabled?
        """
        return pulumi.get(self, 'client_certificate_enabled')

    @property
    @pulumi.getter(name='clientCertificateMode')
    def client_certificate_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The Client Certificate mode. Possible values include `Optional` and `Required`. This property has no effect when `client_cert_enabled` is `false`
        """
        return pulumi.get(self, 'client_certificate_mode')

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> pulumi.Output[Optional[Sequence['outputs.LinuxWebAppSlotConnectionString']]]:
        """
        One or more `connection_string` blocks as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @property
    @pulumi.getter(name='customDomainVerificationId')
    def custom_domain_verification_id(self) -> pulumi.Output[str]:
        """
        The identifier used by App Service to perform domain ownership verification via DNS TXT record.
        """
        return pulumi.get(self, 'custom_domain_verification_id')

    @property
    @pulumi.getter(name='defaultHostname')
    def default_hostname(self) -> pulumi.Output[str]:
        """
        The default hostname of the Linux Web App.
        """
        return pulumi.get(self, 'default_hostname')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Linux Web App be enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Linux Web App require HTTPS connections.
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.LinuxWebAppSlotIdentity']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> pulumi.Output[str]:
        """
        The User Assigned Identity ID used for accessing KeyVault secrets. The identity must be assigned to the application in the `identity` block. [For more information see - Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity)
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The Kind value for this Linux Web App.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Output[Optional['outputs.LinuxWebAppSlotLogs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name which should be used for this Linux Web App. Changing this forces a new Linux Web App to be created.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='outboundIpAddressLists')
    def outbound_ip_address_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of outbound IP addresses - such as `["52.23.25.3", "52.143.43.12"]`
        """
        return pulumi.get(self, 'outbound_ip_address_lists')

    @property
    @pulumi.getter(name='outboundIpAddresses')
    def outbound_ip_addresses(self) -> pulumi.Output[str]:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12`.
        """
        return pulumi.get(self, 'outbound_ip_addresses')

    @property
    @pulumi.getter(name='possibleOutboundIpAddressLists')
    def possible_outbound_ip_address_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        A `possible_outbound_ip_address_list` block as defined below.
        """
        return pulumi.get(self, 'possible_outbound_ip_address_lists')

    @property
    @pulumi.getter(name='possibleOutboundIpAddresses')
    def possible_outbound_ip_addresses(self) -> pulumi.Output[str]:
        """
        A comma separated list of outbound IP addresses - such as `52.23.25.3,52.143.43.12,52.143.43.17` - not all of which are necessarily in use. Superset of `outbound_ip_addresses`.
        """
        return pulumi.get(self, 'possible_outbound_ip_addresses')

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> pulumi.Output['outputs.LinuxWebAppSlotSiteConfig']:
        """
        A `site_config` block as defined below.
        """
        return pulumi.get(self, 'site_config')

    @property
    @pulumi.getter(name='siteCredentials')
    def site_credentials(self) -> pulumi.Output[Sequence['outputs.LinuxWebAppSlotSiteCredential']]:
        """
        A `site_credential` block as defined below.
        """
        return pulumi.get(self, 'site_credentials')

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> pulumi.Output[Optional[Sequence['outputs.LinuxWebAppSlotStorageAccount']]]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags which should be assigned to the Linux Web App.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='zipDeployFile')
    def zip_deploy_file(self) -> pulumi.Output[str]:
        """
        The local path and filename of the Zip packaged application to deploy to this Windows Web App.
        """
        return pulumi.get(self, 'zip_deploy_file')
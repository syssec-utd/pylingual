import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['SlotArgs', 'Slot']

@pulumi.input_type
class SlotArgs:

    def __init__(__self__, *, app_service_name: pulumi.Input[str], app_service_plan_id: pulumi.Input[str], resource_group_name: pulumi.Input[str], app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input['SlotAuthSettingsArgs']]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['SlotIdentityArgs']]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input['SlotLogsArgs']]=None, name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input['SlotSiteConfigArgs']]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Slot resource.
        :param pulumi.Input[str] app_service_name: The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        :param pulumi.Input[str] app_service_plan_id: The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A key-value pair of App Settings.
        :param pulumi.Input['SlotAuthSettingsArgs'] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        :param pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]] connection_strings: An `connection_string` block as defined below.
        :param pulumi.Input[bool] enabled: Is the App Service Slot Enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        :param pulumi.Input['SlotIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input['SlotLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input['SlotSiteConfigArgs'] site_config: A `site_config` object as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        pulumi.set(__self__, 'app_service_name', app_service_name)
        pulumi.set(__self__, 'app_service_plan_id', app_service_plan_id)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if app_settings is not None:
            pulumi.set(__self__, 'app_settings', app_settings)
        if auth_settings is not None:
            pulumi.set(__self__, 'auth_settings', auth_settings)
        if client_affinity_enabled is not None:
            pulumi.set(__self__, 'client_affinity_enabled', client_affinity_enabled)
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
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if logs is not None:
            pulumi.set(__self__, 'logs', logs)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if site_config is not None:
            pulumi.set(__self__, 'site_config', site_config)
        if storage_accounts is not None:
            pulumi.set(__self__, 'storage_accounts', storage_accounts)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='appServiceName')
    def app_service_name(self) -> pulumi.Input[str]:
        """
        The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_name')

    @app_service_name.setter
    def app_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'app_service_name', value)

    @property
    @pulumi.getter(name='appServicePlanId')
    def app_service_plan_id(self) -> pulumi.Input[str]:
        """
        The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_plan_id')

    @app_service_plan_id.setter
    def app_service_plan_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'app_service_plan_id', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A key-value pair of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @app_settings.setter
    def app_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'app_settings', value)

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> Optional[pulumi.Input['SlotAuthSettingsArgs']]:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @auth_settings.setter
    def auth_settings(self, value: Optional[pulumi.Input['SlotAuthSettingsArgs']]):
        pulumi.set(self, 'auth_settings', value)

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @client_affinity_enabled.setter
    def client_affinity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_affinity_enabled', value)

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]:
        """
        An `connection_string` block as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @connection_strings.setter
    def connection_strings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]):
        pulumi.set(self, 'connection_strings', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the App Service Slot Enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        """
        return pulumi.get(self, 'https_only')

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'https_only', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['SlotIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['SlotIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_reference_identity_id', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['SlotLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['SlotLogsArgs']]):
        pulumi.set(self, 'logs', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> Optional[pulumi.Input['SlotSiteConfigArgs']]:
        """
        A `site_config` object as defined below.
        """
        return pulumi.get(self, 'site_config')

    @site_config.setter
    def site_config(self, value: Optional[pulumi.Input['SlotSiteConfigArgs']]):
        pulumi.set(self, 'site_config', value)

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]):
        pulumi.set(self, 'storage_accounts', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

@pulumi.input_type
class _SlotState:

    def __init__(__self__, *, app_service_name: Optional[pulumi.Input[str]]=None, app_service_plan_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input['SlotAuthSettingsArgs']]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]=None, default_site_hostname: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['SlotIdentityArgs']]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input['SlotLogsArgs']]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input['SlotSiteConfigArgs']]=None, site_credentials: Optional[pulumi.Input[Sequence[pulumi.Input['SlotSiteCredentialArgs']]]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        Input properties used for looking up and filtering Slot resources.
        :param pulumi.Input[str] app_service_name: The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        :param pulumi.Input[str] app_service_plan_id: The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A key-value pair of App Settings.
        :param pulumi.Input['SlotAuthSettingsArgs'] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        :param pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]] connection_strings: An `connection_string` block as defined below.
        :param pulumi.Input[str] default_site_hostname: The Default Hostname associated with the App Service Slot - such as `mysite.azurewebsites.net`
        :param pulumi.Input[bool] enabled: Is the App Service Slot Enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        :param pulumi.Input['SlotIdentityArgs'] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input['SlotLogsArgs'] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input['SlotSiteConfigArgs'] site_config: A `site_config` object as defined below.
        :param pulumi.Input[Sequence[pulumi.Input['SlotSiteCredentialArgs']]] site_credentials: A `site_credential` block as defined below, which contains the site-level credentials used to publish to this App Service slot.
        :param pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        if app_service_name is not None:
            pulumi.set(__self__, 'app_service_name', app_service_name)
        if app_service_plan_id is not None:
            pulumi.set(__self__, 'app_service_plan_id', app_service_plan_id)
        if app_settings is not None:
            pulumi.set(__self__, 'app_settings', app_settings)
        if auth_settings is not None:
            pulumi.set(__self__, 'auth_settings', auth_settings)
        if client_affinity_enabled is not None:
            pulumi.set(__self__, 'client_affinity_enabled', client_affinity_enabled)
        if connection_strings is not None:
            pulumi.set(__self__, 'connection_strings', connection_strings)
        if default_site_hostname is not None:
            pulumi.set(__self__, 'default_site_hostname', default_site_hostname)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if key_vault_reference_identity_id is not None:
            pulumi.set(__self__, 'key_vault_reference_identity_id', key_vault_reference_identity_id)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if logs is not None:
            pulumi.set(__self__, 'logs', logs)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if resource_group_name is not None:
            pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if site_config is not None:
            pulumi.set(__self__, 'site_config', site_config)
        if site_credentials is not None:
            pulumi.set(__self__, 'site_credentials', site_credentials)
        if storage_accounts is not None:
            pulumi.set(__self__, 'storage_accounts', storage_accounts)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='appServiceName')
    def app_service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_name')

    @app_service_name.setter
    def app_service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'app_service_name', value)

    @property
    @pulumi.getter(name='appServicePlanId')
    def app_service_plan_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_plan_id')

    @app_service_plan_id.setter
    def app_service_plan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'app_service_plan_id', value)

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A key-value pair of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @app_settings.setter
    def app_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'app_settings', value)

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> Optional[pulumi.Input['SlotAuthSettingsArgs']]:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @auth_settings.setter
    def auth_settings(self, value: Optional[pulumi.Input['SlotAuthSettingsArgs']]):
        pulumi.set(self, 'auth_settings', value)

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @client_affinity_enabled.setter
    def client_affinity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_affinity_enabled', value)

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]:
        """
        An `connection_string` block as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @connection_strings.setter
    def connection_strings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SlotConnectionStringArgs']]]]):
        pulumi.set(self, 'connection_strings', value)

    @property
    @pulumi.getter(name='defaultSiteHostname')
    def default_site_hostname(self) -> Optional[pulumi.Input[str]]:
        """
        The Default Hostname associated with the App Service Slot - such as `mysite.azurewebsites.net`
        """
        return pulumi.get(self, 'default_site_hostname')

    @default_site_hostname.setter
    def default_site_hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_site_hostname', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Is the App Service Slot Enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        """
        return pulumi.get(self, 'https_only')

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'https_only', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['SlotIdentityArgs']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['SlotIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_reference_identity_id', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def logs(self) -> Optional[pulumi.Input['SlotLogsArgs']]:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @logs.setter
    def logs(self, value: Optional[pulumi.Input['SlotLogsArgs']]):
        pulumi.set(self, 'logs', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> Optional[pulumi.Input['SlotSiteConfigArgs']]:
        """
        A `site_config` object as defined below.
        """
        return pulumi.get(self, 'site_config')

    @site_config.setter
    def site_config(self, value: Optional[pulumi.Input['SlotSiteConfigArgs']]):
        pulumi.set(self, 'site_config', value)

    @property
    @pulumi.getter(name='siteCredentials')
    def site_credentials(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SlotSiteCredentialArgs']]]]:
        """
        A `site_credential` block as defined below, which contains the site-level credentials used to publish to this App Service slot.
        """
        return pulumi.get(self, 'site_credentials')

    @site_credentials.setter
    def site_credentials(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SlotSiteCredentialArgs']]]]):
        pulumi.set(self, 'site_credentials', value)

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SlotStorageAccountArgs']]]]):
        pulumi.set(self, 'storage_accounts', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class Slot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_service_name: Optional[pulumi.Input[str]]=None, app_service_plan_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['SlotAuthSettingsArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotConnectionStringArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['SlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['SlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['SlotSiteConfigArgs']]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        ## Example Usage
        ### NET 4.X)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_random as random

        server = random.RandomId("server",
            keepers={
                "azi_id": 1,
            },
            byte_length=8)
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.appservice.PlanSkuArgs(
                tier="Standard",
                size="S1",
            ))
        example_app_service = azure.appservice.AppService("exampleAppService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.AppServiceSiteConfigArgs(
                dotnet_framework_version="v4.0",
            ),
            app_settings={
                "SOME_KEY": "some-value",
            },
            connection_strings=[azure.appservice.AppServiceConnectionStringArgs(
                name="Database",
                type="SQLServer",
                value="Server=some-server.mydomain.com;Integrated Security=SSPI",
            )])
        example_slot = azure.appservice.Slot("exampleSlot",
            app_service_name=example_app_service.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.SlotSiteConfigArgs(
                dotnet_framework_version="v4.0",
            ),
            app_settings={
                "SOME_KEY": "some-value",
            },
            connection_strings=[azure.appservice.SlotConnectionStringArgs(
                name="Database",
                type="SQLServer",
                value="Server=some-server.mydomain.com;Integrated Security=SSPI",
            )])
        ```
        ### Java 1.8)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_random as random

        server = random.RandomId("server",
            keepers={
                "azi_id": 1,
            },
            byte_length=8)
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.appservice.PlanSkuArgs(
                tier="Standard",
                size="S1",
            ))
        example_app_service = azure.appservice.AppService("exampleAppService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.AppServiceSiteConfigArgs(
                java_version="1.8",
                java_container="JETTY",
                java_container_version="9.3",
            ))
        example_slot = azure.appservice.Slot("exampleSlot",
            app_service_name=example_app_service.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.SlotSiteConfigArgs(
                java_version="1.8",
                java_container="JETTY",
                java_container_version="9.3",
            ))
        ```

        ## Import

        App Service Slots can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/slot:Slot instance1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Web/sites/website1/slots/instance1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_service_name: The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        :param pulumi.Input[str] app_service_plan_id: The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A key-value pair of App Settings.
        :param pulumi.Input[pulumi.InputType['SlotAuthSettingsArgs']] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotConnectionStringArgs']]]] connection_strings: An `connection_string` block as defined below.
        :param pulumi.Input[bool] enabled: Is the App Service Slot Enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        :param pulumi.Input[pulumi.InputType['SlotIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['SlotLogsArgs']] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['SlotSiteConfigArgs']] site_config: A `site_config` object as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotStorageAccountArgs']]]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: SlotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        ## Example Usage
        ### NET 4.X)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_random as random

        server = random.RandomId("server",
            keepers={
                "azi_id": 1,
            },
            byte_length=8)
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.appservice.PlanSkuArgs(
                tier="Standard",
                size="S1",
            ))
        example_app_service = azure.appservice.AppService("exampleAppService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.AppServiceSiteConfigArgs(
                dotnet_framework_version="v4.0",
            ),
            app_settings={
                "SOME_KEY": "some-value",
            },
            connection_strings=[azure.appservice.AppServiceConnectionStringArgs(
                name="Database",
                type="SQLServer",
                value="Server=some-server.mydomain.com;Integrated Security=SSPI",
            )])
        example_slot = azure.appservice.Slot("exampleSlot",
            app_service_name=example_app_service.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.SlotSiteConfigArgs(
                dotnet_framework_version="v4.0",
            ),
            app_settings={
                "SOME_KEY": "some-value",
            },
            connection_strings=[azure.appservice.SlotConnectionStringArgs(
                name="Database",
                type="SQLServer",
                value="Server=some-server.mydomain.com;Integrated Security=SSPI",
            )])
        ```
        ### Java 1.8)

        ```python
        import pulumi
        import pulumi_azure as azure
        import pulumi_random as random

        server = random.RandomId("server",
            keepers={
                "azi_id": 1,
            },
            byte_length=8)
        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_plan = azure.appservice.Plan("examplePlan",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            sku=azure.appservice.PlanSkuArgs(
                tier="Standard",
                size="S1",
            ))
        example_app_service = azure.appservice.AppService("exampleAppService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.AppServiceSiteConfigArgs(
                java_version="1.8",
                java_container="JETTY",
                java_container_version="9.3",
            ))
        example_slot = azure.appservice.Slot("exampleSlot",
            app_service_name=example_app_service.name,
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            app_service_plan_id=example_plan.id,
            site_config=azure.appservice.SlotSiteConfigArgs(
                java_version="1.8",
                java_container="JETTY",
                java_container_version="9.3",
            ))
        ```

        ## Import

        App Service Slots can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:appservice/slot:Slot instance1 /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.Web/sites/website1/slots/instance1
        ```

        :param str resource_name: The name of the resource.
        :param SlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(SlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, app_service_name: Optional[pulumi.Input[str]]=None, app_service_plan_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['SlotAuthSettingsArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotConnectionStringArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['SlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['SlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['SlotSiteConfigArgs']]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SlotArgs.__new__(SlotArgs)
            if app_service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'app_service_name'")
            __props__.__dict__['app_service_name'] = app_service_name
            if app_service_plan_id is None and (not opts.urn):
                raise TypeError("Missing required property 'app_service_plan_id'")
            __props__.__dict__['app_service_plan_id'] = app_service_plan_id
            __props__.__dict__['app_settings'] = app_settings
            __props__.__dict__['auth_settings'] = auth_settings
            __props__.__dict__['client_affinity_enabled'] = client_affinity_enabled
            __props__.__dict__['connection_strings'] = connection_strings
            __props__.__dict__['enabled'] = enabled
            __props__.__dict__['https_only'] = https_only
            __props__.__dict__['identity'] = identity
            __props__.__dict__['key_vault_reference_identity_id'] = key_vault_reference_identity_id
            __props__.__dict__['location'] = location
            __props__.__dict__['logs'] = logs
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['site_config'] = site_config
            __props__.__dict__['storage_accounts'] = storage_accounts
            __props__.__dict__['tags'] = tags
            __props__.__dict__['default_site_hostname'] = None
            __props__.__dict__['site_credentials'] = None
        super(Slot, __self__).__init__('azure:appservice/slot:Slot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, app_service_name: Optional[pulumi.Input[str]]=None, app_service_plan_id: Optional[pulumi.Input[str]]=None, app_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, auth_settings: Optional[pulumi.Input[pulumi.InputType['SlotAuthSettingsArgs']]]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, connection_strings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotConnectionStringArgs']]]]]=None, default_site_hostname: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, https_only: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['SlotIdentityArgs']]]=None, key_vault_reference_identity_id: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, logs: Optional[pulumi.Input[pulumi.InputType['SlotLogsArgs']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['SlotSiteConfigArgs']]]=None, site_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotSiteCredentialArgs']]]]]=None, storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotStorageAccountArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None) -> 'Slot':
        """
        Get an existing Slot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_service_name: The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        :param pulumi.Input[str] app_service_plan_id: The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] app_settings: A key-value pair of App Settings.
        :param pulumi.Input[pulumi.InputType['SlotAuthSettingsArgs']] auth_settings: A `auth_settings` block as defined below.
        :param pulumi.Input[bool] client_affinity_enabled: Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotConnectionStringArgs']]]] connection_strings: An `connection_string` block as defined below.
        :param pulumi.Input[str] default_site_hostname: The Default Hostname associated with the App Service Slot - such as `mysite.azurewebsites.net`
        :param pulumi.Input[bool] enabled: Is the App Service Slot Enabled? Defaults to `true`.
        :param pulumi.Input[bool] https_only: Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        :param pulumi.Input[pulumi.InputType['SlotIdentityArgs']] identity: An `identity` block as defined below.
        :param pulumi.Input[str] key_vault_reference_identity_id: The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['SlotLogsArgs']] logs: A `logs` block as defined below.
        :param pulumi.Input[str] name: Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['SlotSiteConfigArgs']] site_config: A `site_config` object as defined below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotSiteCredentialArgs']]]] site_credentials: A `site_credential` block as defined below, which contains the site-level credentials used to publish to this App Service slot.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SlotStorageAccountArgs']]]] storage_accounts: One or more `storage_account` blocks as defined below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _SlotState.__new__(_SlotState)
        __props__.__dict__['app_service_name'] = app_service_name
        __props__.__dict__['app_service_plan_id'] = app_service_plan_id
        __props__.__dict__['app_settings'] = app_settings
        __props__.__dict__['auth_settings'] = auth_settings
        __props__.__dict__['client_affinity_enabled'] = client_affinity_enabled
        __props__.__dict__['connection_strings'] = connection_strings
        __props__.__dict__['default_site_hostname'] = default_site_hostname
        __props__.__dict__['enabled'] = enabled
        __props__.__dict__['https_only'] = https_only
        __props__.__dict__['identity'] = identity
        __props__.__dict__['key_vault_reference_identity_id'] = key_vault_reference_identity_id
        __props__.__dict__['location'] = location
        __props__.__dict__['logs'] = logs
        __props__.__dict__['name'] = name
        __props__.__dict__['resource_group_name'] = resource_group_name
        __props__.__dict__['site_config'] = site_config
        __props__.__dict__['site_credentials'] = site_credentials
        __props__.__dict__['storage_accounts'] = storage_accounts
        __props__.__dict__['tags'] = tags
        return Slot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='appServiceName')
    def app_service_name(self) -> pulumi.Output[str]:
        """
        The name of the App Service within which to create the App Service Slot.  Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_name')

    @property
    @pulumi.getter(name='appServicePlanId')
    def app_service_plan_id(self) -> pulumi.Output[str]:
        """
        The ID of the App Service Plan within which to create this App Service Slot. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'app_service_plan_id')

    @property
    @pulumi.getter(name='appSettings')
    def app_settings(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A key-value pair of App Settings.
        """
        return pulumi.get(self, 'app_settings')

    @property
    @pulumi.getter(name='authSettings')
    def auth_settings(self) -> pulumi.Output['outputs.SlotAuthSettings']:
        """
        A `auth_settings` block as defined below.
        """
        return pulumi.get(self, 'auth_settings')

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> pulumi.Output[bool]:
        """
        Should the App Service Slot send session affinity cookies, which route client requests in the same session to the same instance?
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @property
    @pulumi.getter(name='connectionStrings')
    def connection_strings(self) -> pulumi.Output[Sequence['outputs.SlotConnectionString']]:
        """
        An `connection_string` block as defined below.
        """
        return pulumi.get(self, 'connection_strings')

    @property
    @pulumi.getter(name='defaultSiteHostname')
    def default_site_hostname(self) -> pulumi.Output[str]:
        """
        The Default Hostname associated with the App Service Slot - such as `mysite.azurewebsites.net`
        """
        return pulumi.get(self, 'default_site_hostname')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Is the App Service Slot Enabled? Defaults to `true`.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Can the App Service Slot only be accessed via HTTPS? Defaults to `false`.
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.SlotIdentity']]:
        """
        An `identity` block as defined below.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='keyVaultReferenceIdentityId')
    def key_vault_reference_identity_id(self) -> pulumi.Output[str]:
        """
        The User Assigned Identity Id used for looking up KeyVault secrets. The identity must be assigned to the application. See [Access vaults with a user-assigned identity](https://docs.microsoft.com/azure/app-service/app-service-key-vault-references#access-vaults-with-a-user-assigned-identity) for more information.
        """
        return pulumi.get(self, 'key_vault_reference_identity_id')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Output['outputs.SlotLogs']:
        """
        A `logs` block as defined below.
        """
        return pulumi.get(self, 'logs')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the App Service Slot component. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> pulumi.Output['outputs.SlotSiteConfig']:
        """
        A `site_config` object as defined below.
        """
        return pulumi.get(self, 'site_config')

    @property
    @pulumi.getter(name='siteCredentials')
    def site_credentials(self) -> pulumi.Output[Sequence['outputs.SlotSiteCredential']]:
        """
        A `site_credential` block as defined below, which contains the site-level credentials used to publish to this App Service slot.
        """
        return pulumi.get(self, 'site_credentials')

    @property
    @pulumi.getter(name='storageAccounts')
    def storage_accounts(self) -> pulumi.Output[Sequence['outputs.SlotStorageAccount']]:
        """
        One or more `storage_account` blocks as defined below.
        """
        return pulumi.get(self, 'storage_accounts')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, 'tags')
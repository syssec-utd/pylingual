import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['DomainServiceArgs', 'DomainService']

@pulumi.input_type
class DomainServiceArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], config_diagnostics: Optional[pulumi.Input['ConfigDiagnosticsArgs']]=None, domain_configuration_type: Optional[pulumi.Input[str]]=None, domain_name: Optional[pulumi.Input[str]]=None, domain_security_settings: Optional[pulumi.Input['DomainSecuritySettingsArgs']]=None, domain_service_name: Optional[pulumi.Input[str]]=None, filtered_sync: Optional[pulumi.Input[Union[str, 'FilteredSync']]]=None, ldaps_settings: Optional[pulumi.Input['LdapsSettingsArgs']]=None, location: Optional[pulumi.Input[str]]=None, notification_settings: Optional[pulumi.Input['NotificationSettingsArgs']]=None, replica_sets: Optional[pulumi.Input[Sequence[pulumi.Input['ReplicaSetArgs']]]]=None, resource_forest_settings: Optional[pulumi.Input['ResourceForestSettingsArgs']]=None, sku: Optional[pulumi.Input[str]]=None, sync_scope: Optional[pulumi.Input[Union[str, 'SyncScope']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a DomainService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input['ConfigDiagnosticsArgs'] config_diagnostics: Configuration diagnostics data containing latest execution from client.
        :param pulumi.Input[str] domain_configuration_type: Domain Configuration Type
        :param pulumi.Input[str] domain_name: The name of the Azure domain that the user would like to deploy Domain Services to.
        :param pulumi.Input['DomainSecuritySettingsArgs'] domain_security_settings: DomainSecurity Settings
        :param pulumi.Input[str] domain_service_name: The name of the domain service.
        :param pulumi.Input[Union[str, 'FilteredSync']] filtered_sync: Enabled or Disabled flag to turn on Group-based filtered sync
        :param pulumi.Input['LdapsSettingsArgs'] ldaps_settings: Secure LDAP Settings
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['NotificationSettingsArgs'] notification_settings: Notification Settings
        :param pulumi.Input[Sequence[pulumi.Input['ReplicaSetArgs']]] replica_sets: List of ReplicaSets
        :param pulumi.Input['ResourceForestSettingsArgs'] resource_forest_settings: Resource Forest Settings
        :param pulumi.Input[str] sku: Sku Type
        :param pulumi.Input[Union[str, 'SyncScope']] sync_scope: All or CloudOnly, All users in AAD are synced to AAD DS domain or only users actively syncing in the cloud
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if config_diagnostics is not None:
            pulumi.set(__self__, 'config_diagnostics', config_diagnostics)
        if domain_configuration_type is not None:
            pulumi.set(__self__, 'domain_configuration_type', domain_configuration_type)
        if domain_name is not None:
            pulumi.set(__self__, 'domain_name', domain_name)
        if domain_security_settings is not None:
            pulumi.set(__self__, 'domain_security_settings', domain_security_settings)
        if domain_service_name is not None:
            pulumi.set(__self__, 'domain_service_name', domain_service_name)
        if filtered_sync is not None:
            pulumi.set(__self__, 'filtered_sync', filtered_sync)
        if ldaps_settings is not None:
            pulumi.set(__self__, 'ldaps_settings', ldaps_settings)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if notification_settings is not None:
            pulumi.set(__self__, 'notification_settings', notification_settings)
        if replica_sets is not None:
            pulumi.set(__self__, 'replica_sets', replica_sets)
        if resource_forest_settings is not None:
            pulumi.set(__self__, 'resource_forest_settings', resource_forest_settings)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if sync_scope is not None:
            pulumi.set(__self__, 'sync_scope', sync_scope)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='configDiagnostics')
    def config_diagnostics(self) -> Optional[pulumi.Input['ConfigDiagnosticsArgs']]:
        """
        Configuration diagnostics data containing latest execution from client.
        """
        return pulumi.get(self, 'config_diagnostics')

    @config_diagnostics.setter
    def config_diagnostics(self, value: Optional[pulumi.Input['ConfigDiagnosticsArgs']]):
        pulumi.set(self, 'config_diagnostics', value)

    @property
    @pulumi.getter(name='domainConfigurationType')
    def domain_configuration_type(self) -> Optional[pulumi.Input[str]]:
        """
        Domain Configuration Type
        """
        return pulumi.get(self, 'domain_configuration_type')

    @domain_configuration_type.setter
    def domain_configuration_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'domain_configuration_type', value)

    @property
    @pulumi.getter(name='domainName')
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Azure domain that the user would like to deploy Domain Services to.
        """
        return pulumi.get(self, 'domain_name')

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'domain_name', value)

    @property
    @pulumi.getter(name='domainSecuritySettings')
    def domain_security_settings(self) -> Optional[pulumi.Input['DomainSecuritySettingsArgs']]:
        """
        DomainSecurity Settings
        """
        return pulumi.get(self, 'domain_security_settings')

    @domain_security_settings.setter
    def domain_security_settings(self, value: Optional[pulumi.Input['DomainSecuritySettingsArgs']]):
        pulumi.set(self, 'domain_security_settings', value)

    @property
    @pulumi.getter(name='domainServiceName')
    def domain_service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the domain service.
        """
        return pulumi.get(self, 'domain_service_name')

    @domain_service_name.setter
    def domain_service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'domain_service_name', value)

    @property
    @pulumi.getter(name='filteredSync')
    def filtered_sync(self) -> Optional[pulumi.Input[Union[str, 'FilteredSync']]]:
        """
        Enabled or Disabled flag to turn on Group-based filtered sync
        """
        return pulumi.get(self, 'filtered_sync')

    @filtered_sync.setter
    def filtered_sync(self, value: Optional[pulumi.Input[Union[str, 'FilteredSync']]]):
        pulumi.set(self, 'filtered_sync', value)

    @property
    @pulumi.getter(name='ldapsSettings')
    def ldaps_settings(self) -> Optional[pulumi.Input['LdapsSettingsArgs']]:
        """
        Secure LDAP Settings
        """
        return pulumi.get(self, 'ldaps_settings')

    @ldaps_settings.setter
    def ldaps_settings(self, value: Optional[pulumi.Input['LdapsSettingsArgs']]):
        pulumi.set(self, 'ldaps_settings', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='notificationSettings')
    def notification_settings(self) -> Optional[pulumi.Input['NotificationSettingsArgs']]:
        """
        Notification Settings
        """
        return pulumi.get(self, 'notification_settings')

    @notification_settings.setter
    def notification_settings(self, value: Optional[pulumi.Input['NotificationSettingsArgs']]):
        pulumi.set(self, 'notification_settings', value)

    @property
    @pulumi.getter(name='replicaSets')
    def replica_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReplicaSetArgs']]]]:
        """
        List of ReplicaSets
        """
        return pulumi.get(self, 'replica_sets')

    @replica_sets.setter
    def replica_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReplicaSetArgs']]]]):
        pulumi.set(self, 'replica_sets', value)

    @property
    @pulumi.getter(name='resourceForestSettings')
    def resource_forest_settings(self) -> Optional[pulumi.Input['ResourceForestSettingsArgs']]:
        """
        Resource Forest Settings
        """
        return pulumi.get(self, 'resource_forest_settings')

    @resource_forest_settings.setter
    def resource_forest_settings(self, value: Optional[pulumi.Input['ResourceForestSettingsArgs']]):
        pulumi.set(self, 'resource_forest_settings', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        Sku Type
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter(name='syncScope')
    def sync_scope(self) -> Optional[pulumi.Input[Union[str, 'SyncScope']]]:
        """
        All or CloudOnly, All users in AAD are synced to AAD DS domain or only users actively syncing in the cloud
        """
        return pulumi.get(self, 'sync_scope')

    @sync_scope.setter
    def sync_scope(self, value: Optional[pulumi.Input[Union[str, 'SyncScope']]]):
        pulumi.set(self, 'sync_scope', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class DomainService(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, config_diagnostics: Optional[pulumi.Input[pulumi.InputType['ConfigDiagnosticsArgs']]]=None, domain_configuration_type: Optional[pulumi.Input[str]]=None, domain_name: Optional[pulumi.Input[str]]=None, domain_security_settings: Optional[pulumi.Input[pulumi.InputType['DomainSecuritySettingsArgs']]]=None, domain_service_name: Optional[pulumi.Input[str]]=None, filtered_sync: Optional[pulumi.Input[Union[str, 'FilteredSync']]]=None, ldaps_settings: Optional[pulumi.Input[pulumi.InputType['LdapsSettingsArgs']]]=None, location: Optional[pulumi.Input[str]]=None, notification_settings: Optional[pulumi.Input[pulumi.InputType['NotificationSettingsArgs']]]=None, replica_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicaSetArgs']]]]]=None, resource_forest_settings: Optional[pulumi.Input[pulumi.InputType['ResourceForestSettingsArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[str]]=None, sync_scope: Optional[pulumi.Input[Union[str, 'SyncScope']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Domain service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ConfigDiagnosticsArgs']] config_diagnostics: Configuration diagnostics data containing latest execution from client.
        :param pulumi.Input[str] domain_configuration_type: Domain Configuration Type
        :param pulumi.Input[str] domain_name: The name of the Azure domain that the user would like to deploy Domain Services to.
        :param pulumi.Input[pulumi.InputType['DomainSecuritySettingsArgs']] domain_security_settings: DomainSecurity Settings
        :param pulumi.Input[str] domain_service_name: The name of the domain service.
        :param pulumi.Input[Union[str, 'FilteredSync']] filtered_sync: Enabled or Disabled flag to turn on Group-based filtered sync
        :param pulumi.Input[pulumi.InputType['LdapsSettingsArgs']] ldaps_settings: Secure LDAP Settings
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['NotificationSettingsArgs']] notification_settings: Notification Settings
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicaSetArgs']]]] replica_sets: List of ReplicaSets
        :param pulumi.Input[pulumi.InputType['ResourceForestSettingsArgs']] resource_forest_settings: Resource Forest Settings
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] sku: Sku Type
        :param pulumi.Input[Union[str, 'SyncScope']] sync_scope: All or CloudOnly, All users in AAD are synced to AAD DS domain or only users actively syncing in the cloud
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DomainServiceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Domain service.

        :param str resource_name: The name of the resource.
        :param DomainServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, config_diagnostics: Optional[pulumi.Input[pulumi.InputType['ConfigDiagnosticsArgs']]]=None, domain_configuration_type: Optional[pulumi.Input[str]]=None, domain_name: Optional[pulumi.Input[str]]=None, domain_security_settings: Optional[pulumi.Input[pulumi.InputType['DomainSecuritySettingsArgs']]]=None, domain_service_name: Optional[pulumi.Input[str]]=None, filtered_sync: Optional[pulumi.Input[Union[str, 'FilteredSync']]]=None, ldaps_settings: Optional[pulumi.Input[pulumi.InputType['LdapsSettingsArgs']]]=None, location: Optional[pulumi.Input[str]]=None, notification_settings: Optional[pulumi.Input[pulumi.InputType['NotificationSettingsArgs']]]=None, replica_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ReplicaSetArgs']]]]]=None, resource_forest_settings: Optional[pulumi.Input[pulumi.InputType['ResourceForestSettingsArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[str]]=None, sync_scope: Optional[pulumi.Input[Union[str, 'SyncScope']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainServiceArgs.__new__(DomainServiceArgs)
            __props__.__dict__['config_diagnostics'] = config_diagnostics
            __props__.__dict__['domain_configuration_type'] = domain_configuration_type
            __props__.__dict__['domain_name'] = domain_name
            __props__.__dict__['domain_security_settings'] = domain_security_settings
            __props__.__dict__['domain_service_name'] = domain_service_name
            __props__.__dict__['filtered_sync'] = filtered_sync
            __props__.__dict__['ldaps_settings'] = ldaps_settings
            __props__.__dict__['location'] = location
            __props__.__dict__['notification_settings'] = notification_settings
            __props__.__dict__['replica_sets'] = replica_sets
            __props__.__dict__['resource_forest_settings'] = resource_forest_settings
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['sync_scope'] = sync_scope
            __props__.__dict__['tags'] = tags
            __props__.__dict__['deployment_id'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['migration_properties'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['sync_owner'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['tenant_id'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['version'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:aad:DomainService'), pulumi.Alias(type_='azure-native:aad/v20170101:DomainService'), pulumi.Alias(type_='azure-native:aad/v20170601:DomainService'), pulumi.Alias(type_='azure-native:aad/v20200101:DomainService'), pulumi.Alias(type_='azure-native:aad/v20210301:DomainService'), pulumi.Alias(type_='azure-native:aad/v20210501:DomainService')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DomainService, __self__).__init__('azure-native:aad/v20220901:DomainService', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'DomainService':
        """
        Get an existing DomainService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = DomainServiceArgs.__new__(DomainServiceArgs)
        __props__.__dict__['config_diagnostics'] = None
        __props__.__dict__['deployment_id'] = None
        __props__.__dict__['domain_configuration_type'] = None
        __props__.__dict__['domain_name'] = None
        __props__.__dict__['domain_security_settings'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['filtered_sync'] = None
        __props__.__dict__['ldaps_settings'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['migration_properties'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['notification_settings'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['replica_sets'] = None
        __props__.__dict__['resource_forest_settings'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['sync_owner'] = None
        __props__.__dict__['sync_scope'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['tenant_id'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['version'] = None
        return DomainService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='configDiagnostics')
    def config_diagnostics(self) -> pulumi.Output[Optional['outputs.ConfigDiagnosticsResponse']]:
        """
        Configuration diagnostics data containing latest execution from client.
        """
        return pulumi.get(self, 'config_diagnostics')

    @property
    @pulumi.getter(name='deploymentId')
    def deployment_id(self) -> pulumi.Output[str]:
        """
        Deployment Id
        """
        return pulumi.get(self, 'deployment_id')

    @property
    @pulumi.getter(name='domainConfigurationType')
    def domain_configuration_type(self) -> pulumi.Output[Optional[str]]:
        """
        Domain Configuration Type
        """
        return pulumi.get(self, 'domain_configuration_type')

    @property
    @pulumi.getter(name='domainName')
    def domain_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Azure domain that the user would like to deploy Domain Services to.
        """
        return pulumi.get(self, 'domain_name')

    @property
    @pulumi.getter(name='domainSecuritySettings')
    def domain_security_settings(self) -> pulumi.Output[Optional['outputs.DomainSecuritySettingsResponse']]:
        """
        DomainSecurity Settings
        """
        return pulumi.get(self, 'domain_security_settings')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Resource etag
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='filteredSync')
    def filtered_sync(self) -> pulumi.Output[Optional[str]]:
        """
        Enabled or Disabled flag to turn on Group-based filtered sync
        """
        return pulumi.get(self, 'filtered_sync')

    @property
    @pulumi.getter(name='ldapsSettings')
    def ldaps_settings(self) -> pulumi.Output[Optional['outputs.LdapsSettingsResponse']]:
        """
        Secure LDAP Settings
        """
        return pulumi.get(self, 'ldaps_settings')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='migrationProperties')
    def migration_properties(self) -> pulumi.Output['outputs.MigrationPropertiesResponse']:
        """
        Migration Properties
        """
        return pulumi.get(self, 'migration_properties')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='notificationSettings')
    def notification_settings(self) -> pulumi.Output[Optional['outputs.NotificationSettingsResponse']]:
        """
        Notification Settings
        """
        return pulumi.get(self, 'notification_settings')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        the current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='replicaSets')
    def replica_sets(self) -> pulumi.Output[Optional[Sequence['outputs.ReplicaSetResponse']]]:
        """
        List of ReplicaSets
        """
        return pulumi.get(self, 'replica_sets')

    @property
    @pulumi.getter(name='resourceForestSettings')
    def resource_forest_settings(self) -> pulumi.Output[Optional['outputs.ResourceForestSettingsResponse']]:
        """
        Resource Forest Settings
        """
        return pulumi.get(self, 'resource_forest_settings')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional[str]]:
        """
        Sku Type
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='syncOwner')
    def sync_owner(self) -> pulumi.Output[str]:
        """
        SyncOwner ReplicaSet Id
        """
        return pulumi.get(self, 'sync_owner')

    @property
    @pulumi.getter(name='syncScope')
    def sync_scope(self) -> pulumi.Output[Optional[str]]:
        """
        All or CloudOnly, All users in AAD are synced to AAD DS domain or only users actively syncing in the cloud
        """
        return pulumi.get(self, 'sync_scope')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> pulumi.Output[str]:
        """
        Azure Active Directory Tenant Id
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        Data Model Version
        """
        return pulumi.get(self, 'version')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['WebAppSlotArgs', 'WebAppSlot']

@pulumi.input_type
class WebAppSlotArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_cert_enabled: Optional[pulumi.Input[bool]]=None, client_cert_exclusion_paths: Optional[pulumi.Input[str]]=None, client_cert_mode: Optional[pulumi.Input['ClientCertMode']]=None, cloning_info: Optional[pulumi.Input['CloningInfoArgs']]=None, container_size: Optional[pulumi.Input[int]]=None, custom_domain_verification_id: Optional[pulumi.Input[str]]=None, daily_memory_time_quota: Optional[pulumi.Input[int]]=None, enabled: Optional[pulumi.Input[bool]]=None, extended_location: Optional[pulumi.Input['ExtendedLocationArgs']]=None, host_name_ssl_states: Optional[pulumi.Input[Sequence[pulumi.Input['HostNameSslStateArgs']]]]=None, host_names_disabled: Optional[pulumi.Input[bool]]=None, hosting_environment_profile: Optional[pulumi.Input['HostingEnvironmentProfileArgs']]=None, https_only: Optional[pulumi.Input[bool]]=None, hyper_v: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']]=None, is_xenon: Optional[pulumi.Input[bool]]=None, key_vault_reference_identity: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, redundancy_mode: Optional[pulumi.Input['RedundancyMode']]=None, reserved: Optional[pulumi.Input[bool]]=None, scm_site_also_stopped: Optional[pulumi.Input[bool]]=None, server_farm_id: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input['SiteConfigArgs']]=None, slot: Optional[pulumi.Input[str]]=None, storage_account_required: Optional[pulumi.Input[bool]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_network_subnet_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a WebAppSlot resource.
        :param pulumi.Input[str] name: Unique name of the app to create or update. To create or update a deployment slot, use the {slot} parameter.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[bool] client_affinity_enabled: <code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests in the same session to the same instance. Default is <code>true</code>.
        :param pulumi.Input[bool] client_cert_enabled: <code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is <code>false</code>.
        :param pulumi.Input[str] client_cert_exclusion_paths: client certificate authentication comma-separated exclusion paths
        :param pulumi.Input['ClientCertMode'] client_cert_mode: This composes with ClientCertEnabled setting.
               - ClientCertEnabled: false means ClientCert is ignored.
               - ClientCertEnabled: true and ClientCertMode: Required means ClientCert is required.
               - ClientCertEnabled: true and ClientCertMode: Optional means ClientCert is optional or accepted.
        :param pulumi.Input['CloningInfoArgs'] cloning_info: If specified during app creation, the app is cloned from a source app.
        :param pulumi.Input[int] container_size: Size of the function container.
        :param pulumi.Input[str] custom_domain_verification_id: Unique identifier that verifies the custom domains assigned to the app. Customer will add this id to a txt record for verification.
        :param pulumi.Input[int] daily_memory_time_quota: Maximum allowed daily memory-time quota (applicable on dynamic apps only).
        :param pulumi.Input[bool] enabled: <code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app offline).
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: Extended Location.
        :param pulumi.Input[Sequence[pulumi.Input['HostNameSslStateArgs']]] host_name_ssl_states: Hostname SSL states are used to manage the SSL bindings for app's hostnames.
        :param pulumi.Input[bool] host_names_disabled: <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
                If <code>true</code>, the app is only accessible via API management process.
        :param pulumi.Input['HostingEnvironmentProfileArgs'] hosting_environment_profile: App Service Environment to use for the app.
        :param pulumi.Input[bool] https_only: HttpsOnly: configures a web site to accept only https requests. Issues redirect for
               http requests
        :param pulumi.Input[bool] hyper_v: Hyper-V sandbox.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: Managed service identity.
        :param pulumi.Input[bool] is_xenon: Obsolete: Hyper-V sandbox.
        :param pulumi.Input[str] key_vault_reference_identity: Identity to use for Key Vault Reference authentication.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input['RedundancyMode'] redundancy_mode: Site redundancy mode
        :param pulumi.Input[bool] reserved: <code>true</code> if reserved; otherwise, <code>false</code>.
        :param pulumi.Input[bool] scm_site_also_stopped: <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
        :param pulumi.Input[str] server_farm_id: Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        :param pulumi.Input['SiteConfigArgs'] site_config: Configuration of the app.
        :param pulumi.Input[str] slot: Name of the deployment slot to create or update. By default, this API attempts to create or modify the production slot.
        :param pulumi.Input[bool] storage_account_required: Checks if Customer provided storage account is required
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] virtual_network_subnet_id: Azure Resource Manager ID of the Virtual network and subnet to be joined by Regional VNET Integration.
               This must be of the form /subscriptions/{subscriptionName}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if client_affinity_enabled is not None:
            pulumi.set(__self__, 'client_affinity_enabled', client_affinity_enabled)
        if client_cert_enabled is not None:
            pulumi.set(__self__, 'client_cert_enabled', client_cert_enabled)
        if client_cert_exclusion_paths is not None:
            pulumi.set(__self__, 'client_cert_exclusion_paths', client_cert_exclusion_paths)
        if client_cert_mode is not None:
            pulumi.set(__self__, 'client_cert_mode', client_cert_mode)
        if cloning_info is not None:
            pulumi.set(__self__, 'cloning_info', cloning_info)
        if container_size is not None:
            pulumi.set(__self__, 'container_size', container_size)
        if custom_domain_verification_id is not None:
            pulumi.set(__self__, 'custom_domain_verification_id', custom_domain_verification_id)
        if daily_memory_time_quota is not None:
            pulumi.set(__self__, 'daily_memory_time_quota', daily_memory_time_quota)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if extended_location is not None:
            pulumi.set(__self__, 'extended_location', extended_location)
        if host_name_ssl_states is not None:
            pulumi.set(__self__, 'host_name_ssl_states', host_name_ssl_states)
        if host_names_disabled is not None:
            pulumi.set(__self__, 'host_names_disabled', host_names_disabled)
        if hosting_environment_profile is not None:
            pulumi.set(__self__, 'hosting_environment_profile', hosting_environment_profile)
        if https_only is not None:
            pulumi.set(__self__, 'https_only', https_only)
        if hyper_v is None:
            hyper_v = False
        if hyper_v is not None:
            pulumi.set(__self__, 'hyper_v', hyper_v)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if is_xenon is None:
            is_xenon = False
        if is_xenon is not None:
            pulumi.set(__self__, 'is_xenon', is_xenon)
        if key_vault_reference_identity is not None:
            pulumi.set(__self__, 'key_vault_reference_identity', key_vault_reference_identity)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if redundancy_mode is not None:
            pulumi.set(__self__, 'redundancy_mode', redundancy_mode)
        if reserved is None:
            reserved = False
        if reserved is not None:
            pulumi.set(__self__, 'reserved', reserved)
        if scm_site_also_stopped is None:
            scm_site_also_stopped = False
        if scm_site_also_stopped is not None:
            pulumi.set(__self__, 'scm_site_also_stopped', scm_site_also_stopped)
        if server_farm_id is not None:
            pulumi.set(__self__, 'server_farm_id', server_farm_id)
        if site_config is not None:
            pulumi.set(__self__, 'site_config', site_config)
        if slot is not None:
            pulumi.set(__self__, 'slot', slot)
        if storage_account_required is not None:
            pulumi.set(__self__, 'storage_account_required', storage_account_required)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if virtual_network_subnet_id is not None:
            pulumi.set(__self__, 'virtual_network_subnet_id', virtual_network_subnet_id)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the app to create or update. To create or update a deployment slot, use the {slot} parameter.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests in the same session to the same instance. Default is <code>true</code>.
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @client_affinity_enabled.setter
    def client_affinity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_affinity_enabled', value)

    @property
    @pulumi.getter(name='clientCertEnabled')
    def client_cert_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is <code>false</code>.
        """
        return pulumi.get(self, 'client_cert_enabled')

    @client_cert_enabled.setter
    def client_cert_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_cert_enabled', value)

    @property
    @pulumi.getter(name='clientCertExclusionPaths')
    def client_cert_exclusion_paths(self) -> Optional[pulumi.Input[str]]:
        """
        client certificate authentication comma-separated exclusion paths
        """
        return pulumi.get(self, 'client_cert_exclusion_paths')

    @client_cert_exclusion_paths.setter
    def client_cert_exclusion_paths(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'client_cert_exclusion_paths', value)

    @property
    @pulumi.getter(name='clientCertMode')
    def client_cert_mode(self) -> Optional[pulumi.Input['ClientCertMode']]:
        """
        This composes with ClientCertEnabled setting.
        - ClientCertEnabled: false means ClientCert is ignored.
        - ClientCertEnabled: true and ClientCertMode: Required means ClientCert is required.
        - ClientCertEnabled: true and ClientCertMode: Optional means ClientCert is optional or accepted.
        """
        return pulumi.get(self, 'client_cert_mode')

    @client_cert_mode.setter
    def client_cert_mode(self, value: Optional[pulumi.Input['ClientCertMode']]):
        pulumi.set(self, 'client_cert_mode', value)

    @property
    @pulumi.getter(name='cloningInfo')
    def cloning_info(self) -> Optional[pulumi.Input['CloningInfoArgs']]:
        """
        If specified during app creation, the app is cloned from a source app.
        """
        return pulumi.get(self, 'cloning_info')

    @cloning_info.setter
    def cloning_info(self, value: Optional[pulumi.Input['CloningInfoArgs']]):
        pulumi.set(self, 'cloning_info', value)

    @property
    @pulumi.getter(name='containerSize')
    def container_size(self) -> Optional[pulumi.Input[int]]:
        """
        Size of the function container.
        """
        return pulumi.get(self, 'container_size')

    @container_size.setter
    def container_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'container_size', value)

    @property
    @pulumi.getter(name='customDomainVerificationId')
    def custom_domain_verification_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique identifier that verifies the custom domains assigned to the app. Customer will add this id to a txt record for verification.
        """
        return pulumi.get(self, 'custom_domain_verification_id')

    @custom_domain_verification_id.setter
    def custom_domain_verification_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'custom_domain_verification_id', value)

    @property
    @pulumi.getter(name='dailyMemoryTimeQuota')
    def daily_memory_time_quota(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum allowed daily memory-time quota (applicable on dynamic apps only).
        """
        return pulumi.get(self, 'daily_memory_time_quota')

    @daily_memory_time_quota.setter
    def daily_memory_time_quota(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'daily_memory_time_quota', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app offline).
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> Optional[pulumi.Input['ExtendedLocationArgs']]:
        """
        Extended Location.
        """
        return pulumi.get(self, 'extended_location')

    @extended_location.setter
    def extended_location(self, value: Optional[pulumi.Input['ExtendedLocationArgs']]):
        pulumi.set(self, 'extended_location', value)

    @property
    @pulumi.getter(name='hostNameSslStates')
    def host_name_ssl_states(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HostNameSslStateArgs']]]]:
        """
        Hostname SSL states are used to manage the SSL bindings for app's hostnames.
        """
        return pulumi.get(self, 'host_name_ssl_states')

    @host_name_ssl_states.setter
    def host_name_ssl_states(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HostNameSslStateArgs']]]]):
        pulumi.set(self, 'host_name_ssl_states', value)

    @property
    @pulumi.getter(name='hostNamesDisabled')
    def host_names_disabled(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
         If <code>true</code>, the app is only accessible via API management process.
        """
        return pulumi.get(self, 'host_names_disabled')

    @host_names_disabled.setter
    def host_names_disabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'host_names_disabled', value)

    @property
    @pulumi.getter(name='hostingEnvironmentProfile')
    def hosting_environment_profile(self) -> Optional[pulumi.Input['HostingEnvironmentProfileArgs']]:
        """
        App Service Environment to use for the app.
        """
        return pulumi.get(self, 'hosting_environment_profile')

    @hosting_environment_profile.setter
    def hosting_environment_profile(self, value: Optional[pulumi.Input['HostingEnvironmentProfileArgs']]):
        pulumi.set(self, 'hosting_environment_profile', value)

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> Optional[pulumi.Input[bool]]:
        """
        HttpsOnly: configures a web site to accept only https requests. Issues redirect for
        http requests
        """
        return pulumi.get(self, 'https_only')

    @https_only.setter
    def https_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'https_only', value)

    @property
    @pulumi.getter(name='hyperV')
    def hyper_v(self) -> Optional[pulumi.Input[bool]]:
        """
        Hyper-V sandbox.
        """
        return pulumi.get(self, 'hyper_v')

    @hyper_v.setter
    def hyper_v(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'hyper_v', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        Managed service identity.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter(name='isXenon')
    def is_xenon(self) -> Optional[pulumi.Input[bool]]:
        """
        Obsolete: Hyper-V sandbox.
        """
        return pulumi.get(self, 'is_xenon')

    @is_xenon.setter
    def is_xenon(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_xenon', value)

    @property
    @pulumi.getter(name='keyVaultReferenceIdentity')
    def key_vault_reference_identity(self) -> Optional[pulumi.Input[str]]:
        """
        Identity to use for Key Vault Reference authentication.
        """
        return pulumi.get(self, 'key_vault_reference_identity')

    @key_vault_reference_identity.setter
    def key_vault_reference_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_vault_reference_identity', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='redundancyMode')
    def redundancy_mode(self) -> Optional[pulumi.Input['RedundancyMode']]:
        """
        Site redundancy mode
        """
        return pulumi.get(self, 'redundancy_mode')

    @redundancy_mode.setter
    def redundancy_mode(self, value: Optional[pulumi.Input['RedundancyMode']]):
        pulumi.set(self, 'redundancy_mode', value)

    @property
    @pulumi.getter
    def reserved(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> if reserved; otherwise, <code>false</code>.
        """
        return pulumi.get(self, 'reserved')

    @reserved.setter
    def reserved(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'reserved', value)

    @property
    @pulumi.getter(name='scmSiteAlsoStopped')
    def scm_site_also_stopped(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
        """
        return pulumi.get(self, 'scm_site_also_stopped')

    @scm_site_also_stopped.setter
    def scm_site_also_stopped(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'scm_site_also_stopped', value)

    @property
    @pulumi.getter(name='serverFarmId')
    def server_farm_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        """
        return pulumi.get(self, 'server_farm_id')

    @server_farm_id.setter
    def server_farm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'server_farm_id', value)

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> Optional[pulumi.Input['SiteConfigArgs']]:
        """
        Configuration of the app.
        """
        return pulumi.get(self, 'site_config')

    @site_config.setter
    def site_config(self, value: Optional[pulumi.Input['SiteConfigArgs']]):
        pulumi.set(self, 'site_config', value)

    @property
    @pulumi.getter
    def slot(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the deployment slot to create or update. By default, this API attempts to create or modify the production slot.
        """
        return pulumi.get(self, 'slot')

    @slot.setter
    def slot(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'slot', value)

    @property
    @pulumi.getter(name='storageAccountRequired')
    def storage_account_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Checks if Customer provided storage account is required
        """
        return pulumi.get(self, 'storage_account_required')

    @storage_account_required.setter
    def storage_account_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'storage_account_required', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='virtualNetworkSubnetId')
    def virtual_network_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        Azure Resource Manager ID of the Virtual network and subnet to be joined by Regional VNET Integration.
        This must be of the form /subscriptions/{subscriptionName}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}
        """
        return pulumi.get(self, 'virtual_network_subnet_id')

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'virtual_network_subnet_id', value)

class WebAppSlot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_cert_enabled: Optional[pulumi.Input[bool]]=None, client_cert_exclusion_paths: Optional[pulumi.Input[str]]=None, client_cert_mode: Optional[pulumi.Input['ClientCertMode']]=None, cloning_info: Optional[pulumi.Input[pulumi.InputType['CloningInfoArgs']]]=None, container_size: Optional[pulumi.Input[int]]=None, custom_domain_verification_id: Optional[pulumi.Input[str]]=None, daily_memory_time_quota: Optional[pulumi.Input[int]]=None, enabled: Optional[pulumi.Input[bool]]=None, extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]]=None, host_name_ssl_states: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostNameSslStateArgs']]]]]=None, host_names_disabled: Optional[pulumi.Input[bool]]=None, hosting_environment_profile: Optional[pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']]]=None, https_only: Optional[pulumi.Input[bool]]=None, hyper_v: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, is_xenon: Optional[pulumi.Input[bool]]=None, key_vault_reference_identity: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, redundancy_mode: Optional[pulumi.Input['RedundancyMode']]=None, reserved: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scm_site_also_stopped: Optional[pulumi.Input[bool]]=None, server_farm_id: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['SiteConfigArgs']]]=None, slot: Optional[pulumi.Input[str]]=None, storage_account_required: Optional[pulumi.Input[bool]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_network_subnet_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        A web app, a mobile app backend, or an API app.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] client_affinity_enabled: <code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests in the same session to the same instance. Default is <code>true</code>.
        :param pulumi.Input[bool] client_cert_enabled: <code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is <code>false</code>.
        :param pulumi.Input[str] client_cert_exclusion_paths: client certificate authentication comma-separated exclusion paths
        :param pulumi.Input['ClientCertMode'] client_cert_mode: This composes with ClientCertEnabled setting.
               - ClientCertEnabled: false means ClientCert is ignored.
               - ClientCertEnabled: true and ClientCertMode: Required means ClientCert is required.
               - ClientCertEnabled: true and ClientCertMode: Optional means ClientCert is optional or accepted.
        :param pulumi.Input[pulumi.InputType['CloningInfoArgs']] cloning_info: If specified during app creation, the app is cloned from a source app.
        :param pulumi.Input[int] container_size: Size of the function container.
        :param pulumi.Input[str] custom_domain_verification_id: Unique identifier that verifies the custom domains assigned to the app. Customer will add this id to a txt record for verification.
        :param pulumi.Input[int] daily_memory_time_quota: Maximum allowed daily memory-time quota (applicable on dynamic apps only).
        :param pulumi.Input[bool] enabled: <code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app offline).
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: Extended Location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostNameSslStateArgs']]]] host_name_ssl_states: Hostname SSL states are used to manage the SSL bindings for app's hostnames.
        :param pulumi.Input[bool] host_names_disabled: <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
                If <code>true</code>, the app is only accessible via API management process.
        :param pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']] hosting_environment_profile: App Service Environment to use for the app.
        :param pulumi.Input[bool] https_only: HttpsOnly: configures a web site to accept only https requests. Issues redirect for
               http requests
        :param pulumi.Input[bool] hyper_v: Hyper-V sandbox.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: Managed service identity.
        :param pulumi.Input[bool] is_xenon: Obsolete: Hyper-V sandbox.
        :param pulumi.Input[str] key_vault_reference_identity: Identity to use for Key Vault Reference authentication.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Unique name of the app to create or update. To create or update a deployment slot, use the {slot} parameter.
        :param pulumi.Input['RedundancyMode'] redundancy_mode: Site redundancy mode
        :param pulumi.Input[bool] reserved: <code>true</code> if reserved; otherwise, <code>false</code>.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[bool] scm_site_also_stopped: <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
        :param pulumi.Input[str] server_farm_id: Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        :param pulumi.Input[pulumi.InputType['SiteConfigArgs']] site_config: Configuration of the app.
        :param pulumi.Input[str] slot: Name of the deployment slot to create or update. By default, this API attempts to create or modify the production slot.
        :param pulumi.Input[bool] storage_account_required: Checks if Customer provided storage account is required
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] virtual_network_subnet_id: Azure Resource Manager ID of the Virtual network and subnet to be joined by Regional VNET Integration.
               This must be of the form /subscriptions/{subscriptionName}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WebAppSlotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A web app, a mobile app backend, or an API app.

        :param str resource_name: The name of the resource.
        :param WebAppSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(WebAppSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_affinity_enabled: Optional[pulumi.Input[bool]]=None, client_cert_enabled: Optional[pulumi.Input[bool]]=None, client_cert_exclusion_paths: Optional[pulumi.Input[str]]=None, client_cert_mode: Optional[pulumi.Input['ClientCertMode']]=None, cloning_info: Optional[pulumi.Input[pulumi.InputType['CloningInfoArgs']]]=None, container_size: Optional[pulumi.Input[int]]=None, custom_domain_verification_id: Optional[pulumi.Input[str]]=None, daily_memory_time_quota: Optional[pulumi.Input[int]]=None, enabled: Optional[pulumi.Input[bool]]=None, extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]]=None, host_name_ssl_states: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostNameSslStateArgs']]]]]=None, host_names_disabled: Optional[pulumi.Input[bool]]=None, hosting_environment_profile: Optional[pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']]]=None, https_only: Optional[pulumi.Input[bool]]=None, hyper_v: Optional[pulumi.Input[bool]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, is_xenon: Optional[pulumi.Input[bool]]=None, key_vault_reference_identity: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, redundancy_mode: Optional[pulumi.Input['RedundancyMode']]=None, reserved: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, scm_site_also_stopped: Optional[pulumi.Input[bool]]=None, server_farm_id: Optional[pulumi.Input[str]]=None, site_config: Optional[pulumi.Input[pulumi.InputType['SiteConfigArgs']]]=None, slot: Optional[pulumi.Input[str]]=None, storage_account_required: Optional[pulumi.Input[bool]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_network_subnet_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebAppSlotArgs.__new__(WebAppSlotArgs)
            __props__.__dict__['client_affinity_enabled'] = client_affinity_enabled
            __props__.__dict__['client_cert_enabled'] = client_cert_enabled
            __props__.__dict__['client_cert_exclusion_paths'] = client_cert_exclusion_paths
            __props__.__dict__['client_cert_mode'] = client_cert_mode
            __props__.__dict__['cloning_info'] = cloning_info
            __props__.__dict__['container_size'] = container_size
            __props__.__dict__['custom_domain_verification_id'] = custom_domain_verification_id
            __props__.__dict__['daily_memory_time_quota'] = daily_memory_time_quota
            __props__.__dict__['enabled'] = enabled
            __props__.__dict__['extended_location'] = extended_location
            __props__.__dict__['host_name_ssl_states'] = host_name_ssl_states
            __props__.__dict__['host_names_disabled'] = host_names_disabled
            __props__.__dict__['hosting_environment_profile'] = hosting_environment_profile
            __props__.__dict__['https_only'] = https_only
            if hyper_v is None:
                hyper_v = False
            __props__.__dict__['hyper_v'] = hyper_v
            __props__.__dict__['identity'] = identity
            if is_xenon is None:
                is_xenon = False
            __props__.__dict__['is_xenon'] = is_xenon
            __props__.__dict__['key_vault_reference_identity'] = key_vault_reference_identity
            __props__.__dict__['kind'] = kind
            __props__.__dict__['location'] = location
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['redundancy_mode'] = redundancy_mode
            if reserved is None:
                reserved = False
            __props__.__dict__['reserved'] = reserved
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if scm_site_also_stopped is None:
                scm_site_also_stopped = False
            __props__.__dict__['scm_site_also_stopped'] = scm_site_also_stopped
            __props__.__dict__['server_farm_id'] = server_farm_id
            __props__.__dict__['site_config'] = site_config
            __props__.__dict__['slot'] = slot
            __props__.__dict__['storage_account_required'] = storage_account_required
            __props__.__dict__['tags'] = tags
            __props__.__dict__['virtual_network_subnet_id'] = virtual_network_subnet_id
            __props__.__dict__['availability_state'] = None
            __props__.__dict__['default_host_name'] = None
            __props__.__dict__['enabled_host_names'] = None
            __props__.__dict__['host_names'] = None
            __props__.__dict__['in_progress_operation_id'] = None
            __props__.__dict__['is_default_container'] = None
            __props__.__dict__['last_modified_time_utc'] = None
            __props__.__dict__['max_number_of_workers'] = None
            __props__.__dict__['outbound_ip_addresses'] = None
            __props__.__dict__['possible_outbound_ip_addresses'] = None
            __props__.__dict__['repository_site_name'] = None
            __props__.__dict__['resource_group'] = None
            __props__.__dict__['slot_swap_status'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['suspended_till'] = None
            __props__.__dict__['target_swap_slot'] = None
            __props__.__dict__['traffic_manager_host_names'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['usage_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:web:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20150801:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20160801:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20180201:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20181101:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20190801:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20200601:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20200901:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20201001:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20201201:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20210101:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20210115:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20210301:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20220301:WebAppSlot'), pulumi.Alias(type_='azure-native:web/v20220901:WebAppSlot')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSlot, __self__).__init__('azure-native:web/v20210201:WebAppSlot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'WebAppSlot':
        """
        Get an existing WebAppSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = WebAppSlotArgs.__new__(WebAppSlotArgs)
        __props__.__dict__['availability_state'] = None
        __props__.__dict__['client_affinity_enabled'] = None
        __props__.__dict__['client_cert_enabled'] = None
        __props__.__dict__['client_cert_exclusion_paths'] = None
        __props__.__dict__['client_cert_mode'] = None
        __props__.__dict__['container_size'] = None
        __props__.__dict__['custom_domain_verification_id'] = None
        __props__.__dict__['daily_memory_time_quota'] = None
        __props__.__dict__['default_host_name'] = None
        __props__.__dict__['enabled'] = None
        __props__.__dict__['enabled_host_names'] = None
        __props__.__dict__['extended_location'] = None
        __props__.__dict__['host_name_ssl_states'] = None
        __props__.__dict__['host_names'] = None
        __props__.__dict__['host_names_disabled'] = None
        __props__.__dict__['hosting_environment_profile'] = None
        __props__.__dict__['https_only'] = None
        __props__.__dict__['hyper_v'] = None
        __props__.__dict__['identity'] = None
        __props__.__dict__['in_progress_operation_id'] = None
        __props__.__dict__['is_default_container'] = None
        __props__.__dict__['is_xenon'] = None
        __props__.__dict__['key_vault_reference_identity'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['last_modified_time_utc'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['max_number_of_workers'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['outbound_ip_addresses'] = None
        __props__.__dict__['possible_outbound_ip_addresses'] = None
        __props__.__dict__['redundancy_mode'] = None
        __props__.__dict__['repository_site_name'] = None
        __props__.__dict__['reserved'] = None
        __props__.__dict__['resource_group'] = None
        __props__.__dict__['scm_site_also_stopped'] = None
        __props__.__dict__['server_farm_id'] = None
        __props__.__dict__['site_config'] = None
        __props__.__dict__['slot_swap_status'] = None
        __props__.__dict__['state'] = None
        __props__.__dict__['storage_account_required'] = None
        __props__.__dict__['suspended_till'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['target_swap_slot'] = None
        __props__.__dict__['traffic_manager_host_names'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['usage_state'] = None
        __props__.__dict__['virtual_network_subnet_id'] = None
        return WebAppSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='availabilityState')
    def availability_state(self) -> pulumi.Output[str]:
        """
        Management information availability state for the app.
        """
        return pulumi.get(self, 'availability_state')

    @property
    @pulumi.getter(name='clientAffinityEnabled')
    def client_affinity_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> to enable client affinity; <code>false</code> to stop sending session affinity cookies, which route client requests in the same session to the same instance. Default is <code>true</code>.
        """
        return pulumi.get(self, 'client_affinity_enabled')

    @property
    @pulumi.getter(name='clientCertEnabled')
    def client_cert_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> to enable client certificate authentication (TLS mutual authentication); otherwise, <code>false</code>. Default is <code>false</code>.
        """
        return pulumi.get(self, 'client_cert_enabled')

    @property
    @pulumi.getter(name='clientCertExclusionPaths')
    def client_cert_exclusion_paths(self) -> pulumi.Output[Optional[str]]:
        """
        client certificate authentication comma-separated exclusion paths
        """
        return pulumi.get(self, 'client_cert_exclusion_paths')

    @property
    @pulumi.getter(name='clientCertMode')
    def client_cert_mode(self) -> pulumi.Output[Optional[str]]:
        """
        This composes with ClientCertEnabled setting.
        - ClientCertEnabled: false means ClientCert is ignored.
        - ClientCertEnabled: true and ClientCertMode: Required means ClientCert is required.
        - ClientCertEnabled: true and ClientCertMode: Optional means ClientCert is optional or accepted.
        """
        return pulumi.get(self, 'client_cert_mode')

    @property
    @pulumi.getter(name='containerSize')
    def container_size(self) -> pulumi.Output[Optional[int]]:
        """
        Size of the function container.
        """
        return pulumi.get(self, 'container_size')

    @property
    @pulumi.getter(name='customDomainVerificationId')
    def custom_domain_verification_id(self) -> pulumi.Output[Optional[str]]:
        """
        Unique identifier that verifies the custom domains assigned to the app. Customer will add this id to a txt record for verification.
        """
        return pulumi.get(self, 'custom_domain_verification_id')

    @property
    @pulumi.getter(name='dailyMemoryTimeQuota')
    def daily_memory_time_quota(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum allowed daily memory-time quota (applicable on dynamic apps only).
        """
        return pulumi.get(self, 'daily_memory_time_quota')

    @property
    @pulumi.getter(name='defaultHostName')
    def default_host_name(self) -> pulumi.Output[str]:
        """
        Default hostname of the app. Read-only.
        """
        return pulumi.get(self, 'default_host_name')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> if the app is enabled; otherwise, <code>false</code>. Setting this value to false disables the app (takes the app offline).
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter(name='enabledHostNames')
    def enabled_host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        Enabled hostnames for the app.Hostnames need to be assigned (see HostNames) AND enabled. Otherwise,
        the app is not served on those hostnames.
        """
        return pulumi.get(self, 'enabled_host_names')

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> pulumi.Output[Optional['outputs.ExtendedLocationResponse']]:
        """
        Extended Location.
        """
        return pulumi.get(self, 'extended_location')

    @property
    @pulumi.getter(name='hostNameSslStates')
    def host_name_ssl_states(self) -> pulumi.Output[Optional[Sequence['outputs.HostNameSslStateResponse']]]:
        """
        Hostname SSL states are used to manage the SSL bindings for app's hostnames.
        """
        return pulumi.get(self, 'host_name_ssl_states')

    @property
    @pulumi.getter(name='hostNames')
    def host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        Hostnames associated with the app.
        """
        return pulumi.get(self, 'host_names')

    @property
    @pulumi.getter(name='hostNamesDisabled')
    def host_names_disabled(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> to disable the public hostnames of the app; otherwise, <code>false</code>.
         If <code>true</code>, the app is only accessible via API management process.
        """
        return pulumi.get(self, 'host_names_disabled')

    @property
    @pulumi.getter(name='hostingEnvironmentProfile')
    def hosting_environment_profile(self) -> pulumi.Output[Optional['outputs.HostingEnvironmentProfileResponse']]:
        """
        App Service Environment to use for the app.
        """
        return pulumi.get(self, 'hosting_environment_profile')

    @property
    @pulumi.getter(name='httpsOnly')
    def https_only(self) -> pulumi.Output[Optional[bool]]:
        """
        HttpsOnly: configures a web site to accept only https requests. Issues redirect for
        http requests
        """
        return pulumi.get(self, 'https_only')

    @property
    @pulumi.getter(name='hyperV')
    def hyper_v(self) -> pulumi.Output[Optional[bool]]:
        """
        Hyper-V sandbox.
        """
        return pulumi.get(self, 'hyper_v')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        Managed service identity.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter(name='inProgressOperationId')
    def in_progress_operation_id(self) -> pulumi.Output[str]:
        """
        Specifies an operation id if this site has a pending operation.
        """
        return pulumi.get(self, 'in_progress_operation_id')

    @property
    @pulumi.getter(name='isDefaultContainer')
    def is_default_container(self) -> pulumi.Output[bool]:
        """
        <code>true</code> if the app is a default container; otherwise, <code>false</code>.
        """
        return pulumi.get(self, 'is_default_container')

    @property
    @pulumi.getter(name='isXenon')
    def is_xenon(self) -> pulumi.Output[Optional[bool]]:
        """
        Obsolete: Hyper-V sandbox.
        """
        return pulumi.get(self, 'is_xenon')

    @property
    @pulumi.getter(name='keyVaultReferenceIdentity')
    def key_vault_reference_identity(self) -> pulumi.Output[Optional[str]]:
        """
        Identity to use for Key Vault Reference authentication.
        """
        return pulumi.get(self, 'key_vault_reference_identity')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='lastModifiedTimeUtc')
    def last_modified_time_utc(self) -> pulumi.Output[str]:
        """
        Last time the app was modified, in UTC. Read-only.
        """
        return pulumi.get(self, 'last_modified_time_utc')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='maxNumberOfWorkers')
    def max_number_of_workers(self) -> pulumi.Output[int]:
        """
        Maximum number of workers.
        This only applies to Functions container.
        """
        return pulumi.get(self, 'max_number_of_workers')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='outboundIpAddresses')
    def outbound_ip_addresses(self) -> pulumi.Output[str]:
        """
        List of IP addresses that the app uses for outbound connections (e.g. database access). Includes VIPs from tenants that site can be hosted with current settings. Read-only.
        """
        return pulumi.get(self, 'outbound_ip_addresses')

    @property
    @pulumi.getter(name='possibleOutboundIpAddresses')
    def possible_outbound_ip_addresses(self) -> pulumi.Output[str]:
        """
        List of IP addresses that the app uses for outbound connections (e.g. database access). Includes VIPs from all tenants except dataComponent. Read-only.
        """
        return pulumi.get(self, 'possible_outbound_ip_addresses')

    @property
    @pulumi.getter(name='redundancyMode')
    def redundancy_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Site redundancy mode
        """
        return pulumi.get(self, 'redundancy_mode')

    @property
    @pulumi.getter(name='repositorySiteName')
    def repository_site_name(self) -> pulumi.Output[str]:
        """
        Name of the repository site.
        """
        return pulumi.get(self, 'repository_site_name')

    @property
    @pulumi.getter
    def reserved(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> if reserved; otherwise, <code>false</code>.
        """
        return pulumi.get(self, 'reserved')

    @property
    @pulumi.getter(name='resourceGroup')
    def resource_group(self) -> pulumi.Output[str]:
        """
        Name of the resource group the app belongs to. Read-only.
        """
        return pulumi.get(self, 'resource_group')

    @property
    @pulumi.getter(name='scmSiteAlsoStopped')
    def scm_site_also_stopped(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> to stop SCM (KUDU) site when the app is stopped; otherwise, <code>false</code>. The default is <code>false</code>.
        """
        return pulumi.get(self, 'scm_site_also_stopped')

    @property
    @pulumi.getter(name='serverFarmId')
    def server_farm_id(self) -> pulumi.Output[Optional[str]]:
        """
        Resource ID of the associated App Service plan, formatted as: "/subscriptions/{subscriptionID}/resourceGroups/{groupName}/providers/Microsoft.Web/serverfarms/{appServicePlanName}".
        """
        return pulumi.get(self, 'server_farm_id')

    @property
    @pulumi.getter(name='siteConfig')
    def site_config(self) -> pulumi.Output[Optional['outputs.SiteConfigResponse']]:
        """
        Configuration of the app.
        """
        return pulumi.get(self, 'site_config')

    @property
    @pulumi.getter(name='slotSwapStatus')
    def slot_swap_status(self) -> pulumi.Output['outputs.SlotSwapStatusResponse']:
        """
        Status of the last deployment slot swap operation.
        """
        return pulumi.get(self, 'slot_swap_status')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        Current state of the app.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='storageAccountRequired')
    def storage_account_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Checks if Customer provided storage account is required
        """
        return pulumi.get(self, 'storage_account_required')

    @property
    @pulumi.getter(name='suspendedTill')
    def suspended_till(self) -> pulumi.Output[str]:
        """
        App suspended till in case memory-time quota is exceeded.
        """
        return pulumi.get(self, 'suspended_till')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='targetSwapSlot')
    def target_swap_slot(self) -> pulumi.Output[str]:
        """
        Specifies which deployment slot this app will swap into. Read-only.
        """
        return pulumi.get(self, 'target_swap_slot')

    @property
    @pulumi.getter(name='trafficManagerHostNames')
    def traffic_manager_host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        Azure Traffic Manager hostnames associated with the app. Read-only.
        """
        return pulumi.get(self, 'traffic_manager_host_names')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='usageState')
    def usage_state(self) -> pulumi.Output[str]:
        """
        State indicating whether the app has exceeded its quota usage. Read-only.
        """
        return pulumi.get(self, 'usage_state')

    @property
    @pulumi.getter(name='virtualNetworkSubnetId')
    def virtual_network_subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        Azure Resource Manager ID of the Virtual network and subnet to be joined by Regional VNET Integration.
        This must be of the form /subscriptions/{subscriptionName}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualNetworks/{vnetName}/subnets/{subnetName}
        """
        return pulumi.get(self, 'virtual_network_subnet_id')
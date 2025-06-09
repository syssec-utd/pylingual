import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ManagedClusterArgs', 'ManagedCluster']

@pulumi.input_type
class ManagedClusterArgs:

    def __init__(__self__, *, admin_user_name: pulumi.Input[str], dns_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]]]=None, admin_password: Optional[pulumi.Input[str]]=None, allow_rdp_access: Optional[pulumi.Input[bool]]=None, application_type_versions_cleanup_policy: Optional[pulumi.Input['ApplicationTypeVersionsCleanupPolicyArgs']]=None, auxiliary_subnets: Optional[pulumi.Input[Sequence[pulumi.Input['SubnetArgs']]]]=None, azure_active_directory: Optional[pulumi.Input['AzureActiveDirectoryArgs']]=None, client_connection_port: Optional[pulumi.Input[int]]=None, clients: Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]]=None, cluster_code_version: Optional[pulumi.Input[str]]=None, cluster_name: Optional[pulumi.Input[str]]=None, cluster_upgrade_cadence: Optional[pulumi.Input[Union[str, 'ClusterUpgradeCadence']]]=None, cluster_upgrade_mode: Optional[pulumi.Input[Union[str, 'ClusterUpgradeMode']]]=None, enable_auto_os_upgrade: Optional[pulumi.Input[bool]]=None, enable_ipv6: Optional[pulumi.Input[bool]]=None, enable_service_public_ip: Optional[pulumi.Input[bool]]=None, fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]]=None, http_gateway_connection_port: Optional[pulumi.Input[int]]=None, ip_tags: Optional[pulumi.Input[Sequence[pulumi.Input['IPTagArgs']]]]=None, load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]=None, location: Optional[pulumi.Input[str]]=None, network_security_rules: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkSecurityRuleArgs']]]]=None, service_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceEndpointArgs']]]]=None, sku: Optional[pulumi.Input['SkuArgs']]=None, subnet_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zonal_resiliency: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a ManagedCluster resource.
        :param pulumi.Input[str] admin_user_name: VM admin user name.
        :param pulumi.Input[str] dns_name: The cluster dns name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]] addon_features: List of add-on features to enable on the cluster.
        :param pulumi.Input[str] admin_password: VM admin user password.
        :param pulumi.Input[bool] allow_rdp_access: Setting this to true enables RDP access to the VM. The default NSG rule opens RDP port to Internet which can be overridden with custom Network Security Rules. The default value for this setting is false.
        :param pulumi.Input['ApplicationTypeVersionsCleanupPolicyArgs'] application_type_versions_cleanup_policy: The policy used to clean up unused versions.
        :param pulumi.Input[Sequence[pulumi.Input['SubnetArgs']]] auxiliary_subnets: Auxiliary subnets for the cluster.
        :param pulumi.Input['AzureActiveDirectoryArgs'] azure_active_directory: The AAD authentication settings of the cluster.
        :param pulumi.Input[int] client_connection_port: The port used for client connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]] clients: Client certificates that are allowed to manage the cluster.
        :param pulumi.Input[str] cluster_code_version: The Service Fabric runtime version of the cluster. This property is required when **clusterUpgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[Union[str, 'ClusterUpgradeCadence']] cluster_upgrade_cadence: Indicates when new cluster runtime version upgrades will be applied after they are released. By default is Wave0. Only applies when **clusterUpgradeMode** is set to 'Automatic'.
        :param pulumi.Input[Union[str, 'ClusterUpgradeMode']] cluster_upgrade_mode: The upgrade mode of the cluster when new Service Fabric runtime version is available.
        :param pulumi.Input[bool] enable_auto_os_upgrade: Setting this to true enables automatic OS upgrade for the node types that are created using any platform OS image with version 'latest'. The default value for this setting is false.
        :param pulumi.Input[bool] enable_ipv6: Setting this to true creates IPv6 address space for the default VNet used by the cluster. This setting cannot be changed once the cluster is created. The default value for this setting is false.
        :param pulumi.Input[bool] enable_service_public_ip: Setting this to true will link the IPv4 address as the ServicePublicIP of the IPv6 address. It can only be set to True if IPv6 is enabled on the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]] fabric_settings: The list of custom fabric settings to configure the cluster.
        :param pulumi.Input[int] http_gateway_connection_port: The port used for HTTP connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['IPTagArgs']]] ip_tags: The list of IP tags associated with the default public IP address of the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]] load_balancing_rules: Load balancing rules that are applied to the public load balancer of the cluster.
        :param pulumi.Input[str] location: Azure resource location.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkSecurityRuleArgs']]] network_security_rules: Custom Network Security Rules that are applied to the Virtual Network of the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['ServiceEndpointArgs']]] service_endpoints: Service endpoints for subnets in the cluster.
        :param pulumi.Input['SkuArgs'] sku: The sku of the managed cluster
        :param pulumi.Input[str] subnet_id: If specified, the node types for the cluster are created in this subnet instead of the default VNet. The **networkSecurityRules** specified for the cluster are also applied to this subnet. This setting cannot be changed once the cluster is created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        :param pulumi.Input[bool] zonal_resiliency: Indicates if the cluster has zone resiliency.
        """
        pulumi.set(__self__, 'admin_user_name', admin_user_name)
        pulumi.set(__self__, 'dns_name', dns_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if addon_features is not None:
            pulumi.set(__self__, 'addon_features', addon_features)
        if admin_password is not None:
            pulumi.set(__self__, 'admin_password', admin_password)
        if allow_rdp_access is not None:
            pulumi.set(__self__, 'allow_rdp_access', allow_rdp_access)
        if application_type_versions_cleanup_policy is not None:
            pulumi.set(__self__, 'application_type_versions_cleanup_policy', application_type_versions_cleanup_policy)
        if auxiliary_subnets is not None:
            pulumi.set(__self__, 'auxiliary_subnets', auxiliary_subnets)
        if azure_active_directory is not None:
            pulumi.set(__self__, 'azure_active_directory', azure_active_directory)
        if client_connection_port is None:
            client_connection_port = 19000
        if client_connection_port is not None:
            pulumi.set(__self__, 'client_connection_port', client_connection_port)
        if clients is not None:
            pulumi.set(__self__, 'clients', clients)
        if cluster_code_version is not None:
            pulumi.set(__self__, 'cluster_code_version', cluster_code_version)
        if cluster_name is not None:
            pulumi.set(__self__, 'cluster_name', cluster_name)
        if cluster_upgrade_cadence is not None:
            pulumi.set(__self__, 'cluster_upgrade_cadence', cluster_upgrade_cadence)
        if cluster_upgrade_mode is not None:
            pulumi.set(__self__, 'cluster_upgrade_mode', cluster_upgrade_mode)
        if enable_auto_os_upgrade is not None:
            pulumi.set(__self__, 'enable_auto_os_upgrade', enable_auto_os_upgrade)
        if enable_ipv6 is not None:
            pulumi.set(__self__, 'enable_ipv6', enable_ipv6)
        if enable_service_public_ip is not None:
            pulumi.set(__self__, 'enable_service_public_ip', enable_service_public_ip)
        if fabric_settings is not None:
            pulumi.set(__self__, 'fabric_settings', fabric_settings)
        if http_gateway_connection_port is None:
            http_gateway_connection_port = 19080
        if http_gateway_connection_port is not None:
            pulumi.set(__self__, 'http_gateway_connection_port', http_gateway_connection_port)
        if ip_tags is not None:
            pulumi.set(__self__, 'ip_tags', ip_tags)
        if load_balancing_rules is not None:
            pulumi.set(__self__, 'load_balancing_rules', load_balancing_rules)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if network_security_rules is not None:
            pulumi.set(__self__, 'network_security_rules', network_security_rules)
        if service_endpoints is not None:
            pulumi.set(__self__, 'service_endpoints', service_endpoints)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if subnet_id is not None:
            pulumi.set(__self__, 'subnet_id', subnet_id)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zonal_resiliency is None:
            zonal_resiliency = False
        if zonal_resiliency is not None:
            pulumi.set(__self__, 'zonal_resiliency', zonal_resiliency)

    @property
    @pulumi.getter(name='adminUserName')
    def admin_user_name(self) -> pulumi.Input[str]:
        """
        VM admin user name.
        """
        return pulumi.get(self, 'admin_user_name')

    @admin_user_name.setter
    def admin_user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'admin_user_name', value)

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> pulumi.Input[str]:
        """
        The cluster dns name.
        """
        return pulumi.get(self, 'dns_name')

    @dns_name.setter
    def dns_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'dns_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='addonFeatures')
    def addon_features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]]]:
        """
        List of add-on features to enable on the cluster.
        """
        return pulumi.get(self, 'addon_features')

    @addon_features.setter
    def addon_features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]]]):
        pulumi.set(self, 'addon_features', value)

    @property
    @pulumi.getter(name='adminPassword')
    def admin_password(self) -> Optional[pulumi.Input[str]]:
        """
        VM admin user password.
        """
        return pulumi.get(self, 'admin_password')

    @admin_password.setter
    def admin_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'admin_password', value)

    @property
    @pulumi.getter(name='allowRdpAccess')
    def allow_rdp_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Setting this to true enables RDP access to the VM. The default NSG rule opens RDP port to Internet which can be overridden with custom Network Security Rules. The default value for this setting is false.
        """
        return pulumi.get(self, 'allow_rdp_access')

    @allow_rdp_access.setter
    def allow_rdp_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'allow_rdp_access', value)

    @property
    @pulumi.getter(name='applicationTypeVersionsCleanupPolicy')
    def application_type_versions_cleanup_policy(self) -> Optional[pulumi.Input['ApplicationTypeVersionsCleanupPolicyArgs']]:
        """
        The policy used to clean up unused versions.
        """
        return pulumi.get(self, 'application_type_versions_cleanup_policy')

    @application_type_versions_cleanup_policy.setter
    def application_type_versions_cleanup_policy(self, value: Optional[pulumi.Input['ApplicationTypeVersionsCleanupPolicyArgs']]):
        pulumi.set(self, 'application_type_versions_cleanup_policy', value)

    @property
    @pulumi.getter(name='auxiliarySubnets')
    def auxiliary_subnets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SubnetArgs']]]]:
        """
        Auxiliary subnets for the cluster.
        """
        return pulumi.get(self, 'auxiliary_subnets')

    @auxiliary_subnets.setter
    def auxiliary_subnets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SubnetArgs']]]]):
        pulumi.set(self, 'auxiliary_subnets', value)

    @property
    @pulumi.getter(name='azureActiveDirectory')
    def azure_active_directory(self) -> Optional[pulumi.Input['AzureActiveDirectoryArgs']]:
        """
        The AAD authentication settings of the cluster.
        """
        return pulumi.get(self, 'azure_active_directory')

    @azure_active_directory.setter
    def azure_active_directory(self, value: Optional[pulumi.Input['AzureActiveDirectoryArgs']]):
        pulumi.set(self, 'azure_active_directory', value)

    @property
    @pulumi.getter(name='clientConnectionPort')
    def client_connection_port(self) -> Optional[pulumi.Input[int]]:
        """
        The port used for client connections to the cluster.
        """
        return pulumi.get(self, 'client_connection_port')

    @client_connection_port.setter
    def client_connection_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'client_connection_port', value)

    @property
    @pulumi.getter
    def clients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]]:
        """
        Client certificates that are allowed to manage the cluster.
        """
        return pulumi.get(self, 'clients')

    @clients.setter
    def clients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]]):
        pulumi.set(self, 'clients', value)

    @property
    @pulumi.getter(name='clusterCodeVersion')
    def cluster_code_version(self) -> Optional[pulumi.Input[str]]:
        """
        The Service Fabric runtime version of the cluster. This property is required when **clusterUpgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        """
        return pulumi.get(self, 'cluster_code_version')

    @cluster_code_version.setter
    def cluster_code_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cluster_code_version', value)

    @property
    @pulumi.getter(name='clusterName')
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cluster resource.
        """
        return pulumi.get(self, 'cluster_name')

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cluster_name', value)

    @property
    @pulumi.getter(name='clusterUpgradeCadence')
    def cluster_upgrade_cadence(self) -> Optional[pulumi.Input[Union[str, 'ClusterUpgradeCadence']]]:
        """
        Indicates when new cluster runtime version upgrades will be applied after they are released. By default is Wave0. Only applies when **clusterUpgradeMode** is set to 'Automatic'.
        """
        return pulumi.get(self, 'cluster_upgrade_cadence')

    @cluster_upgrade_cadence.setter
    def cluster_upgrade_cadence(self, value: Optional[pulumi.Input[Union[str, 'ClusterUpgradeCadence']]]):
        pulumi.set(self, 'cluster_upgrade_cadence', value)

    @property
    @pulumi.getter(name='clusterUpgradeMode')
    def cluster_upgrade_mode(self) -> Optional[pulumi.Input[Union[str, 'ClusterUpgradeMode']]]:
        """
        The upgrade mode of the cluster when new Service Fabric runtime version is available.
        """
        return pulumi.get(self, 'cluster_upgrade_mode')

    @cluster_upgrade_mode.setter
    def cluster_upgrade_mode(self, value: Optional[pulumi.Input[Union[str, 'ClusterUpgradeMode']]]):
        pulumi.set(self, 'cluster_upgrade_mode', value)

    @property
    @pulumi.getter(name='enableAutoOSUpgrade')
    def enable_auto_os_upgrade(self) -> Optional[pulumi.Input[bool]]:
        """
        Setting this to true enables automatic OS upgrade for the node types that are created using any platform OS image with version 'latest'. The default value for this setting is false.
        """
        return pulumi.get(self, 'enable_auto_os_upgrade')

    @enable_auto_os_upgrade.setter
    def enable_auto_os_upgrade(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_auto_os_upgrade', value)

    @property
    @pulumi.getter(name='enableIpv6')
    def enable_ipv6(self) -> Optional[pulumi.Input[bool]]:
        """
        Setting this to true creates IPv6 address space for the default VNet used by the cluster. This setting cannot be changed once the cluster is created. The default value for this setting is false.
        """
        return pulumi.get(self, 'enable_ipv6')

    @enable_ipv6.setter
    def enable_ipv6(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_ipv6', value)

    @property
    @pulumi.getter(name='enableServicePublicIP')
    def enable_service_public_ip(self) -> Optional[pulumi.Input[bool]]:
        """
        Setting this to true will link the IPv4 address as the ServicePublicIP of the IPv6 address. It can only be set to True if IPv6 is enabled on the cluster.
        """
        return pulumi.get(self, 'enable_service_public_ip')

    @enable_service_public_ip.setter
    def enable_service_public_ip(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_service_public_ip', value)

    @property
    @pulumi.getter(name='fabricSettings')
    def fabric_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]]:
        """
        The list of custom fabric settings to configure the cluster.
        """
        return pulumi.get(self, 'fabric_settings')

    @fabric_settings.setter
    def fabric_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]]):
        pulumi.set(self, 'fabric_settings', value)

    @property
    @pulumi.getter(name='httpGatewayConnectionPort')
    def http_gateway_connection_port(self) -> Optional[pulumi.Input[int]]:
        """
        The port used for HTTP connections to the cluster.
        """
        return pulumi.get(self, 'http_gateway_connection_port')

    @http_gateway_connection_port.setter
    def http_gateway_connection_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'http_gateway_connection_port', value)

    @property
    @pulumi.getter(name='ipTags')
    def ip_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IPTagArgs']]]]:
        """
        The list of IP tags associated with the default public IP address of the cluster.
        """
        return pulumi.get(self, 'ip_tags')

    @ip_tags.setter
    def ip_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IPTagArgs']]]]):
        pulumi.set(self, 'ip_tags', value)

    @property
    @pulumi.getter(name='loadBalancingRules')
    def load_balancing_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]:
        """
        Load balancing rules that are applied to the public load balancer of the cluster.
        """
        return pulumi.get(self, 'load_balancing_rules')

    @load_balancing_rules.setter
    def load_balancing_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]):
        pulumi.set(self, 'load_balancing_rules', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='networkSecurityRules')
    def network_security_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkSecurityRuleArgs']]]]:
        """
        Custom Network Security Rules that are applied to the Virtual Network of the cluster.
        """
        return pulumi.get(self, 'network_security_rules')

    @network_security_rules.setter
    def network_security_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkSecurityRuleArgs']]]]):
        pulumi.set(self, 'network_security_rules', value)

    @property
    @pulumi.getter(name='serviceEndpoints')
    def service_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceEndpointArgs']]]]:
        """
        Service endpoints for subnets in the cluster.
        """
        return pulumi.get(self, 'service_endpoints')

    @service_endpoints.setter
    def service_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceEndpointArgs']]]]):
        pulumi.set(self, 'service_endpoints', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The sku of the managed cluster
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter(name='subnetId')
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        If specified, the node types for the cluster are created in this subnet instead of the default VNet. The **networkSecurityRules** specified for the cluster are also applied to this subnet. This setting cannot be changed once the cluster is created.
        """
        return pulumi.get(self, 'subnet_id')

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subnet_id', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='zonalResiliency')
    def zonal_resiliency(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if the cluster has zone resiliency.
        """
        return pulumi.get(self, 'zonal_resiliency')

    @zonal_resiliency.setter
    def zonal_resiliency(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'zonal_resiliency', value)

class ManagedCluster(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]]]=None, admin_password: Optional[pulumi.Input[str]]=None, admin_user_name: Optional[pulumi.Input[str]]=None, allow_rdp_access: Optional[pulumi.Input[bool]]=None, application_type_versions_cleanup_policy: Optional[pulumi.Input[pulumi.InputType['ApplicationTypeVersionsCleanupPolicyArgs']]]=None, auxiliary_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubnetArgs']]]]]=None, azure_active_directory: Optional[pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']]]=None, client_connection_port: Optional[pulumi.Input[int]]=None, clients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]]]=None, cluster_code_version: Optional[pulumi.Input[str]]=None, cluster_name: Optional[pulumi.Input[str]]=None, cluster_upgrade_cadence: Optional[pulumi.Input[Union[str, 'ClusterUpgradeCadence']]]=None, cluster_upgrade_mode: Optional[pulumi.Input[Union[str, 'ClusterUpgradeMode']]]=None, dns_name: Optional[pulumi.Input[str]]=None, enable_auto_os_upgrade: Optional[pulumi.Input[bool]]=None, enable_ipv6: Optional[pulumi.Input[bool]]=None, enable_service_public_ip: Optional[pulumi.Input[bool]]=None, fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]]]=None, http_gateway_connection_port: Optional[pulumi.Input[int]]=None, ip_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IPTagArgs']]]]]=None, load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, network_security_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkSecurityRuleArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceEndpointArgs']]]]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, subnet_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zonal_resiliency: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        The manged cluster resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]] addon_features: List of add-on features to enable on the cluster.
        :param pulumi.Input[str] admin_password: VM admin user password.
        :param pulumi.Input[str] admin_user_name: VM admin user name.
        :param pulumi.Input[bool] allow_rdp_access: Setting this to true enables RDP access to the VM. The default NSG rule opens RDP port to Internet which can be overridden with custom Network Security Rules. The default value for this setting is false.
        :param pulumi.Input[pulumi.InputType['ApplicationTypeVersionsCleanupPolicyArgs']] application_type_versions_cleanup_policy: The policy used to clean up unused versions.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubnetArgs']]]] auxiliary_subnets: Auxiliary subnets for the cluster.
        :param pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']] azure_active_directory: The AAD authentication settings of the cluster.
        :param pulumi.Input[int] client_connection_port: The port used for client connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]] clients: Client certificates that are allowed to manage the cluster.
        :param pulumi.Input[str] cluster_code_version: The Service Fabric runtime version of the cluster. This property is required when **clusterUpgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[Union[str, 'ClusterUpgradeCadence']] cluster_upgrade_cadence: Indicates when new cluster runtime version upgrades will be applied after they are released. By default is Wave0. Only applies when **clusterUpgradeMode** is set to 'Automatic'.
        :param pulumi.Input[Union[str, 'ClusterUpgradeMode']] cluster_upgrade_mode: The upgrade mode of the cluster when new Service Fabric runtime version is available.
        :param pulumi.Input[str] dns_name: The cluster dns name.
        :param pulumi.Input[bool] enable_auto_os_upgrade: Setting this to true enables automatic OS upgrade for the node types that are created using any platform OS image with version 'latest'. The default value for this setting is false.
        :param pulumi.Input[bool] enable_ipv6: Setting this to true creates IPv6 address space for the default VNet used by the cluster. This setting cannot be changed once the cluster is created. The default value for this setting is false.
        :param pulumi.Input[bool] enable_service_public_ip: Setting this to true will link the IPv4 address as the ServicePublicIP of the IPv6 address. It can only be set to True if IPv6 is enabled on the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]] fabric_settings: The list of custom fabric settings to configure the cluster.
        :param pulumi.Input[int] http_gateway_connection_port: The port used for HTTP connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IPTagArgs']]]] ip_tags: The list of IP tags associated with the default public IP address of the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]] load_balancing_rules: Load balancing rules that are applied to the public load balancer of the cluster.
        :param pulumi.Input[str] location: Azure resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkSecurityRuleArgs']]]] network_security_rules: Custom Network Security Rules that are applied to the Virtual Network of the cluster.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceEndpointArgs']]]] service_endpoints: Service endpoints for subnets in the cluster.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of the managed cluster
        :param pulumi.Input[str] subnet_id: If specified, the node types for the cluster are created in this subnet instead of the default VNet. The **networkSecurityRules** specified for the cluster are also applied to this subnet. This setting cannot be changed once the cluster is created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        :param pulumi.Input[bool] zonal_resiliency: Indicates if the cluster has zone resiliency.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ManagedClusterArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The manged cluster resource

        :param str resource_name: The name of the resource.
        :param ManagedClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ManagedClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ManagedClusterAddOnFeature']]]]]=None, admin_password: Optional[pulumi.Input[str]]=None, admin_user_name: Optional[pulumi.Input[str]]=None, allow_rdp_access: Optional[pulumi.Input[bool]]=None, application_type_versions_cleanup_policy: Optional[pulumi.Input[pulumi.InputType['ApplicationTypeVersionsCleanupPolicyArgs']]]=None, auxiliary_subnets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubnetArgs']]]]]=None, azure_active_directory: Optional[pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']]]=None, client_connection_port: Optional[pulumi.Input[int]]=None, clients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]]]=None, cluster_code_version: Optional[pulumi.Input[str]]=None, cluster_name: Optional[pulumi.Input[str]]=None, cluster_upgrade_cadence: Optional[pulumi.Input[Union[str, 'ClusterUpgradeCadence']]]=None, cluster_upgrade_mode: Optional[pulumi.Input[Union[str, 'ClusterUpgradeMode']]]=None, dns_name: Optional[pulumi.Input[str]]=None, enable_auto_os_upgrade: Optional[pulumi.Input[bool]]=None, enable_ipv6: Optional[pulumi.Input[bool]]=None, enable_service_public_ip: Optional[pulumi.Input[bool]]=None, fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]]]=None, http_gateway_connection_port: Optional[pulumi.Input[int]]=None, ip_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IPTagArgs']]]]]=None, load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, network_security_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkSecurityRuleArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceEndpointArgs']]]]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, subnet_id: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zonal_resiliency: Optional[pulumi.Input[bool]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagedClusterArgs.__new__(ManagedClusterArgs)
            __props__.__dict__['addon_features'] = addon_features
            __props__.__dict__['admin_password'] = admin_password
            if admin_user_name is None and (not opts.urn):
                raise TypeError("Missing required property 'admin_user_name'")
            __props__.__dict__['admin_user_name'] = admin_user_name
            __props__.__dict__['allow_rdp_access'] = allow_rdp_access
            __props__.__dict__['application_type_versions_cleanup_policy'] = application_type_versions_cleanup_policy
            __props__.__dict__['auxiliary_subnets'] = auxiliary_subnets
            __props__.__dict__['azure_active_directory'] = azure_active_directory
            if client_connection_port is None:
                client_connection_port = 19000
            __props__.__dict__['client_connection_port'] = client_connection_port
            __props__.__dict__['clients'] = clients
            __props__.__dict__['cluster_code_version'] = cluster_code_version
            __props__.__dict__['cluster_name'] = cluster_name
            __props__.__dict__['cluster_upgrade_cadence'] = cluster_upgrade_cadence
            __props__.__dict__['cluster_upgrade_mode'] = cluster_upgrade_mode
            if dns_name is None and (not opts.urn):
                raise TypeError("Missing required property 'dns_name'")
            __props__.__dict__['dns_name'] = dns_name
            __props__.__dict__['enable_auto_os_upgrade'] = enable_auto_os_upgrade
            __props__.__dict__['enable_ipv6'] = enable_ipv6
            __props__.__dict__['enable_service_public_ip'] = enable_service_public_ip
            __props__.__dict__['fabric_settings'] = fabric_settings
            if http_gateway_connection_port is None:
                http_gateway_connection_port = 19080
            __props__.__dict__['http_gateway_connection_port'] = http_gateway_connection_port
            __props__.__dict__['ip_tags'] = ip_tags
            __props__.__dict__['load_balancing_rules'] = load_balancing_rules
            __props__.__dict__['location'] = location
            __props__.__dict__['network_security_rules'] = network_security_rules
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['service_endpoints'] = service_endpoints
            __props__.__dict__['sku'] = sku
            __props__.__dict__['subnet_id'] = subnet_id
            __props__.__dict__['tags'] = tags
            if zonal_resiliency is None:
                zonal_resiliency = False
            __props__.__dict__['zonal_resiliency'] = zonal_resiliency
            __props__.__dict__['cluster_certificate_thumbprints'] = None
            __props__.__dict__['cluster_id'] = None
            __props__.__dict__['cluster_state'] = None
            __props__.__dict__['etag'] = None
            __props__.__dict__['fqdn'] = None
            __props__.__dict__['ipv4_address'] = None
            __props__.__dict__['ipv6_address'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:servicefabric:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20200101preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20210101preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20210501:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20210701preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20210901privatepreview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20211101preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20220101:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20220601preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20220801preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20221001preview:ManagedCluster'), pulumi.Alias(type_='azure-native:servicefabric/v20230201preview:ManagedCluster')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedCluster, __self__).__init__('azure-native:servicefabric/v20220201preview:ManagedCluster', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ManagedCluster':
        """
        Get an existing ManagedCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ManagedClusterArgs.__new__(ManagedClusterArgs)
        __props__.__dict__['addon_features'] = None
        __props__.__dict__['admin_password'] = None
        __props__.__dict__['admin_user_name'] = None
        __props__.__dict__['allow_rdp_access'] = None
        __props__.__dict__['application_type_versions_cleanup_policy'] = None
        __props__.__dict__['auxiliary_subnets'] = None
        __props__.__dict__['azure_active_directory'] = None
        __props__.__dict__['client_connection_port'] = None
        __props__.__dict__['clients'] = None
        __props__.__dict__['cluster_certificate_thumbprints'] = None
        __props__.__dict__['cluster_code_version'] = None
        __props__.__dict__['cluster_id'] = None
        __props__.__dict__['cluster_state'] = None
        __props__.__dict__['cluster_upgrade_cadence'] = None
        __props__.__dict__['cluster_upgrade_mode'] = None
        __props__.__dict__['dns_name'] = None
        __props__.__dict__['enable_auto_os_upgrade'] = None
        __props__.__dict__['enable_ipv6'] = None
        __props__.__dict__['enable_service_public_ip'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['fabric_settings'] = None
        __props__.__dict__['fqdn'] = None
        __props__.__dict__['http_gateway_connection_port'] = None
        __props__.__dict__['ip_tags'] = None
        __props__.__dict__['ipv4_address'] = None
        __props__.__dict__['ipv6_address'] = None
        __props__.__dict__['load_balancing_rules'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['network_security_rules'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['service_endpoints'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['subnet_id'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['zonal_resiliency'] = None
        return ManagedCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='addonFeatures')
    def addon_features(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of add-on features to enable on the cluster.
        """
        return pulumi.get(self, 'addon_features')

    @property
    @pulumi.getter(name='adminPassword')
    def admin_password(self) -> pulumi.Output[Optional[str]]:
        """
        VM admin user password.
        """
        return pulumi.get(self, 'admin_password')

    @property
    @pulumi.getter(name='adminUserName')
    def admin_user_name(self) -> pulumi.Output[str]:
        """
        VM admin user name.
        """
        return pulumi.get(self, 'admin_user_name')

    @property
    @pulumi.getter(name='allowRdpAccess')
    def allow_rdp_access(self) -> pulumi.Output[Optional[bool]]:
        """
        Setting this to true enables RDP access to the VM. The default NSG rule opens RDP port to Internet which can be overridden with custom Network Security Rules. The default value for this setting is false.
        """
        return pulumi.get(self, 'allow_rdp_access')

    @property
    @pulumi.getter(name='applicationTypeVersionsCleanupPolicy')
    def application_type_versions_cleanup_policy(self) -> pulumi.Output[Optional['outputs.ApplicationTypeVersionsCleanupPolicyResponse']]:
        """
        The policy used to clean up unused versions.
        """
        return pulumi.get(self, 'application_type_versions_cleanup_policy')

    @property
    @pulumi.getter(name='auxiliarySubnets')
    def auxiliary_subnets(self) -> pulumi.Output[Optional[Sequence['outputs.SubnetResponse']]]:
        """
        Auxiliary subnets for the cluster.
        """
        return pulumi.get(self, 'auxiliary_subnets')

    @property
    @pulumi.getter(name='azureActiveDirectory')
    def azure_active_directory(self) -> pulumi.Output[Optional['outputs.AzureActiveDirectoryResponse']]:
        """
        The AAD authentication settings of the cluster.
        """
        return pulumi.get(self, 'azure_active_directory')

    @property
    @pulumi.getter(name='clientConnectionPort')
    def client_connection_port(self) -> pulumi.Output[Optional[int]]:
        """
        The port used for client connections to the cluster.
        """
        return pulumi.get(self, 'client_connection_port')

    @property
    @pulumi.getter
    def clients(self) -> pulumi.Output[Optional[Sequence['outputs.ClientCertificateResponse']]]:
        """
        Client certificates that are allowed to manage the cluster.
        """
        return pulumi.get(self, 'clients')

    @property
    @pulumi.getter(name='clusterCertificateThumbprints')
    def cluster_certificate_thumbprints(self) -> pulumi.Output[Sequence[str]]:
        """
        List of thumbprints of the cluster certificates.
        """
        return pulumi.get(self, 'cluster_certificate_thumbprints')

    @property
    @pulumi.getter(name='clusterCodeVersion')
    def cluster_code_version(self) -> pulumi.Output[Optional[str]]:
        """
        The Service Fabric runtime version of the cluster. This property is required when **clusterUpgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        """
        return pulumi.get(self, 'cluster_code_version')

    @property
    @pulumi.getter(name='clusterId')
    def cluster_id(self) -> pulumi.Output[str]:
        """
        A service generated unique identifier for the cluster resource.
        """
        return pulumi.get(self, 'cluster_id')

    @property
    @pulumi.getter(name='clusterState')
    def cluster_state(self) -> pulumi.Output[str]:
        """
        The current state of the cluster.
        """
        return pulumi.get(self, 'cluster_state')

    @property
    @pulumi.getter(name='clusterUpgradeCadence')
    def cluster_upgrade_cadence(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates when new cluster runtime version upgrades will be applied after they are released. By default is Wave0. Only applies when **clusterUpgradeMode** is set to 'Automatic'.
        """
        return pulumi.get(self, 'cluster_upgrade_cadence')

    @property
    @pulumi.getter(name='clusterUpgradeMode')
    def cluster_upgrade_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The upgrade mode of the cluster when new Service Fabric runtime version is available.
        """
        return pulumi.get(self, 'cluster_upgrade_mode')

    @property
    @pulumi.getter(name='dnsName')
    def dns_name(self) -> pulumi.Output[str]:
        """
        The cluster dns name.
        """
        return pulumi.get(self, 'dns_name')

    @property
    @pulumi.getter(name='enableAutoOSUpgrade')
    def enable_auto_os_upgrade(self) -> pulumi.Output[Optional[bool]]:
        """
        Setting this to true enables automatic OS upgrade for the node types that are created using any platform OS image with version 'latest'. The default value for this setting is false.
        """
        return pulumi.get(self, 'enable_auto_os_upgrade')

    @property
    @pulumi.getter(name='enableIpv6')
    def enable_ipv6(self) -> pulumi.Output[Optional[bool]]:
        """
        Setting this to true creates IPv6 address space for the default VNet used by the cluster. This setting cannot be changed once the cluster is created. The default value for this setting is false.
        """
        return pulumi.get(self, 'enable_ipv6')

    @property
    @pulumi.getter(name='enableServicePublicIP')
    def enable_service_public_ip(self) -> pulumi.Output[Optional[bool]]:
        """
        Setting this to true will link the IPv4 address as the ServicePublicIP of the IPv6 address. It can only be set to True if IPv6 is enabled on the cluster.
        """
        return pulumi.get(self, 'enable_service_public_ip')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Azure resource etag.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='fabricSettings')
    def fabric_settings(self) -> pulumi.Output[Optional[Sequence['outputs.SettingsSectionDescriptionResponse']]]:
        """
        The list of custom fabric settings to configure the cluster.
        """
        return pulumi.get(self, 'fabric_settings')

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name associated with the public load balancer of the cluster.
        """
        return pulumi.get(self, 'fqdn')

    @property
    @pulumi.getter(name='httpGatewayConnectionPort')
    def http_gateway_connection_port(self) -> pulumi.Output[Optional[int]]:
        """
        The port used for HTTP connections to the cluster.
        """
        return pulumi.get(self, 'http_gateway_connection_port')

    @property
    @pulumi.getter(name='ipTags')
    def ip_tags(self) -> pulumi.Output[Optional[Sequence['outputs.IPTagResponse']]]:
        """
        The list of IP tags associated with the default public IP address of the cluster.
        """
        return pulumi.get(self, 'ip_tags')

    @property
    @pulumi.getter(name='ipv4Address')
    def ipv4_address(self) -> pulumi.Output[str]:
        """
        The IPv4 address associated with the public load balancer of the cluster.
        """
        return pulumi.get(self, 'ipv4_address')

    @property
    @pulumi.getter(name='ipv6Address')
    def ipv6_address(self) -> pulumi.Output[str]:
        """
        IPv6 address for the cluster if IPv6 is enabled.
        """
        return pulumi.get(self, 'ipv6_address')

    @property
    @pulumi.getter(name='loadBalancingRules')
    def load_balancing_rules(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancingRuleResponse']]]:
        """
        Load balancing rules that are applied to the public load balancer of the cluster.
        """
        return pulumi.get(self, 'load_balancing_rules')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Azure resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='networkSecurityRules')
    def network_security_rules(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkSecurityRuleResponse']]]:
        """
        Custom Network Security Rules that are applied to the Virtual Network of the cluster.
        """
        return pulumi.get(self, 'network_security_rules')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the managed cluster resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='serviceEndpoints')
    def service_endpoints(self) -> pulumi.Output[Optional[Sequence['outputs.ServiceEndpointResponse']]]:
        """
        Service endpoints for subnets in the cluster.
        """
        return pulumi.get(self, 'service_endpoints')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the managed cluster
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='subnetId')
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        If specified, the node types for the cluster are created in this subnet instead of the default VNet. The **networkSecurityRules** specified for the cluster are also applied to this subnet. This setting cannot be changed once the cluster is created.
        """
        return pulumi.get(self, 'subnet_id')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='zonalResiliency')
    def zonal_resiliency(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if the cluster has zone resiliency.
        """
        return pulumi.get(self, 'zonal_resiliency')
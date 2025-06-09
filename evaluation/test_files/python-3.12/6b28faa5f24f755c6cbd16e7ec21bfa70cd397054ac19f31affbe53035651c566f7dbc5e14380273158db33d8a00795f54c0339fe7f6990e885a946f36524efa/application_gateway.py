import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ApplicationGatewayArgs', 'ApplicationGateway']

@pulumi.input_type
class ApplicationGatewayArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], application_gateway_name: Optional[pulumi.Input[str]]=None, authentication_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayAuthenticationCertificateArgs']]]]=None, autoscale_configuration: Optional[pulumi.Input['ApplicationGatewayAutoscaleConfigurationArgs']]=None, backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendAddressPoolArgs']]]]=None, backend_http_settings_collection: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendHttpSettingsArgs']]]]=None, custom_error_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayCustomErrorArgs']]]]=None, enable_fips: Optional[pulumi.Input[bool]]=None, enable_http2: Optional[pulumi.Input[bool]]=None, firewall_policy: Optional[pulumi.Input['SubResourceArgs']]=None, force_firewall_policy_association: Optional[pulumi.Input[bool]]=None, frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendIPConfigurationArgs']]]]=None, frontend_ports: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendPortArgs']]]]=None, gateway_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayIPConfigurationArgs']]]]=None, http_listeners: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayHttpListenerArgs']]]]=None, id: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']]=None, location: Optional[pulumi.Input[str]]=None, private_link_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayPrivateLinkConfigurationArgs']]]]=None, probes: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayProbeArgs']]]]=None, redirect_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRedirectConfigurationArgs']]]]=None, request_routing_rules: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRequestRoutingRuleArgs']]]]=None, rewrite_rule_sets: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRewriteRuleSetArgs']]]]=None, sku: Optional[pulumi.Input['ApplicationGatewaySkuArgs']]=None, ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslCertificateArgs']]]]=None, ssl_policy: Optional[pulumi.Input['ApplicationGatewaySslPolicyArgs']]=None, ssl_profiles: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslProfileArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, trusted_client_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedClientCertificateArgs']]]]=None, trusted_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedRootCertificateArgs']]]]=None, url_path_maps: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayUrlPathMapArgs']]]]=None, web_application_firewall_configuration: Optional[pulumi.Input['ApplicationGatewayWebApplicationFirewallConfigurationArgs']]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ApplicationGateway resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] application_gateway_name: The name of the application gateway.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayAuthenticationCertificateArgs']]] authentication_certificates: Authentication certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input['ApplicationGatewayAutoscaleConfigurationArgs'] autoscale_configuration: Autoscale Configuration.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendAddressPoolArgs']]] backend_address_pools: Backend address pool of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendHttpSettingsArgs']]] backend_http_settings_collection: Backend http settings of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayCustomErrorArgs']]] custom_error_configurations: Custom error configurations of the application gateway resource.
        :param pulumi.Input[bool] enable_fips: Whether FIPS is enabled on the application gateway resource.
        :param pulumi.Input[bool] enable_http2: Whether HTTP2 is enabled on the application gateway resource.
        :param pulumi.Input['SubResourceArgs'] firewall_policy: Reference to the FirewallPolicy resource.
        :param pulumi.Input[bool] force_firewall_policy_association: If true, associates a firewall policy with an application gateway regardless whether the policy differs from the WAF Config.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendIPConfigurationArgs']]] frontend_ip_configurations: Frontend IP addresses of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendPortArgs']]] frontend_ports: Frontend ports of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayIPConfigurationArgs']]] gateway_ip_configurations: Subnets of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayHttpListenerArgs']]] http_listeners: Http listeners of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: The identity of the application gateway, if configured.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayPrivateLinkConfigurationArgs']]] private_link_configurations: PrivateLink configurations on application gateway.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayProbeArgs']]] probes: Probes of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRedirectConfigurationArgs']]] redirect_configurations: Redirect configurations of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRequestRoutingRuleArgs']]] request_routing_rules: Request routing rules of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRewriteRuleSetArgs']]] rewrite_rule_sets: Rewrite rules for the application gateway resource.
        :param pulumi.Input['ApplicationGatewaySkuArgs'] sku: SKU of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslCertificateArgs']]] ssl_certificates: SSL certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input['ApplicationGatewaySslPolicyArgs'] ssl_policy: SSL policy of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslProfileArgs']]] ssl_profiles: SSL profiles of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedClientCertificateArgs']]] trusted_client_certificates: Trusted client certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedRootCertificateArgs']]] trusted_root_certificates: Trusted Root certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayUrlPathMapArgs']]] url_path_maps: URL path map of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input['ApplicationGatewayWebApplicationFirewallConfigurationArgs'] web_application_firewall_configuration: Web application firewall configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: A list of availability zones denoting where the resource needs to come from.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if application_gateway_name is not None:
            pulumi.set(__self__, 'application_gateway_name', application_gateway_name)
        if authentication_certificates is not None:
            pulumi.set(__self__, 'authentication_certificates', authentication_certificates)
        if autoscale_configuration is not None:
            pulumi.set(__self__, 'autoscale_configuration', autoscale_configuration)
        if backend_address_pools is not None:
            pulumi.set(__self__, 'backend_address_pools', backend_address_pools)
        if backend_http_settings_collection is not None:
            pulumi.set(__self__, 'backend_http_settings_collection', backend_http_settings_collection)
        if custom_error_configurations is not None:
            pulumi.set(__self__, 'custom_error_configurations', custom_error_configurations)
        if enable_fips is not None:
            pulumi.set(__self__, 'enable_fips', enable_fips)
        if enable_http2 is not None:
            pulumi.set(__self__, 'enable_http2', enable_http2)
        if firewall_policy is not None:
            pulumi.set(__self__, 'firewall_policy', firewall_policy)
        if force_firewall_policy_association is not None:
            pulumi.set(__self__, 'force_firewall_policy_association', force_firewall_policy_association)
        if frontend_ip_configurations is not None:
            pulumi.set(__self__, 'frontend_ip_configurations', frontend_ip_configurations)
        if frontend_ports is not None:
            pulumi.set(__self__, 'frontend_ports', frontend_ports)
        if gateway_ip_configurations is not None:
            pulumi.set(__self__, 'gateway_ip_configurations', gateway_ip_configurations)
        if http_listeners is not None:
            pulumi.set(__self__, 'http_listeners', http_listeners)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if identity is not None:
            pulumi.set(__self__, 'identity', identity)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if private_link_configurations is not None:
            pulumi.set(__self__, 'private_link_configurations', private_link_configurations)
        if probes is not None:
            pulumi.set(__self__, 'probes', probes)
        if redirect_configurations is not None:
            pulumi.set(__self__, 'redirect_configurations', redirect_configurations)
        if request_routing_rules is not None:
            pulumi.set(__self__, 'request_routing_rules', request_routing_rules)
        if rewrite_rule_sets is not None:
            pulumi.set(__self__, 'rewrite_rule_sets', rewrite_rule_sets)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if ssl_certificates is not None:
            pulumi.set(__self__, 'ssl_certificates', ssl_certificates)
        if ssl_policy is not None:
            pulumi.set(__self__, 'ssl_policy', ssl_policy)
        if ssl_profiles is not None:
            pulumi.set(__self__, 'ssl_profiles', ssl_profiles)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if trusted_client_certificates is not None:
            pulumi.set(__self__, 'trusted_client_certificates', trusted_client_certificates)
        if trusted_root_certificates is not None:
            pulumi.set(__self__, 'trusted_root_certificates', trusted_root_certificates)
        if url_path_maps is not None:
            pulumi.set(__self__, 'url_path_maps', url_path_maps)
        if web_application_firewall_configuration is not None:
            pulumi.set(__self__, 'web_application_firewall_configuration', web_application_firewall_configuration)
        if zones is not None:
            pulumi.set(__self__, 'zones', zones)

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
    @pulumi.getter(name='applicationGatewayName')
    def application_gateway_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application gateway.
        """
        return pulumi.get(self, 'application_gateway_name')

    @application_gateway_name.setter
    def application_gateway_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'application_gateway_name', value)

    @property
    @pulumi.getter(name='authenticationCertificates')
    def authentication_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayAuthenticationCertificateArgs']]]]:
        """
        Authentication certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'authentication_certificates')

    @authentication_certificates.setter
    def authentication_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayAuthenticationCertificateArgs']]]]):
        pulumi.set(self, 'authentication_certificates', value)

    @property
    @pulumi.getter(name='autoscaleConfiguration')
    def autoscale_configuration(self) -> Optional[pulumi.Input['ApplicationGatewayAutoscaleConfigurationArgs']]:
        """
        Autoscale Configuration.
        """
        return pulumi.get(self, 'autoscale_configuration')

    @autoscale_configuration.setter
    def autoscale_configuration(self, value: Optional[pulumi.Input['ApplicationGatewayAutoscaleConfigurationArgs']]):
        pulumi.set(self, 'autoscale_configuration', value)

    @property
    @pulumi.getter(name='backendAddressPools')
    def backend_address_pools(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendAddressPoolArgs']]]]:
        """
        Backend address pool of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_address_pools')

    @backend_address_pools.setter
    def backend_address_pools(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendAddressPoolArgs']]]]):
        pulumi.set(self, 'backend_address_pools', value)

    @property
    @pulumi.getter(name='backendHttpSettingsCollection')
    def backend_http_settings_collection(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendHttpSettingsArgs']]]]:
        """
        Backend http settings of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_http_settings_collection')

    @backend_http_settings_collection.setter
    def backend_http_settings_collection(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayBackendHttpSettingsArgs']]]]):
        pulumi.set(self, 'backend_http_settings_collection', value)

    @property
    @pulumi.getter(name='customErrorConfigurations')
    def custom_error_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayCustomErrorArgs']]]]:
        """
        Custom error configurations of the application gateway resource.
        """
        return pulumi.get(self, 'custom_error_configurations')

    @custom_error_configurations.setter
    def custom_error_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayCustomErrorArgs']]]]):
        pulumi.set(self, 'custom_error_configurations', value)

    @property
    @pulumi.getter(name='enableFips')
    def enable_fips(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether FIPS is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_fips')

    @enable_fips.setter
    def enable_fips(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_fips', value)

    @property
    @pulumi.getter(name='enableHttp2')
    def enable_http2(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether HTTP2 is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_http2')

    @enable_http2.setter
    def enable_http2(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enable_http2', value)

    @property
    @pulumi.getter(name='firewallPolicy')
    def firewall_policy(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Reference to the FirewallPolicy resource.
        """
        return pulumi.get(self, 'firewall_policy')

    @firewall_policy.setter
    def firewall_policy(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, 'firewall_policy', value)

    @property
    @pulumi.getter(name='forceFirewallPolicyAssociation')
    def force_firewall_policy_association(self) -> Optional[pulumi.Input[bool]]:
        """
        If true, associates a firewall policy with an application gateway regardless whether the policy differs from the WAF Config.
        """
        return pulumi.get(self, 'force_firewall_policy_association')

    @force_firewall_policy_association.setter
    def force_firewall_policy_association(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'force_firewall_policy_association', value)

    @property
    @pulumi.getter(name='frontendIPConfigurations')
    def frontend_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendIPConfigurationArgs']]]]:
        """
        Frontend IP addresses of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ip_configurations')

    @frontend_ip_configurations.setter
    def frontend_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendIPConfigurationArgs']]]]):
        pulumi.set(self, 'frontend_ip_configurations', value)

    @property
    @pulumi.getter(name='frontendPorts')
    def frontend_ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendPortArgs']]]]:
        """
        Frontend ports of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ports')

    @frontend_ports.setter
    def frontend_ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayFrontendPortArgs']]]]):
        pulumi.set(self, 'frontend_ports', value)

    @property
    @pulumi.getter(name='gatewayIPConfigurations')
    def gateway_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayIPConfigurationArgs']]]]:
        """
        Subnets of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'gateway_ip_configurations')

    @gateway_ip_configurations.setter
    def gateway_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayIPConfigurationArgs']]]]):
        pulumi.set(self, 'gateway_ip_configurations', value)

    @property
    @pulumi.getter(name='httpListeners')
    def http_listeners(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayHttpListenerArgs']]]]:
        """
        Http listeners of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'http_listeners')

    @http_listeners.setter
    def http_listeners(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayHttpListenerArgs']]]]):
        pulumi.set(self, 'http_listeners', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        The identity of the application gateway, if configured.
        """
        return pulumi.get(self, 'identity')

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, 'identity', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='privateLinkConfigurations')
    def private_link_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayPrivateLinkConfigurationArgs']]]]:
        """
        PrivateLink configurations on application gateway.
        """
        return pulumi.get(self, 'private_link_configurations')

    @private_link_configurations.setter
    def private_link_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayPrivateLinkConfigurationArgs']]]]):
        pulumi.set(self, 'private_link_configurations', value)

    @property
    @pulumi.getter
    def probes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayProbeArgs']]]]:
        """
        Probes of the application gateway resource.
        """
        return pulumi.get(self, 'probes')

    @probes.setter
    def probes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayProbeArgs']]]]):
        pulumi.set(self, 'probes', value)

    @property
    @pulumi.getter(name='redirectConfigurations')
    def redirect_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRedirectConfigurationArgs']]]]:
        """
        Redirect configurations of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'redirect_configurations')

    @redirect_configurations.setter
    def redirect_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRedirectConfigurationArgs']]]]):
        pulumi.set(self, 'redirect_configurations', value)

    @property
    @pulumi.getter(name='requestRoutingRules')
    def request_routing_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRequestRoutingRuleArgs']]]]:
        """
        Request routing rules of the application gateway resource.
        """
        return pulumi.get(self, 'request_routing_rules')

    @request_routing_rules.setter
    def request_routing_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRequestRoutingRuleArgs']]]]):
        pulumi.set(self, 'request_routing_rules', value)

    @property
    @pulumi.getter(name='rewriteRuleSets')
    def rewrite_rule_sets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRewriteRuleSetArgs']]]]:
        """
        Rewrite rules for the application gateway resource.
        """
        return pulumi.get(self, 'rewrite_rule_sets')

    @rewrite_rule_sets.setter
    def rewrite_rule_sets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayRewriteRuleSetArgs']]]]):
        pulumi.set(self, 'rewrite_rule_sets', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ApplicationGatewaySkuArgs']]:
        """
        SKU of the application gateway resource.
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ApplicationGatewaySkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter(name='sslCertificates')
    def ssl_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslCertificateArgs']]]]:
        """
        SSL certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_certificates')

    @ssl_certificates.setter
    def ssl_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslCertificateArgs']]]]):
        pulumi.set(self, 'ssl_certificates', value)

    @property
    @pulumi.getter(name='sslPolicy')
    def ssl_policy(self) -> Optional[pulumi.Input['ApplicationGatewaySslPolicyArgs']]:
        """
        SSL policy of the application gateway resource.
        """
        return pulumi.get(self, 'ssl_policy')

    @ssl_policy.setter
    def ssl_policy(self, value: Optional[pulumi.Input['ApplicationGatewaySslPolicyArgs']]):
        pulumi.set(self, 'ssl_policy', value)

    @property
    @pulumi.getter(name='sslProfiles')
    def ssl_profiles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslProfileArgs']]]]:
        """
        SSL profiles of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_profiles')

    @ssl_profiles.setter
    def ssl_profiles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewaySslProfileArgs']]]]):
        pulumi.set(self, 'ssl_profiles', value)

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
    @pulumi.getter(name='trustedClientCertificates')
    def trusted_client_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedClientCertificateArgs']]]]:
        """
        Trusted client certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_client_certificates')

    @trusted_client_certificates.setter
    def trusted_client_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedClientCertificateArgs']]]]):
        pulumi.set(self, 'trusted_client_certificates', value)

    @property
    @pulumi.getter(name='trustedRootCertificates')
    def trusted_root_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedRootCertificateArgs']]]]:
        """
        Trusted Root certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_root_certificates')

    @trusted_root_certificates.setter
    def trusted_root_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayTrustedRootCertificateArgs']]]]):
        pulumi.set(self, 'trusted_root_certificates', value)

    @property
    @pulumi.getter(name='urlPathMaps')
    def url_path_maps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayUrlPathMapArgs']]]]:
        """
        URL path map of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'url_path_maps')

    @url_path_maps.setter
    def url_path_maps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ApplicationGatewayUrlPathMapArgs']]]]):
        pulumi.set(self, 'url_path_maps', value)

    @property
    @pulumi.getter(name='webApplicationFirewallConfiguration')
    def web_application_firewall_configuration(self) -> Optional[pulumi.Input['ApplicationGatewayWebApplicationFirewallConfigurationArgs']]:
        """
        Web application firewall configuration.
        """
        return pulumi.get(self, 'web_application_firewall_configuration')

    @web_application_firewall_configuration.setter
    def web_application_firewall_configuration(self, value: Optional[pulumi.Input['ApplicationGatewayWebApplicationFirewallConfigurationArgs']]):
        pulumi.set(self, 'web_application_firewall_configuration', value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of availability zones denoting where the resource needs to come from.
        """
        return pulumi.get(self, 'zones')

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'zones', value)

class ApplicationGateway(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_gateway_name: Optional[pulumi.Input[str]]=None, authentication_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayAuthenticationCertificateArgs']]]]]=None, autoscale_configuration: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewayAutoscaleConfigurationArgs']]]=None, backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendAddressPoolArgs']]]]]=None, backend_http_settings_collection: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendHttpSettingsArgs']]]]]=None, custom_error_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayCustomErrorArgs']]]]]=None, enable_fips: Optional[pulumi.Input[bool]]=None, enable_http2: Optional[pulumi.Input[bool]]=None, firewall_policy: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]]=None, force_firewall_policy_association: Optional[pulumi.Input[bool]]=None, frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendIPConfigurationArgs']]]]]=None, frontend_ports: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendPortArgs']]]]]=None, gateway_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayIPConfigurationArgs']]]]]=None, http_listeners: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayHttpListenerArgs']]]]]=None, id: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, private_link_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayPrivateLinkConfigurationArgs']]]]]=None, probes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayProbeArgs']]]]]=None, redirect_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRedirectConfigurationArgs']]]]]=None, request_routing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRequestRoutingRuleArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rewrite_rule_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRewriteRuleSetArgs']]]]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewaySkuArgs']]]=None, ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslCertificateArgs']]]]]=None, ssl_policy: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewaySslPolicyArgs']]]=None, ssl_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslProfileArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, trusted_client_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedClientCertificateArgs']]]]]=None, trusted_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedRootCertificateArgs']]]]]=None, url_path_maps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayUrlPathMapArgs']]]]]=None, web_application_firewall_configuration: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewayWebApplicationFirewallConfigurationArgs']]]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        Application gateway resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_gateway_name: The name of the application gateway.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayAuthenticationCertificateArgs']]]] authentication_certificates: Authentication certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[pulumi.InputType['ApplicationGatewayAutoscaleConfigurationArgs']] autoscale_configuration: Autoscale Configuration.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendAddressPoolArgs']]]] backend_address_pools: Backend address pool of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendHttpSettingsArgs']]]] backend_http_settings_collection: Backend http settings of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayCustomErrorArgs']]]] custom_error_configurations: Custom error configurations of the application gateway resource.
        :param pulumi.Input[bool] enable_fips: Whether FIPS is enabled on the application gateway resource.
        :param pulumi.Input[bool] enable_http2: Whether HTTP2 is enabled on the application gateway resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] firewall_policy: Reference to the FirewallPolicy resource.
        :param pulumi.Input[bool] force_firewall_policy_association: If true, associates a firewall policy with an application gateway regardless whether the policy differs from the WAF Config.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendIPConfigurationArgs']]]] frontend_ip_configurations: Frontend IP addresses of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendPortArgs']]]] frontend_ports: Frontend ports of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayIPConfigurationArgs']]]] gateway_ip_configurations: Subnets of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayHttpListenerArgs']]]] http_listeners: Http listeners of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: The identity of the application gateway, if configured.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayPrivateLinkConfigurationArgs']]]] private_link_configurations: PrivateLink configurations on application gateway.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayProbeArgs']]]] probes: Probes of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRedirectConfigurationArgs']]]] redirect_configurations: Redirect configurations of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRequestRoutingRuleArgs']]]] request_routing_rules: Request routing rules of the application gateway resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRewriteRuleSetArgs']]]] rewrite_rule_sets: Rewrite rules for the application gateway resource.
        :param pulumi.Input[pulumi.InputType['ApplicationGatewaySkuArgs']] sku: SKU of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslCertificateArgs']]]] ssl_certificates: SSL certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[pulumi.InputType['ApplicationGatewaySslPolicyArgs']] ssl_policy: SSL policy of the application gateway resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslProfileArgs']]]] ssl_profiles: SSL profiles of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedClientCertificateArgs']]]] trusted_client_certificates: Trusted client certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedRootCertificateArgs']]]] trusted_root_certificates: Trusted Root certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayUrlPathMapArgs']]]] url_path_maps: URL path map of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        :param pulumi.Input[pulumi.InputType['ApplicationGatewayWebApplicationFirewallConfigurationArgs']] web_application_firewall_configuration: Web application firewall configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: A list of availability zones denoting where the resource needs to come from.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ApplicationGatewayArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Application gateway resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param ApplicationGatewayArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationGatewayArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_gateway_name: Optional[pulumi.Input[str]]=None, authentication_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayAuthenticationCertificateArgs']]]]]=None, autoscale_configuration: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewayAutoscaleConfigurationArgs']]]=None, backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendAddressPoolArgs']]]]]=None, backend_http_settings_collection: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayBackendHttpSettingsArgs']]]]]=None, custom_error_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayCustomErrorArgs']]]]]=None, enable_fips: Optional[pulumi.Input[bool]]=None, enable_http2: Optional[pulumi.Input[bool]]=None, firewall_policy: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]]=None, force_firewall_policy_association: Optional[pulumi.Input[bool]]=None, frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendIPConfigurationArgs']]]]]=None, frontend_ports: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayFrontendPortArgs']]]]]=None, gateway_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayIPConfigurationArgs']]]]]=None, http_listeners: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayHttpListenerArgs']]]]]=None, id: Optional[pulumi.Input[str]]=None, identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]]=None, location: Optional[pulumi.Input[str]]=None, private_link_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayPrivateLinkConfigurationArgs']]]]]=None, probes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayProbeArgs']]]]]=None, redirect_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRedirectConfigurationArgs']]]]]=None, request_routing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRequestRoutingRuleArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rewrite_rule_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayRewriteRuleSetArgs']]]]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewaySkuArgs']]]=None, ssl_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslCertificateArgs']]]]]=None, ssl_policy: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewaySslPolicyArgs']]]=None, ssl_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewaySslProfileArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, trusted_client_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedClientCertificateArgs']]]]]=None, trusted_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayTrustedRootCertificateArgs']]]]]=None, url_path_maps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationGatewayUrlPathMapArgs']]]]]=None, web_application_firewall_configuration: Optional[pulumi.Input[pulumi.InputType['ApplicationGatewayWebApplicationFirewallConfigurationArgs']]]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationGatewayArgs.__new__(ApplicationGatewayArgs)
            __props__.__dict__['application_gateway_name'] = application_gateway_name
            __props__.__dict__['authentication_certificates'] = authentication_certificates
            __props__.__dict__['autoscale_configuration'] = autoscale_configuration
            __props__.__dict__['backend_address_pools'] = backend_address_pools
            __props__.__dict__['backend_http_settings_collection'] = backend_http_settings_collection
            __props__.__dict__['custom_error_configurations'] = custom_error_configurations
            __props__.__dict__['enable_fips'] = enable_fips
            __props__.__dict__['enable_http2'] = enable_http2
            __props__.__dict__['firewall_policy'] = firewall_policy
            __props__.__dict__['force_firewall_policy_association'] = force_firewall_policy_association
            __props__.__dict__['frontend_ip_configurations'] = frontend_ip_configurations
            __props__.__dict__['frontend_ports'] = frontend_ports
            __props__.__dict__['gateway_ip_configurations'] = gateway_ip_configurations
            __props__.__dict__['http_listeners'] = http_listeners
            __props__.__dict__['id'] = id
            __props__.__dict__['identity'] = identity
            __props__.__dict__['location'] = location
            __props__.__dict__['private_link_configurations'] = private_link_configurations
            __props__.__dict__['probes'] = probes
            __props__.__dict__['redirect_configurations'] = redirect_configurations
            __props__.__dict__['request_routing_rules'] = request_routing_rules
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['rewrite_rule_sets'] = rewrite_rule_sets
            __props__.__dict__['sku'] = sku
            __props__.__dict__['ssl_certificates'] = ssl_certificates
            __props__.__dict__['ssl_policy'] = ssl_policy
            __props__.__dict__['ssl_profiles'] = ssl_profiles
            __props__.__dict__['tags'] = tags
            __props__.__dict__['trusted_client_certificates'] = trusted_client_certificates
            __props__.__dict__['trusted_root_certificates'] = trusted_root_certificates
            __props__.__dict__['url_path_maps'] = url_path_maps
            __props__.__dict__['web_application_firewall_configuration'] = web_application_firewall_configuration
            __props__.__dict__['zones'] = zones
            __props__.__dict__['etag'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['operational_state'] = None
            __props__.__dict__['private_endpoint_connections'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['resource_guid'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:network/v20150501preview:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20150615:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20160330:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20160601:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20160901:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20161201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20170301:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20170601:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20170801:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20170901:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20171001:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20171101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180401:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180601:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180701:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20180801:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20181001:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20181101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20181201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190401:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190601:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190701:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190801:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20190901:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20191101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20191201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200301:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200401:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200501:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200601:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200701:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20200801:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20201101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20210201:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20210301:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20210501:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20210801:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20220101:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20220501:ApplicationGateway'), pulumi.Alias(type_='azure-native:network/v20220701:ApplicationGateway')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationGateway, __self__).__init__('azure-native:network:ApplicationGateway', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ApplicationGateway':
        """
        Get an existing ApplicationGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ApplicationGatewayArgs.__new__(ApplicationGatewayArgs)
        __props__.__dict__['authentication_certificates'] = None
        __props__.__dict__['autoscale_configuration'] = None
        __props__.__dict__['backend_address_pools'] = None
        __props__.__dict__['backend_http_settings_collection'] = None
        __props__.__dict__['custom_error_configurations'] = None
        __props__.__dict__['enable_fips'] = None
        __props__.__dict__['enable_http2'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['firewall_policy'] = None
        __props__.__dict__['force_firewall_policy_association'] = None
        __props__.__dict__['frontend_ip_configurations'] = None
        __props__.__dict__['frontend_ports'] = None
        __props__.__dict__['gateway_ip_configurations'] = None
        __props__.__dict__['http_listeners'] = None
        __props__.__dict__['identity'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['operational_state'] = None
        __props__.__dict__['private_endpoint_connections'] = None
        __props__.__dict__['private_link_configurations'] = None
        __props__.__dict__['probes'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['redirect_configurations'] = None
        __props__.__dict__['request_routing_rules'] = None
        __props__.__dict__['resource_guid'] = None
        __props__.__dict__['rewrite_rule_sets'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['ssl_certificates'] = None
        __props__.__dict__['ssl_policy'] = None
        __props__.__dict__['ssl_profiles'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['trusted_client_certificates'] = None
        __props__.__dict__['trusted_root_certificates'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['url_path_maps'] = None
        __props__.__dict__['web_application_firewall_configuration'] = None
        __props__.__dict__['zones'] = None
        return ApplicationGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='authenticationCertificates')
    def authentication_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayAuthenticationCertificateResponse']]]:
        """
        Authentication certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'authentication_certificates')

    @property
    @pulumi.getter(name='autoscaleConfiguration')
    def autoscale_configuration(self) -> pulumi.Output[Optional['outputs.ApplicationGatewayAutoscaleConfigurationResponse']]:
        """
        Autoscale Configuration.
        """
        return pulumi.get(self, 'autoscale_configuration')

    @property
    @pulumi.getter(name='backendAddressPools')
    def backend_address_pools(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayBackendAddressPoolResponse']]]:
        """
        Backend address pool of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_address_pools')

    @property
    @pulumi.getter(name='backendHttpSettingsCollection')
    def backend_http_settings_collection(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayBackendHttpSettingsResponse']]]:
        """
        Backend http settings of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_http_settings_collection')

    @property
    @pulumi.getter(name='customErrorConfigurations')
    def custom_error_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayCustomErrorResponse']]]:
        """
        Custom error configurations of the application gateway resource.
        """
        return pulumi.get(self, 'custom_error_configurations')

    @property
    @pulumi.getter(name='enableFips')
    def enable_fips(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether FIPS is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_fips')

    @property
    @pulumi.getter(name='enableHttp2')
    def enable_http2(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether HTTP2 is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_http2')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='firewallPolicy')
    def firewall_policy(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Reference to the FirewallPolicy resource.
        """
        return pulumi.get(self, 'firewall_policy')

    @property
    @pulumi.getter(name='forceFirewallPolicyAssociation')
    def force_firewall_policy_association(self) -> pulumi.Output[Optional[bool]]:
        """
        If true, associates a firewall policy with an application gateway regardless whether the policy differs from the WAF Config.
        """
        return pulumi.get(self, 'force_firewall_policy_association')

    @property
    @pulumi.getter(name='frontendIPConfigurations')
    def frontend_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayFrontendIPConfigurationResponse']]]:
        """
        Frontend IP addresses of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ip_configurations')

    @property
    @pulumi.getter(name='frontendPorts')
    def frontend_ports(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayFrontendPortResponse']]]:
        """
        Frontend ports of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ports')

    @property
    @pulumi.getter(name='gatewayIPConfigurations')
    def gateway_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayIPConfigurationResponse']]]:
        """
        Subnets of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'gateway_ip_configurations')

    @property
    @pulumi.getter(name='httpListeners')
    def http_listeners(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayHttpListenerResponse']]]:
        """
        Http listeners of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'http_listeners')

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        The identity of the application gateway, if configured.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='operationalState')
    def operational_state(self) -> pulumi.Output[str]:
        """
        Operational state of the application gateway resource.
        """
        return pulumi.get(self, 'operational_state')

    @property
    @pulumi.getter(name='privateEndpointConnections')
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.ApplicationGatewayPrivateEndpointConnectionResponse']]:
        """
        Private Endpoint connections on application gateway.
        """
        return pulumi.get(self, 'private_endpoint_connections')

    @property
    @pulumi.getter(name='privateLinkConfigurations')
    def private_link_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayPrivateLinkConfigurationResponse']]]:
        """
        PrivateLink configurations on application gateway.
        """
        return pulumi.get(self, 'private_link_configurations')

    @property
    @pulumi.getter
    def probes(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayProbeResponse']]]:
        """
        Probes of the application gateway resource.
        """
        return pulumi.get(self, 'probes')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the application gateway resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='redirectConfigurations')
    def redirect_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayRedirectConfigurationResponse']]]:
        """
        Redirect configurations of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'redirect_configurations')

    @property
    @pulumi.getter(name='requestRoutingRules')
    def request_routing_rules(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayRequestRoutingRuleResponse']]]:
        """
        Request routing rules of the application gateway resource.
        """
        return pulumi.get(self, 'request_routing_rules')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the application gateway resource.
        """
        return pulumi.get(self, 'resource_guid')

    @property
    @pulumi.getter(name='rewriteRuleSets')
    def rewrite_rule_sets(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayRewriteRuleSetResponse']]]:
        """
        Rewrite rules for the application gateway resource.
        """
        return pulumi.get(self, 'rewrite_rule_sets')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ApplicationGatewaySkuResponse']]:
        """
        SKU of the application gateway resource.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='sslCertificates')
    def ssl_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewaySslCertificateResponse']]]:
        """
        SSL certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_certificates')

    @property
    @pulumi.getter(name='sslPolicy')
    def ssl_policy(self) -> pulumi.Output[Optional['outputs.ApplicationGatewaySslPolicyResponse']]:
        """
        SSL policy of the application gateway resource.
        """
        return pulumi.get(self, 'ssl_policy')

    @property
    @pulumi.getter(name='sslProfiles')
    def ssl_profiles(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewaySslProfileResponse']]]:
        """
        SSL profiles of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_profiles')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='trustedClientCertificates')
    def trusted_client_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayTrustedClientCertificateResponse']]]:
        """
        Trusted client certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_client_certificates')

    @property
    @pulumi.getter(name='trustedRootCertificates')
    def trusted_root_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayTrustedRootCertificateResponse']]]:
        """
        Trusted Root certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_root_certificates')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='urlPathMaps')
    def url_path_maps(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationGatewayUrlPathMapResponse']]]:
        """
        URL path map of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'url_path_maps')

    @property
    @pulumi.getter(name='webApplicationFirewallConfiguration')
    def web_application_firewall_configuration(self) -> pulumi.Output[Optional['outputs.ApplicationGatewayWebApplicationFirewallConfigurationResponse']]:
        """
        Web application firewall configuration.
        """
        return pulumi.get(self, 'web_application_firewall_configuration')

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of availability zones denoting where the resource needs to come from.
        """
        return pulumi.get(self, 'zones')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetApplicationGatewayResult', 'AwaitableGetApplicationGatewayResult', 'get_application_gateway', 'get_application_gateway_output']

@pulumi.output_type
class GetApplicationGatewayResult:
    """
    Application gateway resource.
    """

    def __init__(__self__, authentication_certificates=None, autoscale_configuration=None, backend_address_pools=None, backend_http_settings_collection=None, custom_error_configurations=None, enable_fips=None, enable_http2=None, etag=None, firewall_policy=None, force_firewall_policy_association=None, frontend_ip_configurations=None, frontend_ports=None, gateway_ip_configurations=None, http_listeners=None, id=None, identity=None, location=None, name=None, operational_state=None, private_endpoint_connections=None, private_link_configurations=None, probes=None, provisioning_state=None, redirect_configurations=None, request_routing_rules=None, resource_guid=None, rewrite_rule_sets=None, sku=None, ssl_certificates=None, ssl_policy=None, ssl_profiles=None, tags=None, trusted_client_certificates=None, trusted_root_certificates=None, type=None, url_path_maps=None, web_application_firewall_configuration=None, zones=None):
        if authentication_certificates and (not isinstance(authentication_certificates, list)):
            raise TypeError("Expected argument 'authentication_certificates' to be a list")
        pulumi.set(__self__, 'authentication_certificates', authentication_certificates)
        if autoscale_configuration and (not isinstance(autoscale_configuration, dict)):
            raise TypeError("Expected argument 'autoscale_configuration' to be a dict")
        pulumi.set(__self__, 'autoscale_configuration', autoscale_configuration)
        if backend_address_pools and (not isinstance(backend_address_pools, list)):
            raise TypeError("Expected argument 'backend_address_pools' to be a list")
        pulumi.set(__self__, 'backend_address_pools', backend_address_pools)
        if backend_http_settings_collection and (not isinstance(backend_http_settings_collection, list)):
            raise TypeError("Expected argument 'backend_http_settings_collection' to be a list")
        pulumi.set(__self__, 'backend_http_settings_collection', backend_http_settings_collection)
        if custom_error_configurations and (not isinstance(custom_error_configurations, list)):
            raise TypeError("Expected argument 'custom_error_configurations' to be a list")
        pulumi.set(__self__, 'custom_error_configurations', custom_error_configurations)
        if enable_fips and (not isinstance(enable_fips, bool)):
            raise TypeError("Expected argument 'enable_fips' to be a bool")
        pulumi.set(__self__, 'enable_fips', enable_fips)
        if enable_http2 and (not isinstance(enable_http2, bool)):
            raise TypeError("Expected argument 'enable_http2' to be a bool")
        pulumi.set(__self__, 'enable_http2', enable_http2)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if firewall_policy and (not isinstance(firewall_policy, dict)):
            raise TypeError("Expected argument 'firewall_policy' to be a dict")
        pulumi.set(__self__, 'firewall_policy', firewall_policy)
        if force_firewall_policy_association and (not isinstance(force_firewall_policy_association, bool)):
            raise TypeError("Expected argument 'force_firewall_policy_association' to be a bool")
        pulumi.set(__self__, 'force_firewall_policy_association', force_firewall_policy_association)
        if frontend_ip_configurations and (not isinstance(frontend_ip_configurations, list)):
            raise TypeError("Expected argument 'frontend_ip_configurations' to be a list")
        pulumi.set(__self__, 'frontend_ip_configurations', frontend_ip_configurations)
        if frontend_ports and (not isinstance(frontend_ports, list)):
            raise TypeError("Expected argument 'frontend_ports' to be a list")
        pulumi.set(__self__, 'frontend_ports', frontend_ports)
        if gateway_ip_configurations and (not isinstance(gateway_ip_configurations, list)):
            raise TypeError("Expected argument 'gateway_ip_configurations' to be a list")
        pulumi.set(__self__, 'gateway_ip_configurations', gateway_ip_configurations)
        if http_listeners and (not isinstance(http_listeners, list)):
            raise TypeError("Expected argument 'http_listeners' to be a list")
        pulumi.set(__self__, 'http_listeners', http_listeners)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if identity and (not isinstance(identity, dict)):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, 'identity', identity)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if operational_state and (not isinstance(operational_state, str)):
            raise TypeError("Expected argument 'operational_state' to be a str")
        pulumi.set(__self__, 'operational_state', operational_state)
        if private_endpoint_connections and (not isinstance(private_endpoint_connections, list)):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, 'private_endpoint_connections', private_endpoint_connections)
        if private_link_configurations and (not isinstance(private_link_configurations, list)):
            raise TypeError("Expected argument 'private_link_configurations' to be a list")
        pulumi.set(__self__, 'private_link_configurations', private_link_configurations)
        if probes and (not isinstance(probes, list)):
            raise TypeError("Expected argument 'probes' to be a list")
        pulumi.set(__self__, 'probes', probes)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if redirect_configurations and (not isinstance(redirect_configurations, list)):
            raise TypeError("Expected argument 'redirect_configurations' to be a list")
        pulumi.set(__self__, 'redirect_configurations', redirect_configurations)
        if request_routing_rules and (not isinstance(request_routing_rules, list)):
            raise TypeError("Expected argument 'request_routing_rules' to be a list")
        pulumi.set(__self__, 'request_routing_rules', request_routing_rules)
        if resource_guid and (not isinstance(resource_guid, str)):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, 'resource_guid', resource_guid)
        if rewrite_rule_sets and (not isinstance(rewrite_rule_sets, list)):
            raise TypeError("Expected argument 'rewrite_rule_sets' to be a list")
        pulumi.set(__self__, 'rewrite_rule_sets', rewrite_rule_sets)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if ssl_certificates and (not isinstance(ssl_certificates, list)):
            raise TypeError("Expected argument 'ssl_certificates' to be a list")
        pulumi.set(__self__, 'ssl_certificates', ssl_certificates)
        if ssl_policy and (not isinstance(ssl_policy, dict)):
            raise TypeError("Expected argument 'ssl_policy' to be a dict")
        pulumi.set(__self__, 'ssl_policy', ssl_policy)
        if ssl_profiles and (not isinstance(ssl_profiles, list)):
            raise TypeError("Expected argument 'ssl_profiles' to be a list")
        pulumi.set(__self__, 'ssl_profiles', ssl_profiles)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if trusted_client_certificates and (not isinstance(trusted_client_certificates, list)):
            raise TypeError("Expected argument 'trusted_client_certificates' to be a list")
        pulumi.set(__self__, 'trusted_client_certificates', trusted_client_certificates)
        if trusted_root_certificates and (not isinstance(trusted_root_certificates, list)):
            raise TypeError("Expected argument 'trusted_root_certificates' to be a list")
        pulumi.set(__self__, 'trusted_root_certificates', trusted_root_certificates)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if url_path_maps and (not isinstance(url_path_maps, list)):
            raise TypeError("Expected argument 'url_path_maps' to be a list")
        pulumi.set(__self__, 'url_path_maps', url_path_maps)
        if web_application_firewall_configuration and (not isinstance(web_application_firewall_configuration, dict)):
            raise TypeError("Expected argument 'web_application_firewall_configuration' to be a dict")
        pulumi.set(__self__, 'web_application_firewall_configuration', web_application_firewall_configuration)
        if zones and (not isinstance(zones, list)):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, 'zones', zones)

    @property
    @pulumi.getter(name='authenticationCertificates')
    def authentication_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewayAuthenticationCertificateResponse']]:
        """
        Authentication certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'authentication_certificates')

    @property
    @pulumi.getter(name='autoscaleConfiguration')
    def autoscale_configuration(self) -> Optional['outputs.ApplicationGatewayAutoscaleConfigurationResponse']:
        """
        Autoscale Configuration.
        """
        return pulumi.get(self, 'autoscale_configuration')

    @property
    @pulumi.getter(name='backendAddressPools')
    def backend_address_pools(self) -> Optional[Sequence['outputs.ApplicationGatewayBackendAddressPoolResponse']]:
        """
        Backend address pool of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_address_pools')

    @property
    @pulumi.getter(name='backendHttpSettingsCollection')
    def backend_http_settings_collection(self) -> Optional[Sequence['outputs.ApplicationGatewayBackendHttpSettingsResponse']]:
        """
        Backend http settings of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'backend_http_settings_collection')

    @property
    @pulumi.getter(name='customErrorConfigurations')
    def custom_error_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayCustomErrorResponse']]:
        """
        Custom error configurations of the application gateway resource.
        """
        return pulumi.get(self, 'custom_error_configurations')

    @property
    @pulumi.getter(name='enableFips')
    def enable_fips(self) -> Optional[bool]:
        """
        Whether FIPS is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_fips')

    @property
    @pulumi.getter(name='enableHttp2')
    def enable_http2(self) -> Optional[bool]:
        """
        Whether HTTP2 is enabled on the application gateway resource.
        """
        return pulumi.get(self, 'enable_http2')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='firewallPolicy')
    def firewall_policy(self) -> Optional['outputs.SubResourceResponse']:
        """
        Reference to the FirewallPolicy resource.
        """
        return pulumi.get(self, 'firewall_policy')

    @property
    @pulumi.getter(name='forceFirewallPolicyAssociation')
    def force_firewall_policy_association(self) -> Optional[bool]:
        """
        If true, associates a firewall policy with an application gateway regardless whether the policy differs from the WAF Config.
        """
        return pulumi.get(self, 'force_firewall_policy_association')

    @property
    @pulumi.getter(name='frontendIPConfigurations')
    def frontend_ip_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayFrontendIPConfigurationResponse']]:
        """
        Frontend IP addresses of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ip_configurations')

    @property
    @pulumi.getter(name='frontendPorts')
    def frontend_ports(self) -> Optional[Sequence['outputs.ApplicationGatewayFrontendPortResponse']]:
        """
        Frontend ports of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'frontend_ports')

    @property
    @pulumi.getter(name='gatewayIPConfigurations')
    def gateway_ip_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayIPConfigurationResponse']]:
        """
        Subnets of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'gateway_ip_configurations')

    @property
    @pulumi.getter(name='httpListeners')
    def http_listeners(self) -> Optional[Sequence['outputs.ApplicationGatewayHttpListenerResponse']]:
        """
        Http listeners of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'http_listeners')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ManagedServiceIdentityResponse']:
        """
        The identity of the application gateway, if configured.
        """
        return pulumi.get(self, 'identity')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='operationalState')
    def operational_state(self) -> str:
        """
        Operational state of the application gateway resource.
        """
        return pulumi.get(self, 'operational_state')

    @property
    @pulumi.getter(name='privateEndpointConnections')
    def private_endpoint_connections(self) -> Sequence['outputs.ApplicationGatewayPrivateEndpointConnectionResponse']:
        """
        Private Endpoint connections on application gateway.
        """
        return pulumi.get(self, 'private_endpoint_connections')

    @property
    @pulumi.getter(name='privateLinkConfigurations')
    def private_link_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayPrivateLinkConfigurationResponse']]:
        """
        PrivateLink configurations on application gateway.
        """
        return pulumi.get(self, 'private_link_configurations')

    @property
    @pulumi.getter
    def probes(self) -> Optional[Sequence['outputs.ApplicationGatewayProbeResponse']]:
        """
        Probes of the application gateway resource.
        """
        return pulumi.get(self, 'probes')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the application gateway resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='redirectConfigurations')
    def redirect_configurations(self) -> Optional[Sequence['outputs.ApplicationGatewayRedirectConfigurationResponse']]:
        """
        Redirect configurations of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'redirect_configurations')

    @property
    @pulumi.getter(name='requestRoutingRules')
    def request_routing_rules(self) -> Optional[Sequence['outputs.ApplicationGatewayRequestRoutingRuleResponse']]:
        """
        Request routing rules of the application gateway resource.
        """
        return pulumi.get(self, 'request_routing_rules')

    @property
    @pulumi.getter(name='resourceGuid')
    def resource_guid(self) -> str:
        """
        The resource GUID property of the application gateway resource.
        """
        return pulumi.get(self, 'resource_guid')

    @property
    @pulumi.getter(name='rewriteRuleSets')
    def rewrite_rule_sets(self) -> Optional[Sequence['outputs.ApplicationGatewayRewriteRuleSetResponse']]:
        """
        Rewrite rules for the application gateway resource.
        """
        return pulumi.get(self, 'rewrite_rule_sets')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ApplicationGatewaySkuResponse']:
        """
        SKU of the application gateway resource.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='sslCertificates')
    def ssl_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewaySslCertificateResponse']]:
        """
        SSL certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_certificates')

    @property
    @pulumi.getter(name='sslPolicy')
    def ssl_policy(self) -> Optional['outputs.ApplicationGatewaySslPolicyResponse']:
        """
        SSL policy of the application gateway resource.
        """
        return pulumi.get(self, 'ssl_policy')

    @property
    @pulumi.getter(name='sslProfiles')
    def ssl_profiles(self) -> Optional[Sequence['outputs.ApplicationGatewaySslProfileResponse']]:
        """
        SSL profiles of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'ssl_profiles')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter(name='trustedClientCertificates')
    def trusted_client_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewayTrustedClientCertificateResponse']]:
        """
        Trusted client certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_client_certificates')

    @property
    @pulumi.getter(name='trustedRootCertificates')
    def trusted_root_certificates(self) -> Optional[Sequence['outputs.ApplicationGatewayTrustedRootCertificateResponse']]:
        """
        Trusted Root certificates of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'trusted_root_certificates')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='urlPathMaps')
    def url_path_maps(self) -> Optional[Sequence['outputs.ApplicationGatewayUrlPathMapResponse']]:
        """
        URL path map of the application gateway resource. For default limits, see [Application Gateway limits](https://docs.microsoft.com/azure/azure-subscription-service-limits#application-gateway-limits).
        """
        return pulumi.get(self, 'url_path_maps')

    @property
    @pulumi.getter(name='webApplicationFirewallConfiguration')
    def web_application_firewall_configuration(self) -> Optional['outputs.ApplicationGatewayWebApplicationFirewallConfigurationResponse']:
        """
        Web application firewall configuration.
        """
        return pulumi.get(self, 'web_application_firewall_configuration')

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        A list of availability zones denoting where the resource needs to come from.
        """
        return pulumi.get(self, 'zones')

class AwaitableGetApplicationGatewayResult(GetApplicationGatewayResult):

    def __await__(self):
        if False:
            yield self
        return GetApplicationGatewayResult(authentication_certificates=self.authentication_certificates, autoscale_configuration=self.autoscale_configuration, backend_address_pools=self.backend_address_pools, backend_http_settings_collection=self.backend_http_settings_collection, custom_error_configurations=self.custom_error_configurations, enable_fips=self.enable_fips, enable_http2=self.enable_http2, etag=self.etag, firewall_policy=self.firewall_policy, force_firewall_policy_association=self.force_firewall_policy_association, frontend_ip_configurations=self.frontend_ip_configurations, frontend_ports=self.frontend_ports, gateway_ip_configurations=self.gateway_ip_configurations, http_listeners=self.http_listeners, id=self.id, identity=self.identity, location=self.location, name=self.name, operational_state=self.operational_state, private_endpoint_connections=self.private_endpoint_connections, private_link_configurations=self.private_link_configurations, probes=self.probes, provisioning_state=self.provisioning_state, redirect_configurations=self.redirect_configurations, request_routing_rules=self.request_routing_rules, resource_guid=self.resource_guid, rewrite_rule_sets=self.rewrite_rule_sets, sku=self.sku, ssl_certificates=self.ssl_certificates, ssl_policy=self.ssl_policy, ssl_profiles=self.ssl_profiles, tags=self.tags, trusted_client_certificates=self.trusted_client_certificates, trusted_root_certificates=self.trusted_root_certificates, type=self.type, url_path_maps=self.url_path_maps, web_application_firewall_configuration=self.web_application_firewall_configuration, zones=self.zones)

def get_application_gateway(application_gateway_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetApplicationGatewayResult:
    """
    Application gateway resource.


    :param str application_gateway_name: The name of the application gateway.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['applicationGatewayName'] = application_gateway_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20201101:getApplicationGateway', __args__, opts=opts, typ=GetApplicationGatewayResult).value
    return AwaitableGetApplicationGatewayResult(authentication_certificates=__ret__.authentication_certificates, autoscale_configuration=__ret__.autoscale_configuration, backend_address_pools=__ret__.backend_address_pools, backend_http_settings_collection=__ret__.backend_http_settings_collection, custom_error_configurations=__ret__.custom_error_configurations, enable_fips=__ret__.enable_fips, enable_http2=__ret__.enable_http2, etag=__ret__.etag, firewall_policy=__ret__.firewall_policy, force_firewall_policy_association=__ret__.force_firewall_policy_association, frontend_ip_configurations=__ret__.frontend_ip_configurations, frontend_ports=__ret__.frontend_ports, gateway_ip_configurations=__ret__.gateway_ip_configurations, http_listeners=__ret__.http_listeners, id=__ret__.id, identity=__ret__.identity, location=__ret__.location, name=__ret__.name, operational_state=__ret__.operational_state, private_endpoint_connections=__ret__.private_endpoint_connections, private_link_configurations=__ret__.private_link_configurations, probes=__ret__.probes, provisioning_state=__ret__.provisioning_state, redirect_configurations=__ret__.redirect_configurations, request_routing_rules=__ret__.request_routing_rules, resource_guid=__ret__.resource_guid, rewrite_rule_sets=__ret__.rewrite_rule_sets, sku=__ret__.sku, ssl_certificates=__ret__.ssl_certificates, ssl_policy=__ret__.ssl_policy, ssl_profiles=__ret__.ssl_profiles, tags=__ret__.tags, trusted_client_certificates=__ret__.trusted_client_certificates, trusted_root_certificates=__ret__.trusted_root_certificates, type=__ret__.type, url_path_maps=__ret__.url_path_maps, web_application_firewall_configuration=__ret__.web_application_firewall_configuration, zones=__ret__.zones)

@_utilities.lift_output_func(get_application_gateway)
def get_application_gateway_output(application_gateway_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetApplicationGatewayResult]:
    """
    Application gateway resource.


    :param str application_gateway_name: The name of the application gateway.
    :param str resource_group_name: The name of the resource group.
    """
    ...
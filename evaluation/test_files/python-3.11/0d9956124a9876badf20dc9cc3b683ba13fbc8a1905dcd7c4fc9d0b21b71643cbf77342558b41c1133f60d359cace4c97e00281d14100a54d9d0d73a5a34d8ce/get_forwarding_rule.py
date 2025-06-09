import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetForwardingRuleResult', 'AwaitableGetForwardingRuleResult', 'get_forwarding_rule', 'get_forwarding_rule_output']

@pulumi.output_type
class GetForwardingRuleResult:

    def __init__(__self__, all_ports=None, allow_global_access=None, backend_service=None, creation_timestamp=None, description=None, fingerprint=None, ip_address=None, ip_protocol=None, ip_version=None, is_mirroring_collector=None, kind=None, label_fingerprint=None, labels=None, load_balancing_scheme=None, metadata_filters=None, name=None, network=None, network_tier=None, no_automate_dns_zone=None, port_range=None, ports=None, psc_connection_id=None, psc_connection_status=None, region=None, self_link=None, service_directory_registrations=None, service_label=None, service_name=None, subnetwork=None, target=None):
        if all_ports and (not isinstance(all_ports, bool)):
            raise TypeError("Expected argument 'all_ports' to be a bool")
        pulumi.set(__self__, 'all_ports', all_ports)
        if allow_global_access and (not isinstance(allow_global_access, bool)):
            raise TypeError("Expected argument 'allow_global_access' to be a bool")
        pulumi.set(__self__, 'allow_global_access', allow_global_access)
        if backend_service and (not isinstance(backend_service, str)):
            raise TypeError("Expected argument 'backend_service' to be a str")
        pulumi.set(__self__, 'backend_service', backend_service)
        if creation_timestamp and (not isinstance(creation_timestamp, str)):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, 'creation_timestamp', creation_timestamp)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if fingerprint and (not isinstance(fingerprint, str)):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, 'fingerprint', fingerprint)
        if ip_address and (not isinstance(ip_address, str)):
            raise TypeError("Expected argument 'ip_address' to be a str")
        pulumi.set(__self__, 'ip_address', ip_address)
        if ip_protocol and (not isinstance(ip_protocol, str)):
            raise TypeError("Expected argument 'ip_protocol' to be a str")
        pulumi.set(__self__, 'ip_protocol', ip_protocol)
        if ip_version and (not isinstance(ip_version, str)):
            raise TypeError("Expected argument 'ip_version' to be a str")
        pulumi.set(__self__, 'ip_version', ip_version)
        if is_mirroring_collector and (not isinstance(is_mirroring_collector, bool)):
            raise TypeError("Expected argument 'is_mirroring_collector' to be a bool")
        pulumi.set(__self__, 'is_mirroring_collector', is_mirroring_collector)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if label_fingerprint and (not isinstance(label_fingerprint, str)):
            raise TypeError("Expected argument 'label_fingerprint' to be a str")
        pulumi.set(__self__, 'label_fingerprint', label_fingerprint)
        if labels and (not isinstance(labels, dict)):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, 'labels', labels)
        if load_balancing_scheme and (not isinstance(load_balancing_scheme, str)):
            raise TypeError("Expected argument 'load_balancing_scheme' to be a str")
        pulumi.set(__self__, 'load_balancing_scheme', load_balancing_scheme)
        if metadata_filters and (not isinstance(metadata_filters, list)):
            raise TypeError("Expected argument 'metadata_filters' to be a list")
        pulumi.set(__self__, 'metadata_filters', metadata_filters)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if network and (not isinstance(network, str)):
            raise TypeError("Expected argument 'network' to be a str")
        pulumi.set(__self__, 'network', network)
        if network_tier and (not isinstance(network_tier, str)):
            raise TypeError("Expected argument 'network_tier' to be a str")
        pulumi.set(__self__, 'network_tier', network_tier)
        if no_automate_dns_zone and (not isinstance(no_automate_dns_zone, bool)):
            raise TypeError("Expected argument 'no_automate_dns_zone' to be a bool")
        pulumi.set(__self__, 'no_automate_dns_zone', no_automate_dns_zone)
        if port_range and (not isinstance(port_range, str)):
            raise TypeError("Expected argument 'port_range' to be a str")
        pulumi.set(__self__, 'port_range', port_range)
        if ports and (not isinstance(ports, list)):
            raise TypeError("Expected argument 'ports' to be a list")
        pulumi.set(__self__, 'ports', ports)
        if psc_connection_id and (not isinstance(psc_connection_id, str)):
            raise TypeError("Expected argument 'psc_connection_id' to be a str")
        pulumi.set(__self__, 'psc_connection_id', psc_connection_id)
        if psc_connection_status and (not isinstance(psc_connection_status, str)):
            raise TypeError("Expected argument 'psc_connection_status' to be a str")
        pulumi.set(__self__, 'psc_connection_status', psc_connection_status)
        if region and (not isinstance(region, str)):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, 'region', region)
        if self_link and (not isinstance(self_link, str)):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, 'self_link', self_link)
        if service_directory_registrations and (not isinstance(service_directory_registrations, list)):
            raise TypeError("Expected argument 'service_directory_registrations' to be a list")
        pulumi.set(__self__, 'service_directory_registrations', service_directory_registrations)
        if service_label and (not isinstance(service_label, str)):
            raise TypeError("Expected argument 'service_label' to be a str")
        pulumi.set(__self__, 'service_label', service_label)
        if service_name and (not isinstance(service_name, str)):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, 'service_name', service_name)
        if subnetwork and (not isinstance(subnetwork, str)):
            raise TypeError("Expected argument 'subnetwork' to be a str")
        pulumi.set(__self__, 'subnetwork', subnetwork)
        if target and (not isinstance(target, str)):
            raise TypeError("Expected argument 'target' to be a str")
        pulumi.set(__self__, 'target', target)

    @property
    @pulumi.getter(name='allPorts')
    def all_ports(self) -> bool:
        """
        This field is used along with the backend_service field for Internal TCP/UDP Load Balancing or Network Load Balancing, or with the target field for internal and external TargetInstance. You can only use one of ports and port_range, or allPorts. The three are mutually exclusive. For TCP, UDP and SCTP traffic, packets addressed to any ports will be forwarded to the target or backendService.
        """
        return pulumi.get(self, 'all_ports')

    @property
    @pulumi.getter(name='allowGlobalAccess')
    def allow_global_access(self) -> bool:
        """
        This field is used along with the backend_service field for internal load balancing or with the target field for internal TargetInstance. If the field is set to TRUE, clients can access ILB from all regions. Otherwise only allows access from clients in the same region as the internal load balancer.
        """
        return pulumi.get(self, 'allow_global_access')

    @property
    @pulumi.getter(name='backendService')
    def backend_service(self) -> str:
        """
        Identifies the backend service to which the forwarding rule sends traffic. Required for Internal TCP/UDP Load Balancing and Network Load Balancing; must be omitted for all other load balancer types.
        """
        return pulumi.get(self, 'backend_service')

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> str:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        Fingerprint of this resource. A hash of the contents stored in this object. This field is used in optimistic locking. This field will be ignored when inserting a ForwardingRule. Include the fingerprint in patch request to ensure that you do not overwrite changes that were applied from another concurrent request. To see the latest fingerprint, make a get() request to retrieve a ForwardingRule.
        """
        return pulumi.get(self, 'fingerprint')

    @property
    @pulumi.getter(name='ipAddress')
    def ip_address(self) -> str:
        """
        IP address for which this forwarding rule accepts traffic. When a client sends traffic to this IP address, the forwarding rule directs the traffic to the referenced target or backendService. While creating a forwarding rule, specifying an IPAddress is required under the following circumstances: - When the target is set to targetGrpcProxy and validateForProxyless is set to true, the IPAddress should be set to 0.0.0.0. - When the target is a Private Service Connect Google APIs bundle, you must specify an IPAddress. Otherwise, you can optionally specify an IP address that references an existing static (reserved) IP address resource. When omitted, Google Cloud assigns an ephemeral IP address. Use one of the following formats to specify an IP address while creating a forwarding rule: * IP address number, as in `100.1.2.3` * Full resource URL, as in https://www.googleapis.com/compute/v1/projects/project_id/regions/region /addresses/address-name * Partial URL or by name, as in: - projects/project_id/regions/region/addresses/address-name - regions/region/addresses/address-name - global/addresses/address-name - address-name The forwarding rule's target or backendService, and in most cases, also the loadBalancingScheme, determine the type of IP address that you can use. For detailed information, see [IP address specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#ip_address_specifications). When reading an IPAddress, the API always returns the IP address number.
        """
        return pulumi.get(self, 'ip_address')

    @property
    @pulumi.getter(name='ipProtocol')
    def ip_protocol(self) -> str:
        """
        The IP protocol to which this rule applies. For protocol forwarding, valid options are TCP, UDP, ESP, AH, SCTP, ICMP and L3_DEFAULT. The valid IP protocols are different for different load balancing products as described in [Load balancing features](https://cloud.google.com/load-balancing/docs/features#protocols_from_the_load_balancer_to_the_backends).
        """
        return pulumi.get(self, 'ip_protocol')

    @property
    @pulumi.getter(name='ipVersion')
    def ip_version(self) -> str:
        """
        The IP Version that will be used by this forwarding rule. Valid options are IPV4 or IPV6.
        """
        return pulumi.get(self, 'ip_version')

    @property
    @pulumi.getter(name='isMirroringCollector')
    def is_mirroring_collector(self) -> bool:
        """
        Indicates whether or not this load balancer can be used as a collector for packet mirroring. To prevent mirroring loops, instances behind this load balancer will not have their traffic mirrored even if a PacketMirroring rule applies to them. This can only be set to true for load balancers that have their loadBalancingScheme set to INTERNAL.
        """
        return pulumi.get(self, 'is_mirroring_collector')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Type of the resource. Always compute#forwardingRule for Forwarding Rule resources.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='labelFingerprint')
    def label_fingerprint(self) -> str:
        """
        A fingerprint for the labels being applied to this resource, which is essentially a hash of the labels set used for optimistic locking. The fingerprint is initially generated by Compute Engine and changes after every request to modify or update labels. You must always provide an up-to-date fingerprint hash in order to update or change labels, otherwise the request will fail with error 412 conditionNotMet. To see the latest fingerprint, make a get() request to retrieve a ForwardingRule.
        """
        return pulumi.get(self, 'label_fingerprint')

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Labels for this resource. These can only be added or modified by the setLabels method. Each label key/value pair must comply with RFC1035. Label values may be empty.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter(name='loadBalancingScheme')
    def load_balancing_scheme(self) -> str:
        """
        Specifies the forwarding rule type. For more information about forwarding rules, refer to Forwarding rule concepts.
        """
        return pulumi.get(self, 'load_balancing_scheme')

    @property
    @pulumi.getter(name='metadataFilters')
    def metadata_filters(self) -> Sequence['outputs.MetadataFilterResponse']:
        """
        Opaque filter criteria used by load balancer to restrict routing configuration to a limited set of xDS compliant clients. In their xDS requests to load balancer, xDS clients present node metadata. When there is a match, the relevant configuration is made available to those proxies. Otherwise, all the resources (e.g. TargetHttpProxy, UrlMap) referenced by the ForwardingRule are not visible to those proxies. For each metadataFilter in this list, if its filterMatchCriteria is set to MATCH_ANY, at least one of the filterLabels must match the corresponding label provided in the metadata. If its filterMatchCriteria is set to MATCH_ALL, then all of its filterLabels must match with corresponding labels provided in the metadata. If multiple metadataFilters are specified, all of them need to be satisfied in order to be considered a match. metadataFilters specified here will be applifed before those specified in the UrlMap that this ForwardingRule references. metadataFilters only applies to Loadbalancers that have their loadBalancingScheme set to INTERNAL_SELF_MANAGED.
        """
        return pulumi.get(self, 'metadata_filters')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource; provided by the client when the resource is created. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. For Private Service Connect forwarding rules that forward traffic to Google APIs, the forwarding rule name must be a 1-20 characters string with lowercase letters and numbers and must start with a letter.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def network(self) -> str:
        """
        This field is not used for external load balancing. For Internal TCP/UDP Load Balancing, this field identifies the network that the load balanced IP should belong to for this Forwarding Rule. If this field is not specified, the default network will be used. For Private Service Connect forwarding rules that forward traffic to Google APIs, a network must be provided.
        """
        return pulumi.get(self, 'network')

    @property
    @pulumi.getter(name='networkTier')
    def network_tier(self) -> str:
        """
        This signifies the networking tier used for configuring this load balancer and can only take the following values: PREMIUM, STANDARD. For regional ForwardingRule, the valid values are PREMIUM and STANDARD. For GlobalForwardingRule, the valid value is PREMIUM. If this field is not specified, it is assumed to be PREMIUM. If IPAddress is specified, this value must be equal to the networkTier of the Address.
        """
        return pulumi.get(self, 'network_tier')

    @property
    @pulumi.getter(name='noAutomateDnsZone')
    def no_automate_dns_zone(self) -> bool:
        """
        This is used in PSC consumer ForwardingRule to control whether it should try to auto-generate a DNS zone or not. Non-PSC forwarding rules do not use this field.
        """
        return pulumi.get(self, 'no_automate_dns_zone')

    @property
    @pulumi.getter(name='portRange')
    def port_range(self) -> str:
        """
        This field can be used only if: - Load balancing scheme is one of EXTERNAL, INTERNAL_SELF_MANAGED or INTERNAL_MANAGED - IPProtocol is one of TCP, UDP, or SCTP. Packets addressed to ports in the specified range will be forwarded to target or backend_service. You can only use one of ports, port_range, or allPorts. The three are mutually exclusive. Forwarding rules with the same [IPAddress, IPProtocol] pair must have disjoint ports. Some types of forwarding target have constraints on the acceptable ports. For more information, see [Port specifications](https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications). @pattern: \\\\d+(?:-\\\\d+)?
        """
        return pulumi.get(self, 'port_range')

    @property
    @pulumi.getter
    def ports(self) -> Sequence[str]:
        """
        The ports field is only supported when the forwarding rule references a backend_service directly. Only packets addressed to the [specified list of ports]((https://cloud.google.com/load-balancing/docs/forwarding-rule-concepts#port_specifications)) are forwarded to backends. You can only use one of ports and port_range, or allPorts. The three are mutually exclusive. You can specify a list of up to five ports, which can be non-contiguous. Forwarding rules with the same [IPAddress, IPProtocol] pair must have disjoint ports. @pattern: \\\\d+(?:-\\\\d+)?
        """
        return pulumi.get(self, 'ports')

    @property
    @pulumi.getter(name='pscConnectionId')
    def psc_connection_id(self) -> str:
        """
        The PSC connection id of the PSC Forwarding Rule.
        """
        return pulumi.get(self, 'psc_connection_id')

    @property
    @pulumi.getter(name='pscConnectionStatus')
    def psc_connection_status(self) -> str:
        return pulumi.get(self, 'psc_connection_status')

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        URL of the region where the regional forwarding rule resides. This field is not applicable to global forwarding rules. You must specify this field as part of the HTTP request URL. It is not settable as a field in the request body.
        """
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> str:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter(name='serviceDirectoryRegistrations')
    def service_directory_registrations(self) -> Sequence['outputs.ForwardingRuleServiceDirectoryRegistrationResponse']:
        """
        Service Directory resources to register this forwarding rule with. Currently, only supports a single Service Directory resource.
        """
        return pulumi.get(self, 'service_directory_registrations')

    @property
    @pulumi.getter(name='serviceLabel')
    def service_label(self) -> str:
        """
        An optional prefix to the service name for this Forwarding Rule. If specified, the prefix is the first label of the fully qualified service name. The label must be 1-63 characters long, and comply with RFC1035. Specifically, the label must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. This field is only used for internal load balancing.
        """
        return pulumi.get(self, 'service_label')

    @property
    @pulumi.getter(name='serviceName')
    def service_name(self) -> str:
        """
        The internal fully qualified service name for this Forwarding Rule. This field is only used for internal load balancing.
        """
        return pulumi.get(self, 'service_name')

    @property
    @pulumi.getter
    def subnetwork(self) -> str:
        """
        This field identifies the subnetwork that the load balanced IP should belong to for this Forwarding Rule, used in internal load balancing and network load balancing with IPv6. If the network specified is in auto subnet mode, this field is optional. However, a subnetwork must be specified if the network is in custom subnet mode or when creating external forwarding rule with IPv6.
        """
        return pulumi.get(self, 'subnetwork')

    @property
    @pulumi.getter
    def target(self) -> str:
        return pulumi.get(self, 'target')

class AwaitableGetForwardingRuleResult(GetForwardingRuleResult):

    def __await__(self):
        if False:
            yield self
        return GetForwardingRuleResult(all_ports=self.all_ports, allow_global_access=self.allow_global_access, backend_service=self.backend_service, creation_timestamp=self.creation_timestamp, description=self.description, fingerprint=self.fingerprint, ip_address=self.ip_address, ip_protocol=self.ip_protocol, ip_version=self.ip_version, is_mirroring_collector=self.is_mirroring_collector, kind=self.kind, label_fingerprint=self.label_fingerprint, labels=self.labels, load_balancing_scheme=self.load_balancing_scheme, metadata_filters=self.metadata_filters, name=self.name, network=self.network, network_tier=self.network_tier, no_automate_dns_zone=self.no_automate_dns_zone, port_range=self.port_range, ports=self.ports, psc_connection_id=self.psc_connection_id, psc_connection_status=self.psc_connection_status, region=self.region, self_link=self.self_link, service_directory_registrations=self.service_directory_registrations, service_label=self.service_label, service_name=self.service_name, subnetwork=self.subnetwork, target=self.target)

def get_forwarding_rule(forwarding_rule: Optional[str]=None, project: Optional[str]=None, region: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetForwardingRuleResult:
    """
    Returns the specified ForwardingRule resource.
    """
    __args__ = dict()
    __args__['forwardingRule'] = forwarding_rule
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:compute/v1:getForwardingRule', __args__, opts=opts, typ=GetForwardingRuleResult).value
    return AwaitableGetForwardingRuleResult(all_ports=__ret__.all_ports, allow_global_access=__ret__.allow_global_access, backend_service=__ret__.backend_service, creation_timestamp=__ret__.creation_timestamp, description=__ret__.description, fingerprint=__ret__.fingerprint, ip_address=__ret__.ip_address, ip_protocol=__ret__.ip_protocol, ip_version=__ret__.ip_version, is_mirroring_collector=__ret__.is_mirroring_collector, kind=__ret__.kind, label_fingerprint=__ret__.label_fingerprint, labels=__ret__.labels, load_balancing_scheme=__ret__.load_balancing_scheme, metadata_filters=__ret__.metadata_filters, name=__ret__.name, network=__ret__.network, network_tier=__ret__.network_tier, no_automate_dns_zone=__ret__.no_automate_dns_zone, port_range=__ret__.port_range, ports=__ret__.ports, psc_connection_id=__ret__.psc_connection_id, psc_connection_status=__ret__.psc_connection_status, region=__ret__.region, self_link=__ret__.self_link, service_directory_registrations=__ret__.service_directory_registrations, service_label=__ret__.service_label, service_name=__ret__.service_name, subnetwork=__ret__.subnetwork, target=__ret__.target)

@_utilities.lift_output_func(get_forwarding_rule)
def get_forwarding_rule_output(forwarding_rule: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[Optional[str]]]=None, region: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetForwardingRuleResult]:
    """
    Returns the specified ForwardingRule resource.
    """
    ...
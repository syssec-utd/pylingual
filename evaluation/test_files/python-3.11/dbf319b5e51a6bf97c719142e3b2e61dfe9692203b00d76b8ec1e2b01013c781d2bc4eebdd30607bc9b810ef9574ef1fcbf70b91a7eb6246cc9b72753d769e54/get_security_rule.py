import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetSecurityRuleResult', 'AwaitableGetSecurityRuleResult', 'get_security_rule', 'get_security_rule_output']

@pulumi.output_type
class GetSecurityRuleResult:
    """
    Network security rule.
    """

    def __init__(__self__, access=None, description=None, destination_address_prefix=None, destination_address_prefixes=None, destination_application_security_groups=None, destination_port_range=None, destination_port_ranges=None, direction=None, etag=None, id=None, name=None, priority=None, protocol=None, provisioning_state=None, source_address_prefix=None, source_address_prefixes=None, source_application_security_groups=None, source_port_range=None, source_port_ranges=None):
        if access and (not isinstance(access, str)):
            raise TypeError("Expected argument 'access' to be a str")
        pulumi.set(__self__, 'access', access)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if destination_address_prefix and (not isinstance(destination_address_prefix, str)):
            raise TypeError("Expected argument 'destination_address_prefix' to be a str")
        pulumi.set(__self__, 'destination_address_prefix', destination_address_prefix)
        if destination_address_prefixes and (not isinstance(destination_address_prefixes, list)):
            raise TypeError("Expected argument 'destination_address_prefixes' to be a list")
        pulumi.set(__self__, 'destination_address_prefixes', destination_address_prefixes)
        if destination_application_security_groups and (not isinstance(destination_application_security_groups, list)):
            raise TypeError("Expected argument 'destination_application_security_groups' to be a list")
        pulumi.set(__self__, 'destination_application_security_groups', destination_application_security_groups)
        if destination_port_range and (not isinstance(destination_port_range, str)):
            raise TypeError("Expected argument 'destination_port_range' to be a str")
        pulumi.set(__self__, 'destination_port_range', destination_port_range)
        if destination_port_ranges and (not isinstance(destination_port_ranges, list)):
            raise TypeError("Expected argument 'destination_port_ranges' to be a list")
        pulumi.set(__self__, 'destination_port_ranges', destination_port_ranges)
        if direction and (not isinstance(direction, str)):
            raise TypeError("Expected argument 'direction' to be a str")
        pulumi.set(__self__, 'direction', direction)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if priority and (not isinstance(priority, int)):
            raise TypeError("Expected argument 'priority' to be a int")
        pulumi.set(__self__, 'priority', priority)
        if protocol and (not isinstance(protocol, str)):
            raise TypeError("Expected argument 'protocol' to be a str")
        pulumi.set(__self__, 'protocol', protocol)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if source_address_prefix and (not isinstance(source_address_prefix, str)):
            raise TypeError("Expected argument 'source_address_prefix' to be a str")
        pulumi.set(__self__, 'source_address_prefix', source_address_prefix)
        if source_address_prefixes and (not isinstance(source_address_prefixes, list)):
            raise TypeError("Expected argument 'source_address_prefixes' to be a list")
        pulumi.set(__self__, 'source_address_prefixes', source_address_prefixes)
        if source_application_security_groups and (not isinstance(source_application_security_groups, list)):
            raise TypeError("Expected argument 'source_application_security_groups' to be a list")
        pulumi.set(__self__, 'source_application_security_groups', source_application_security_groups)
        if source_port_range and (not isinstance(source_port_range, str)):
            raise TypeError("Expected argument 'source_port_range' to be a str")
        pulumi.set(__self__, 'source_port_range', source_port_range)
        if source_port_ranges and (not isinstance(source_port_ranges, list)):
            raise TypeError("Expected argument 'source_port_ranges' to be a list")
        pulumi.set(__self__, 'source_port_ranges', source_port_ranges)

    @property
    @pulumi.getter
    def access(self) -> str:
        """
        The network traffic is allowed or denied.
        """
        return pulumi.get(self, 'access')

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='destinationAddressPrefix')
    def destination_address_prefix(self) -> Optional[str]:
        """
        The destination address prefix. CIDR or destination IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used.
        """
        return pulumi.get(self, 'destination_address_prefix')

    @property
    @pulumi.getter(name='destinationAddressPrefixes')
    def destination_address_prefixes(self) -> Optional[Sequence[str]]:
        """
        The destination address prefixes. CIDR or destination IP ranges.
        """
        return pulumi.get(self, 'destination_address_prefixes')

    @property
    @pulumi.getter(name='destinationApplicationSecurityGroups')
    def destination_application_security_groups(self) -> Optional[Sequence['outputs.ApplicationSecurityGroupResponse']]:
        """
        The application security group specified as destination.
        """
        return pulumi.get(self, 'destination_application_security_groups')

    @property
    @pulumi.getter(name='destinationPortRange')
    def destination_port_range(self) -> Optional[str]:
        """
        The destination port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, 'destination_port_range')

    @property
    @pulumi.getter(name='destinationPortRanges')
    def destination_port_ranges(self) -> Optional[Sequence[str]]:
        """
        The destination port ranges.
        """
        return pulumi.get(self, 'destination_port_ranges')

    @property
    @pulumi.getter
    def direction(self) -> str:
        """
        The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
        """
        return pulumi.get(self, 'direction')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def priority(self) -> Optional[int]:
        """
        The priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        """
        return pulumi.get(self, 'priority')

    @property
    @pulumi.getter
    def protocol(self) -> str:
        """
        Network protocol this rule applies to.
        """
        return pulumi.get(self, 'protocol')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the security rule resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='sourceAddressPrefix')
    def source_address_prefix(self) -> Optional[str]:
        """
        The CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from.
        """
        return pulumi.get(self, 'source_address_prefix')

    @property
    @pulumi.getter(name='sourceAddressPrefixes')
    def source_address_prefixes(self) -> Optional[Sequence[str]]:
        """
        The CIDR or source IP ranges.
        """
        return pulumi.get(self, 'source_address_prefixes')

    @property
    @pulumi.getter(name='sourceApplicationSecurityGroups')
    def source_application_security_groups(self) -> Optional[Sequence['outputs.ApplicationSecurityGroupResponse']]:
        """
        The application security group specified as source.
        """
        return pulumi.get(self, 'source_application_security_groups')

    @property
    @pulumi.getter(name='sourcePortRange')
    def source_port_range(self) -> Optional[str]:
        """
        The source port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, 'source_port_range')

    @property
    @pulumi.getter(name='sourcePortRanges')
    def source_port_ranges(self) -> Optional[Sequence[str]]:
        """
        The source port ranges.
        """
        return pulumi.get(self, 'source_port_ranges')

class AwaitableGetSecurityRuleResult(GetSecurityRuleResult):

    def __await__(self):
        if False:
            yield self
        return GetSecurityRuleResult(access=self.access, description=self.description, destination_address_prefix=self.destination_address_prefix, destination_address_prefixes=self.destination_address_prefixes, destination_application_security_groups=self.destination_application_security_groups, destination_port_range=self.destination_port_range, destination_port_ranges=self.destination_port_ranges, direction=self.direction, etag=self.etag, id=self.id, name=self.name, priority=self.priority, protocol=self.protocol, provisioning_state=self.provisioning_state, source_address_prefix=self.source_address_prefix, source_address_prefixes=self.source_address_prefixes, source_application_security_groups=self.source_application_security_groups, source_port_range=self.source_port_range, source_port_ranges=self.source_port_ranges)

def get_security_rule(network_security_group_name: Optional[str]=None, resource_group_name: Optional[str]=None, security_rule_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetSecurityRuleResult:
    """
    Get the specified network security rule.


    :param str network_security_group_name: The name of the network security group.
    :param str resource_group_name: The name of the resource group.
    :param str security_rule_name: The name of the security rule.
    """
    __args__ = dict()
    __args__['networkSecurityGroupName'] = network_security_group_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['securityRuleName'] = security_rule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20190901:getSecurityRule', __args__, opts=opts, typ=GetSecurityRuleResult).value
    return AwaitableGetSecurityRuleResult(access=__ret__.access, description=__ret__.description, destination_address_prefix=__ret__.destination_address_prefix, destination_address_prefixes=__ret__.destination_address_prefixes, destination_application_security_groups=__ret__.destination_application_security_groups, destination_port_range=__ret__.destination_port_range, destination_port_ranges=__ret__.destination_port_ranges, direction=__ret__.direction, etag=__ret__.etag, id=__ret__.id, name=__ret__.name, priority=__ret__.priority, protocol=__ret__.protocol, provisioning_state=__ret__.provisioning_state, source_address_prefix=__ret__.source_address_prefix, source_address_prefixes=__ret__.source_address_prefixes, source_application_security_groups=__ret__.source_application_security_groups, source_port_range=__ret__.source_port_range, source_port_ranges=__ret__.source_port_ranges)

@_utilities.lift_output_func(get_security_rule)
def get_security_rule_output(network_security_group_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, security_rule_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetSecurityRuleResult]:
    """
    Get the specified network security rule.


    :param str network_security_group_name: The name of the network security group.
    :param str resource_group_name: The name of the resource group.
    :param str security_rule_name: The name of the security rule.
    """
    ...
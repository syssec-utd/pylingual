import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetWebApplicationFirewallPolicyResult', 'AwaitableGetWebApplicationFirewallPolicyResult', 'get_web_application_firewall_policy', 'get_web_application_firewall_policy_output']

@pulumi.output_type
class GetWebApplicationFirewallPolicyResult:
    """
    Defines web application firewall policy.
    """

    def __init__(__self__, application_gateways=None, custom_rules=None, etag=None, http_listeners=None, id=None, location=None, managed_rules=None, name=None, path_based_rules=None, policy_settings=None, provisioning_state=None, resource_state=None, tags=None, type=None):
        if application_gateways and (not isinstance(application_gateways, list)):
            raise TypeError("Expected argument 'application_gateways' to be a list")
        pulumi.set(__self__, 'application_gateways', application_gateways)
        if custom_rules and (not isinstance(custom_rules, list)):
            raise TypeError("Expected argument 'custom_rules' to be a list")
        pulumi.set(__self__, 'custom_rules', custom_rules)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if http_listeners and (not isinstance(http_listeners, list)):
            raise TypeError("Expected argument 'http_listeners' to be a list")
        pulumi.set(__self__, 'http_listeners', http_listeners)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if managed_rules and (not isinstance(managed_rules, dict)):
            raise TypeError("Expected argument 'managed_rules' to be a dict")
        pulumi.set(__self__, 'managed_rules', managed_rules)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if path_based_rules and (not isinstance(path_based_rules, list)):
            raise TypeError("Expected argument 'path_based_rules' to be a list")
        pulumi.set(__self__, 'path_based_rules', path_based_rules)
        if policy_settings and (not isinstance(policy_settings, dict)):
            raise TypeError("Expected argument 'policy_settings' to be a dict")
        pulumi.set(__self__, 'policy_settings', policy_settings)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if resource_state and (not isinstance(resource_state, str)):
            raise TypeError("Expected argument 'resource_state' to be a str")
        pulumi.set(__self__, 'resource_state', resource_state)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='applicationGateways')
    def application_gateways(self) -> Sequence['outputs.ApplicationGatewayResponse']:
        """
        A collection of references to application gateways.
        """
        return pulumi.get(self, 'application_gateways')

    @property
    @pulumi.getter(name='customRules')
    def custom_rules(self) -> Optional[Sequence['outputs.WebApplicationFirewallCustomRuleResponse']]:
        """
        The custom rules inside the policy.
        """
        return pulumi.get(self, 'custom_rules')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter(name='httpListeners')
    def http_listeners(self) -> Sequence['outputs.SubResourceResponse']:
        """
        A collection of references to application gateway http listeners.
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
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='managedRules')
    def managed_rules(self) -> 'outputs.ManagedRulesDefinitionResponse':
        """
        Describes the managedRules structure.
        """
        return pulumi.get(self, 'managed_rules')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='pathBasedRules')
    def path_based_rules(self) -> Sequence['outputs.SubResourceResponse']:
        """
        A collection of references to application gateway path rules.
        """
        return pulumi.get(self, 'path_based_rules')

    @property
    @pulumi.getter(name='policySettings')
    def policy_settings(self) -> Optional['outputs.PolicySettingsResponse']:
        """
        The PolicySettings for policy.
        """
        return pulumi.get(self, 'policy_settings')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        The provisioning state of the web application firewall policy resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='resourceState')
    def resource_state(self) -> str:
        """
        Resource status of the policy.
        """
        return pulumi.get(self, 'resource_state')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetWebApplicationFirewallPolicyResult(GetWebApplicationFirewallPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetWebApplicationFirewallPolicyResult(application_gateways=self.application_gateways, custom_rules=self.custom_rules, etag=self.etag, http_listeners=self.http_listeners, id=self.id, location=self.location, managed_rules=self.managed_rules, name=self.name, path_based_rules=self.path_based_rules, policy_settings=self.policy_settings, provisioning_state=self.provisioning_state, resource_state=self.resource_state, tags=self.tags, type=self.type)

def get_web_application_firewall_policy(policy_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWebApplicationFirewallPolicyResult:
    """
    Retrieve protection policy with specified name within a resource group.


    :param str policy_name: The name of the policy.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['policyName'] = policy_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220101:getWebApplicationFirewallPolicy', __args__, opts=opts, typ=GetWebApplicationFirewallPolicyResult).value
    return AwaitableGetWebApplicationFirewallPolicyResult(application_gateways=__ret__.application_gateways, custom_rules=__ret__.custom_rules, etag=__ret__.etag, http_listeners=__ret__.http_listeners, id=__ret__.id, location=__ret__.location, managed_rules=__ret__.managed_rules, name=__ret__.name, path_based_rules=__ret__.path_based_rules, policy_settings=__ret__.policy_settings, provisioning_state=__ret__.provisioning_state, resource_state=__ret__.resource_state, tags=__ret__.tags, type=__ret__.type)

@_utilities.lift_output_func(get_web_application_firewall_policy)
def get_web_application_firewall_policy_output(policy_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWebApplicationFirewallPolicyResult]:
    """
    Retrieve protection policy with specified name within a resource group.


    :param str policy_name: The name of the policy.
    :param str resource_group_name: The name of the resource group.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['EventHubAuthorizationRuleArgs', 'EventHubAuthorizationRule']

@pulumi.input_type
class EventHubAuthorizationRuleArgs:

    def __init__(__self__, *, event_hub_name: pulumi.Input[str], namespace_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], rights: pulumi.Input[Sequence[pulumi.Input['AccessRights']]], authorization_rule_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a EventHubAuthorizationRule resource.
        :param pulumi.Input[str] event_hub_name: The Event Hub name
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input['AccessRights']]] rights: The rights associated with the rule.
        :param pulumi.Input[str] authorization_rule_name: The authorization rule name.
        :param pulumi.Input[str] location: Data center location.
        :param pulumi.Input[str] name: Name of the AuthorizationRule.
        """
        pulumi.set(__self__, 'event_hub_name', event_hub_name)
        pulumi.set(__self__, 'namespace_name', namespace_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'rights', rights)
        if authorization_rule_name is not None:
            pulumi.set(__self__, 'authorization_rule_name', authorization_rule_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter(name='eventHubName')
    def event_hub_name(self) -> pulumi.Input[str]:
        """
        The Event Hub name
        """
        return pulumi.get(self, 'event_hub_name')

    @event_hub_name.setter
    def event_hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'event_hub_name', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The Namespace name
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the azure subscription.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Input[Sequence[pulumi.Input['AccessRights']]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, 'rights')

    @rights.setter
    def rights(self, value: pulumi.Input[Sequence[pulumi.Input['AccessRights']]]):
        pulumi.set(self, 'rights', value)

    @property
    @pulumi.getter(name='authorizationRuleName')
    def authorization_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The authorization rule name.
        """
        return pulumi.get(self, 'authorization_rule_name')

    @authorization_rule_name.setter
    def authorization_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'authorization_rule_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Data center location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the AuthorizationRule.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)
warnings.warn('Version 2015-08-01 will be removed in v2 of the provider.', DeprecationWarning)

class EventHubAuthorizationRule(pulumi.CustomResource):
    warnings.warn('Version 2015-08-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, authorization_rule_name: Optional[pulumi.Input[str]]=None, event_hub_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rights: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]]=None, __props__=None):
        """
        Single item in a List or Get AuthorizationRule operation

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_rule_name: The authorization rule name.
        :param pulumi.Input[str] event_hub_name: The Event Hub name
        :param pulumi.Input[str] location: Data center location.
        :param pulumi.Input[str] name: Name of the AuthorizationRule.
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input['AccessRights']]] rights: The rights associated with the rule.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: EventHubAuthorizationRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Single item in a List or Get AuthorizationRule operation

        :param str resource_name: The name of the resource.
        :param EventHubAuthorizationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(EventHubAuthorizationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, authorization_rule_name: Optional[pulumi.Input[str]]=None, event_hub_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rights: Optional[pulumi.Input[Sequence[pulumi.Input['AccessRights']]]]=None, __props__=None):
        pulumi.log.warn('EventHubAuthorizationRule is deprecated: Version 2015-08-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventHubAuthorizationRuleArgs.__new__(EventHubAuthorizationRuleArgs)
            __props__.__dict__['authorization_rule_name'] = authorization_rule_name
            if event_hub_name is None and (not opts.urn):
                raise TypeError("Missing required property 'event_hub_name'")
            __props__.__dict__['event_hub_name'] = event_hub_name
            __props__.__dict__['location'] = location
            __props__.__dict__['name'] = name
            if namespace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__['namespace_name'] = namespace_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if rights is None and (not opts.urn):
                raise TypeError("Missing required property 'rights'")
            __props__.__dict__['rights'] = rights
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:eventhub:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20140901:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20170401:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20180101preview:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20210101preview:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20210601preview:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20211101:EventHubAuthorizationRule'), pulumi.Alias(type_='azure-native:eventhub/v20220101preview:EventHubAuthorizationRule')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventHubAuthorizationRule, __self__).__init__('azure-native:eventhub/v20150801:EventHubAuthorizationRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'EventHubAuthorizationRule':
        """
        Get an existing EventHubAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = EventHubAuthorizationRuleArgs.__new__(EventHubAuthorizationRuleArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['rights'] = None
        __props__.__dict__['type'] = None
        return EventHubAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Output[Sequence[str]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, 'rights')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')
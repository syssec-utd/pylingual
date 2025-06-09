import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['RuleArgs', 'Rule']

@pulumi.input_type
class RuleArgs:

    def __init__(__self__, *, namespace_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], subscription_name: pulumi.Input[str], topic_name: pulumi.Input[str], action: Optional[pulumi.Input['ActionArgs']]=None, correlation_filter: Optional[pulumi.Input['CorrelationFilterArgs']]=None, filter_type: Optional[pulumi.Input['FilterType']]=None, rule_name: Optional[pulumi.Input[str]]=None, sql_filter: Optional[pulumi.Input['SqlFilterArgs']]=None):
        """
        The set of arguments for constructing a Rule resource.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] subscription_name: The subscription name.
        :param pulumi.Input[str] topic_name: The topic name.
        :param pulumi.Input['ActionArgs'] action: Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        :param pulumi.Input['CorrelationFilterArgs'] correlation_filter: Properties of correlationFilter
        :param pulumi.Input['FilterType'] filter_type: Filter type that is evaluated against a BrokeredMessage.
        :param pulumi.Input[str] rule_name: The rule name.
        :param pulumi.Input['SqlFilterArgs'] sql_filter: Properties of sqlFilter
        """
        pulumi.set(__self__, 'namespace_name', namespace_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'subscription_name', subscription_name)
        pulumi.set(__self__, 'topic_name', topic_name)
        if action is not None:
            pulumi.set(__self__, 'action', action)
        if correlation_filter is not None:
            pulumi.set(__self__, 'correlation_filter', correlation_filter)
        if filter_type is not None:
            pulumi.set(__self__, 'filter_type', filter_type)
        if rule_name is not None:
            pulumi.set(__self__, 'rule_name', rule_name)
        if sql_filter is not None:
            pulumi.set(__self__, 'sql_filter', sql_filter)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The namespace name
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Resource group within the Azure subscription.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='subscriptionName')
    def subscription_name(self) -> pulumi.Input[str]:
        """
        The subscription name.
        """
        return pulumi.get(self, 'subscription_name')

    @subscription_name.setter
    def subscription_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'subscription_name', value)

    @property
    @pulumi.getter(name='topicName')
    def topic_name(self) -> pulumi.Input[str]:
        """
        The topic name.
        """
        return pulumi.get(self, 'topic_name')

    @topic_name.setter
    def topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'topic_name', value)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input['ActionArgs']]:
        """
        Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        """
        return pulumi.get(self, 'action')

    @action.setter
    def action(self, value: Optional[pulumi.Input['ActionArgs']]):
        pulumi.set(self, 'action', value)

    @property
    @pulumi.getter(name='correlationFilter')
    def correlation_filter(self) -> Optional[pulumi.Input['CorrelationFilterArgs']]:
        """
        Properties of correlationFilter
        """
        return pulumi.get(self, 'correlation_filter')

    @correlation_filter.setter
    def correlation_filter(self, value: Optional[pulumi.Input['CorrelationFilterArgs']]):
        pulumi.set(self, 'correlation_filter', value)

    @property
    @pulumi.getter(name='filterType')
    def filter_type(self) -> Optional[pulumi.Input['FilterType']]:
        """
        Filter type that is evaluated against a BrokeredMessage.
        """
        return pulumi.get(self, 'filter_type')

    @filter_type.setter
    def filter_type(self, value: Optional[pulumi.Input['FilterType']]):
        pulumi.set(self, 'filter_type', value)

    @property
    @pulumi.getter(name='ruleName')
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The rule name.
        """
        return pulumi.get(self, 'rule_name')

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'rule_name', value)

    @property
    @pulumi.getter(name='sqlFilter')
    def sql_filter(self) -> Optional[pulumi.Input['SqlFilterArgs']]:
        """
        Properties of sqlFilter
        """
        return pulumi.get(self, 'sql_filter')

    @sql_filter.setter
    def sql_filter(self, value: Optional[pulumi.Input['SqlFilterArgs']]):
        pulumi.set(self, 'sql_filter', value)

class Rule(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, action: Optional[pulumi.Input[pulumi.InputType['ActionArgs']]]=None, correlation_filter: Optional[pulumi.Input[pulumi.InputType['CorrelationFilterArgs']]]=None, filter_type: Optional[pulumi.Input['FilterType']]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_name: Optional[pulumi.Input[str]]=None, sql_filter: Optional[pulumi.Input[pulumi.InputType['SqlFilterArgs']]]=None, subscription_name: Optional[pulumi.Input[str]]=None, topic_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Description of Rule Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ActionArgs']] action: Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        :param pulumi.Input[pulumi.InputType['CorrelationFilterArgs']] correlation_filter: Properties of correlationFilter
        :param pulumi.Input['FilterType'] filter_type: Filter type that is evaluated against a BrokeredMessage.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] rule_name: The rule name.
        :param pulumi.Input[pulumi.InputType['SqlFilterArgs']] sql_filter: Properties of sqlFilter
        :param pulumi.Input[str] subscription_name: The subscription name.
        :param pulumi.Input[str] topic_name: The topic name.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: RuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Description of Rule Resource.

        :param str resource_name: The name of the resource.
        :param RuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(RuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, action: Optional[pulumi.Input[pulumi.InputType['ActionArgs']]]=None, correlation_filter: Optional[pulumi.Input[pulumi.InputType['CorrelationFilterArgs']]]=None, filter_type: Optional[pulumi.Input['FilterType']]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, rule_name: Optional[pulumi.Input[str]]=None, sql_filter: Optional[pulumi.Input[pulumi.InputType['SqlFilterArgs']]]=None, subscription_name: Optional[pulumi.Input[str]]=None, topic_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RuleArgs.__new__(RuleArgs)
            __props__.__dict__['action'] = action
            __props__.__dict__['correlation_filter'] = correlation_filter
            __props__.__dict__['filter_type'] = filter_type
            if namespace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__['namespace_name'] = namespace_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['rule_name'] = rule_name
            __props__.__dict__['sql_filter'] = sql_filter
            if subscription_name is None and (not opts.urn):
                raise TypeError("Missing required property 'subscription_name'")
            __props__.__dict__['subscription_name'] = subscription_name
            if topic_name is None and (not opts.urn):
                raise TypeError("Missing required property 'topic_name'")
            __props__.__dict__['topic_name'] = topic_name
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:servicebus:Rule'), pulumi.Alias(type_='azure-native:servicebus/v20180101preview:Rule'), pulumi.Alias(type_='azure-native:servicebus/v20210101preview:Rule'), pulumi.Alias(type_='azure-native:servicebus/v20210601preview:Rule'), pulumi.Alias(type_='azure-native:servicebus/v20211101:Rule'), pulumi.Alias(type_='azure-native:servicebus/v20220101preview:Rule')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Rule, __self__).__init__('azure-native:servicebus/v20170401:Rule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = RuleArgs.__new__(RuleArgs)
        __props__.__dict__['action'] = None
        __props__.__dict__['correlation_filter'] = None
        __props__.__dict__['filter_type'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['sql_filter'] = None
        __props__.__dict__['type'] = None
        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[Optional['outputs.ActionResponse']]:
        """
        Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        """
        return pulumi.get(self, 'action')

    @property
    @pulumi.getter(name='correlationFilter')
    def correlation_filter(self) -> pulumi.Output[Optional['outputs.CorrelationFilterResponse']]:
        """
        Properties of correlationFilter
        """
        return pulumi.get(self, 'correlation_filter')

    @property
    @pulumi.getter(name='filterType')
    def filter_type(self) -> pulumi.Output[Optional[str]]:
        """
        Filter type that is evaluated against a BrokeredMessage.
        """
        return pulumi.get(self, 'filter_type')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='sqlFilter')
    def sql_filter(self) -> pulumi.Output[Optional['outputs.SqlFilterResponse']]:
        """
        Properties of sqlFilter
        """
        return pulumi.get(self, 'sql_filter')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')
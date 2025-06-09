import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['AntiBruteForceRuleArgs', 'AntiBruteForceRule']

@pulumi.input_type
class AntiBruteForceRuleArgs:

    def __init__(__self__, *, anti_brute_force_rule_name: pulumi.Input[str], fail_count: pulumi.Input[int], forbidden_time: pulumi.Input[int], span: pulumi.Input[int], uuid_lists: pulumi.Input[Sequence[pulumi.Input[str]]], default_rule: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a AntiBruteForceRule resource.
        :param pulumi.Input[str] anti_brute_force_rule_name: The name of the defense rule.
        :param pulumi.Input[int] fail_count: The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        :param pulumi.Input[int] forbidden_time: The period of time during which logons from an account are not allowed. Unit: minutes.
        :param pulumi.Input[int] span: The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] uuid_lists: An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        :param pulumi.Input[bool] default_rule: Specifies whether to set the defense rule as the default rule.
        """
        pulumi.set(__self__, 'anti_brute_force_rule_name', anti_brute_force_rule_name)
        pulumi.set(__self__, 'fail_count', fail_count)
        pulumi.set(__self__, 'forbidden_time', forbidden_time)
        pulumi.set(__self__, 'span', span)
        pulumi.set(__self__, 'uuid_lists', uuid_lists)
        if default_rule is not None:
            pulumi.set(__self__, 'default_rule', default_rule)

    @property
    @pulumi.getter(name='antiBruteForceRuleName')
    def anti_brute_force_rule_name(self) -> pulumi.Input[str]:
        """
        The name of the defense rule.
        """
        return pulumi.get(self, 'anti_brute_force_rule_name')

    @anti_brute_force_rule_name.setter
    def anti_brute_force_rule_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'anti_brute_force_rule_name', value)

    @property
    @pulumi.getter(name='failCount')
    def fail_count(self) -> pulumi.Input[int]:
        """
        The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        """
        return pulumi.get(self, 'fail_count')

    @fail_count.setter
    def fail_count(self, value: pulumi.Input[int]):
        pulumi.set(self, 'fail_count', value)

    @property
    @pulumi.getter(name='forbiddenTime')
    def forbidden_time(self) -> pulumi.Input[int]:
        """
        The period of time during which logons from an account are not allowed. Unit: minutes.
        """
        return pulumi.get(self, 'forbidden_time')

    @forbidden_time.setter
    def forbidden_time(self, value: pulumi.Input[int]):
        pulumi.set(self, 'forbidden_time', value)

    @property
    @pulumi.getter
    def span(self) -> pulumi.Input[int]:
        """
        The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        """
        return pulumi.get(self, 'span')

    @span.setter
    def span(self, value: pulumi.Input[int]):
        pulumi.set(self, 'span', value)

    @property
    @pulumi.getter(name='uuidLists')
    def uuid_lists(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        return pulumi.get(self, 'uuid_lists')

    @uuid_lists.setter
    def uuid_lists(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'uuid_lists', value)

    @property
    @pulumi.getter(name='defaultRule')
    def default_rule(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to set the defense rule as the default rule.
        """
        return pulumi.get(self, 'default_rule')

    @default_rule.setter
    def default_rule(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'default_rule', value)

@pulumi.input_type
class _AntiBruteForceRuleState:

    def __init__(__self__, *, anti_brute_force_rule_id: Optional[pulumi.Input[str]]=None, anti_brute_force_rule_name: Optional[pulumi.Input[str]]=None, default_rule: Optional[pulumi.Input[bool]]=None, fail_count: Optional[pulumi.Input[int]]=None, forbidden_time: Optional[pulumi.Input[int]]=None, span: Optional[pulumi.Input[int]]=None, uuid_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        Input properties used for looking up and filtering AntiBruteForceRule resources.
        :param pulumi.Input[str] anti_brute_force_rule_id: The ID of the defense rule.
        :param pulumi.Input[str] anti_brute_force_rule_name: The name of the defense rule.
        :param pulumi.Input[bool] default_rule: Specifies whether to set the defense rule as the default rule.
        :param pulumi.Input[int] fail_count: The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        :param pulumi.Input[int] forbidden_time: The period of time during which logons from an account are not allowed. Unit: minutes.
        :param pulumi.Input[int] span: The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] uuid_lists: An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        if anti_brute_force_rule_id is not None:
            pulumi.set(__self__, 'anti_brute_force_rule_id', anti_brute_force_rule_id)
        if anti_brute_force_rule_name is not None:
            pulumi.set(__self__, 'anti_brute_force_rule_name', anti_brute_force_rule_name)
        if default_rule is not None:
            pulumi.set(__self__, 'default_rule', default_rule)
        if fail_count is not None:
            pulumi.set(__self__, 'fail_count', fail_count)
        if forbidden_time is not None:
            pulumi.set(__self__, 'forbidden_time', forbidden_time)
        if span is not None:
            pulumi.set(__self__, 'span', span)
        if uuid_lists is not None:
            pulumi.set(__self__, 'uuid_lists', uuid_lists)

    @property
    @pulumi.getter(name='antiBruteForceRuleId')
    def anti_brute_force_rule_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the defense rule.
        """
        return pulumi.get(self, 'anti_brute_force_rule_id')

    @anti_brute_force_rule_id.setter
    def anti_brute_force_rule_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'anti_brute_force_rule_id', value)

    @property
    @pulumi.getter(name='antiBruteForceRuleName')
    def anti_brute_force_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the defense rule.
        """
        return pulumi.get(self, 'anti_brute_force_rule_name')

    @anti_brute_force_rule_name.setter
    def anti_brute_force_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'anti_brute_force_rule_name', value)

    @property
    @pulumi.getter(name='defaultRule')
    def default_rule(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to set the defense rule as the default rule.
        """
        return pulumi.get(self, 'default_rule')

    @default_rule.setter
    def default_rule(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'default_rule', value)

    @property
    @pulumi.getter(name='failCount')
    def fail_count(self) -> Optional[pulumi.Input[int]]:
        """
        The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        """
        return pulumi.get(self, 'fail_count')

    @fail_count.setter
    def fail_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'fail_count', value)

    @property
    @pulumi.getter(name='forbiddenTime')
    def forbidden_time(self) -> Optional[pulumi.Input[int]]:
        """
        The period of time during which logons from an account are not allowed. Unit: minutes.
        """
        return pulumi.get(self, 'forbidden_time')

    @forbidden_time.setter
    def forbidden_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'forbidden_time', value)

    @property
    @pulumi.getter
    def span(self) -> Optional[pulumi.Input[int]]:
        """
        The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        """
        return pulumi.get(self, 'span')

    @span.setter
    def span(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'span', value)

    @property
    @pulumi.getter(name='uuidLists')
    def uuid_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        return pulumi.get(self, 'uuid_lists')

    @uuid_lists.setter
    def uuid_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'uuid_lists', value)

class AntiBruteForceRule(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, anti_brute_force_rule_name: Optional[pulumi.Input[str]]=None, default_rule: Optional[pulumi.Input[bool]]=None, fail_count: Optional[pulumi.Input[int]]=None, forbidden_time: Optional[pulumi.Input[int]]=None, span: Optional[pulumi.Input[int]]=None, uuid_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        Provides a Threat Detection Anti Brute Force Rule resource.

        For information about Threat Detection Anti Brute Force Rule and how to use it, see [What is Anti Brute Force Rule](https://www.alibabacloud.com/help/en/security-center/latest/api-doc-sas-2018-12-03-api-doc-createantibruteforcerule).

        > **NOTE:** Available in v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.threatdetection.AntiBruteForceRule("default",
            anti_brute_force_rule_name="apispec_test",
            fail_count=80,
            forbidden_time=360,
            span=10,
            uuid_lists=["032b618f-b220-4a0d-bd37-fbdc6ef58b6a"])
        ```

        ## Import

        Threat Detection Anti Brute Force Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:threatdetection/antiBruteForceRule:AntiBruteForceRule example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] anti_brute_force_rule_name: The name of the defense rule.
        :param pulumi.Input[bool] default_rule: Specifies whether to set the defense rule as the default rule.
        :param pulumi.Input[int] fail_count: The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        :param pulumi.Input[int] forbidden_time: The period of time during which logons from an account are not allowed. Unit: minutes.
        :param pulumi.Input[int] span: The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] uuid_lists: An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: AntiBruteForceRuleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a Threat Detection Anti Brute Force Rule resource.

        For information about Threat Detection Anti Brute Force Rule and how to use it, see [What is Anti Brute Force Rule](https://www.alibabacloud.com/help/en/security-center/latest/api-doc-sas-2018-12-03-api-doc-createantibruteforcerule).

        > **NOTE:** Available in v1.195.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.threatdetection.AntiBruteForceRule("default",
            anti_brute_force_rule_name="apispec_test",
            fail_count=80,
            forbidden_time=360,
            span=10,
            uuid_lists=["032b618f-b220-4a0d-bd37-fbdc6ef58b6a"])
        ```

        ## Import

        Threat Detection Anti Brute Force Rule can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:threatdetection/antiBruteForceRule:AntiBruteForceRule example <id>
        ```

        :param str resource_name: The name of the resource.
        :param AntiBruteForceRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(AntiBruteForceRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, anti_brute_force_rule_name: Optional[pulumi.Input[str]]=None, default_rule: Optional[pulumi.Input[bool]]=None, fail_count: Optional[pulumi.Input[int]]=None, forbidden_time: Optional[pulumi.Input[int]]=None, span: Optional[pulumi.Input[int]]=None, uuid_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AntiBruteForceRuleArgs.__new__(AntiBruteForceRuleArgs)
            if anti_brute_force_rule_name is None and (not opts.urn):
                raise TypeError("Missing required property 'anti_brute_force_rule_name'")
            __props__.__dict__['anti_brute_force_rule_name'] = anti_brute_force_rule_name
            __props__.__dict__['default_rule'] = default_rule
            if fail_count is None and (not opts.urn):
                raise TypeError("Missing required property 'fail_count'")
            __props__.__dict__['fail_count'] = fail_count
            if forbidden_time is None and (not opts.urn):
                raise TypeError("Missing required property 'forbidden_time'")
            __props__.__dict__['forbidden_time'] = forbidden_time
            if span is None and (not opts.urn):
                raise TypeError("Missing required property 'span'")
            __props__.__dict__['span'] = span
            if uuid_lists is None and (not opts.urn):
                raise TypeError("Missing required property 'uuid_lists'")
            __props__.__dict__['uuid_lists'] = uuid_lists
            __props__.__dict__['anti_brute_force_rule_id'] = None
        super(AntiBruteForceRule, __self__).__init__('alicloud:threatdetection/antiBruteForceRule:AntiBruteForceRule', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, anti_brute_force_rule_id: Optional[pulumi.Input[str]]=None, anti_brute_force_rule_name: Optional[pulumi.Input[str]]=None, default_rule: Optional[pulumi.Input[bool]]=None, fail_count: Optional[pulumi.Input[int]]=None, forbidden_time: Optional[pulumi.Input[int]]=None, span: Optional[pulumi.Input[int]]=None, uuid_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None) -> 'AntiBruteForceRule':
        """
        Get an existing AntiBruteForceRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] anti_brute_force_rule_id: The ID of the defense rule.
        :param pulumi.Input[str] anti_brute_force_rule_name: The name of the defense rule.
        :param pulumi.Input[bool] default_rule: Specifies whether to set the defense rule as the default rule.
        :param pulumi.Input[int] fail_count: The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        :param pulumi.Input[int] forbidden_time: The period of time during which logons from an account are not allowed. Unit: minutes.
        :param pulumi.Input[int] span: The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] uuid_lists: An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _AntiBruteForceRuleState.__new__(_AntiBruteForceRuleState)
        __props__.__dict__['anti_brute_force_rule_id'] = anti_brute_force_rule_id
        __props__.__dict__['anti_brute_force_rule_name'] = anti_brute_force_rule_name
        __props__.__dict__['default_rule'] = default_rule
        __props__.__dict__['fail_count'] = fail_count
        __props__.__dict__['forbidden_time'] = forbidden_time
        __props__.__dict__['span'] = span
        __props__.__dict__['uuid_lists'] = uuid_lists
        return AntiBruteForceRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='antiBruteForceRuleId')
    def anti_brute_force_rule_id(self) -> pulumi.Output[str]:
        """
        The ID of the defense rule.
        """
        return pulumi.get(self, 'anti_brute_force_rule_id')

    @property
    @pulumi.getter(name='antiBruteForceRuleName')
    def anti_brute_force_rule_name(self) -> pulumi.Output[str]:
        """
        The name of the defense rule.
        """
        return pulumi.get(self, 'anti_brute_force_rule_name')

    @property
    @pulumi.getter(name='defaultRule')
    def default_rule(self) -> pulumi.Output[bool]:
        """
        Specifies whether to set the defense rule as the default rule.
        """
        return pulumi.get(self, 'default_rule')

    @property
    @pulumi.getter(name='failCount')
    def fail_count(self) -> pulumi.Output[int]:
        """
        The threshold for the number of failed user logins when the brute-force defense rule takes effect.
        """
        return pulumi.get(self, 'fail_count')

    @property
    @pulumi.getter(name='forbiddenTime')
    def forbidden_time(self) -> pulumi.Output[int]:
        """
        The period of time during which logons from an account are not allowed. Unit: minutes.
        """
        return pulumi.get(self, 'forbidden_time')

    @property
    @pulumi.getter
    def span(self) -> pulumi.Output[int]:
        """
        The period of time during which logon failures from an account are measured. Unit: minutes. If Span is set to 10, the defense rule takes effect when the logon failures measured within 10 minutes reaches the specified threshold. The IP address of attackers cannot be used to log on to the server in the specified period of time.
        """
        return pulumi.get(self, 'span')

    @property
    @pulumi.getter(name='uuidLists')
    def uuid_lists(self) -> pulumi.Output[Sequence[str]]:
        """
        An array consisting of the UUIDs of servers to which the defense rule is applied.**The binding status must be Enterprise Edition.**
        """
        return pulumi.get(self, 'uuid_lists')
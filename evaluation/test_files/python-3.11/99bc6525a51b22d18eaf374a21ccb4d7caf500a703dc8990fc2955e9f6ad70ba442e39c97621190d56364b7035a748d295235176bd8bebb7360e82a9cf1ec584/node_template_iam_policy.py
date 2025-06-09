import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['NodeTemplateIamPolicyArgs', 'NodeTemplateIamPolicy']

@pulumi.input_type
class NodeTemplateIamPolicyArgs:

    def __init__(__self__, *, region: pulumi.Input[str], resource: pulumi.Input[str], audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input['BindingArgs']]]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, rules: Optional[pulumi.Input[Sequence[pulumi.Input['RuleArgs']]]]=None, version: Optional[pulumi.Input[int]]=None):
        """
        The set of arguments for constructing a NodeTemplateIamPolicy resource.
        :param pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]] audit_configs: Specifies cloud audit logging configuration for this policy.
        :param pulumi.Input[Sequence[pulumi.Input['BindingArgs']]] bindings: Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        :param pulumi.Input[Sequence[pulumi.Input['RuleArgs']]] rules: This is deprecated and has no effect. Do not use.
        :param pulumi.Input[int] version: Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        pulumi.set(__self__, 'region', region)
        pulumi.set(__self__, 'resource', resource)
        if audit_configs is not None:
            pulumi.set(__self__, 'audit_configs', audit_configs)
        if bindings is not None:
            pulumi.set(__self__, 'bindings', bindings)
        if etag is not None:
            pulumi.set(__self__, 'etag', etag)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if rules is not None:
            pulumi.set(__self__, 'rules', rules)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def region(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'region')

    @region.setter
    def region(self, value: pulumi.Input[str]):
        pulumi.set(self, 'region', value)

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'resource')

    @resource.setter
    def resource(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource', value)

    @property
    @pulumi.getter(name='auditConfigs')
    def audit_configs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]]]:
        """
        Specifies cloud audit logging configuration for this policy.
        """
        return pulumi.get(self, 'audit_configs')

    @audit_configs.setter
    def audit_configs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]]]):
        pulumi.set(self, 'audit_configs', value)

    @property
    @pulumi.getter
    def bindings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BindingArgs']]]]:
        """
        Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        """
        return pulumi.get(self, 'bindings')

    @bindings.setter
    def bindings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BindingArgs']]]]):
        pulumi.set(self, 'bindings', value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        """
        return pulumi.get(self, 'etag')

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'etag', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RuleArgs']]]]:
        """
        This is deprecated and has no effect. Do not use.
        """
        return pulumi.get(self, 'rules')

    @rules.setter
    def rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RuleArgs']]]]):
        pulumi.set(self, 'rules', value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, 'version')

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'version', value)

class NodeTemplateIamPolicy(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, resource: Optional[pulumi.Input[str]]=None, rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleArgs']]]]]=None, version: Optional[pulumi.Input[int]]=None, __props__=None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]] audit_configs: Specifies cloud audit logging configuration for this policy.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]] bindings: Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleArgs']]]] rules: This is deprecated and has no effect. Do not use.
        :param pulumi.Input[int] version: Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: NodeTemplateIamPolicyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param NodeTemplateIamPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NodeTemplateIamPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, resource: Optional[pulumi.Input[str]]=None, rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RuleArgs']]]]]=None, version: Optional[pulumi.Input[int]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        else:
            opts = copy.copy(opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NodeTemplateIamPolicyArgs.__new__(NodeTemplateIamPolicyArgs)
            __props__.__dict__['audit_configs'] = audit_configs
            __props__.__dict__['bindings'] = bindings
            __props__.__dict__['etag'] = etag
            __props__.__dict__['project'] = project
            if region is None and (not opts.urn):
                raise TypeError("Missing required property 'region'")
            __props__.__dict__['region'] = region
            if resource is None and (not opts.urn):
                raise TypeError("Missing required property 'resource'")
            __props__.__dict__['resource'] = resource
            __props__.__dict__['rules'] = rules
            __props__.__dict__['version'] = version
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['project', 'region', 'resource'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(NodeTemplateIamPolicy, __self__).__init__('google-native:compute/alpha:NodeTemplateIamPolicy', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'NodeTemplateIamPolicy':
        """
        Get an existing NodeTemplateIamPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = NodeTemplateIamPolicyArgs.__new__(NodeTemplateIamPolicyArgs)
        __props__.__dict__['audit_configs'] = None
        __props__.__dict__['bindings'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['region'] = None
        __props__.__dict__['resource'] = None
        __props__.__dict__['rules'] = None
        __props__.__dict__['version'] = None
        return NodeTemplateIamPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='auditConfigs')
    def audit_configs(self) -> pulumi.Output[Sequence['outputs.AuditConfigResponse']]:
        """
        Specifies cloud audit logging configuration for this policy.
        """
        return pulumi.get(self, 'audit_configs')

    @property
    @pulumi.getter
    def bindings(self) -> pulumi.Output[Sequence['outputs.BindingResponse']]:
        """
        Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        """
        return pulumi.get(self, 'bindings')

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'resource')

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Sequence['outputs.RuleResponse']]:
        """
        This is deprecated and has no effect. Do not use.
        """
        return pulumi.get(self, 'rules')

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, 'version')
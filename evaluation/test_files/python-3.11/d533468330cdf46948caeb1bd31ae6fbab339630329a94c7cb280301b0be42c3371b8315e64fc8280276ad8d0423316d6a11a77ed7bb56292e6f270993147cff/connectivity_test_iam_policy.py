import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ConnectivityTestIamPolicyArgs', 'ConnectivityTestIamPolicy']

@pulumi.input_type
class ConnectivityTestIamPolicyArgs:

    def __init__(__self__, *, connectivity_test_id: pulumi.Input[str], audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input['BindingArgs']]]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, update_mask: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[int]]=None):
        """
        The set of arguments for constructing a ConnectivityTestIamPolicy resource.
        :param pulumi.Input[Sequence[pulumi.Input['AuditConfigArgs']]] audit_configs: Specifies cloud audit logging configuration for this policy.
        :param pulumi.Input[Sequence[pulumi.Input['BindingArgs']]] bindings: Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        :param pulumi.Input[str] update_mask: OPTIONAL: A FieldMask specifying which fields of the policy to modify. Only the fields in the mask will be modified. If no mask is provided, the following default mask is used: `paths: "bindings, etag"`
        :param pulumi.Input[int] version: Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        pulumi.set(__self__, 'connectivity_test_id', connectivity_test_id)
        if audit_configs is not None:
            pulumi.set(__self__, 'audit_configs', audit_configs)
        if bindings is not None:
            pulumi.set(__self__, 'bindings', bindings)
        if etag is not None:
            pulumi.set(__self__, 'etag', etag)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if update_mask is not None:
            pulumi.set(__self__, 'update_mask', update_mask)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter(name='connectivityTestId')
    def connectivity_test_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'connectivity_test_id')

    @connectivity_test_id.setter
    def connectivity_test_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'connectivity_test_id', value)

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
    @pulumi.getter(name='updateMask')
    def update_mask(self) -> Optional[pulumi.Input[str]]:
        """
        OPTIONAL: A FieldMask specifying which fields of the policy to modify. Only the fields in the mask will be modified. If no mask is provided, the following default mask is used: `paths: "bindings, etag"`
        """
        return pulumi.get(self, 'update_mask')

    @update_mask.setter
    def update_mask(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'update_mask', value)

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

class ConnectivityTestIamPolicy(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]]]=None, connectivity_test_id: Optional[pulumi.Input[str]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, update_mask: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[int]]=None, __props__=None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]] audit_configs: Specifies cloud audit logging configuration for this policy.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]] bindings: Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        :param pulumi.Input[str] etag: `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        :param pulumi.Input[str] update_mask: OPTIONAL: A FieldMask specifying which fields of the policy to modify. Only the fields in the mask will be modified. If no mask is provided, the following default mask is used: `paths: "bindings, etag"`
        :param pulumi.Input[int] version: Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ConnectivityTestIamPolicyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Sets the access control policy on the specified resource. Replaces any existing policy. Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.
        Note - this resource's API doesn't support deletion. When deleted, the resource will persist
        on Google Cloud even though it will be deleted from Pulumi state.

        :param str resource_name: The name of the resource.
        :param ConnectivityTestIamPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectivityTestIamPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, audit_configs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AuditConfigArgs']]]]]=None, bindings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BindingArgs']]]]]=None, connectivity_test_id: Optional[pulumi.Input[str]]=None, etag: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, update_mask: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[int]]=None, __props__=None):
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
            __props__ = ConnectivityTestIamPolicyArgs.__new__(ConnectivityTestIamPolicyArgs)
            __props__.__dict__['audit_configs'] = audit_configs
            __props__.__dict__['bindings'] = bindings
            if connectivity_test_id is None and (not opts.urn):
                raise TypeError("Missing required property 'connectivity_test_id'")
            __props__.__dict__['connectivity_test_id'] = connectivity_test_id
            __props__.__dict__['etag'] = etag
            __props__.__dict__['project'] = project
            __props__.__dict__['update_mask'] = update_mask
            __props__.__dict__['version'] = version
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['connectivity_test_id', 'project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ConnectivityTestIamPolicy, __self__).__init__('google-native:networkmanagement/v1beta1:ConnectivityTestIamPolicy', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ConnectivityTestIamPolicy':
        """
        Get an existing ConnectivityTestIamPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ConnectivityTestIamPolicyArgs.__new__(ConnectivityTestIamPolicyArgs)
        __props__.__dict__['audit_configs'] = None
        __props__.__dict__['bindings'] = None
        __props__.__dict__['connectivity_test_id'] = None
        __props__.__dict__['etag'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['version'] = None
        return ConnectivityTestIamPolicy(resource_name, opts=opts, __props__=__props__)

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
    @pulumi.getter(name='connectivityTestId')
    def connectivity_test_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'connectivity_test_id')

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
    def version(self) -> pulumi.Output[int]:
        """
        Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, 'version')
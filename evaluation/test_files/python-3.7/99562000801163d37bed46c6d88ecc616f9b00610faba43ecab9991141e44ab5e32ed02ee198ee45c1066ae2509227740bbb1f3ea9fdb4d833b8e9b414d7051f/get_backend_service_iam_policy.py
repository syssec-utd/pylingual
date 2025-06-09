import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetBackendServiceIamPolicyResult', 'AwaitableGetBackendServiceIamPolicyResult', 'get_backend_service_iam_policy', 'get_backend_service_iam_policy_output']

@pulumi.output_type
class GetBackendServiceIamPolicyResult:

    def __init__(__self__, audit_configs=None, bindings=None, etag=None, rules=None, version=None):
        if audit_configs and (not isinstance(audit_configs, list)):
            raise TypeError("Expected argument 'audit_configs' to be a list")
        pulumi.set(__self__, 'audit_configs', audit_configs)
        if bindings and (not isinstance(bindings, list)):
            raise TypeError("Expected argument 'bindings' to be a list")
        pulumi.set(__self__, 'bindings', bindings)
        if etag and (not isinstance(etag, str)):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, 'etag', etag)
        if rules and (not isinstance(rules, list)):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, 'rules', rules)
        if version and (not isinstance(version, int)):
            raise TypeError("Expected argument 'version' to be a int")
        pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter(name='auditConfigs')
    def audit_configs(self) -> Sequence['outputs.AuditConfigResponse']:
        """
        Specifies cloud audit logging configuration for this policy.
        """
        return pulumi.get(self, 'audit_configs')

    @property
    @pulumi.getter
    def bindings(self) -> Sequence['outputs.BindingResponse']:
        """
        Associates a list of `members`, or principals, with a `role`. Optionally, may specify a `condition` that determines how and when the `bindings` are applied. Each of the `bindings` must contain at least one principal. The `bindings` in a `Policy` can refer to up to 1,500 principals; up to 250 of these principals can be Google groups. Each occurrence of a principal counts towards these limits. For example, if the `bindings` grant 50 different roles to `user:alice@example.com`, and not to any other principal, then you can add another 1,450 principals to the `bindings` in the `Policy`.
        """
        return pulumi.get(self, 'bindings')

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        `etag` is used for optimistic concurrency control as a way to help prevent simultaneous updates of a policy from overwriting each other. It is strongly suggested that systems make use of the `etag` in the read-modify-write cycle to perform policy updates in order to avoid race conditions: An `etag` is returned in the response to `getIamPolicy`, and systems are expected to put that etag in the request to `setIamPolicy` to ensure that their change will be applied to the same version of the policy. **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def rules(self) -> Sequence['outputs.RuleResponse']:
        """
        This is deprecated and has no effect. Do not use.
        """
        return pulumi.get(self, 'rules')

    @property
    @pulumi.getter
    def version(self) -> int:
        """
        Specifies the format of the policy. Valid values are `0`, `1`, and `3`. Requests that specify an invalid value are rejected. Any operation that affects conditional role bindings must specify version `3`. This requirement applies to the following operations: * Getting a policy that includes a conditional role binding * Adding a conditional role binding to a policy * Changing a conditional role binding in a policy * Removing any role binding, with or without a condition, from a policy that includes conditions **Important:** If you use IAM Conditions, you must include the `etag` field whenever you call `setIamPolicy`. If you omit this field, then IAM allows you to overwrite a version `3` policy with a version `1` policy, and all of the conditions in the version `3` policy are lost. If a policy does not include any conditions, operations on that policy may specify any valid version or leave the field unset. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, 'version')

class AwaitableGetBackendServiceIamPolicyResult(GetBackendServiceIamPolicyResult):

    def __await__(self):
        if False:
            yield self
        return GetBackendServiceIamPolicyResult(audit_configs=self.audit_configs, bindings=self.bindings, etag=self.etag, rules=self.rules, version=self.version)

def get_backend_service_iam_policy(options_requested_policy_version: Optional[str]=None, project: Optional[str]=None, resource: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetBackendServiceIamPolicyResult:
    """
    Gets the access control policy for a resource. May be empty if no such policy or resource exists.
    """
    __args__ = dict()
    __args__['optionsRequestedPolicyVersion'] = options_requested_policy_version
    __args__['project'] = project
    __args__['resource'] = resource
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:compute/beta:getBackendServiceIamPolicy', __args__, opts=opts, typ=GetBackendServiceIamPolicyResult).value
    return AwaitableGetBackendServiceIamPolicyResult(audit_configs=__ret__.audit_configs, bindings=__ret__.bindings, etag=__ret__.etag, rules=__ret__.rules, version=__ret__.version)

@_utilities.lift_output_func(get_backend_service_iam_policy)
def get_backend_service_iam_policy_output(options_requested_policy_version: Optional[pulumi.Input[Optional[str]]]=None, project: Optional[pulumi.Input[Optional[str]]]=None, resource: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetBackendServiceIamPolicyResult]:
    """
    Gets the access control policy for a resource. May be empty if no such policy or resource exists.
    """
    ...
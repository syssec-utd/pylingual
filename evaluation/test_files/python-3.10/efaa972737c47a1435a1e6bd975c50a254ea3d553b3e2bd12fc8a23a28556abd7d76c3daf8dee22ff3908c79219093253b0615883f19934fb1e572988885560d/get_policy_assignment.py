import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPolicyAssignmentResult', 'AwaitableGetPolicyAssignmentResult', 'get_policy_assignment', 'get_policy_assignment_output']

@pulumi.output_type
class GetPolicyAssignmentResult:
    """
    The policy assignment.
    """

    def __init__(__self__, description=None, display_name=None, id=None, metadata=None, name=None, not_scopes=None, parameters=None, policy_definition_id=None, scope=None, sku=None, type=None):
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if metadata and (not isinstance(metadata, dict)):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, 'metadata', metadata)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if not_scopes and (not isinstance(not_scopes, list)):
            raise TypeError("Expected argument 'not_scopes' to be a list")
        pulumi.set(__self__, 'not_scopes', not_scopes)
        if parameters and (not isinstance(parameters, dict)):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, 'parameters', parameters)
        if policy_definition_id and (not isinstance(policy_definition_id, str)):
            raise TypeError("Expected argument 'policy_definition_id' to be a str")
        pulumi.set(__self__, 'policy_definition_id', policy_definition_id)
        if scope and (not isinstance(scope, str)):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, 'scope', scope)
        if sku and (not isinstance(sku, dict)):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, 'sku', sku)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        This message will be part of response in case of policy violation.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        The display name of the policy assignment.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the policy assignment.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Any]:
        """
        The policy assignment metadata.
        """
        return pulumi.get(self, 'metadata')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the policy assignment.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='notScopes')
    def not_scopes(self) -> Optional[Sequence[str]]:
        """
        The policy's excluded scopes.
        """
        return pulumi.get(self, 'not_scopes')

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        """
        Required if a parameter is used in policy rule.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter(name='policyDefinitionId')
    def policy_definition_id(self) -> Optional[str]:
        """
        The ID of the policy definition.
        """
        return pulumi.get(self, 'policy_definition_id')

    @property
    @pulumi.getter
    def scope(self) -> Optional[str]:
        """
        The scope for the policy assignment.
        """
        return pulumi.get(self, 'scope')

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.PolicySkuResponse']:
        """
        The policy sku.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the policy assignment.
        """
        return pulumi.get(self, 'type')

class AwaitableGetPolicyAssignmentResult(GetPolicyAssignmentResult):

    def __await__(self):
        if False:
            yield self
        return GetPolicyAssignmentResult(description=self.description, display_name=self.display_name, id=self.id, metadata=self.metadata, name=self.name, not_scopes=self.not_scopes, parameters=self.parameters, policy_definition_id=self.policy_definition_id, scope=self.scope, sku=self.sku, type=self.type)

def get_policy_assignment(policy_assignment_name: Optional[str]=None, scope: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPolicyAssignmentResult:
    """
    The policy assignment.


    :param str policy_assignment_name: The name of the policy assignment to get.
    :param str scope: The scope of the policy assignment.
    """
    __args__ = dict()
    __args__['policyAssignmentName'] = policy_assignment_name
    __args__['scope'] = scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20170601preview:getPolicyAssignment', __args__, opts=opts, typ=GetPolicyAssignmentResult).value
    return AwaitableGetPolicyAssignmentResult(description=__ret__.description, display_name=__ret__.display_name, id=__ret__.id, metadata=__ret__.metadata, name=__ret__.name, not_scopes=__ret__.not_scopes, parameters=__ret__.parameters, policy_definition_id=__ret__.policy_definition_id, scope=__ret__.scope, sku=__ret__.sku, type=__ret__.type)

@_utilities.lift_output_func(get_policy_assignment)
def get_policy_assignment_output(policy_assignment_name: Optional[pulumi.Input[str]]=None, scope: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPolicyAssignmentResult]:
    """
    The policy assignment.


    :param str policy_assignment_name: The name of the policy assignment to get.
    :param str scope: The scope of the policy assignment.
    """
    ...
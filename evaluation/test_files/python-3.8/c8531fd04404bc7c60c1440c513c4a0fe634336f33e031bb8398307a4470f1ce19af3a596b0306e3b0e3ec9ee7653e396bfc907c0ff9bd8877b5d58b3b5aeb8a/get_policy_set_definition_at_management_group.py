import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPolicySetDefinitionAtManagementGroupResult', 'AwaitableGetPolicySetDefinitionAtManagementGroupResult', 'get_policy_set_definition_at_management_group', 'get_policy_set_definition_at_management_group_output']

@pulumi.output_type
class GetPolicySetDefinitionAtManagementGroupResult:
    """
    The policy set definition.
    """

    def __init__(__self__, description=None, display_name=None, id=None, metadata=None, name=None, parameters=None, policy_definition_groups=None, policy_definitions=None, policy_type=None, type=None):
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
        if parameters and (not isinstance(parameters, dict)):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, 'parameters', parameters)
        if policy_definition_groups and (not isinstance(policy_definition_groups, list)):
            raise TypeError("Expected argument 'policy_definition_groups' to be a list")
        pulumi.set(__self__, 'policy_definition_groups', policy_definition_groups)
        if policy_definitions and (not isinstance(policy_definitions, list)):
            raise TypeError("Expected argument 'policy_definitions' to be a list")
        pulumi.set(__self__, 'policy_definitions', policy_definitions)
        if policy_type and (not isinstance(policy_type, str)):
            raise TypeError("Expected argument 'policy_type' to be a str")
        pulumi.set(__self__, 'policy_type', policy_type)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The policy set definition description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        The display name of the policy set definition.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the policy set definition.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Any]:
        """
        The policy set definition metadata.  Metadata is an open ended object and is typically a collection of key value pairs.
        """
        return pulumi.get(self, 'metadata')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the policy set definition.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, 'outputs.ParameterDefinitionsValueResponse']]:
        """
        The policy set definition parameters that can be used in policy definition references.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter(name='policyDefinitionGroups')
    def policy_definition_groups(self) -> Optional[Sequence['outputs.PolicyDefinitionGroupResponse']]:
        """
        The metadata describing groups of policy definition references within the policy set definition.
        """
        return pulumi.get(self, 'policy_definition_groups')

    @property
    @pulumi.getter(name='policyDefinitions')
    def policy_definitions(self) -> Sequence['outputs.PolicyDefinitionReferenceResponse']:
        """
        An array of policy definition references.
        """
        return pulumi.get(self, 'policy_definitions')

    @property
    @pulumi.getter(name='policyType')
    def policy_type(self) -> Optional[str]:
        """
        The type of policy definition. Possible values are NotSpecified, BuiltIn, Custom, and Static.
        """
        return pulumi.get(self, 'policy_type')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource (Microsoft.Authorization/policySetDefinitions).
        """
        return pulumi.get(self, 'type')

class AwaitableGetPolicySetDefinitionAtManagementGroupResult(GetPolicySetDefinitionAtManagementGroupResult):

    def __await__(self):
        if False:
            yield self
        return GetPolicySetDefinitionAtManagementGroupResult(description=self.description, display_name=self.display_name, id=self.id, metadata=self.metadata, name=self.name, parameters=self.parameters, policy_definition_groups=self.policy_definition_groups, policy_definitions=self.policy_definitions, policy_type=self.policy_type, type=self.type)

def get_policy_set_definition_at_management_group(management_group_id: Optional[str]=None, policy_set_definition_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPolicySetDefinitionAtManagementGroupResult:
    """
    This operation retrieves the policy set definition in the given management group with the given name.


    :param str management_group_id: The ID of the management group.
    :param str policy_set_definition_name: The name of the policy set definition to get.
    """
    __args__ = dict()
    __args__['managementGroupId'] = management_group_id
    __args__['policySetDefinitionName'] = policy_set_definition_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20190901:getPolicySetDefinitionAtManagementGroup', __args__, opts=opts, typ=GetPolicySetDefinitionAtManagementGroupResult).value
    return AwaitableGetPolicySetDefinitionAtManagementGroupResult(description=__ret__.description, display_name=__ret__.display_name, id=__ret__.id, metadata=__ret__.metadata, name=__ret__.name, parameters=__ret__.parameters, policy_definition_groups=__ret__.policy_definition_groups, policy_definitions=__ret__.policy_definitions, policy_type=__ret__.policy_type, type=__ret__.type)

@_utilities.lift_output_func(get_policy_set_definition_at_management_group)
def get_policy_set_definition_at_management_group_output(management_group_id: Optional[pulumi.Input[str]]=None, policy_set_definition_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPolicySetDefinitionAtManagementGroupResult]:
    """
    This operation retrieves the policy set definition in the given management group with the given name.


    :param str management_group_id: The ID of the management group.
    :param str policy_set_definition_name: The name of the policy set definition to get.
    """
    ...
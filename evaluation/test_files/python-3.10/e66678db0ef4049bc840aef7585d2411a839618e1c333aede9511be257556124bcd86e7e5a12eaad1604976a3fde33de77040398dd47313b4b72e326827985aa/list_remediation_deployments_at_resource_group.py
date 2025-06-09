import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['ListRemediationDeploymentsAtResourceGroupResult', 'AwaitableListRemediationDeploymentsAtResourceGroupResult', 'list_remediation_deployments_at_resource_group', 'list_remediation_deployments_at_resource_group_output']

@pulumi.output_type
class ListRemediationDeploymentsAtResourceGroupResult:
    """
    List of deployments for a remediation.
    """

    def __init__(__self__, next_link=None, value=None):
        if next_link and (not isinstance(next_link, str)):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, 'next_link', next_link)
        if value and (not isinstance(value, list)):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter(name='nextLink')
    def next_link(self) -> str:
        """
        The URL to get the next set of results.
        """
        return pulumi.get(self, 'next_link')

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.RemediationDeploymentResponse']:
        """
        Array of deployments for the remediation.
        """
        return pulumi.get(self, 'value')

class AwaitableListRemediationDeploymentsAtResourceGroupResult(ListRemediationDeploymentsAtResourceGroupResult):

    def __await__(self):
        if False:
            yield self
        return ListRemediationDeploymentsAtResourceGroupResult(next_link=self.next_link, value=self.value)

def list_remediation_deployments_at_resource_group(remediation_name: Optional[str]=None, resource_group_name: Optional[str]=None, top: Optional[int]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListRemediationDeploymentsAtResourceGroupResult:
    """
    List of deployments for a remediation.
    API Version: 2019-07-01.


    :param str remediation_name: The name of the remediation.
    :param str resource_group_name: Resource group name.
    :param int top: Maximum number of records to return.
    """
    __args__ = dict()
    __args__['remediationName'] = remediation_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['top'] = top
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:policyinsights:listRemediationDeploymentsAtResourceGroup', __args__, opts=opts, typ=ListRemediationDeploymentsAtResourceGroupResult).value
    return AwaitableListRemediationDeploymentsAtResourceGroupResult(next_link=__ret__.next_link, value=__ret__.value)

@_utilities.lift_output_func(list_remediation_deployments_at_resource_group)
def list_remediation_deployments_at_resource_group_output(remediation_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, top: Optional[pulumi.Input[Optional[int]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListRemediationDeploymentsAtResourceGroupResult]:
    """
    List of deployments for a remediation.
    API Version: 2019-07-01.


    :param str remediation_name: The name of the remediation.
    :param str resource_group_name: Resource group name.
    :param int top: Maximum number of records to return.
    """
    ...
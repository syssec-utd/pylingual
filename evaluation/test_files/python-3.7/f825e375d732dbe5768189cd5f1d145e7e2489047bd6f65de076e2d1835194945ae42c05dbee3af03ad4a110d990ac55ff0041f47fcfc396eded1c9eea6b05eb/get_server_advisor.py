import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetServerAdvisorResult', 'AwaitableGetServerAdvisorResult', 'get_server_advisor', 'get_server_advisor_output']

@pulumi.output_type
class GetServerAdvisorResult:
    """
    Database, Server or Elastic Pool Advisor.
    """

    def __init__(__self__, advisor_status=None, auto_execute_status=None, auto_execute_status_inherited_from=None, id=None, kind=None, last_checked=None, location=None, name=None, recommendations_status=None, recommended_actions=None, type=None):
        if advisor_status and (not isinstance(advisor_status, str)):
            raise TypeError("Expected argument 'advisor_status' to be a str")
        pulumi.set(__self__, 'advisor_status', advisor_status)
        if auto_execute_status and (not isinstance(auto_execute_status, str)):
            raise TypeError("Expected argument 'auto_execute_status' to be a str")
        pulumi.set(__self__, 'auto_execute_status', auto_execute_status)
        if auto_execute_status_inherited_from and (not isinstance(auto_execute_status_inherited_from, str)):
            raise TypeError("Expected argument 'auto_execute_status_inherited_from' to be a str")
        pulumi.set(__self__, 'auto_execute_status_inherited_from', auto_execute_status_inherited_from)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if last_checked and (not isinstance(last_checked, str)):
            raise TypeError("Expected argument 'last_checked' to be a str")
        pulumi.set(__self__, 'last_checked', last_checked)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if recommendations_status and (not isinstance(recommendations_status, str)):
            raise TypeError("Expected argument 'recommendations_status' to be a str")
        pulumi.set(__self__, 'recommendations_status', recommendations_status)
        if recommended_actions and (not isinstance(recommended_actions, list)):
            raise TypeError("Expected argument 'recommended_actions' to be a list")
        pulumi.set(__self__, 'recommended_actions', recommended_actions)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='advisorStatus')
    def advisor_status(self) -> str:
        """
        Gets the status of availability of this advisor to customers. Possible values are 'GA', 'PublicPreview', 'LimitedPublicPreview' and 'PrivatePreview'.
        """
        return pulumi.get(self, 'advisor_status')

    @property
    @pulumi.getter(name='autoExecuteStatus')
    def auto_execute_status(self) -> str:
        """
        Gets the auto-execute status (whether to let the system execute the recommendations) of this advisor. Possible values are 'Enabled' and 'Disabled'
        """
        return pulumi.get(self, 'auto_execute_status')

    @property
    @pulumi.getter(name='autoExecuteStatusInheritedFrom')
    def auto_execute_status_inherited_from(self) -> str:
        """
        Gets the resource from which current value of auto-execute status is inherited. Auto-execute status can be set on (and inherited from) different levels in the resource hierarchy. Possible values are 'Subscription', 'Server', 'ElasticPool', 'Database' and 'Default' (when status is not explicitly set on any level).
        """
        return pulumi.get(self, 'auto_execute_status_inherited_from')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Resource kind.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='lastChecked')
    def last_checked(self) -> str:
        """
        Gets the time when the current resource was analyzed for recommendations by this advisor.
        """
        return pulumi.get(self, 'last_checked')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='recommendationsStatus')
    def recommendations_status(self) -> str:
        """
        Gets that status of recommendations for this advisor and reason for not having any recommendations. Possible values include, but are not limited to, 'Ok' (Recommendations available),LowActivity (not enough workload to analyze), 'DbSeemsTuned' (Database is doing well), etc.
        """
        return pulumi.get(self, 'recommendations_status')

    @property
    @pulumi.getter(name='recommendedActions')
    def recommended_actions(self) -> Sequence['outputs.RecommendedActionResponse']:
        """
        Gets the recommended actions for this advisor.
        """
        return pulumi.get(self, 'recommended_actions')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetServerAdvisorResult(GetServerAdvisorResult):

    def __await__(self):
        if False:
            yield self
        return GetServerAdvisorResult(advisor_status=self.advisor_status, auto_execute_status=self.auto_execute_status, auto_execute_status_inherited_from=self.auto_execute_status_inherited_from, id=self.id, kind=self.kind, last_checked=self.last_checked, location=self.location, name=self.name, recommendations_status=self.recommendations_status, recommended_actions=self.recommended_actions, type=self.type)

def get_server_advisor(advisor_name: Optional[str]=None, resource_group_name: Optional[str]=None, server_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetServerAdvisorResult:
    """
    Database, Server or Elastic Pool Advisor.


    :param str advisor_name: The name of the Server Advisor.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['advisorName'] = advisor_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20201101preview:getServerAdvisor', __args__, opts=opts, typ=GetServerAdvisorResult).value
    return AwaitableGetServerAdvisorResult(advisor_status=__ret__.advisor_status, auto_execute_status=__ret__.auto_execute_status, auto_execute_status_inherited_from=__ret__.auto_execute_status_inherited_from, id=__ret__.id, kind=__ret__.kind, last_checked=__ret__.last_checked, location=__ret__.location, name=__ret__.name, recommendations_status=__ret__.recommendations_status, recommended_actions=__ret__.recommended_actions, type=__ret__.type)

@_utilities.lift_output_func(get_server_advisor)
def get_server_advisor_output(advisor_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetServerAdvisorResult]:
    """
    Database, Server or Elastic Pool Advisor.


    :param str advisor_name: The name of the Server Advisor.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    """
    ...
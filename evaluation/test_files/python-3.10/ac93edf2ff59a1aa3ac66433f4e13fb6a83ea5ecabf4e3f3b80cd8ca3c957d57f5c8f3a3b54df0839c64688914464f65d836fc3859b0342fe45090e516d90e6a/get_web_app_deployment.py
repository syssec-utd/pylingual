import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GetWebAppDeploymentResult', 'AwaitableGetWebAppDeploymentResult', 'get_web_app_deployment', 'get_web_app_deployment_output']

@pulumi.output_type
class GetWebAppDeploymentResult:
    """
    User credentials used for publishing activity.
    """

    def __init__(__self__, active=None, author=None, author_email=None, deployer=None, details=None, end_time=None, id=None, kind=None, message=None, name=None, start_time=None, status=None, type=None):
        if active and (not isinstance(active, bool)):
            raise TypeError("Expected argument 'active' to be a bool")
        pulumi.set(__self__, 'active', active)
        if author and (not isinstance(author, str)):
            raise TypeError("Expected argument 'author' to be a str")
        pulumi.set(__self__, 'author', author)
        if author_email and (not isinstance(author_email, str)):
            raise TypeError("Expected argument 'author_email' to be a str")
        pulumi.set(__self__, 'author_email', author_email)
        if deployer and (not isinstance(deployer, str)):
            raise TypeError("Expected argument 'deployer' to be a str")
        pulumi.set(__self__, 'deployer', deployer)
        if details and (not isinstance(details, str)):
            raise TypeError("Expected argument 'details' to be a str")
        pulumi.set(__self__, 'details', details)
        if end_time and (not isinstance(end_time, str)):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, 'end_time', end_time)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if message and (not isinstance(message, str)):
            raise TypeError("Expected argument 'message' to be a str")
        pulumi.set(__self__, 'message', message)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if start_time and (not isinstance(start_time, str)):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, 'start_time', start_time)
        if status and (not isinstance(status, int)):
            raise TypeError("Expected argument 'status' to be a int")
        pulumi.set(__self__, 'status', status)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def active(self) -> Optional[bool]:
        """
        True if deployment is currently active, false if completed and null if not started.
        """
        return pulumi.get(self, 'active')

    @property
    @pulumi.getter
    def author(self) -> Optional[str]:
        """
        Who authored the deployment.
        """
        return pulumi.get(self, 'author')

    @property
    @pulumi.getter(name='authorEmail')
    def author_email(self) -> Optional[str]:
        """
        Author email.
        """
        return pulumi.get(self, 'author_email')

    @property
    @pulumi.getter
    def deployer(self) -> Optional[str]:
        """
        Who performed the deployment.
        """
        return pulumi.get(self, 'deployer')

    @property
    @pulumi.getter
    def details(self) -> Optional[str]:
        """
        Details on deployment.
        """
        return pulumi.get(self, 'details')

    @property
    @pulumi.getter(name='endTime')
    def end_time(self) -> Optional[str]:
        """
        End time.
        """
        return pulumi.get(self, 'end_time')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        Details about deployment status.
        """
        return pulumi.get(self, 'message')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='startTime')
    def start_time(self) -> Optional[str]:
        """
        Start time.
        """
        return pulumi.get(self, 'start_time')

    @property
    @pulumi.getter
    def status(self) -> Optional[int]:
        """
        Deployment status.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableGetWebAppDeploymentResult(GetWebAppDeploymentResult):

    def __await__(self):
        if False:
            yield self
        return GetWebAppDeploymentResult(active=self.active, author=self.author, author_email=self.author_email, deployer=self.deployer, details=self.details, end_time=self.end_time, id=self.id, kind=self.kind, message=self.message, name=self.name, start_time=self.start_time, status=self.status, type=self.type)

def get_web_app_deployment(id: Optional[str]=None, name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetWebAppDeploymentResult:
    """
    Description for Get a deployment by its ID for an app, or a deployment slot.


    :param str id: Deployment ID.
    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20220901:getWebAppDeployment', __args__, opts=opts, typ=GetWebAppDeploymentResult).value
    return AwaitableGetWebAppDeploymentResult(active=__ret__.active, author=__ret__.author, author_email=__ret__.author_email, deployer=__ret__.deployer, details=__ret__.details, end_time=__ret__.end_time, id=__ret__.id, kind=__ret__.kind, message=__ret__.message, name=__ret__.name, start_time=__ret__.start_time, status=__ret__.status, type=__ret__.type)

@_utilities.lift_output_func(get_web_app_deployment)
def get_web_app_deployment_output(id: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetWebAppDeploymentResult]:
    """
    Description for Get a deployment by its ID for an app, or a deployment slot.


    :param str id: Deployment ID.
    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
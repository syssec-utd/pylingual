import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetEnvironmentSettingResult', 'AwaitableGetEnvironmentSettingResult', 'get_environment_setting', 'get_environment_setting_output']

@pulumi.output_type
class GetEnvironmentSettingResult:
    """
    Represents settings of an environment, from which environment instances would be created
    """

    def __init__(__self__, configuration_state=None, description=None, id=None, last_changed=None, last_published=None, latest_operation_result=None, location=None, name=None, provisioning_state=None, publishing_state=None, resource_settings=None, tags=None, title=None, type=None, unique_identifier=None):
        if configuration_state and (not isinstance(configuration_state, str)):
            raise TypeError("Expected argument 'configuration_state' to be a str")
        pulumi.set(__self__, 'configuration_state', configuration_state)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if last_changed and (not isinstance(last_changed, str)):
            raise TypeError("Expected argument 'last_changed' to be a str")
        pulumi.set(__self__, 'last_changed', last_changed)
        if last_published and (not isinstance(last_published, str)):
            raise TypeError("Expected argument 'last_published' to be a str")
        pulumi.set(__self__, 'last_published', last_published)
        if latest_operation_result and (not isinstance(latest_operation_result, dict)):
            raise TypeError("Expected argument 'latest_operation_result' to be a dict")
        pulumi.set(__self__, 'latest_operation_result', latest_operation_result)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if publishing_state and (not isinstance(publishing_state, str)):
            raise TypeError("Expected argument 'publishing_state' to be a str")
        pulumi.set(__self__, 'publishing_state', publishing_state)
        if resource_settings and (not isinstance(resource_settings, dict)):
            raise TypeError("Expected argument 'resource_settings' to be a dict")
        pulumi.set(__self__, 'resource_settings', resource_settings)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if title and (not isinstance(title, str)):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, 'title', title)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if unique_identifier and (not isinstance(unique_identifier, str)):
            raise TypeError("Expected argument 'unique_identifier' to be a str")
        pulumi.set(__self__, 'unique_identifier', unique_identifier)

    @property
    @pulumi.getter(name='configurationState')
    def configuration_state(self) -> Optional[str]:
        """
        Describes the user's progress in configuring their environment setting
        """
        return pulumi.get(self, 'configuration_state')

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Describes the environment and its resource settings
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='lastChanged')
    def last_changed(self) -> str:
        """
        Time when the template VM was last changed.
        """
        return pulumi.get(self, 'last_changed')

    @property
    @pulumi.getter(name='lastPublished')
    def last_published(self) -> str:
        """
        Time when the template VM was last sent for publishing.
        """
        return pulumi.get(self, 'last_published')

    @property
    @pulumi.getter(name='latestOperationResult')
    def latest_operation_result(self) -> 'outputs.LatestOperationResultResponse':
        """
        The details of the latest operation. ex: status, error
        """
        return pulumi.get(self, 'latest_operation_result')

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publishingState')
    def publishing_state(self) -> str:
        """
        Describes the readiness of this environment setting
        """
        return pulumi.get(self, 'publishing_state')

    @property
    @pulumi.getter(name='resourceSettings')
    def resource_settings(self) -> 'outputs.ResourceSettingsResponse':
        """
        The resource specific settings
        """
        return pulumi.get(self, 'resource_settings')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def title(self) -> Optional[str]:
        """
        Brief title describing the environment and its resource settings
        """
        return pulumi.get(self, 'title')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='uniqueIdentifier')
    def unique_identifier(self) -> Optional[str]:
        """
        The unique immutable identifier of a resource (Guid).
        """
        return pulumi.get(self, 'unique_identifier')

class AwaitableGetEnvironmentSettingResult(GetEnvironmentSettingResult):

    def __await__(self):
        if False:
            yield self
        return GetEnvironmentSettingResult(configuration_state=self.configuration_state, description=self.description, id=self.id, last_changed=self.last_changed, last_published=self.last_published, latest_operation_result=self.latest_operation_result, location=self.location, name=self.name, provisioning_state=self.provisioning_state, publishing_state=self.publishing_state, resource_settings=self.resource_settings, tags=self.tags, title=self.title, type=self.type, unique_identifier=self.unique_identifier)

def get_environment_setting(environment_setting_name: Optional[str]=None, expand: Optional[str]=None, lab_account_name: Optional[str]=None, lab_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetEnvironmentSettingResult:
    """
    Represents settings of an environment, from which environment instances would be created
    API Version: 2018-10-15.


    :param str environment_setting_name: The name of the environment Setting.
    :param str expand: Specify the $expand query. Example: 'properties($select=publishingState)'
    :param str lab_account_name: The name of the lab Account.
    :param str lab_name: The name of the lab.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['environmentSettingName'] = environment_setting_name
    __args__['expand'] = expand
    __args__['labAccountName'] = lab_account_name
    __args__['labName'] = lab_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:labservices:getEnvironmentSetting', __args__, opts=opts, typ=GetEnvironmentSettingResult).value
    return AwaitableGetEnvironmentSettingResult(configuration_state=__ret__.configuration_state, description=__ret__.description, id=__ret__.id, last_changed=__ret__.last_changed, last_published=__ret__.last_published, latest_operation_result=__ret__.latest_operation_result, location=__ret__.location, name=__ret__.name, provisioning_state=__ret__.provisioning_state, publishing_state=__ret__.publishing_state, resource_settings=__ret__.resource_settings, tags=__ret__.tags, title=__ret__.title, type=__ret__.type, unique_identifier=__ret__.unique_identifier)

@_utilities.lift_output_func(get_environment_setting)
def get_environment_setting_output(environment_setting_name: Optional[pulumi.Input[str]]=None, expand: Optional[pulumi.Input[Optional[str]]]=None, lab_account_name: Optional[pulumi.Input[str]]=None, lab_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetEnvironmentSettingResult]:
    """
    Represents settings of an environment, from which environment instances would be created
    API Version: 2018-10-15.


    :param str environment_setting_name: The name of the environment Setting.
    :param str expand: Specify the $expand query. Example: 'properties($select=publishingState)'
    :param str lab_account_name: The name of the lab Account.
    :param str lab_name: The name of the lab.
    :param str resource_group_name: The name of the resource group.
    """
    ...
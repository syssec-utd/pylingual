import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetMediaWorkflowResult', 'AwaitableGetMediaWorkflowResult', 'get_media_workflow', 'get_media_workflow_output']

@pulumi.output_type
class GetMediaWorkflowResult:
    """
    A collection of values returned by getMediaWorkflow.
    """

    def __init__(__self__, compartment_id=None, defined_tags=None, display_name=None, freeform_tags=None, id=None, lifecyle_details=None, media_workflow_configuration_ids=None, media_workflow_id=None, parameters=None, state=None, system_tags=None, tasks=None, time_created=None, time_updated=None, version=None):
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if defined_tags and (not isinstance(defined_tags, dict)):
            raise TypeError("Expected argument 'defined_tags' to be a dict")
        pulumi.set(__self__, 'defined_tags', defined_tags)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if freeform_tags and (not isinstance(freeform_tags, dict)):
            raise TypeError("Expected argument 'freeform_tags' to be a dict")
        pulumi.set(__self__, 'freeform_tags', freeform_tags)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if lifecyle_details and (not isinstance(lifecyle_details, str)):
            raise TypeError("Expected argument 'lifecyle_details' to be a str")
        pulumi.set(__self__, 'lifecyle_details', lifecyle_details)
        if media_workflow_configuration_ids and (not isinstance(media_workflow_configuration_ids, list)):
            raise TypeError("Expected argument 'media_workflow_configuration_ids' to be a list")
        pulumi.set(__self__, 'media_workflow_configuration_ids', media_workflow_configuration_ids)
        if media_workflow_id and (not isinstance(media_workflow_id, str)):
            raise TypeError("Expected argument 'media_workflow_id' to be a str")
        pulumi.set(__self__, 'media_workflow_id', media_workflow_id)
        if parameters and (not isinstance(parameters, str)):
            raise TypeError("Expected argument 'parameters' to be a str")
        pulumi.set(__self__, 'parameters', parameters)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if system_tags and (not isinstance(system_tags, dict)):
            raise TypeError("Expected argument 'system_tags' to be a dict")
        pulumi.set(__self__, 'system_tags', system_tags)
        if tasks and (not isinstance(tasks, list)):
            raise TypeError("Expected argument 'tasks' to be a list")
        pulumi.set(__self__, 'tasks', tasks)
        if time_created and (not isinstance(time_created, str)):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, 'time_created', time_created)
        if time_updated and (not isinstance(time_updated, str)):
            raise TypeError("Expected argument 'time_updated' to be a str")
        pulumi.set(__self__, 'time_updated', time_updated)
        if version and (not isinstance(version, str)):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        """
        Compartment Identifier.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='definedTags')
    def defined_tags(self) -> Mapping[str, Any]:
        """
        Defined tags for this resource. Each key is predefined and scoped to a namespace. Example: `{"foo-namespace.bar-key": "value"}`
        """
        return pulumi.get(self, 'defined_tags')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        Name of the Media Workflow. Does not have to be unique, and it's changeable. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='freeformTags')
    def freeform_tags(self) -> Mapping[str, Any]:
        """
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only. Example: `{"bar-key": "value"}`
        """
        return pulumi.get(self, 'freeform_tags')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Unique identifier that is immutable on creation.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='lifecyleDetails')
    def lifecyle_details(self) -> str:
        """
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.
        """
        return pulumi.get(self, 'lifecyle_details')

    @property
    @pulumi.getter(name='mediaWorkflowConfigurationIds')
    def media_workflow_configuration_ids(self) -> Sequence[str]:
        """
        Configurations to be applied to all the runs of this workflow. Parameters in these configurations are overridden by parameters in the MediaWorkflowConfigurations of the MediaWorkflowJob and the parameters of the MediaWorkflowJob. If the same parameter appears in multiple configurations, the values that appear in the configuration at the highest index will be used.
        """
        return pulumi.get(self, 'media_workflow_configuration_ids')

    @property
    @pulumi.getter(name='mediaWorkflowId')
    def media_workflow_id(self) -> str:
        return pulumi.get(self, 'media_workflow_id')

    @property
    @pulumi.getter
    def parameters(self) -> str:
        """
        Data specifiying how this task is to be run. The data is a JSON object that must conform to the JSON Schema specified by the parameters of the MediaWorkflowTaskDeclaration this task references. The parameters may contain values or references to other parameters.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the MediaWorkflow.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='systemTags')
    def system_tags(self) -> Mapping[str, Any]:
        """
        Usage of system tag keys. These predefined keys are scoped to namespaces. Example: `{"orcl-cloud.free-tier-retained": "true"}`
        """
        return pulumi.get(self, 'system_tags')

    @property
    @pulumi.getter
    def tasks(self) -> Sequence['outputs.GetMediaWorkflowTaskResult']:
        """
        The processing to be done in this workflow. Each key of the MediaWorkflowTasks in this array is unique within the array.  The order of the items is preserved from the order of the tasks array in CreateMediaWorkflowDetails or UpdateMediaWorkflowDetails.
        """
        return pulumi.get(self, 'tasks')

    @property
    @pulumi.getter(name='timeCreated')
    def time_created(self) -> str:
        """
        The time when the MediaWorkflow was created. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_created')

    @property
    @pulumi.getter(name='timeUpdated')
    def time_updated(self) -> str:
        """
        The time when the MediaWorkflow was updated. An RFC3339 formatted datetime string.
        """
        return pulumi.get(self, 'time_updated')

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the MediaWorkflow.
        """
        return pulumi.get(self, 'version')

class AwaitableGetMediaWorkflowResult(GetMediaWorkflowResult):

    def __await__(self):
        if False:
            yield self
        return GetMediaWorkflowResult(compartment_id=self.compartment_id, defined_tags=self.defined_tags, display_name=self.display_name, freeform_tags=self.freeform_tags, id=self.id, lifecyle_details=self.lifecyle_details, media_workflow_configuration_ids=self.media_workflow_configuration_ids, media_workflow_id=self.media_workflow_id, parameters=self.parameters, state=self.state, system_tags=self.system_tags, tasks=self.tasks, time_created=self.time_created, time_updated=self.time_updated, version=self.version)

def get_media_workflow(media_workflow_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetMediaWorkflowResult:
    """
    This data source provides details about a specific Media Workflow resource in Oracle Cloud Infrastructure Media Services service.

    Gets a MediaWorkflow by identifier.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_media_workflow = oci.MediaServices.get_media_workflow(media_workflow_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str media_workflow_id: Unique MediaWorkflow identifier.
    """
    __args__ = dict()
    __args__['mediaWorkflowId'] = media_workflow_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:MediaServices/getMediaWorkflow:getMediaWorkflow', __args__, opts=opts, typ=GetMediaWorkflowResult).value
    return AwaitableGetMediaWorkflowResult(compartment_id=__ret__.compartment_id, defined_tags=__ret__.defined_tags, display_name=__ret__.display_name, freeform_tags=__ret__.freeform_tags, id=__ret__.id, lifecyle_details=__ret__.lifecyle_details, media_workflow_configuration_ids=__ret__.media_workflow_configuration_ids, media_workflow_id=__ret__.media_workflow_id, parameters=__ret__.parameters, state=__ret__.state, system_tags=__ret__.system_tags, tasks=__ret__.tasks, time_created=__ret__.time_created, time_updated=__ret__.time_updated, version=__ret__.version)

@_utilities.lift_output_func(get_media_workflow)
def get_media_workflow_output(media_workflow_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetMediaWorkflowResult]:
    """
    This data source provides details about a specific Media Workflow resource in Oracle Cloud Infrastructure Media Services service.

    Gets a MediaWorkflow by identifier.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_media_workflow = oci.MediaServices.get_media_workflow(media_workflow_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str media_workflow_id: Unique MediaWorkflow identifier.
    """
    ...
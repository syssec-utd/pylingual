import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetPipelinesResult', 'AwaitableGetPipelinesResult', 'get_pipelines', 'get_pipelines_output']

@pulumi.output_type
class GetPipelinesResult:
    """
    A collection of values returned by getPipelines.
    """

    def __init__(__self__, compartment_id=None, created_by=None, display_name=None, filters=None, id=None, pipelines=None, project_id=None, state=None):
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if created_by and (not isinstance(created_by, str)):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, 'created_by', created_by)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if pipelines and (not isinstance(pipelines, list)):
            raise TypeError("Expected argument 'pipelines' to be a list")
        pulumi.set(__self__, 'pipelines', pipelines)
        if project_id and (not isinstance(project_id, str)):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, 'project_id', project_id)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment where you want to create the pipeline.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='createdBy')
    def created_by(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the user who created the pipeline.
        """
        return pulumi.get(self, 'created_by')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        A user-friendly display name for the resource.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetPipelinesFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the pipeline.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def pipelines(self) -> Sequence['outputs.GetPipelinesPipelineResult']:
        """
        The list of pipelines.
        """
        return pulumi.get(self, 'pipelines')

    @property
    @pulumi.getter(name='projectId')
    def project_id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the project to associate the pipeline with.
        """
        return pulumi.get(self, 'project_id')

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The current state of the pipeline.
        """
        return pulumi.get(self, 'state')

class AwaitableGetPipelinesResult(GetPipelinesResult):

    def __await__(self):
        if False:
            yield self
        return GetPipelinesResult(compartment_id=self.compartment_id, created_by=self.created_by, display_name=self.display_name, filters=self.filters, id=self.id, pipelines=self.pipelines, project_id=self.project_id, state=self.state)

def get_pipelines(compartment_id: Optional[str]=None, created_by: Optional[str]=None, display_name: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetPipelinesFilterArgs']]]=None, id: Optional[str]=None, project_id: Optional[str]=None, state: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPipelinesResult:
    """
    This data source provides the list of Pipelines in Oracle Cloud Infrastructure Data Science service.

    Returns a list of Pipelines.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_pipelines = oci.DataScience.get_pipelines(compartment_id=var["compartment_id"],
        created_by=var["pipeline_created_by"],
        display_name=var["pipeline_display_name"],
        id=var["pipeline_id"],
        project_id=oci_datascience_project["test_project"]["id"],
        state=var["pipeline_state"])
    ```


    :param str compartment_id: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str created_by: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the user who created the resource.
    :param str display_name: <b>Filter</b> results by its user-friendly name.
    :param str id: <b>Filter</b> results by [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm). Must be an OCID of the correct type for the resource type.
    :param str project_id: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the project.
    :param str state: The current state of the Pipeline.
    """
    __args__ = dict()
    __args__['compartmentId'] = compartment_id
    __args__['createdBy'] = created_by
    __args__['displayName'] = display_name
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['projectId'] = project_id
    __args__['state'] = state
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:DataScience/getPipelines:getPipelines', __args__, opts=opts, typ=GetPipelinesResult).value
    return AwaitableGetPipelinesResult(compartment_id=__ret__.compartment_id, created_by=__ret__.created_by, display_name=__ret__.display_name, filters=__ret__.filters, id=__ret__.id, pipelines=__ret__.pipelines, project_id=__ret__.project_id, state=__ret__.state)

@_utilities.lift_output_func(get_pipelines)
def get_pipelines_output(compartment_id: Optional[pulumi.Input[str]]=None, created_by: Optional[pulumi.Input[Optional[str]]]=None, display_name: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetPipelinesFilterArgs']]]]]=None, id: Optional[pulumi.Input[Optional[str]]]=None, project_id: Optional[pulumi.Input[Optional[str]]]=None, state: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPipelinesResult]:
    """
    This data source provides the list of Pipelines in Oracle Cloud Infrastructure Data Science service.

    Returns a list of Pipelines.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_pipelines = oci.DataScience.get_pipelines(compartment_id=var["compartment_id"],
        created_by=var["pipeline_created_by"],
        display_name=var["pipeline_display_name"],
        id=var["pipeline_id"],
        project_id=oci_datascience_project["test_project"]["id"],
        state=var["pipeline_state"])
    ```


    :param str compartment_id: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str created_by: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the user who created the resource.
    :param str display_name: <b>Filter</b> results by its user-friendly name.
    :param str id: <b>Filter</b> results by [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm). Must be an OCID of the correct type for the resource type.
    :param str project_id: <b>Filter</b> results by the [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the project.
    :param str state: The current state of the Pipeline.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetPipelineJobResult', 'AwaitableGetPipelineJobResult', 'get_pipeline_job', 'get_pipeline_job_output']

@pulumi.output_type
class GetPipelineJobResult:
    """
    Pipeline job represents a unique instance of a batch topology, used for offline processing of selected portions of archived content.
    """

    def __init__(__self__, description=None, error=None, expiration=None, id=None, name=None, parameters=None, state=None, system_data=None, topology_name=None, type=None):
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if error and (not isinstance(error, dict)):
            raise TypeError("Expected argument 'error' to be a dict")
        pulumi.set(__self__, 'error', error)
        if expiration and (not isinstance(expiration, str)):
            raise TypeError("Expected argument 'expiration' to be a str")
        pulumi.set(__self__, 'expiration', expiration)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if parameters and (not isinstance(parameters, list)):
            raise TypeError("Expected argument 'parameters' to be a list")
        pulumi.set(__self__, 'parameters', parameters)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if topology_name and (not isinstance(topology_name, str)):
            raise TypeError("Expected argument 'topology_name' to be a str")
        pulumi.set(__self__, 'topology_name', topology_name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description for the pipeline.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def error(self) -> 'outputs.PipelineJobErrorResponse':
        """
        Details about the error, in case the pipeline job fails.
        """
        return pulumi.get(self, 'error')

    @property
    @pulumi.getter
    def expiration(self) -> str:
        """
        The date-time by when this pipeline job will be automatically deleted from your account.
        """
        return pulumi.get(self, 'expiration')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Sequence['outputs.ParameterDefinitionResponse']]:
        """
        List of the instance level parameter values for the user-defined topology parameters. A pipeline can only define or override parameters values for parameters which have been declared in the referenced topology. Topology parameters without a default value must be defined. Topology parameters with a default value can be optionally be overridden.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the pipeline (read-only).
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter(name='topologyName')
    def topology_name(self) -> str:
        """
        Reference to an existing pipeline topology. When activated, this pipeline job will process content according to the pipeline topology definition.
        """
        return pulumi.get(self, 'topology_name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetPipelineJobResult(GetPipelineJobResult):

    def __await__(self):
        if False:
            yield self
        return GetPipelineJobResult(description=self.description, error=self.error, expiration=self.expiration, id=self.id, name=self.name, parameters=self.parameters, state=self.state, system_data=self.system_data, topology_name=self.topology_name, type=self.type)

def get_pipeline_job(account_name: Optional[str]=None, pipeline_job_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPipelineJobResult:
    """
    Pipeline job represents a unique instance of a batch topology, used for offline processing of selected portions of archived content.


    :param str account_name: The Azure Video Analyzer account name.
    :param str pipeline_job_name: The pipeline job name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['pipelineJobName'] = pipeline_job_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:videoanalyzer/v20211101preview:getPipelineJob', __args__, opts=opts, typ=GetPipelineJobResult).value
    return AwaitableGetPipelineJobResult(description=__ret__.description, error=__ret__.error, expiration=__ret__.expiration, id=__ret__.id, name=__ret__.name, parameters=__ret__.parameters, state=__ret__.state, system_data=__ret__.system_data, topology_name=__ret__.topology_name, type=__ret__.type)

@_utilities.lift_output_func(get_pipeline_job)
def get_pipeline_job_output(account_name: Optional[pulumi.Input[str]]=None, pipeline_job_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPipelineJobResult]:
    """
    Pipeline job represents a unique instance of a batch topology, used for offline processing of selected portions of archived content.


    :param str account_name: The Azure Video Analyzer account name.
    :param str pipeline_job_name: The pipeline job name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
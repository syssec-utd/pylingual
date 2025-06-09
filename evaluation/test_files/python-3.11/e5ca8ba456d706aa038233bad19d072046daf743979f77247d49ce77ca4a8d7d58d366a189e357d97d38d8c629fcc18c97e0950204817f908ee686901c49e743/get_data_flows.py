import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetDataFlowsResult', 'AwaitableGetDataFlowsResult', 'get_data_flows', 'get_data_flows_output']

@pulumi.output_type
class GetDataFlowsResult:
    """
    A collection of values returned by getDataFlows.
    """

    def __init__(__self__, file_system_id=None, flows=None, id=None, ids=None, output_file=None, status=None):
        if file_system_id and (not isinstance(file_system_id, str)):
            raise TypeError("Expected argument 'file_system_id' to be a str")
        pulumi.set(__self__, 'file_system_id', file_system_id)
        if flows and (not isinstance(flows, list)):
            raise TypeError("Expected argument 'flows' to be a list")
        pulumi.set(__self__, 'flows', flows)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if ids and (not isinstance(ids, list)):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, 'ids', ids)
        if output_file and (not isinstance(output_file, str)):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, 'output_file', output_file)
        if status and (not isinstance(status, str)):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter(name='fileSystemId')
    def file_system_id(self) -> str:
        return pulumi.get(self, 'file_system_id')

    @property
    @pulumi.getter
    def flows(self) -> Sequence['outputs.GetDataFlowsFlowResult']:
        return pulumi.get(self, 'flows')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, 'ids')

    @property
    @pulumi.getter(name='outputFile')
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, 'output_file')

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, 'status')

class AwaitableGetDataFlowsResult(GetDataFlowsResult):

    def __await__(self):
        if False:
            yield self
        return GetDataFlowsResult(file_system_id=self.file_system_id, flows=self.flows, id=self.id, ids=self.ids, output_file=self.output_file, status=self.status)

def get_data_flows(file_system_id: Optional[str]=None, ids: Optional[Sequence[str]]=None, output_file: Optional[str]=None, status: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetDataFlowsResult:
    """
    This data source provides the Nas Data Flows of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.153.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.nas.get_data_flows(file_system_id="example_value",
        ids=[
            "example_value-1",
            "example_value-2",
        ])
    pulumi.export("nasDataFlowId1", ids.flows[0].id)
    status = alicloud.nas.get_data_flows(file_system_id="example_value",
        status="Running")
    pulumi.export("nasDataFlowId2", status.flows[0].id)
    ```


    :param str file_system_id: The ID of the file system.
    :param Sequence[str] ids: A list of Data Flow IDs.
    :param str status: The status of the Data flow.
    """
    __args__ = dict()
    __args__['fileSystemId'] = file_system_id
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['status'] = status
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('alicloud:nas/getDataFlows:getDataFlows', __args__, opts=opts, typ=GetDataFlowsResult).value
    return AwaitableGetDataFlowsResult(file_system_id=__ret__.file_system_id, flows=__ret__.flows, id=__ret__.id, ids=__ret__.ids, output_file=__ret__.output_file, status=__ret__.status)

@_utilities.lift_output_func(get_data_flows)
def get_data_flows_output(file_system_id: Optional[pulumi.Input[str]]=None, ids: Optional[pulumi.Input[Optional[Sequence[str]]]]=None, output_file: Optional[pulumi.Input[Optional[str]]]=None, status: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetDataFlowsResult]:
    """
    This data source provides the Nas Data Flows of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.153.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.nas.get_data_flows(file_system_id="example_value",
        ids=[
            "example_value-1",
            "example_value-2",
        ])
    pulumi.export("nasDataFlowId1", ids.flows[0].id)
    status = alicloud.nas.get_data_flows(file_system_id="example_value",
        status="Running")
    pulumi.export("nasDataFlowId2", status.flows[0].id)
    ```


    :param str file_system_id: The ID of the file system.
    :param Sequence[str] ids: A list of Data Flow IDs.
    :param str status: The status of the Data flow.
    """
    ...
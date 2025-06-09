import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetNodeTemplateResult', 'AwaitableGetNodeTemplateResult', 'get_node_template', 'get_node_template_output']

@pulumi.output_type
class GetNodeTemplateResult:

    def __init__(__self__, accelerators=None, cpu_overcommit_type=None, creation_timestamp=None, description=None, disks=None, kind=None, name=None, node_affinity_labels=None, node_type=None, node_type_flexibility=None, region=None, self_link=None, server_binding=None, status=None, status_message=None):
        if accelerators and (not isinstance(accelerators, list)):
            raise TypeError("Expected argument 'accelerators' to be a list")
        pulumi.set(__self__, 'accelerators', accelerators)
        if cpu_overcommit_type and (not isinstance(cpu_overcommit_type, str)):
            raise TypeError("Expected argument 'cpu_overcommit_type' to be a str")
        pulumi.set(__self__, 'cpu_overcommit_type', cpu_overcommit_type)
        if creation_timestamp and (not isinstance(creation_timestamp, str)):
            raise TypeError("Expected argument 'creation_timestamp' to be a str")
        pulumi.set(__self__, 'creation_timestamp', creation_timestamp)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if disks and (not isinstance(disks, list)):
            raise TypeError("Expected argument 'disks' to be a list")
        pulumi.set(__self__, 'disks', disks)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if node_affinity_labels and (not isinstance(node_affinity_labels, dict)):
            raise TypeError("Expected argument 'node_affinity_labels' to be a dict")
        pulumi.set(__self__, 'node_affinity_labels', node_affinity_labels)
        if node_type and (not isinstance(node_type, str)):
            raise TypeError("Expected argument 'node_type' to be a str")
        pulumi.set(__self__, 'node_type', node_type)
        if node_type_flexibility and (not isinstance(node_type_flexibility, dict)):
            raise TypeError("Expected argument 'node_type_flexibility' to be a dict")
        pulumi.set(__self__, 'node_type_flexibility', node_type_flexibility)
        if region and (not isinstance(region, str)):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, 'region', region)
        if self_link and (not isinstance(self_link, str)):
            raise TypeError("Expected argument 'self_link' to be a str")
        pulumi.set(__self__, 'self_link', self_link)
        if server_binding and (not isinstance(server_binding, dict)):
            raise TypeError("Expected argument 'server_binding' to be a dict")
        pulumi.set(__self__, 'server_binding', server_binding)
        if status and (not isinstance(status, str)):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, 'status', status)
        if status_message and (not isinstance(status_message, str)):
            raise TypeError("Expected argument 'status_message' to be a str")
        pulumi.set(__self__, 'status_message', status_message)

    @property
    @pulumi.getter
    def accelerators(self) -> Sequence['outputs.AcceleratorConfigResponse']:
        return pulumi.get(self, 'accelerators')

    @property
    @pulumi.getter(name='cpuOvercommitType')
    def cpu_overcommit_type(self) -> str:
        """
        CPU overcommit.
        """
        return pulumi.get(self, 'cpu_overcommit_type')

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> str:
        """
        Creation timestamp in RFC3339 text format.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional description of this resource. Provide this property when you create the resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def disks(self) -> Sequence['outputs.LocalDiskResponse']:
        return pulumi.get(self, 'disks')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The type of the resource. Always compute#nodeTemplate for node templates.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource, provided by the client when initially creating the resource. The resource name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression `[a-z]([-a-z0-9]*[a-z0-9])?` which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='nodeAffinityLabels')
    def node_affinity_labels(self) -> Mapping[str, str]:
        """
        Labels to use for node affinity, which will be used in instance scheduling.
        """
        return pulumi.get(self, 'node_affinity_labels')

    @property
    @pulumi.getter(name='nodeType')
    def node_type(self) -> str:
        """
        The node type to use for nodes group that are created from this template.
        """
        return pulumi.get(self, 'node_type')

    @property
    @pulumi.getter(name='nodeTypeFlexibility')
    def node_type_flexibility(self) -> 'outputs.NodeTemplateNodeTypeFlexibilityResponse':
        """
        The flexible properties of the desired node type. Node groups that use this node template will create nodes of a type that matches these properties. This field is mutually exclusive with the node_type property; you can only define one or the other, but not both.
        """
        return pulumi.get(self, 'node_type_flexibility')

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        The name of the region where the node template resides, such as us-central1.
        """
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> str:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter(name='serverBinding')
    def server_binding(self) -> 'outputs.ServerBindingResponse':
        """
        Sets the binding properties for the physical server. Valid values include: - *[Default]* RESTART_NODE_ON_ANY_SERVER: Restarts VMs on any available physical server - RESTART_NODE_ON_MINIMAL_SERVER: Restarts VMs on the same physical server whenever possible See Sole-tenant node options for more information.
        """
        return pulumi.get(self, 'server_binding')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the node template. One of the following values: CREATING, READY, and DELETING.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter(name='statusMessage')
    def status_message(self) -> str:
        """
        An optional, human-readable explanation of the status.
        """
        return pulumi.get(self, 'status_message')

class AwaitableGetNodeTemplateResult(GetNodeTemplateResult):

    def __await__(self):
        if False:
            yield self
        return GetNodeTemplateResult(accelerators=self.accelerators, cpu_overcommit_type=self.cpu_overcommit_type, creation_timestamp=self.creation_timestamp, description=self.description, disks=self.disks, kind=self.kind, name=self.name, node_affinity_labels=self.node_affinity_labels, node_type=self.node_type, node_type_flexibility=self.node_type_flexibility, region=self.region, self_link=self.self_link, server_binding=self.server_binding, status=self.status, status_message=self.status_message)

def get_node_template(node_template: Optional[str]=None, project: Optional[str]=None, region: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetNodeTemplateResult:
    """
    Returns the specified node template. Gets a list of available node templates by making a list() request.
    """
    __args__ = dict()
    __args__['nodeTemplate'] = node_template
    __args__['project'] = project
    __args__['region'] = region
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('google-native:compute/beta:getNodeTemplate', __args__, opts=opts, typ=GetNodeTemplateResult).value
    return AwaitableGetNodeTemplateResult(accelerators=__ret__.accelerators, cpu_overcommit_type=__ret__.cpu_overcommit_type, creation_timestamp=__ret__.creation_timestamp, description=__ret__.description, disks=__ret__.disks, kind=__ret__.kind, name=__ret__.name, node_affinity_labels=__ret__.node_affinity_labels, node_type=__ret__.node_type, node_type_flexibility=__ret__.node_type_flexibility, region=__ret__.region, self_link=__ret__.self_link, server_binding=__ret__.server_binding, status=__ret__.status, status_message=__ret__.status_message)

@_utilities.lift_output_func(get_node_template)
def get_node_template_output(node_template: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[Optional[str]]]=None, region: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetNodeTemplateResult]:
    """
    Returns the specified node template. Gets a list of available node templates by making a list() request.
    """
    ...
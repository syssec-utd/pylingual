import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetTriggersResult', 'AwaitableGetTriggersResult', 'get_triggers', 'get_triggers_output']

@pulumi.output_type
class GetTriggersResult:
    """
    A collection of values returned by getTriggers.
    """

    def __init__(__self__, compartment_id=None, display_name=None, filters=None, id=None, project_id=None, state=None, trigger_collections=None):
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if project_id and (not isinstance(project_id, str)):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, 'project_id', project_id)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)
        if trigger_collections and (not isinstance(trigger_collections, list)):
            raise TypeError("Expected argument 'trigger_collections' to be a list")
        pulumi.set(__self__, 'trigger_collections', trigger_collections)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[str]:
        """
        The OCID of the compartment that contains the trigger.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        Trigger display name. Avoid entering confidential information.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetTriggersFilterResult']]:
        """
        The filters for the trigger.
        """
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Unique identifier that is immutable on creation.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='projectId')
    def project_id(self) -> Optional[str]:
        """
        The OCID of the DevOps project to which the trigger belongs to.
        """
        return pulumi.get(self, 'project_id')

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The current state of the trigger.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='triggerCollections')
    def trigger_collections(self) -> Sequence['outputs.GetTriggersTriggerCollectionResult']:
        """
        The list of trigger_collection.
        """
        return pulumi.get(self, 'trigger_collections')

class AwaitableGetTriggersResult(GetTriggersResult):

    def __await__(self):
        if False:
            yield self
        return GetTriggersResult(compartment_id=self.compartment_id, display_name=self.display_name, filters=self.filters, id=self.id, project_id=self.project_id, state=self.state, trigger_collections=self.trigger_collections)

def get_triggers(compartment_id: Optional[str]=None, display_name: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetTriggersFilterArgs']]]=None, id: Optional[str]=None, project_id: Optional[str]=None, state: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetTriggersResult:
    """
    This data source provides the list of Triggers in Oracle Cloud Infrastructure Devops service.

    Returns a list of triggers.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_triggers = oci.DevOps.get_triggers(compartment_id=var["compartment_id"],
        display_name=var["trigger_display_name"],
        id=var["trigger_id"],
        project_id=oci_devops_project["test_project"]["id"],
        state=var["trigger_state"])
    ```


    :param str compartment_id: The OCID of the compartment in which to list resources.
    :param str display_name: A filter to return only resources that match the entire display name given.
    :param Sequence[pulumi.InputType['GetTriggersFilterArgs']] filters: The filters for the trigger.
    :param str id: Unique trigger identifier.
    :param str project_id: unique project identifier
    :param str state: A filter to return only triggers that matches the given lifecycle state.
    """
    __args__ = dict()
    __args__['compartmentId'] = compartment_id
    __args__['displayName'] = display_name
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['projectId'] = project_id
    __args__['state'] = state
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:DevOps/getTriggers:getTriggers', __args__, opts=opts, typ=GetTriggersResult).value
    return AwaitableGetTriggersResult(compartment_id=__ret__.compartment_id, display_name=__ret__.display_name, filters=__ret__.filters, id=__ret__.id, project_id=__ret__.project_id, state=__ret__.state, trigger_collections=__ret__.trigger_collections)

@_utilities.lift_output_func(get_triggers)
def get_triggers_output(compartment_id: Optional[pulumi.Input[Optional[str]]]=None, display_name: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetTriggersFilterArgs']]]]]=None, id: Optional[pulumi.Input[Optional[str]]]=None, project_id: Optional[pulumi.Input[Optional[str]]]=None, state: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetTriggersResult]:
    """
    This data source provides the list of Triggers in Oracle Cloud Infrastructure Devops service.

    Returns a list of triggers.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_triggers = oci.DevOps.get_triggers(compartment_id=var["compartment_id"],
        display_name=var["trigger_display_name"],
        id=var["trigger_id"],
        project_id=oci_devops_project["test_project"]["id"],
        state=var["trigger_state"])
    ```


    :param str compartment_id: The OCID of the compartment in which to list resources.
    :param str display_name: A filter to return only resources that match the entire display name given.
    :param Sequence[pulumi.InputType['GetTriggersFilterArgs']] filters: The filters for the trigger.
    :param str id: Unique trigger identifier.
    :param str project_id: unique project identifier
    :param str state: A filter to return only triggers that matches the given lifecycle state.
    """
    ...
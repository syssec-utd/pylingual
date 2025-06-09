import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetCompartmentsResult', 'AwaitableGetCompartmentsResult', 'get_compartments', 'get_compartments_output']

@pulumi.output_type
class GetCompartmentsResult:
    """
    A collection of values returned by getCompartments.
    """

    def __init__(__self__, access_level=None, compartment_id=None, compartment_id_in_subtree=None, compartments=None, filters=None, id=None, name=None, state=None):
        if access_level and (not isinstance(access_level, str)):
            raise TypeError("Expected argument 'access_level' to be a str")
        pulumi.set(__self__, 'access_level', access_level)
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if compartment_id_in_subtree and (not isinstance(compartment_id_in_subtree, bool)):
            raise TypeError("Expected argument 'compartment_id_in_subtree' to be a bool")
        pulumi.set(__self__, 'compartment_id_in_subtree', compartment_id_in_subtree)
        if compartments and (not isinstance(compartments, list)):
            raise TypeError("Expected argument 'compartments' to be a list")
        pulumi.set(__self__, 'compartments', compartments)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if state and (not isinstance(state, str)):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, 'state', state)

    @property
    @pulumi.getter(name='accessLevel')
    def access_level(self) -> Optional[str]:
        return pulumi.get(self, 'access_level')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        """
        The OCID of the parent compartment containing the compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='compartmentIdInSubtree')
    def compartment_id_in_subtree(self) -> Optional[bool]:
        return pulumi.get(self, 'compartment_id_in_subtree')

    @property
    @pulumi.getter
    def compartments(self) -> Sequence['outputs.GetCompartmentsCompartmentResult']:
        """
        The list of compartments.
        """
        return pulumi.get(self, 'compartments')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetCompartmentsFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name you assign to the compartment during creation. The name must be unique across all compartments in the parent. Avoid entering confidential information.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The compartment's current state.
        """
        return pulumi.get(self, 'state')

class AwaitableGetCompartmentsResult(GetCompartmentsResult):

    def __await__(self):
        if False:
            yield self
        return GetCompartmentsResult(access_level=self.access_level, compartment_id=self.compartment_id, compartment_id_in_subtree=self.compartment_id_in_subtree, compartments=self.compartments, filters=self.filters, id=self.id, name=self.name, state=self.state)

def get_compartments(access_level: Optional[str]=None, compartment_id: Optional[str]=None, compartment_id_in_subtree: Optional[bool]=None, filters: Optional[Sequence[pulumi.InputType['GetCompartmentsFilterArgs']]]=None, name: Optional[str]=None, state: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetCompartmentsResult:
    """
    This data source provides the list of Compartments in Oracle Cloud Infrastructure Identity service.

    Lists the compartments in a specified compartment. The members of the list
    returned depends on the values set for several parameters.

    With the exception of the tenancy (root compartment), the ListCompartments operation
    returns only the first-level child compartments in the parent compartment specified in
    `compartmentId`. The list does not include any subcompartments of the child
    compartments (grandchildren).

    The parameter `accessLevel` specifies whether to return only those compartments for which the
    requestor has INSPECT permissions on at least one resource directly
    or indirectly (the resource can be in a subcompartment).

    The parameter `compartmentIdInSubtree` applies only when you perform ListCompartments on the
    tenancy (root compartment). When set to true, the entire hierarchy of compartments can be returned.
    To get a full list of all compartments and subcompartments in the tenancy (root compartment),
    set the parameter `compartmentIdInSubtree` to true and `accessLevel` to ANY.

    See [Where to Get the Tenancy's OCID and User's OCID](https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apisigningkey.htm#five).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_compartments = oci.Identity.get_compartments(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        access_level=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        compartment_id_in_subtree=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str access_level: Valid values are `ANY` and `ACCESSIBLE`. Default is `ANY`. Setting this to `ACCESSIBLE` returns only those compartments for which the user has INSPECT permissions directly or indirectly (permissions can be on a resource in a subcompartment). For the compartments on which the user indirectly has INSPECT permissions, a restricted set of fields is returned.
           
           When set to `ANY` permissions are not checked.
    :param str compartment_id: The OCID of the compartment (remember that the tenancy is simply the root compartment).
    :param bool compartment_id_in_subtree: Default is false. Can only be set to true when performing ListCompartments on the tenancy (root compartment). When set to true, the hierarchy of compartments is traversed and all compartments and subcompartments in the tenancy are returned depending on the the setting of `accessLevel`.
    :param str name: A filter to only return resources that match the given name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state.  The state value is case-insensitive.
    """
    __args__ = dict()
    __args__['accessLevel'] = access_level
    __args__['compartmentId'] = compartment_id
    __args__['compartmentIdInSubtree'] = compartment_id_in_subtree
    __args__['filters'] = filters
    __args__['name'] = name
    __args__['state'] = state
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:Identity/getCompartments:getCompartments', __args__, opts=opts, typ=GetCompartmentsResult).value
    return AwaitableGetCompartmentsResult(access_level=__ret__.access_level, compartment_id=__ret__.compartment_id, compartment_id_in_subtree=__ret__.compartment_id_in_subtree, compartments=__ret__.compartments, filters=__ret__.filters, id=__ret__.id, name=__ret__.name, state=__ret__.state)

@_utilities.lift_output_func(get_compartments)
def get_compartments_output(access_level: Optional[pulumi.Input[Optional[str]]]=None, compartment_id: Optional[pulumi.Input[str]]=None, compartment_id_in_subtree: Optional[pulumi.Input[Optional[bool]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetCompartmentsFilterArgs']]]]]=None, name: Optional[pulumi.Input[Optional[str]]]=None, state: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetCompartmentsResult]:
    """
    This data source provides the list of Compartments in Oracle Cloud Infrastructure Identity service.

    Lists the compartments in a specified compartment. The members of the list
    returned depends on the values set for several parameters.

    With the exception of the tenancy (root compartment), the ListCompartments operation
    returns only the first-level child compartments in the parent compartment specified in
    `compartmentId`. The list does not include any subcompartments of the child
    compartments (grandchildren).

    The parameter `accessLevel` specifies whether to return only those compartments for which the
    requestor has INSPECT permissions on at least one resource directly
    or indirectly (the resource can be in a subcompartment).

    The parameter `compartmentIdInSubtree` applies only when you perform ListCompartments on the
    tenancy (root compartment). When set to true, the entire hierarchy of compartments can be returned.
    To get a full list of all compartments and subcompartments in the tenancy (root compartment),
    set the parameter `compartmentIdInSubtree` to true and `accessLevel` to ANY.

    See [Where to Get the Tenancy's OCID and User's OCID](https://docs.cloud.oracle.com/iaas/Content/API/Concepts/apisigningkey.htm#five).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_compartments = oci.Identity.get_compartments(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        access_level=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        compartment_id_in_subtree=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        state=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str access_level: Valid values are `ANY` and `ACCESSIBLE`. Default is `ANY`. Setting this to `ACCESSIBLE` returns only those compartments for which the user has INSPECT permissions directly or indirectly (permissions can be on a resource in a subcompartment). For the compartments on which the user indirectly has INSPECT permissions, a restricted set of fields is returned.
           
           When set to `ANY` permissions are not checked.
    :param str compartment_id: The OCID of the compartment (remember that the tenancy is simply the root compartment).
    :param bool compartment_id_in_subtree: Default is false. Can only be set to true when performing ListCompartments on the tenancy (root compartment). When set to true, the hierarchy of compartments is traversed and all compartments and subcompartments in the tenancy are returned depending on the the setting of `accessLevel`.
    :param str name: A filter to only return resources that match the given name exactly.
    :param str state: A filter to only return resources that match the given lifecycle state.  The state value is case-insensitive.
    """
    ...
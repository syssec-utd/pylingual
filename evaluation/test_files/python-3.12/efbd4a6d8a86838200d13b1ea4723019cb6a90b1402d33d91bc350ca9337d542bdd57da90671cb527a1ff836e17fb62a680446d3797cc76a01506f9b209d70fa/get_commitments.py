import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetCommitmentsResult', 'AwaitableGetCommitmentsResult', 'get_commitments', 'get_commitments_output']

@pulumi.output_type
class GetCommitmentsResult:
    """
    A collection of values returned by getCommitments.
    """

    def __init__(__self__, commitments=None, compartment_id=None, filters=None, id=None, subscribed_service_id=None):
        if commitments and (not isinstance(commitments, list)):
            raise TypeError("Expected argument 'commitments' to be a list")
        pulumi.set(__self__, 'commitments', commitments)
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if subscribed_service_id and (not isinstance(subscribed_service_id, str)):
            raise TypeError("Expected argument 'subscribed_service_id' to be a str")
        pulumi.set(__self__, 'subscribed_service_id', subscribed_service_id)

    @property
    @pulumi.getter
    def commitments(self) -> Sequence['outputs.GetCommitmentsCommitmentResult']:
        """
        The list of commitments.
        """
        return pulumi.get(self, 'commitments')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> str:
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetCommitmentsFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='subscribedServiceId')
    def subscribed_service_id(self) -> str:
        """
        SPM internal Subscribed Service ID
        """
        return pulumi.get(self, 'subscribed_service_id')

class AwaitableGetCommitmentsResult(GetCommitmentsResult):

    def __await__(self):
        if False:
            yield self
        return GetCommitmentsResult(commitments=self.commitments, compartment_id=self.compartment_id, filters=self.filters, id=self.id, subscribed_service_id=self.subscribed_service_id)

def get_commitments(compartment_id: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetCommitmentsFilterArgs']]]=None, subscribed_service_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetCommitmentsResult:
    """
    This data source provides the list of Commitments in Oracle Cloud Infrastructure Onesubscription service.

    This list API returns all commitments for a particular Subscribed Service

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_commitments = oci.OneSubsription.get_commitments(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        subscribed_service_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The OCID of the root compartment.
    :param str subscribed_service_id: This param is used to get the commitments for a particular subscribed service
    """
    __args__ = dict()
    __args__['compartmentId'] = compartment_id
    __args__['filters'] = filters
    __args__['subscribedServiceId'] = subscribed_service_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:OneSubsription/getCommitments:getCommitments', __args__, opts=opts, typ=GetCommitmentsResult).value
    return AwaitableGetCommitmentsResult(commitments=__ret__.commitments, compartment_id=__ret__.compartment_id, filters=__ret__.filters, id=__ret__.id, subscribed_service_id=__ret__.subscribed_service_id)

@_utilities.lift_output_func(get_commitments)
def get_commitments_output(compartment_id: Optional[pulumi.Input[str]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetCommitmentsFilterArgs']]]]]=None, subscribed_service_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetCommitmentsResult]:
    """
    This data source provides the list of Commitments in Oracle Cloud Infrastructure Onesubscription service.

    This list API returns all commitments for a particular Subscribed Service

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_commitments = oci.OneSubsription.get_commitments(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        subscribed_service_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The OCID of the root compartment.
    :param str subscribed_service_id: This param is used to get the commitments for a particular subscribed service
    """
    ...
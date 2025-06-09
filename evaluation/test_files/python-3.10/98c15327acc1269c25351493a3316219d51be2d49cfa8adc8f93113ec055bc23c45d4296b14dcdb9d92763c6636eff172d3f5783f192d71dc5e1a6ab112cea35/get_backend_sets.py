import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetBackendSetsResult', 'AwaitableGetBackendSetsResult', 'get_backend_sets', 'get_backend_sets_output']

@pulumi.output_type
class GetBackendSetsResult:
    """
    A collection of values returned by getBackendSets.
    """

    def __init__(__self__, backend_set_collections=None, filters=None, id=None, network_load_balancer_id=None):
        if backend_set_collections and (not isinstance(backend_set_collections, list)):
            raise TypeError("Expected argument 'backend_set_collections' to be a list")
        pulumi.set(__self__, 'backend_set_collections', backend_set_collections)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if network_load_balancer_id and (not isinstance(network_load_balancer_id, str)):
            raise TypeError("Expected argument 'network_load_balancer_id' to be a str")
        pulumi.set(__self__, 'network_load_balancer_id', network_load_balancer_id)

    @property
    @pulumi.getter(name='backendSetCollections')
    def backend_set_collections(self) -> Sequence['outputs.GetBackendSetsBackendSetCollectionResult']:
        """
        The list of backend_set_collection.
        """
        return pulumi.get(self, 'backend_set_collections')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetBackendSetsFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='networkLoadBalancerId')
    def network_load_balancer_id(self) -> str:
        return pulumi.get(self, 'network_load_balancer_id')

class AwaitableGetBackendSetsResult(GetBackendSetsResult):

    def __await__(self):
        if False:
            yield self
        return GetBackendSetsResult(backend_set_collections=self.backend_set_collections, filters=self.filters, id=self.id, network_load_balancer_id=self.network_load_balancer_id)

def get_backend_sets(filters: Optional[Sequence[pulumi.InputType['GetBackendSetsFilterArgs']]]=None, network_load_balancer_id: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetBackendSetsResult:
    """
    This data source provides the list of Backend Sets in Oracle Cloud Infrastructure Network Load Balancer service.

    Lists all backend sets associated with a given network load balancer.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_backend_sets = oci.NetworkLoadBalancer.get_backend_sets(network_load_balancer_id=oci_network_load_balancer_network_load_balancer["test_network_load_balancer"]["id"])
    ```


    :param str network_load_balancer_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the network load balancer to update.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['networkLoadBalancerId'] = network_load_balancer_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:NetworkLoadBalancer/getBackendSets:getBackendSets', __args__, opts=opts, typ=GetBackendSetsResult).value
    return AwaitableGetBackendSetsResult(backend_set_collections=__ret__.backend_set_collections, filters=__ret__.filters, id=__ret__.id, network_load_balancer_id=__ret__.network_load_balancer_id)

@_utilities.lift_output_func(get_backend_sets)
def get_backend_sets_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetBackendSetsFilterArgs']]]]]=None, network_load_balancer_id: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetBackendSetsResult]:
    """
    This data source provides the list of Backend Sets in Oracle Cloud Infrastructure Network Load Balancer service.

    Lists all backend sets associated with a given network load balancer.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_backend_sets = oci.NetworkLoadBalancer.get_backend_sets(network_load_balancer_id=oci_network_load_balancer_network_load_balancer["test_network_load_balancer"]["id"])
    ```


    :param str network_load_balancer_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the network load balancer to update.
    """
    ...
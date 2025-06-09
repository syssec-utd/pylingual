import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetExternalClustersResult', 'AwaitableGetExternalClustersResult', 'get_external_clusters', 'get_external_clusters_output']

@pulumi.output_type
class GetExternalClustersResult:
    """
    A collection of values returned by getExternalClusters.
    """

    def __init__(__self__, compartment_id=None, display_name=None, external_cluster_collections=None, external_db_system_id=None, filters=None, id=None):
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if external_cluster_collections and (not isinstance(external_cluster_collections, list)):
            raise TypeError("Expected argument 'external_cluster_collections' to be a list")
        pulumi.set(__self__, 'external_cluster_collections', external_cluster_collections)
        if external_db_system_id and (not isinstance(external_db_system_id, str)):
            raise TypeError("Expected argument 'external_db_system_id' to be a str")
        pulumi.set(__self__, 'external_db_system_id', external_db_system_id)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[str]:
        """
        The user-friendly name for the external cluster. The name does not have to be unique.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='externalClusterCollections')
    def external_cluster_collections(self) -> Sequence['outputs.GetExternalClustersExternalClusterCollectionResult']:
        """
        The list of external_cluster_collection.
        """
        return pulumi.get(self, 'external_cluster_collections')

    @property
    @pulumi.getter(name='externalDbSystemId')
    def external_db_system_id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the external DB system that the cluster is a part of.
        """
        return pulumi.get(self, 'external_db_system_id')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetExternalClustersFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

class AwaitableGetExternalClustersResult(GetExternalClustersResult):

    def __await__(self):
        if False:
            yield self
        return GetExternalClustersResult(compartment_id=self.compartment_id, display_name=self.display_name, external_cluster_collections=self.external_cluster_collections, external_db_system_id=self.external_db_system_id, filters=self.filters, id=self.id)

def get_external_clusters(compartment_id: Optional[str]=None, display_name: Optional[str]=None, external_db_system_id: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetExternalClustersFilterArgs']]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetExternalClustersResult:
    """
    This data source provides the list of External Clusters in Oracle Cloud Infrastructure Database Management service.

    Lists the clusters in the specified external DB system.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_external_clusters = oci.DatabaseManagement.get_external_clusters(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        external_db_system_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to only return the resources that match the entire display name.
    :param str external_db_system_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the external DB system.
    """
    __args__ = dict()
    __args__['compartmentId'] = compartment_id
    __args__['displayName'] = display_name
    __args__['externalDbSystemId'] = external_db_system_id
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:DatabaseManagement/getExternalClusters:getExternalClusters', __args__, opts=opts, typ=GetExternalClustersResult).value
    return AwaitableGetExternalClustersResult(compartment_id=__ret__.compartment_id, display_name=__ret__.display_name, external_cluster_collections=__ret__.external_cluster_collections, external_db_system_id=__ret__.external_db_system_id, filters=__ret__.filters, id=__ret__.id)

@_utilities.lift_output_func(get_external_clusters)
def get_external_clusters_output(compartment_id: Optional[pulumi.Input[Optional[str]]]=None, display_name: Optional[pulumi.Input[Optional[str]]]=None, external_db_system_id: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetExternalClustersFilterArgs']]]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetExternalClustersResult]:
    """
    This data source provides the list of External Clusters in Oracle Cloud Infrastructure Database Management service.

    Lists the clusters in the specified external DB system.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_external_clusters = oci.DatabaseManagement.get_external_clusters(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        display_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        external_db_system_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
    :param str display_name: A filter to only return the resources that match the entire display name.
    :param str external_db_system_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the external DB system.
    """
    ...
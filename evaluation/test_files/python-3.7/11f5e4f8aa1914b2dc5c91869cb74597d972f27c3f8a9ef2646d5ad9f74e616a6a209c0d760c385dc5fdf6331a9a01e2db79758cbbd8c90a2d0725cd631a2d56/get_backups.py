import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['GetBackupsResult', 'AwaitableGetBackupsResult', 'get_backups', 'get_backups_output']

@pulumi.output_type
class GetBackupsResult:
    """
    A collection of values returned by getBackups.
    """

    def __init__(__self__, backups=None, compartment_id=None, database_id=None, filters=None, id=None):
        if backups and (not isinstance(backups, list)):
            raise TypeError("Expected argument 'backups' to be a list")
        pulumi.set(__self__, 'backups', backups)
        if compartment_id and (not isinstance(compartment_id, str)):
            raise TypeError("Expected argument 'compartment_id' to be a str")
        pulumi.set(__self__, 'compartment_id', compartment_id)
        if database_id and (not isinstance(database_id, str)):
            raise TypeError("Expected argument 'database_id' to be a str")
        pulumi.set(__self__, 'database_id', database_id)
        if filters and (not isinstance(filters, list)):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, 'filters', filters)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def backups(self) -> Sequence['outputs.GetBackupsBackupResult']:
        """
        The list of backups.
        """
        return pulumi.get(self, 'backups')

    @property
    @pulumi.getter(name='compartmentId')
    def compartment_id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the compartment.
        """
        return pulumi.get(self, 'compartment_id')

    @property
    @pulumi.getter(name='databaseId')
    def database_id(self) -> Optional[str]:
        """
        The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the database.
        """
        return pulumi.get(self, 'database_id')

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetBackupsFilterResult']]:
        return pulumi.get(self, 'filters')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, 'id')

class AwaitableGetBackupsResult(GetBackupsResult):

    def __await__(self):
        if False:
            yield self
        return GetBackupsResult(backups=self.backups, compartment_id=self.compartment_id, database_id=self.database_id, filters=self.filters, id=self.id)

def get_backups(compartment_id: Optional[str]=None, database_id: Optional[str]=None, filters: Optional[Sequence[pulumi.InputType['GetBackupsFilterArgs']]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetBackupsResult:
    """
    This data source provides the list of Backups in Oracle Cloud Infrastructure Database service.

    Gets a list of backups based on the `databaseId` or `compartmentId` specified. Either one of these query parameters must be provided.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_backups = oci.Database.get_backups(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        database_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The compartment [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm).
    :param str database_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the database.
    """
    __args__ = dict()
    __args__['compartmentId'] = compartment_id
    __args__['databaseId'] = database_id
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('oci:Database/getBackups:getBackups', __args__, opts=opts, typ=GetBackupsResult).value
    return AwaitableGetBackupsResult(backups=__ret__.backups, compartment_id=__ret__.compartment_id, database_id=__ret__.database_id, filters=__ret__.filters, id=__ret__.id)

@_utilities.lift_output_func(get_backups)
def get_backups_output(compartment_id: Optional[pulumi.Input[Optional[str]]]=None, database_id: Optional[pulumi.Input[Optional[str]]]=None, filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetBackupsFilterArgs']]]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetBackupsResult]:
    """
    This data source provides the list of Backups in Oracle Cloud Infrastructure Database service.

    Gets a list of backups based on the `databaseId` or `compartmentId` specified. Either one of these query parameters must be provided.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_oci as oci

    test_backups = oci.Database.get_backups(compartment_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
        database_id=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str compartment_id: The compartment [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm).
    :param str database_id: The [OCID](https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm) of the database.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ListWebAppSiteBackupsResult', 'AwaitableListWebAppSiteBackupsResult', 'list_web_app_site_backups', 'list_web_app_site_backups_output']

@pulumi.output_type
class ListWebAppSiteBackupsResult:
    """
    Collection of backup items.
    """

    def __init__(__self__, next_link=None, value=None):
        if next_link and (not isinstance(next_link, str)):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, 'next_link', next_link)
        if value and (not isinstance(value, list)):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter(name='nextLink')
    def next_link(self) -> str:
        """
        Link to next page of resources.
        """
        return pulumi.get(self, 'next_link')

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.BackupItemResponse']:
        """
        Collection of resources.
        """
        return pulumi.get(self, 'value')

class AwaitableListWebAppSiteBackupsResult(ListWebAppSiteBackupsResult):

    def __await__(self):
        if False:
            yield self
        return ListWebAppSiteBackupsResult(next_link=self.next_link, value=self.value)

def list_web_app_site_backups(name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListWebAppSiteBackupsResult:
    """
    Gets existing backups of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20190801:listWebAppSiteBackups', __args__, opts=opts, typ=ListWebAppSiteBackupsResult).value
    return AwaitableListWebAppSiteBackupsResult(next_link=__ret__.next_link, value=__ret__.value)

@_utilities.lift_output_func(list_web_app_site_backups)
def list_web_app_site_backups_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListWebAppSiteBackupsResult]:
    """
    Gets existing backups of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
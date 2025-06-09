import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ListWebAppAzureStorageAccountsSlotResult', 'AwaitableListWebAppAzureStorageAccountsSlotResult', 'list_web_app_azure_storage_accounts_slot', 'list_web_app_azure_storage_accounts_slot_output']

@pulumi.output_type
class ListWebAppAzureStorageAccountsSlotResult:
    """
    AzureStorageInfo dictionary resource.
    """

    def __init__(__self__, id=None, kind=None, name=None, properties=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if properties and (not isinstance(properties, dict)):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, 'properties', properties)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, 'outputs.AzureStorageInfoValueResponse']:
        """
        Azure storage accounts.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

class AwaitableListWebAppAzureStorageAccountsSlotResult(ListWebAppAzureStorageAccountsSlotResult):

    def __await__(self):
        if False:
            yield self
        return ListWebAppAzureStorageAccountsSlotResult(id=self.id, kind=self.kind, name=self.name, properties=self.properties, type=self.type)

def list_web_app_azure_storage_accounts_slot(name: Optional[str]=None, resource_group_name: Optional[str]=None, slot: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableListWebAppAzureStorageAccountsSlotResult:
    """
    Gets the Azure storage account configurations of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will update the Azure storage account configurations for the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20210301:listWebAppAzureStorageAccountsSlot', __args__, opts=opts, typ=ListWebAppAzureStorageAccountsSlotResult).value
    return AwaitableListWebAppAzureStorageAccountsSlotResult(id=__ret__.id, kind=__ret__.kind, name=__ret__.name, properties=__ret__.properties, type=__ret__.type)

@_utilities.lift_output_func(list_web_app_azure_storage_accounts_slot)
def list_web_app_azure_storage_accounts_slot_output(name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[ListWebAppAzureStorageAccountsSlotResult]:
    """
    Gets the Azure storage account configurations of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will update the Azure storage account configurations for the production slot.
    """
    ...
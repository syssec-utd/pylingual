import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetInventoryItemResult', 'AwaitableGetInventoryItemResult', 'get_inventory_item', 'get_inventory_item_output']

@pulumi.output_type
class GetInventoryItemResult:
    """
    Defines the inventory item.
    """

    def __init__(__self__, id=None, inventory_type=None, kind=None, managed_resource_id=None, mo_name=None, mo_ref_id=None, name=None, provisioning_state=None, system_data=None, type=None):
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if inventory_type and (not isinstance(inventory_type, str)):
            raise TypeError("Expected argument 'inventory_type' to be a str")
        pulumi.set(__self__, 'inventory_type', inventory_type)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if managed_resource_id and (not isinstance(managed_resource_id, str)):
            raise TypeError("Expected argument 'managed_resource_id' to be a str")
        pulumi.set(__self__, 'managed_resource_id', managed_resource_id)
        if mo_name and (not isinstance(mo_name, str)):
            raise TypeError("Expected argument 'mo_name' to be a str")
        pulumi.set(__self__, 'mo_name', mo_name)
        if mo_ref_id and (not isinstance(mo_ref_id, str)):
            raise TypeError("Expected argument 'mo_ref_id' to be a str")
        pulumi.set(__self__, 'mo_ref_id', mo_ref_id)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='inventoryType')
    def inventory_type(self) -> str:
        """
        They inventory type.
        """
        return pulumi.get(self, 'inventory_type')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter(name='managedResourceId')
    def managed_resource_id(self) -> Optional[str]:
        """
        Gets or sets the tracked resource id corresponding to the inventory resource.
        """
        return pulumi.get(self, 'managed_resource_id')

    @property
    @pulumi.getter(name='moName')
    def mo_name(self) -> Optional[str]:
        """
        Gets or sets the vCenter Managed Object name for the inventory item.
        """
        return pulumi.get(self, 'mo_name')

    @property
    @pulumi.getter(name='moRefId')
    def mo_ref_id(self) -> Optional[str]:
        """
        Gets or sets the MoRef (Managed Object Reference) ID for the inventory item.
        """
        return pulumi.get(self, 'mo_ref_id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Gets or sets the provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system data.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')

class AwaitableGetInventoryItemResult(GetInventoryItemResult):

    def __await__(self):
        if False:
            yield self
        return GetInventoryItemResult(id=self.id, inventory_type=self.inventory_type, kind=self.kind, managed_resource_id=self.managed_resource_id, mo_name=self.mo_name, mo_ref_id=self.mo_ref_id, name=self.name, provisioning_state=self.provisioning_state, system_data=self.system_data, type=self.type)

def get_inventory_item(inventory_item_name: Optional[str]=None, resource_group_name: Optional[str]=None, vcenter_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetInventoryItemResult:
    """
    Implements InventoryItem GET method.


    :param str inventory_item_name: Name of the inventoryItem.
    :param str resource_group_name: The Resource Group Name.
    :param str vcenter_name: Name of the vCenter.
    """
    __args__ = dict()
    __args__['inventoryItemName'] = inventory_item_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vcenterName'] = vcenter_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:connectedvmwarevsphere/v20220110preview:getInventoryItem', __args__, opts=opts, typ=GetInventoryItemResult).value
    return AwaitableGetInventoryItemResult(id=__ret__.id, inventory_type=__ret__.inventory_type, kind=__ret__.kind, managed_resource_id=__ret__.managed_resource_id, mo_name=__ret__.mo_name, mo_ref_id=__ret__.mo_ref_id, name=__ret__.name, provisioning_state=__ret__.provisioning_state, system_data=__ret__.system_data, type=__ret__.type)

@_utilities.lift_output_func(get_inventory_item)
def get_inventory_item_output(inventory_item_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, vcenter_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetInventoryItemResult]:
    """
    Implements InventoryItem GET method.


    :param str inventory_item_name: Name of the inventoryItem.
    :param str resource_group_name: The Resource Group Name.
    :param str vcenter_name: Name of the vCenter.
    """
    ...
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetVirtualNetworkResult', 'AwaitableGetVirtualNetworkResult', 'get_virtual_network', 'get_virtual_network_output']

@pulumi.output_type
class GetVirtualNetworkResult:
    """
    Define the virtualNetwork.
    """

    def __init__(__self__, custom_resource_name=None, extended_location=None, id=None, inventory_item_id=None, kind=None, location=None, mo_name=None, mo_ref_id=None, name=None, provisioning_state=None, statuses=None, system_data=None, tags=None, type=None, uuid=None, v_center_id=None):
        if custom_resource_name and (not isinstance(custom_resource_name, str)):
            raise TypeError("Expected argument 'custom_resource_name' to be a str")
        pulumi.set(__self__, 'custom_resource_name', custom_resource_name)
        if extended_location and (not isinstance(extended_location, dict)):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, 'extended_location', extended_location)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if inventory_item_id and (not isinstance(inventory_item_id, str)):
            raise TypeError("Expected argument 'inventory_item_id' to be a str")
        pulumi.set(__self__, 'inventory_item_id', inventory_item_id)
        if kind and (not isinstance(kind, str)):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, 'kind', kind)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
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
        if statuses and (not isinstance(statuses, list)):
            raise TypeError("Expected argument 'statuses' to be a list")
        pulumi.set(__self__, 'statuses', statuses)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if uuid and (not isinstance(uuid, str)):
            raise TypeError("Expected argument 'uuid' to be a str")
        pulumi.set(__self__, 'uuid', uuid)
        if v_center_id and (not isinstance(v_center_id, str)):
            raise TypeError("Expected argument 'v_center_id' to be a str")
        pulumi.set(__self__, 'v_center_id', v_center_id)

    @property
    @pulumi.getter(name='customResourceName')
    def custom_resource_name(self) -> str:
        """
        Gets the name of the corresponding resource in Kubernetes.
        """
        return pulumi.get(self, 'custom_resource_name')

    @property
    @pulumi.getter(name='extendedLocation')
    def extended_location(self) -> Optional['outputs.ExtendedLocationResponse']:
        """
        Gets or sets the extended location.
        """
        return pulumi.get(self, 'extended_location')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Gets or sets the Id.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter(name='inventoryItemId')
    def inventory_item_id(self) -> Optional[str]:
        """
        Gets or sets the inventory Item ID for the virtual network.
        """
        return pulumi.get(self, 'inventory_item_id')

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='moName')
    def mo_name(self) -> str:
        """
        Gets or sets the vCenter Managed Object name for the virtual network.
        """
        return pulumi.get(self, 'mo_name')

    @property
    @pulumi.getter(name='moRefId')
    def mo_ref_id(self) -> Optional[str]:
        """
        Gets or sets the vCenter MoRef (Managed Object Reference) ID for the virtual network.
        """
        return pulumi.get(self, 'mo_ref_id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Gets or sets the name.
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
    @pulumi.getter
    def statuses(self) -> Sequence['outputs.ResourceStatusResponse']:
        """
        The resource status information.
        """
        return pulumi.get(self, 'statuses')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system data.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Gets or sets the Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Gets or sets the type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def uuid(self) -> str:
        """
        Gets or sets a unique identifier for this resource.
        """
        return pulumi.get(self, 'uuid')

    @property
    @pulumi.getter(name='vCenterId')
    def v_center_id(self) -> Optional[str]:
        """
        Gets or sets the ARM Id of the vCenter resource in which this template resides.
        """
        return pulumi.get(self, 'v_center_id')

class AwaitableGetVirtualNetworkResult(GetVirtualNetworkResult):

    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkResult(custom_resource_name=self.custom_resource_name, extended_location=self.extended_location, id=self.id, inventory_item_id=self.inventory_item_id, kind=self.kind, location=self.location, mo_name=self.mo_name, mo_ref_id=self.mo_ref_id, name=self.name, provisioning_state=self.provisioning_state, statuses=self.statuses, system_data=self.system_data, tags=self.tags, type=self.type, uuid=self.uuid, v_center_id=self.v_center_id)

def get_virtual_network(resource_group_name: Optional[str]=None, virtual_network_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetVirtualNetworkResult:
    """
    Implements virtual network GET method.


    :param str resource_group_name: The Resource Group Name.
    :param str virtual_network_name: Name of the virtual network resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualNetworkName'] = virtual_network_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:connectedvmwarevsphere/v20220110preview:getVirtualNetwork', __args__, opts=opts, typ=GetVirtualNetworkResult).value
    return AwaitableGetVirtualNetworkResult(custom_resource_name=__ret__.custom_resource_name, extended_location=__ret__.extended_location, id=__ret__.id, inventory_item_id=__ret__.inventory_item_id, kind=__ret__.kind, location=__ret__.location, mo_name=__ret__.mo_name, mo_ref_id=__ret__.mo_ref_id, name=__ret__.name, provisioning_state=__ret__.provisioning_state, statuses=__ret__.statuses, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type, uuid=__ret__.uuid, v_center_id=__ret__.v_center_id)

@_utilities.lift_output_func(get_virtual_network)
def get_virtual_network_output(resource_group_name: Optional[pulumi.Input[str]]=None, virtual_network_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetVirtualNetworkResult]:
    """
    Implements virtual network GET method.


    :param str resource_group_name: The Resource Group Name.
    :param str virtual_network_name: Name of the virtual network resource.
    """
    ...
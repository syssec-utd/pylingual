import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['AvailabilitySetArgs', 'AvailabilitySet']

@pulumi.input_type
class AvailabilitySetArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], availability_set_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, platform_fault_domain_count: Optional[pulumi.Input[int]]=None, platform_update_domain_count: Optional[pulumi.Input[int]]=None, proximity_placement_group: Optional[pulumi.Input['SubResourceArgs']]=None, sku: Optional[pulumi.Input['SkuArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_machines: Optional[pulumi.Input[Sequence[pulumi.Input['SubResourceArgs']]]]=None):
        """
        The set of arguments for constructing a AvailabilitySet resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] availability_set_name: The name of the availability set.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] platform_fault_domain_count: Fault Domain count.
        :param pulumi.Input[int] platform_update_domain_count: Update Domain count.
        :param pulumi.Input['SubResourceArgs'] proximity_placement_group: Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        :param pulumi.Input['SkuArgs'] sku: Sku of the availability set, only name is required to be set. See AvailabilitySetSkuTypes for possible set of values. Use 'Aligned' for virtual machines with managed disks and 'Classic' for virtual machines with unmanaged disks. Default value is 'Classic'.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input['SubResourceArgs']]] virtual_machines: A list of references to all virtual machines in the availability set.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if availability_set_name is not None:
            pulumi.set(__self__, 'availability_set_name', availability_set_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if platform_fault_domain_count is not None:
            pulumi.set(__self__, 'platform_fault_domain_count', platform_fault_domain_count)
        if platform_update_domain_count is not None:
            pulumi.set(__self__, 'platform_update_domain_count', platform_update_domain_count)
        if proximity_placement_group is not None:
            pulumi.set(__self__, 'proximity_placement_group', proximity_placement_group)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if virtual_machines is not None:
            pulumi.set(__self__, 'virtual_machines', virtual_machines)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='availabilitySetName')
    def availability_set_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the availability set.
        """
        return pulumi.get(self, 'availability_set_name')

    @availability_set_name.setter
    def availability_set_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'availability_set_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='platformFaultDomainCount')
    def platform_fault_domain_count(self) -> Optional[pulumi.Input[int]]:
        """
        Fault Domain count.
        """
        return pulumi.get(self, 'platform_fault_domain_count')

    @platform_fault_domain_count.setter
    def platform_fault_domain_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'platform_fault_domain_count', value)

    @property
    @pulumi.getter(name='platformUpdateDomainCount')
    def platform_update_domain_count(self) -> Optional[pulumi.Input[int]]:
        """
        Update Domain count.
        """
        return pulumi.get(self, 'platform_update_domain_count')

    @platform_update_domain_count.setter
    def platform_update_domain_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'platform_update_domain_count', value)

    @property
    @pulumi.getter(name='proximityPlacementGroup')
    def proximity_placement_group(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        """
        return pulumi.get(self, 'proximity_placement_group')

    @proximity_placement_group.setter
    def proximity_placement_group(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, 'proximity_placement_group', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        Sku of the availability set, only name is required to be set. See AvailabilitySetSkuTypes for possible set of values. Use 'Aligned' for virtual machines with managed disks and 'Classic' for virtual machines with unmanaged disks. Default value is 'Classic'.
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter(name='virtualMachines')
    def virtual_machines(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SubResourceArgs']]]]:
        """
        A list of references to all virtual machines in the availability set.
        """
        return pulumi.get(self, 'virtual_machines')

    @virtual_machines.setter
    def virtual_machines(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SubResourceArgs']]]]):
        pulumi.set(self, 'virtual_machines', value)

class AvailabilitySet(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, availability_set_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, platform_fault_domain_count: Optional[pulumi.Input[int]]=None, platform_update_domain_count: Optional[pulumi.Input[int]]=None, proximity_placement_group: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_machines: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubResourceArgs']]]]]=None, __props__=None):
        """
        Specifies information about the availability set that the virtual machine should be assigned to. Virtual machines specified in the same availability set are allocated to different nodes to maximize availability. For more information about availability sets, see [Manage the availability of virtual machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-manage-availability?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json). <br><br> For more information on Azure planned maintenance, see [Planned maintenance for virtual machines in Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-planned-maintenance?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json) <br><br> Currently, a VM can only be added to availability set at creation time. An existing VM cannot be added to an availability set.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_set_name: The name of the availability set.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] platform_fault_domain_count: Fault Domain count.
        :param pulumi.Input[int] platform_update_domain_count: Update Domain count.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] proximity_placement_group: Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Sku of the availability set, only name is required to be set. See AvailabilitySetSkuTypes for possible set of values. Use 'Aligned' for virtual machines with managed disks and 'Classic' for virtual machines with unmanaged disks. Default value is 'Classic'.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubResourceArgs']]]] virtual_machines: A list of references to all virtual machines in the availability set.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: AvailabilitySetArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Specifies information about the availability set that the virtual machine should be assigned to. Virtual machines specified in the same availability set are allocated to different nodes to maximize availability. For more information about availability sets, see [Manage the availability of virtual machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-manage-availability?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json). <br><br> For more information on Azure planned maintenance, see [Planned maintenance for virtual machines in Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-planned-maintenance?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json) <br><br> Currently, a VM can only be added to availability set at creation time. An existing VM cannot be added to an availability set.

        :param str resource_name: The name of the resource.
        :param AvailabilitySetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AvailabilitySetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, availability_set_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, platform_fault_domain_count: Optional[pulumi.Input[int]]=None, platform_update_domain_count: Optional[pulumi.Input[int]]=None, proximity_placement_group: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, virtual_machines: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubResourceArgs']]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AvailabilitySetArgs.__new__(AvailabilitySetArgs)
            __props__.__dict__['availability_set_name'] = availability_set_name
            __props__.__dict__['location'] = location
            __props__.__dict__['platform_fault_domain_count'] = platform_fault_domain_count
            __props__.__dict__['platform_update_domain_count'] = platform_update_domain_count
            __props__.__dict__['proximity_placement_group'] = proximity_placement_group
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['tags'] = tags
            __props__.__dict__['virtual_machines'] = virtual_machines
            __props__.__dict__['name'] = None
            __props__.__dict__['statuses'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:compute:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20150615:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20160330:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20160430preview:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20170330:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20171201:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20180401:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20180601:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20181001:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20190301:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20190701:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20191201:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20200601:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20210301:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20210401:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20210701:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20211101:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20220301:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20220801:AvailabilitySet'), pulumi.Alias(type_='azure-native:compute/v20221101:AvailabilitySet')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AvailabilitySet, __self__).__init__('azure-native:compute/v20201201:AvailabilitySet', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'AvailabilitySet':
        """
        Get an existing AvailabilitySet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = AvailabilitySetArgs.__new__(AvailabilitySetArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['platform_fault_domain_count'] = None
        __props__.__dict__['platform_update_domain_count'] = None
        __props__.__dict__['proximity_placement_group'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['statuses'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['virtual_machines'] = None
        return AvailabilitySet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='platformFaultDomainCount')
    def platform_fault_domain_count(self) -> pulumi.Output[Optional[int]]:
        """
        Fault Domain count.
        """
        return pulumi.get(self, 'platform_fault_domain_count')

    @property
    @pulumi.getter(name='platformUpdateDomainCount')
    def platform_update_domain_count(self) -> pulumi.Output[Optional[int]]:
        """
        Update Domain count.
        """
        return pulumi.get(self, 'platform_update_domain_count')

    @property
    @pulumi.getter(name='proximityPlacementGroup')
    def proximity_placement_group(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        """
        return pulumi.get(self, 'proximity_placement_group')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Sku of the availability set, only name is required to be set. See AvailabilitySetSkuTypes for possible set of values. Use 'Aligned' for virtual machines with managed disks and 'Classic' for virtual machines with unmanaged disks. Default value is 'Classic'.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def statuses(self) -> pulumi.Output[Sequence['outputs.InstanceViewStatusResponse']]:
        """
        The resource status information.
        """
        return pulumi.get(self, 'statuses')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='virtualMachines')
    def virtual_machines(self) -> pulumi.Output[Optional[Sequence['outputs.SubResourceResponse']]]:
        """
        A list of references to all virtual machines in the availability set.
        """
        return pulumi.get(self, 'virtual_machines')
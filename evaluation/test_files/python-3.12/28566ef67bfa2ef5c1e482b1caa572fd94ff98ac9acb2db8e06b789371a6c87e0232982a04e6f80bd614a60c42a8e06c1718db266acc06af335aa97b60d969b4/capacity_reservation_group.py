import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['CapacityReservationGroupArgs', 'CapacityReservationGroup']

@pulumi.input_type
class CapacityReservationGroupArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], capacity_reservation_group_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a CapacityReservationGroup resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] capacity_reservation_group_name: The name of the capacity reservation group.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: Availability Zones to use for this capacity reservation group. The zones can be assigned only during creation. If not provided, the group supports only regional resources in the region. If provided, enforces each capacity reservation in the group to be in one of the zones.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if capacity_reservation_group_name is not None:
            pulumi.set(__self__, 'capacity_reservation_group_name', capacity_reservation_group_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if zones is not None:
            pulumi.set(__self__, 'zones', zones)

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
    @pulumi.getter(name='capacityReservationGroupName')
    def capacity_reservation_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the capacity reservation group.
        """
        return pulumi.get(self, 'capacity_reservation_group_name')

    @capacity_reservation_group_name.setter
    def capacity_reservation_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'capacity_reservation_group_name', value)

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
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Availability Zones to use for this capacity reservation group. The zones can be assigned only during creation. If not provided, the group supports only regional resources in the region. If provided, enforces each capacity reservation in the group to be in one of the zones.
        """
        return pulumi.get(self, 'zones')

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'zones', value)

class CapacityReservationGroup(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, capacity_reservation_group_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        Specifies information about the capacity reservation group that the capacity reservations should be assigned to. <br><br> Currently, a capacity reservation can only be added to a capacity reservation group at creation time. An existing capacity reservation cannot be added or moved to another capacity reservation group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] capacity_reservation_group_name: The name of the capacity reservation group.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: Availability Zones to use for this capacity reservation group. The zones can be assigned only during creation. If not provided, the group supports only regional resources in the region. If provided, enforces each capacity reservation in the group to be in one of the zones.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: CapacityReservationGroupArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Specifies information about the capacity reservation group that the capacity reservations should be assigned to. <br><br> Currently, a capacity reservation can only be added to a capacity reservation group at creation time. An existing capacity reservation cannot be added or moved to another capacity reservation group.

        :param str resource_name: The name of the resource.
        :param CapacityReservationGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CapacityReservationGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, capacity_reservation_group_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CapacityReservationGroupArgs.__new__(CapacityReservationGroupArgs)
            __props__.__dict__['capacity_reservation_group_name'] = capacity_reservation_group_name
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['zones'] = zones
            __props__.__dict__['capacity_reservations'] = None
            __props__.__dict__['instance_view'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['virtual_machines_associated'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:compute:CapacityReservationGroup'), pulumi.Alias(type_='azure-native:compute/v20210401:CapacityReservationGroup'), pulumi.Alias(type_='azure-native:compute/v20211101:CapacityReservationGroup'), pulumi.Alias(type_='azure-native:compute/v20220301:CapacityReservationGroup'), pulumi.Alias(type_='azure-native:compute/v20220801:CapacityReservationGroup'), pulumi.Alias(type_='azure-native:compute/v20221101:CapacityReservationGroup')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(CapacityReservationGroup, __self__).__init__('azure-native:compute/v20210701:CapacityReservationGroup', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'CapacityReservationGroup':
        """
        Get an existing CapacityReservationGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = CapacityReservationGroupArgs.__new__(CapacityReservationGroupArgs)
        __props__.__dict__['capacity_reservations'] = None
        __props__.__dict__['instance_view'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['virtual_machines_associated'] = None
        __props__.__dict__['zones'] = None
        return CapacityReservationGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='capacityReservations')
    def capacity_reservations(self) -> pulumi.Output[Sequence['outputs.SubResourceReadOnlyResponse']]:
        """
        A list of all capacity reservation resource ids that belong to capacity reservation group.
        """
        return pulumi.get(self, 'capacity_reservations')

    @property
    @pulumi.getter(name='instanceView')
    def instance_view(self) -> pulumi.Output['outputs.CapacityReservationGroupInstanceViewResponse']:
        """
        The capacity reservation group instance view which has the list of instance views for all the capacity reservations that belong to the capacity reservation group.
        """
        return pulumi.get(self, 'instance_view')

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
    @pulumi.getter(name='virtualMachinesAssociated')
    def virtual_machines_associated(self) -> pulumi.Output[Sequence['outputs.SubResourceReadOnlyResponse']]:
        """
        A list of references to all virtual machines associated to the capacity reservation group.
        """
        return pulumi.get(self, 'virtual_machines_associated')

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Availability Zones to use for this capacity reservation group. The zones can be assigned only during creation. If not provided, the group supports only regional resources in the region. If provided, enforces each capacity reservation in the group to be in one of the zones.
        """
        return pulumi.get(self, 'zones')
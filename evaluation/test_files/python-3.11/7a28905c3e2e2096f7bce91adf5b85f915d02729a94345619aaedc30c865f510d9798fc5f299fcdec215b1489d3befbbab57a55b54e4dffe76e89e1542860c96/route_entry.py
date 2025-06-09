import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['RouteEntryArgs', 'RouteEntry']

@pulumi.input_type
class RouteEntryArgs:

    def __init__(__self__, *, cidr_block: pulumi.Input[str], instance_id: pulumi.Input[str], route_table_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a RouteEntry resource.
        :param pulumi.Input[str] cidr_block: The destination CIDR block of the route entry to publish.
               
               ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.
               
               ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] route_table_id: The route table of the attached VBR or VPC.
        """
        pulumi.set(__self__, 'cidr_block', cidr_block)
        pulumi.set(__self__, 'instance_id', instance_id)
        pulumi.set(__self__, 'route_table_id', route_table_id)

    @property
    @pulumi.getter(name='cidrBlock')
    def cidr_block(self) -> pulumi.Input[str]:
        """
        The destination CIDR block of the route entry to publish.

        ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.

        ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        """
        return pulumi.get(self, 'cidr_block')

    @cidr_block.setter
    def cidr_block(self, value: pulumi.Input[str]):
        pulumi.set(self, 'cidr_block', value)

    @property
    @pulumi.getter(name='instanceId')
    def instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, 'instance_id')

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'instance_id', value)

    @property
    @pulumi.getter(name='routeTableId')
    def route_table_id(self) -> pulumi.Input[str]:
        """
        The route table of the attached VBR or VPC.
        """
        return pulumi.get(self, 'route_table_id')

    @route_table_id.setter
    def route_table_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'route_table_id', value)

@pulumi.input_type
class _RouteEntryState:

    def __init__(__self__, *, cidr_block: Optional[pulumi.Input[str]]=None, instance_id: Optional[pulumi.Input[str]]=None, route_table_id: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering RouteEntry resources.
        :param pulumi.Input[str] cidr_block: The destination CIDR block of the route entry to publish.
               
               ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.
               
               ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] route_table_id: The route table of the attached VBR or VPC.
        """
        if cidr_block is not None:
            pulumi.set(__self__, 'cidr_block', cidr_block)
        if instance_id is not None:
            pulumi.set(__self__, 'instance_id', instance_id)
        if route_table_id is not None:
            pulumi.set(__self__, 'route_table_id', route_table_id)

    @property
    @pulumi.getter(name='cidrBlock')
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The destination CIDR block of the route entry to publish.

        ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.

        ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        """
        return pulumi.get(self, 'cidr_block')

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cidr_block', value)

    @property
    @pulumi.getter(name='instanceId')
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, 'instance_id')

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'instance_id', value)

    @property
    @pulumi.getter(name='routeTableId')
    def route_table_id(self) -> Optional[pulumi.Input[str]]:
        """
        The route table of the attached VBR or VPC.
        """
        return pulumi.get(self, 'route_table_id')

    @route_table_id.setter
    def route_table_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'route_table_id', value)

class RouteEntry(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cidr_block: Optional[pulumi.Input[str]]=None, instance_id: Optional[pulumi.Input[str]]=None, route_table_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Provides a CEN route entry resource. Cloud Enterprise Network (CEN) supports publishing and withdrawing route entries of attached networks. You can publish a route entry of an attached VPC or VBR to a CEN instance, then other attached networks can learn the route if there is no route conflict. You can withdraw a published route entry when CEN does not need it any more.

        For information about CEN route entries publishment and how to use it, see [Manage network routes](https://www.alibabacloud.com/help/doc-detail/86980.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a cen_route_entry resource and use it to publish a route entry pointing to an ECS.
        hz = alicloud.Provider("hz", region="cn-hangzhou")
        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenRouteEntryConfig"
        default_zones = alicloud.get_zones(available_disk_category="cloud_efficiency",
            available_resource_creation="VSwitch")
        default_instance_types = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            cpu_core_count=1,
            memory_size=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        vpc = alicloud.vpc.Network("vpc",
            vpc_name=name,
            cidr_block="172.16.0.0/12",
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=vpc.id,
            cidr_block="172.16.0.0/21",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_security_group = alicloud.ecs.SecurityGroup("defaultSecurityGroup",
            description="foo",
            vpc_id=vpc.id,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_instance = alicloud.ecs.Instance("defaultInstance",
            vswitch_id=default_switch.id,
            image_id=default_images.images[0].id,
            instance_type=default_instance_types.instance_types[0].id,
            system_disk_category="cloud_efficiency",
            internet_charge_type="PayByTraffic",
            internet_max_bandwidth_out=5,
            security_groups=[default_security_group.id],
            instance_name=name,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        cen = alicloud.cen.Instance("cen")
        attach = alicloud.cen.InstanceAttachment("attach",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-hangzhou",
            opts=pulumi.ResourceOptions(depends_on=[default_switch]))
        route = alicloud.vpc.RouteEntry("route",
            route_table_id=vpc.route_table_id,
            destination_cidrblock="11.0.0.0/16",
            nexthop_type="Instance",
            nexthop_id=default_instance.id,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        foo = alicloud.cen.RouteEntry("foo",
            instance_id=cen.id,
            route_table_id=vpc.route_table_id,
            cidr_block=route.destination_cidrblock,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"],
                depends_on=[attach]))
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/routeEntry:RouteEntry example cen-abc123456:vtb-abc123:192.168.0.0/24
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The destination CIDR block of the route entry to publish.
               
               ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.
               
               ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] route_table_id: The route table of the attached VBR or VPC.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: RouteEntryArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a CEN route entry resource. Cloud Enterprise Network (CEN) supports publishing and withdrawing route entries of attached networks. You can publish a route entry of an attached VPC or VBR to a CEN instance, then other attached networks can learn the route if there is no route conflict. You can withdraw a published route entry when CEN does not need it any more.

        For information about CEN route entries publishment and how to use it, see [Manage network routes](https://www.alibabacloud.com/help/doc-detail/86980.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        # Create a cen_route_entry resource and use it to publish a route entry pointing to an ECS.
        hz = alicloud.Provider("hz", region="cn-hangzhou")
        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenRouteEntryConfig"
        default_zones = alicloud.get_zones(available_disk_category="cloud_efficiency",
            available_resource_creation="VSwitch")
        default_instance_types = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            cpu_core_count=1,
            memory_size=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        vpc = alicloud.vpc.Network("vpc",
            vpc_name=name,
            cidr_block="172.16.0.0/12",
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=vpc.id,
            cidr_block="172.16.0.0/21",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_security_group = alicloud.ecs.SecurityGroup("defaultSecurityGroup",
            description="foo",
            vpc_id=vpc.id,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        default_instance = alicloud.ecs.Instance("defaultInstance",
            vswitch_id=default_switch.id,
            image_id=default_images.images[0].id,
            instance_type=default_instance_types.instance_types[0].id,
            system_disk_category="cloud_efficiency",
            internet_charge_type="PayByTraffic",
            internet_max_bandwidth_out=5,
            security_groups=[default_security_group.id],
            instance_name=name,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        cen = alicloud.cen.Instance("cen")
        attach = alicloud.cen.InstanceAttachment("attach",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-hangzhou",
            opts=pulumi.ResourceOptions(depends_on=[default_switch]))
        route = alicloud.vpc.RouteEntry("route",
            route_table_id=vpc.route_table_id,
            destination_cidrblock="11.0.0.0/16",
            nexthop_type="Instance",
            nexthop_id=default_instance.id,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"]))
        foo = alicloud.cen.RouteEntry("foo",
            instance_id=cen.id,
            route_table_id=vpc.route_table_id,
            cidr_block=route.destination_cidrblock,
            opts=pulumi.ResourceOptions(provider=alicloud["hz"],
                depends_on=[attach]))
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/routeEntry:RouteEntry example cen-abc123456:vtb-abc123:192.168.0.0/24
        ```

        :param str resource_name: The name of the resource.
        :param RouteEntryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RouteEntryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cidr_block: Optional[pulumi.Input[str]]=None, instance_id: Optional[pulumi.Input[str]]=None, route_table_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RouteEntryArgs.__new__(RouteEntryArgs)
            if cidr_block is None and (not opts.urn):
                raise TypeError("Missing required property 'cidr_block'")
            __props__.__dict__['cidr_block'] = cidr_block
            if instance_id is None and (not opts.urn):
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__['instance_id'] = instance_id
            if route_table_id is None and (not opts.urn):
                raise TypeError("Missing required property 'route_table_id'")
            __props__.__dict__['route_table_id'] = route_table_id
        super(RouteEntry, __self__).__init__('alicloud:cen/routeEntry:RouteEntry', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, cidr_block: Optional[pulumi.Input[str]]=None, instance_id: Optional[pulumi.Input[str]]=None, route_table_id: Optional[pulumi.Input[str]]=None) -> 'RouteEntry':
        """
        Get an existing RouteEntry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The destination CIDR block of the route entry to publish.
               
               ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.
               
               ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] route_table_id: The route table of the attached VBR or VPC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _RouteEntryState.__new__(_RouteEntryState)
        __props__.__dict__['cidr_block'] = cidr_block
        __props__.__dict__['instance_id'] = instance_id
        __props__.__dict__['route_table_id'] = route_table_id
        return RouteEntry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='cidrBlock')
    def cidr_block(self) -> pulumi.Output[str]:
        """
        The destination CIDR block of the route entry to publish.

        ->**NOTE:** The "alicloud_cen_instance_route_entries" resource depends on the related "cen.InstanceAttachment" resource.

        ->**NOTE:** The "cen.InstanceAttachment" resource should depend on the related "vpc.Switch" resource.
        """
        return pulumi.get(self, 'cidr_block')

    @property
    @pulumi.getter(name='instanceId')
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, 'instance_id')

    @property
    @pulumi.getter(name='routeTableId')
    def route_table_id(self) -> pulumi.Output[str]:
        """
        The route table of the attached VBR or VPC.
        """
        return pulumi.get(self, 'route_table_id')
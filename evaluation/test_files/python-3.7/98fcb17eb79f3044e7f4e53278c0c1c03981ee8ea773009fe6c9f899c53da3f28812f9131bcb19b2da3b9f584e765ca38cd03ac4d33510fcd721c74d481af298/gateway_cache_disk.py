import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GatewayCacheDiskArgs', 'GatewayCacheDisk']

@pulumi.input_type
class GatewayCacheDiskArgs:

    def __init__(__self__, *, cache_disk_size_in_gb: pulumi.Input[int], gateway_id: pulumi.Input[str], cache_disk_category: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a GatewayCacheDisk resource.
        :param pulumi.Input[int] cache_disk_size_in_gb: size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        :param pulumi.Input[str] gateway_id: The ID of the gateway.
        :param pulumi.Input[str] cache_disk_category: The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        """
        pulumi.set(__self__, 'cache_disk_size_in_gb', cache_disk_size_in_gb)
        pulumi.set(__self__, 'gateway_id', gateway_id)
        if cache_disk_category is not None:
            pulumi.set(__self__, 'cache_disk_category', cache_disk_category)

    @property
    @pulumi.getter(name='cacheDiskSizeInGb')
    def cache_disk_size_in_gb(self) -> pulumi.Input[int]:
        """
        size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        """
        return pulumi.get(self, 'cache_disk_size_in_gb')

    @cache_disk_size_in_gb.setter
    def cache_disk_size_in_gb(self, value: pulumi.Input[int]):
        pulumi.set(self, 'cache_disk_size_in_gb', value)

    @property
    @pulumi.getter(name='gatewayId')
    def gateway_id(self) -> pulumi.Input[str]:
        """
        The ID of the gateway.
        """
        return pulumi.get(self, 'gateway_id')

    @gateway_id.setter
    def gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'gateway_id', value)

    @property
    @pulumi.getter(name='cacheDiskCategory')
    def cache_disk_category(self) -> Optional[pulumi.Input[str]]:
        """
        The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        """
        return pulumi.get(self, 'cache_disk_category')

    @cache_disk_category.setter
    def cache_disk_category(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cache_disk_category', value)

@pulumi.input_type
class _GatewayCacheDiskState:

    def __init__(__self__, *, cache_disk_category: Optional[pulumi.Input[str]]=None, cache_disk_size_in_gb: Optional[pulumi.Input[int]]=None, cache_id: Optional[pulumi.Input[str]]=None, gateway_id: Optional[pulumi.Input[str]]=None, local_file_path: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[int]]=None):
        """
        Input properties used for looking up and filtering GatewayCacheDisk resources.
        :param pulumi.Input[str] cache_disk_category: The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        :param pulumi.Input[int] cache_disk_size_in_gb: size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        :param pulumi.Input[str] cache_id: The ID of the cache.
        :param pulumi.Input[str] gateway_id: The ID of the gateway.
        :param pulumi.Input[str] local_file_path: The cache disk inside the device name.
        :param pulumi.Input[int] status: The status of the resource. Valid values: `0`, `1`, `2`. `0`: Normal. `1`: Is about to expire. `2`: Has expired.
        """
        if cache_disk_category is not None:
            pulumi.set(__self__, 'cache_disk_category', cache_disk_category)
        if cache_disk_size_in_gb is not None:
            pulumi.set(__self__, 'cache_disk_size_in_gb', cache_disk_size_in_gb)
        if cache_id is not None:
            pulumi.set(__self__, 'cache_id', cache_id)
        if gateway_id is not None:
            pulumi.set(__self__, 'gateway_id', gateway_id)
        if local_file_path is not None:
            pulumi.set(__self__, 'local_file_path', local_file_path)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter(name='cacheDiskCategory')
    def cache_disk_category(self) -> Optional[pulumi.Input[str]]:
        """
        The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        """
        return pulumi.get(self, 'cache_disk_category')

    @cache_disk_category.setter
    def cache_disk_category(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cache_disk_category', value)

    @property
    @pulumi.getter(name='cacheDiskSizeInGb')
    def cache_disk_size_in_gb(self) -> Optional[pulumi.Input[int]]:
        """
        size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        """
        return pulumi.get(self, 'cache_disk_size_in_gb')

    @cache_disk_size_in_gb.setter
    def cache_disk_size_in_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cache_disk_size_in_gb', value)

    @property
    @pulumi.getter(name='cacheId')
    def cache_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the cache.
        """
        return pulumi.get(self, 'cache_id')

    @cache_id.setter
    def cache_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cache_id', value)

    @property
    @pulumi.getter(name='gatewayId')
    def gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the gateway.
        """
        return pulumi.get(self, 'gateway_id')

    @gateway_id.setter
    def gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'gateway_id', value)

    @property
    @pulumi.getter(name='localFilePath')
    def local_file_path(self) -> Optional[pulumi.Input[str]]:
        """
        The cache disk inside the device name.
        """
        return pulumi.get(self, 'local_file_path')

    @local_file_path.setter
    def local_file_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'local_file_path', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[int]]:
        """
        The status of the resource. Valid values: `0`, `1`, `2`. `0`: Normal. `1`: Is about to expire. `2`: Has expired.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'status', value)

class GatewayCacheDisk(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cache_disk_category: Optional[pulumi.Input[str]]=None, cache_disk_size_in_gb: Optional[pulumi.Input[int]]=None, gateway_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Provides a Cloud Storage Gateway Gateway Cache Disk resource.

        For information about Cloud Storage Gateway Gateway Cache Disk and how to use it, see [What is Gateway Cache Disk](https://www.alibabacloud.com/help/zh/doc-detail/170294.htm).

        > **NOTE:** Available in v1.144.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_stocks = alicloud.cloudstoragegateway.get_stocks(gateway_class="Standard")
        vpc = alicloud.vpc.Network("vpc",
            vpc_name="example_value",
            cidr_block="172.16.0.0/12")
        example_switch = alicloud.vpc.Switch("exampleSwitch",
            vpc_id=vpc.id,
            cidr_block="172.16.0.0/21",
            zone_id=example_stocks.stocks[0].zone_id,
            vswitch_name="example_value")
        example_storage_bundle = alicloud.cloudstoragegateway.StorageBundle("exampleStorageBundle", storage_bundle_name="example_value")
        example_gateway = alicloud.cloudstoragegateway.Gateway("exampleGateway",
            description="tf-acctestDesalone",
            gateway_class="Standard",
            type="File",
            payment_type="PayAsYouGo",
            vswitch_id=example_switch.id,
            release_after_expiration=True,
            public_network_bandwidth=10,
            storage_bundle_id=example_storage_bundle.id,
            location="Cloud",
            gateway_name="example_value")
        example_gateway_cache_disk = alicloud.cloudstoragegateway.GatewayCacheDisk("exampleGatewayCacheDisk",
            cache_disk_category="cloud_efficiency",
            gateway_id=alicloud_cloud_storage_gateway_gateways["example"]["id"],
            cache_disk_size_in_gb=50)
        ```

        ## Import

        Cloud Storage Gateway Gateway Cache Disk can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudstoragegateway/gatewayCacheDisk:GatewayCacheDisk example <gateway_id>:<cache_id>:<local_file_path>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cache_disk_category: The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        :param pulumi.Input[int] cache_disk_size_in_gb: size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        :param pulumi.Input[str] gateway_id: The ID of the gateway.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: GatewayCacheDiskArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provides a Cloud Storage Gateway Gateway Cache Disk resource.

        For information about Cloud Storage Gateway Gateway Cache Disk and how to use it, see [What is Gateway Cache Disk](https://www.alibabacloud.com/help/zh/doc-detail/170294.htm).

        > **NOTE:** Available in v1.144.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example_stocks = alicloud.cloudstoragegateway.get_stocks(gateway_class="Standard")
        vpc = alicloud.vpc.Network("vpc",
            vpc_name="example_value",
            cidr_block="172.16.0.0/12")
        example_switch = alicloud.vpc.Switch("exampleSwitch",
            vpc_id=vpc.id,
            cidr_block="172.16.0.0/21",
            zone_id=example_stocks.stocks[0].zone_id,
            vswitch_name="example_value")
        example_storage_bundle = alicloud.cloudstoragegateway.StorageBundle("exampleStorageBundle", storage_bundle_name="example_value")
        example_gateway = alicloud.cloudstoragegateway.Gateway("exampleGateway",
            description="tf-acctestDesalone",
            gateway_class="Standard",
            type="File",
            payment_type="PayAsYouGo",
            vswitch_id=example_switch.id,
            release_after_expiration=True,
            public_network_bandwidth=10,
            storage_bundle_id=example_storage_bundle.id,
            location="Cloud",
            gateway_name="example_value")
        example_gateway_cache_disk = alicloud.cloudstoragegateway.GatewayCacheDisk("exampleGatewayCacheDisk",
            cache_disk_category="cloud_efficiency",
            gateway_id=alicloud_cloud_storage_gateway_gateways["example"]["id"],
            cache_disk_size_in_gb=50)
        ```

        ## Import

        Cloud Storage Gateway Gateway Cache Disk can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudstoragegateway/gatewayCacheDisk:GatewayCacheDisk example <gateway_id>:<cache_id>:<local_file_path>
        ```

        :param str resource_name: The name of the resource.
        :param GatewayCacheDiskArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(GatewayCacheDiskArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cache_disk_category: Optional[pulumi.Input[str]]=None, cache_disk_size_in_gb: Optional[pulumi.Input[int]]=None, gateway_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GatewayCacheDiskArgs.__new__(GatewayCacheDiskArgs)
            __props__.__dict__['cache_disk_category'] = cache_disk_category
            if cache_disk_size_in_gb is None and (not opts.urn):
                raise TypeError("Missing required property 'cache_disk_size_in_gb'")
            __props__.__dict__['cache_disk_size_in_gb'] = cache_disk_size_in_gb
            if gateway_id is None and (not opts.urn):
                raise TypeError("Missing required property 'gateway_id'")
            __props__.__dict__['gateway_id'] = gateway_id
            __props__.__dict__['cache_id'] = None
            __props__.__dict__['local_file_path'] = None
            __props__.__dict__['status'] = None
        super(GatewayCacheDisk, __self__).__init__('alicloud:cloudstoragegateway/gatewayCacheDisk:GatewayCacheDisk', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, cache_disk_category: Optional[pulumi.Input[str]]=None, cache_disk_size_in_gb: Optional[pulumi.Input[int]]=None, cache_id: Optional[pulumi.Input[str]]=None, gateway_id: Optional[pulumi.Input[str]]=None, local_file_path: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[int]]=None) -> 'GatewayCacheDisk':
        """
        Get an existing GatewayCacheDisk resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cache_disk_category: The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        :param pulumi.Input[int] cache_disk_size_in_gb: size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        :param pulumi.Input[str] cache_id: The ID of the cache.
        :param pulumi.Input[str] gateway_id: The ID of the gateway.
        :param pulumi.Input[str] local_file_path: The cache disk inside the device name.
        :param pulumi.Input[int] status: The status of the resource. Valid values: `0`, `1`, `2`. `0`: Normal. `1`: Is about to expire. `2`: Has expired.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _GatewayCacheDiskState.__new__(_GatewayCacheDiskState)
        __props__.__dict__['cache_disk_category'] = cache_disk_category
        __props__.__dict__['cache_disk_size_in_gb'] = cache_disk_size_in_gb
        __props__.__dict__['cache_id'] = cache_id
        __props__.__dict__['gateway_id'] = gateway_id
        __props__.__dict__['local_file_path'] = local_file_path
        __props__.__dict__['status'] = status
        return GatewayCacheDisk(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='cacheDiskCategory')
    def cache_disk_category(self) -> pulumi.Output[str]:
        """
        The cache disk type. Valid values: `cloud_efficiency`, `cloud_ssd`.
        """
        return pulumi.get(self, 'cache_disk_category')

    @property
    @pulumi.getter(name='cacheDiskSizeInGb')
    def cache_disk_size_in_gb(self) -> pulumi.Output[int]:
        """
        size of the cache disk. Unit: `GB`. The upper limit of the basic gateway cache disk is `1` TB (`1024` GB), that of the standard gateway is `2` TB (`2048` GB), and that of other gateway cache disks is `32` TB (`32768` GB). The lower limit for the file gateway cache disk capacity is `40` GB, and the lower limit for the block gateway cache disk capacity is `20` GB.
        """
        return pulumi.get(self, 'cache_disk_size_in_gb')

    @property
    @pulumi.getter(name='cacheId')
    def cache_id(self) -> pulumi.Output[str]:
        """
        The ID of the cache.
        """
        return pulumi.get(self, 'cache_id')

    @property
    @pulumi.getter(name='gatewayId')
    def gateway_id(self) -> pulumi.Output[str]:
        """
        The ID of the gateway.
        """
        return pulumi.get(self, 'gateway_id')

    @property
    @pulumi.getter(name='localFilePath')
    def local_file_path(self) -> pulumi.Output[str]:
        """
        The cache disk inside the device name.
        """
        return pulumi.get(self, 'local_file_path')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[int]:
        """
        The status of the resource. Valid values: `0`, `1`, `2`. `0`: Normal. `1`: Is about to expire. `2`: Has expired.
        """
        return pulumi.get(self, 'status')
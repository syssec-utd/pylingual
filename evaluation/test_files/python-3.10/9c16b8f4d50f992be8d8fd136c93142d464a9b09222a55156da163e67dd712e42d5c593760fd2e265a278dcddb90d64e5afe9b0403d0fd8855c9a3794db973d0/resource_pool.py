import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
__all__ = ['ResourcePoolArgs', 'ResourcePool']

@pulumi.input_type
class ResourcePoolArgs:

    def __init__(__self__, *, parent_resource_pool_id: pulumi.Input[str], cpu_expandable: Optional[pulumi.Input[bool]]=None, cpu_limit: Optional[pulumi.Input[int]]=None, cpu_reservation: Optional[pulumi.Input[int]]=None, cpu_share_level: Optional[pulumi.Input[str]]=None, cpu_shares: Optional[pulumi.Input[int]]=None, custom_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, memory_expandable: Optional[pulumi.Input[bool]]=None, memory_limit: Optional[pulumi.Input[int]]=None, memory_reservation: Optional[pulumi.Input[int]]=None, memory_share_level: Optional[pulumi.Input[str]]=None, memory_shares: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, scale_descendants_shares: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a ResourcePool resource.
        :param pulumi.Input[str] parent_resource_pool_id: The managed object ID
               of the parent resource pool. This can be the root resource pool for a cluster
               or standalone host, or a resource pool itself. When moving a resource pool
               from one parent resource pool to another, both must share a common root
               resource pool.
        :param pulumi.Input[bool] cpu_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] cpu_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] cpu_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] cpu_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `cpu_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] cpu_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `cpu_share_level` must be `custom`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_attributes: A list of custom attributes to set on this resource.
        :param pulumi.Input[bool] memory_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] memory_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] memory_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] memory_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `memory_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] memory_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `memory_share_level` must be `custom`.
        :param pulumi.Input[str] name: The name of the resource pool.
        :param pulumi.Input[str] scale_descendants_shares: Determines if the shares of all
               descendants of the resource pool are scaled up or down when the shares
               of the resource pool are scaled up or down. Can be one of `disabled` or
               `scaleCpuAndMemoryShares`. Default: `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The IDs of any tags to attach to this resource.
        """
        pulumi.set(__self__, 'parent_resource_pool_id', parent_resource_pool_id)
        if cpu_expandable is not None:
            pulumi.set(__self__, 'cpu_expandable', cpu_expandable)
        if cpu_limit is not None:
            pulumi.set(__self__, 'cpu_limit', cpu_limit)
        if cpu_reservation is not None:
            pulumi.set(__self__, 'cpu_reservation', cpu_reservation)
        if cpu_share_level is not None:
            pulumi.set(__self__, 'cpu_share_level', cpu_share_level)
        if cpu_shares is not None:
            pulumi.set(__self__, 'cpu_shares', cpu_shares)
        if custom_attributes is not None:
            pulumi.set(__self__, 'custom_attributes', custom_attributes)
        if memory_expandable is not None:
            pulumi.set(__self__, 'memory_expandable', memory_expandable)
        if memory_limit is not None:
            pulumi.set(__self__, 'memory_limit', memory_limit)
        if memory_reservation is not None:
            pulumi.set(__self__, 'memory_reservation', memory_reservation)
        if memory_share_level is not None:
            pulumi.set(__self__, 'memory_share_level', memory_share_level)
        if memory_shares is not None:
            pulumi.set(__self__, 'memory_shares', memory_shares)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if scale_descendants_shares is not None:
            pulumi.set(__self__, 'scale_descendants_shares', scale_descendants_shares)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='parentResourcePoolId')
    def parent_resource_pool_id(self) -> pulumi.Input[str]:
        """
        The managed object ID
        of the parent resource pool. This can be the root resource pool for a cluster
        or standalone host, or a resource pool itself. When moving a resource pool
        from one parent resource pool to another, both must share a common root
        resource pool.
        """
        return pulumi.get(self, 'parent_resource_pool_id')

    @parent_resource_pool_id.setter
    def parent_resource_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'parent_resource_pool_id', value)

    @property
    @pulumi.getter(name='cpuExpandable')
    def cpu_expandable(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'cpu_expandable')

    @cpu_expandable.setter
    def cpu_expandable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'cpu_expandable', value)

    @property
    @pulumi.getter(name='cpuLimit')
    def cpu_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'cpu_limit')

    @cpu_limit.setter
    def cpu_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_limit', value)

    @property
    @pulumi.getter(name='cpuReservation')
    def cpu_reservation(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'cpu_reservation')

    @cpu_reservation.setter
    def cpu_reservation(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_reservation', value)

    @property
    @pulumi.getter(name='cpuShareLevel')
    def cpu_share_level(self) -> Optional[pulumi.Input[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `cpu_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'cpu_share_level')

    @cpu_share_level.setter
    def cpu_share_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cpu_share_level', value)

    @property
    @pulumi.getter(name='cpuShares')
    def cpu_shares(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `cpu_share_level` must be `custom`.
        """
        return pulumi.get(self, 'cpu_shares')

    @cpu_shares.setter
    def cpu_shares(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_shares', value)

    @property
    @pulumi.getter(name='customAttributes')
    def custom_attributes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A list of custom attributes to set on this resource.
        """
        return pulumi.get(self, 'custom_attributes')

    @custom_attributes.setter
    def custom_attributes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'custom_attributes', value)

    @property
    @pulumi.getter(name='memoryExpandable')
    def memory_expandable(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'memory_expandable')

    @memory_expandable.setter
    def memory_expandable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'memory_expandable', value)

    @property
    @pulumi.getter(name='memoryLimit')
    def memory_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'memory_limit')

    @memory_limit.setter
    def memory_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_limit', value)

    @property
    @pulumi.getter(name='memoryReservation')
    def memory_reservation(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'memory_reservation')

    @memory_reservation.setter
    def memory_reservation(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_reservation', value)

    @property
    @pulumi.getter(name='memoryShareLevel')
    def memory_share_level(self) -> Optional[pulumi.Input[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `memory_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'memory_share_level')

    @memory_share_level.setter
    def memory_share_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'memory_share_level', value)

    @property
    @pulumi.getter(name='memoryShares')
    def memory_shares(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `memory_share_level` must be `custom`.
        """
        return pulumi.get(self, 'memory_shares')

    @memory_shares.setter
    def memory_shares(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_shares', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource pool.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='scaleDescendantsShares')
    def scale_descendants_shares(self) -> Optional[pulumi.Input[str]]:
        """
        Determines if the shares of all
        descendants of the resource pool are scaled up or down when the shares
        of the resource pool are scaled up or down. Can be one of `disabled` or
        `scaleCpuAndMemoryShares`. Default: `disabled`.
        """
        return pulumi.get(self, 'scale_descendants_shares')

    @scale_descendants_shares.setter
    def scale_descendants_shares(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'scale_descendants_shares', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IDs of any tags to attach to this resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

@pulumi.input_type
class _ResourcePoolState:

    def __init__(__self__, *, cpu_expandable: Optional[pulumi.Input[bool]]=None, cpu_limit: Optional[pulumi.Input[int]]=None, cpu_reservation: Optional[pulumi.Input[int]]=None, cpu_share_level: Optional[pulumi.Input[str]]=None, cpu_shares: Optional[pulumi.Input[int]]=None, custom_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, memory_expandable: Optional[pulumi.Input[bool]]=None, memory_limit: Optional[pulumi.Input[int]]=None, memory_reservation: Optional[pulumi.Input[int]]=None, memory_share_level: Optional[pulumi.Input[str]]=None, memory_shares: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, parent_resource_pool_id: Optional[pulumi.Input[str]]=None, scale_descendants_shares: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        Input properties used for looking up and filtering ResourcePool resources.
        :param pulumi.Input[bool] cpu_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] cpu_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] cpu_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] cpu_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `cpu_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] cpu_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `cpu_share_level` must be `custom`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_attributes: A list of custom attributes to set on this resource.
        :param pulumi.Input[bool] memory_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] memory_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] memory_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] memory_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `memory_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] memory_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `memory_share_level` must be `custom`.
        :param pulumi.Input[str] name: The name of the resource pool.
        :param pulumi.Input[str] parent_resource_pool_id: The managed object ID
               of the parent resource pool. This can be the root resource pool for a cluster
               or standalone host, or a resource pool itself. When moving a resource pool
               from one parent resource pool to another, both must share a common root
               resource pool.
        :param pulumi.Input[str] scale_descendants_shares: Determines if the shares of all
               descendants of the resource pool are scaled up or down when the shares
               of the resource pool are scaled up or down. Can be one of `disabled` or
               `scaleCpuAndMemoryShares`. Default: `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The IDs of any tags to attach to this resource.
        """
        if cpu_expandable is not None:
            pulumi.set(__self__, 'cpu_expandable', cpu_expandable)
        if cpu_limit is not None:
            pulumi.set(__self__, 'cpu_limit', cpu_limit)
        if cpu_reservation is not None:
            pulumi.set(__self__, 'cpu_reservation', cpu_reservation)
        if cpu_share_level is not None:
            pulumi.set(__self__, 'cpu_share_level', cpu_share_level)
        if cpu_shares is not None:
            pulumi.set(__self__, 'cpu_shares', cpu_shares)
        if custom_attributes is not None:
            pulumi.set(__self__, 'custom_attributes', custom_attributes)
        if memory_expandable is not None:
            pulumi.set(__self__, 'memory_expandable', memory_expandable)
        if memory_limit is not None:
            pulumi.set(__self__, 'memory_limit', memory_limit)
        if memory_reservation is not None:
            pulumi.set(__self__, 'memory_reservation', memory_reservation)
        if memory_share_level is not None:
            pulumi.set(__self__, 'memory_share_level', memory_share_level)
        if memory_shares is not None:
            pulumi.set(__self__, 'memory_shares', memory_shares)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if parent_resource_pool_id is not None:
            pulumi.set(__self__, 'parent_resource_pool_id', parent_resource_pool_id)
        if scale_descendants_shares is not None:
            pulumi.set(__self__, 'scale_descendants_shares', scale_descendants_shares)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='cpuExpandable')
    def cpu_expandable(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'cpu_expandable')

    @cpu_expandable.setter
    def cpu_expandable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'cpu_expandable', value)

    @property
    @pulumi.getter(name='cpuLimit')
    def cpu_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'cpu_limit')

    @cpu_limit.setter
    def cpu_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_limit', value)

    @property
    @pulumi.getter(name='cpuReservation')
    def cpu_reservation(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'cpu_reservation')

    @cpu_reservation.setter
    def cpu_reservation(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_reservation', value)

    @property
    @pulumi.getter(name='cpuShareLevel')
    def cpu_share_level(self) -> Optional[pulumi.Input[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `cpu_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'cpu_share_level')

    @cpu_share_level.setter
    def cpu_share_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'cpu_share_level', value)

    @property
    @pulumi.getter(name='cpuShares')
    def cpu_shares(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `cpu_share_level` must be `custom`.
        """
        return pulumi.get(self, 'cpu_shares')

    @cpu_shares.setter
    def cpu_shares(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'cpu_shares', value)

    @property
    @pulumi.getter(name='customAttributes')
    def custom_attributes(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A list of custom attributes to set on this resource.
        """
        return pulumi.get(self, 'custom_attributes')

    @custom_attributes.setter
    def custom_attributes(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'custom_attributes', value)

    @property
    @pulumi.getter(name='memoryExpandable')
    def memory_expandable(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'memory_expandable')

    @memory_expandable.setter
    def memory_expandable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'memory_expandable', value)

    @property
    @pulumi.getter(name='memoryLimit')
    def memory_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'memory_limit')

    @memory_limit.setter
    def memory_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_limit', value)

    @property
    @pulumi.getter(name='memoryReservation')
    def memory_reservation(self) -> Optional[pulumi.Input[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'memory_reservation')

    @memory_reservation.setter
    def memory_reservation(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_reservation', value)

    @property
    @pulumi.getter(name='memoryShareLevel')
    def memory_share_level(self) -> Optional[pulumi.Input[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `memory_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'memory_share_level')

    @memory_share_level.setter
    def memory_share_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'memory_share_level', value)

    @property
    @pulumi.getter(name='memoryShares')
    def memory_shares(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `memory_share_level` must be `custom`.
        """
        return pulumi.get(self, 'memory_shares')

    @memory_shares.setter
    def memory_shares(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'memory_shares', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource pool.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='parentResourcePoolId')
    def parent_resource_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The managed object ID
        of the parent resource pool. This can be the root resource pool for a cluster
        or standalone host, or a resource pool itself. When moving a resource pool
        from one parent resource pool to another, both must share a common root
        resource pool.
        """
        return pulumi.get(self, 'parent_resource_pool_id')

    @parent_resource_pool_id.setter
    def parent_resource_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'parent_resource_pool_id', value)

    @property
    @pulumi.getter(name='scaleDescendantsShares')
    def scale_descendants_shares(self) -> Optional[pulumi.Input[str]]:
        """
        Determines if the shares of all
        descendants of the resource pool are scaled up or down when the shares
        of the resource pool are scaled up or down. Can be one of `disabled` or
        `scaleCpuAndMemoryShares`. Default: `disabled`.
        """
        return pulumi.get(self, 'scale_descendants_shares')

    @scale_descendants_shares.setter
    def scale_descendants_shares(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'scale_descendants_shares', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IDs of any tags to attach to this resource.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class ResourcePool(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cpu_expandable: Optional[pulumi.Input[bool]]=None, cpu_limit: Optional[pulumi.Input[int]]=None, cpu_reservation: Optional[pulumi.Input[int]]=None, cpu_share_level: Optional[pulumi.Input[str]]=None, cpu_shares: Optional[pulumi.Input[int]]=None, custom_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, memory_expandable: Optional[pulumi.Input[bool]]=None, memory_limit: Optional[pulumi.Input[int]]=None, memory_reservation: Optional[pulumi.Input[int]]=None, memory_share_level: Optional[pulumi.Input[str]]=None, memory_shares: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, parent_resource_pool_id: Optional[pulumi.Input[str]]=None, scale_descendants_shares: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        """
        The `ResourcePool` resource can be used to create and manage
        resource pools on DRS-enabled vSphere clusters or standalone ESXi hosts.

        For more information on vSphere resource pools, please refer to the
        [product documentation][ref-vsphere-resource_pools].

        [ref-vsphere-resource_pools]: https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.resmgmt.doc/GUID-60077B40-66FF-4625-934A-641703ED7601.html

        ## Example Usage

        The following example sets up a resource pool in an existing compute cluster
        with the default settings for CPU and memory reservations, shares, and limits.

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        datacenter = vsphere.get_datacenter(name="dc-01")
        compute_cluster = vsphere.get_compute_cluster(name="cluster-01",
            datacenter_id=datacenter.id)
        resource_pool = vsphere.ResourcePool("resourcePool", parent_resource_pool_id=compute_cluster.resource_pool_id)
        ```

        A virtual machine resource could be targeted to use the default resource pool
        of the cluster using the following:

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        vm = vsphere.VirtualMachine("vm", resource_pool_id=data["vsphere_compute_cluster"]["cluster"]["resource_pool_id"])
        # ... other configuration ...
        ```

        The following example sets up a parent resource pool in an existing compute cluster
        with a child resource pool nested below. Each resource pool is configured with
        the default settings for CPU and memory reservations, shares, and limits.

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        datacenter = vsphere.get_datacenter(name="dc-01")
        compute_cluster = vsphere.get_compute_cluster(name="cluster-01",
            datacenter_id=datacenter.id)
        resource_pool_parent = vsphere.ResourcePool("resourcePoolParent", parent_resource_pool_id=compute_cluster.resource_pool_id)
        resource_pool_child = vsphere.ResourcePool("resourcePoolChild", parent_resource_pool_id=resource_pool_parent.id)
        ```
        ## Importing
        ### Settings that Require vSphere 7.0 or higher

        These settings require vSphere 7.0 or higher:

        * `scale_descendants_shares`

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cpu_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] cpu_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] cpu_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] cpu_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `cpu_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] cpu_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `cpu_share_level` must be `custom`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_attributes: A list of custom attributes to set on this resource.
        :param pulumi.Input[bool] memory_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] memory_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] memory_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] memory_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `memory_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] memory_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `memory_share_level` must be `custom`.
        :param pulumi.Input[str] name: The name of the resource pool.
        :param pulumi.Input[str] parent_resource_pool_id: The managed object ID
               of the parent resource pool. This can be the root resource pool for a cluster
               or standalone host, or a resource pool itself. When moving a resource pool
               from one parent resource pool to another, both must share a common root
               resource pool.
        :param pulumi.Input[str] scale_descendants_shares: Determines if the shares of all
               descendants of the resource pool are scaled up or down when the shares
               of the resource pool are scaled up or down. Can be one of `disabled` or
               `scaleCpuAndMemoryShares`. Default: `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The IDs of any tags to attach to this resource.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ResourcePoolArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The `ResourcePool` resource can be used to create and manage
        resource pools on DRS-enabled vSphere clusters or standalone ESXi hosts.

        For more information on vSphere resource pools, please refer to the
        [product documentation][ref-vsphere-resource_pools].

        [ref-vsphere-resource_pools]: https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.resmgmt.doc/GUID-60077B40-66FF-4625-934A-641703ED7601.html

        ## Example Usage

        The following example sets up a resource pool in an existing compute cluster
        with the default settings for CPU and memory reservations, shares, and limits.

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        datacenter = vsphere.get_datacenter(name="dc-01")
        compute_cluster = vsphere.get_compute_cluster(name="cluster-01",
            datacenter_id=datacenter.id)
        resource_pool = vsphere.ResourcePool("resourcePool", parent_resource_pool_id=compute_cluster.resource_pool_id)
        ```

        A virtual machine resource could be targeted to use the default resource pool
        of the cluster using the following:

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        vm = vsphere.VirtualMachine("vm", resource_pool_id=data["vsphere_compute_cluster"]["cluster"]["resource_pool_id"])
        # ... other configuration ...
        ```

        The following example sets up a parent resource pool in an existing compute cluster
        with a child resource pool nested below. Each resource pool is configured with
        the default settings for CPU and memory reservations, shares, and limits.

        ```python
        import pulumi
        import pulumi_vsphere as vsphere

        datacenter = vsphere.get_datacenter(name="dc-01")
        compute_cluster = vsphere.get_compute_cluster(name="cluster-01",
            datacenter_id=datacenter.id)
        resource_pool_parent = vsphere.ResourcePool("resourcePoolParent", parent_resource_pool_id=compute_cluster.resource_pool_id)
        resource_pool_child = vsphere.ResourcePool("resourcePoolChild", parent_resource_pool_id=resource_pool_parent.id)
        ```
        ## Importing
        ### Settings that Require vSphere 7.0 or higher

        These settings require vSphere 7.0 or higher:

        * `scale_descendants_shares`

        :param str resource_name: The name of the resource.
        :param ResourcePoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ResourcePoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, cpu_expandable: Optional[pulumi.Input[bool]]=None, cpu_limit: Optional[pulumi.Input[int]]=None, cpu_reservation: Optional[pulumi.Input[int]]=None, cpu_share_level: Optional[pulumi.Input[str]]=None, cpu_shares: Optional[pulumi.Input[int]]=None, custom_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, memory_expandable: Optional[pulumi.Input[bool]]=None, memory_limit: Optional[pulumi.Input[int]]=None, memory_reservation: Optional[pulumi.Input[int]]=None, memory_share_level: Optional[pulumi.Input[str]]=None, memory_shares: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, parent_resource_pool_id: Optional[pulumi.Input[str]]=None, scale_descendants_shares: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourcePoolArgs.__new__(ResourcePoolArgs)
            __props__.__dict__['cpu_expandable'] = cpu_expandable
            __props__.__dict__['cpu_limit'] = cpu_limit
            __props__.__dict__['cpu_reservation'] = cpu_reservation
            __props__.__dict__['cpu_share_level'] = cpu_share_level
            __props__.__dict__['cpu_shares'] = cpu_shares
            __props__.__dict__['custom_attributes'] = custom_attributes
            __props__.__dict__['memory_expandable'] = memory_expandable
            __props__.__dict__['memory_limit'] = memory_limit
            __props__.__dict__['memory_reservation'] = memory_reservation
            __props__.__dict__['memory_share_level'] = memory_share_level
            __props__.__dict__['memory_shares'] = memory_shares
            __props__.__dict__['name'] = name
            if parent_resource_pool_id is None and (not opts.urn):
                raise TypeError("Missing required property 'parent_resource_pool_id'")
            __props__.__dict__['parent_resource_pool_id'] = parent_resource_pool_id
            __props__.__dict__['scale_descendants_shares'] = scale_descendants_shares
            __props__.__dict__['tags'] = tags
        super(ResourcePool, __self__).__init__('vsphere:index/resourcePool:ResourcePool', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, cpu_expandable: Optional[pulumi.Input[bool]]=None, cpu_limit: Optional[pulumi.Input[int]]=None, cpu_reservation: Optional[pulumi.Input[int]]=None, cpu_share_level: Optional[pulumi.Input[str]]=None, cpu_shares: Optional[pulumi.Input[int]]=None, custom_attributes: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, memory_expandable: Optional[pulumi.Input[bool]]=None, memory_limit: Optional[pulumi.Input[int]]=None, memory_reservation: Optional[pulumi.Input[int]]=None, memory_share_level: Optional[pulumi.Input[str]]=None, memory_shares: Optional[pulumi.Input[int]]=None, name: Optional[pulumi.Input[str]]=None, parent_resource_pool_id: Optional[pulumi.Input[str]]=None, scale_descendants_shares: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None) -> 'ResourcePool':
        """
        Get an existing ResourcePool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cpu_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] cpu_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] cpu_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] cpu_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `cpu_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] cpu_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `cpu_share_level` must be `custom`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_attributes: A list of custom attributes to set on this resource.
        :param pulumi.Input[bool] memory_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] memory_limit: The CPU utilization of a resource pool will not
               exceed this limit, even if there are available resources. Set to `-1` for
               unlimited. Default: `-1`
        :param pulumi.Input[int] memory_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] memory_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `memory_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] memory_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `memory_share_level` must be `custom`.
        :param pulumi.Input[str] name: The name of the resource pool.
        :param pulumi.Input[str] parent_resource_pool_id: The managed object ID
               of the parent resource pool. This can be the root resource pool for a cluster
               or standalone host, or a resource pool itself. When moving a resource pool
               from one parent resource pool to another, both must share a common root
               resource pool.
        :param pulumi.Input[str] scale_descendants_shares: Determines if the shares of all
               descendants of the resource pool are scaled up or down when the shares
               of the resource pool are scaled up or down. Can be one of `disabled` or
               `scaleCpuAndMemoryShares`. Default: `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: The IDs of any tags to attach to this resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ResourcePoolState.__new__(_ResourcePoolState)
        __props__.__dict__['cpu_expandable'] = cpu_expandable
        __props__.__dict__['cpu_limit'] = cpu_limit
        __props__.__dict__['cpu_reservation'] = cpu_reservation
        __props__.__dict__['cpu_share_level'] = cpu_share_level
        __props__.__dict__['cpu_shares'] = cpu_shares
        __props__.__dict__['custom_attributes'] = custom_attributes
        __props__.__dict__['memory_expandable'] = memory_expandable
        __props__.__dict__['memory_limit'] = memory_limit
        __props__.__dict__['memory_reservation'] = memory_reservation
        __props__.__dict__['memory_share_level'] = memory_share_level
        __props__.__dict__['memory_shares'] = memory_shares
        __props__.__dict__['name'] = name
        __props__.__dict__['parent_resource_pool_id'] = parent_resource_pool_id
        __props__.__dict__['scale_descendants_shares'] = scale_descendants_shares
        __props__.__dict__['tags'] = tags
        return ResourcePool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='cpuExpandable')
    def cpu_expandable(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'cpu_expandable')

    @property
    @pulumi.getter(name='cpuLimit')
    def cpu_limit(self) -> pulumi.Output[Optional[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'cpu_limit')

    @property
    @pulumi.getter(name='cpuReservation')
    def cpu_reservation(self) -> pulumi.Output[Optional[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'cpu_reservation')

    @property
    @pulumi.getter(name='cpuShareLevel')
    def cpu_share_level(self) -> pulumi.Output[Optional[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `cpu_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'cpu_share_level')

    @property
    @pulumi.getter(name='cpuShares')
    def cpu_shares(self) -> pulumi.Output[int]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `cpu_share_level` must be `custom`.
        """
        return pulumi.get(self, 'cpu_shares')

    @property
    @pulumi.getter(name='customAttributes')
    def custom_attributes(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A list of custom attributes to set on this resource.
        """
        return pulumi.get(self, 'custom_attributes')

    @property
    @pulumi.getter(name='memoryExpandable')
    def memory_expandable(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines if the reservation on a resource
        pool can grow beyond the specified value if the parent resource pool has
        unreserved resources. Default: `true`
        """
        return pulumi.get(self, 'memory_expandable')

    @property
    @pulumi.getter(name='memoryLimit')
    def memory_limit(self) -> pulumi.Output[Optional[int]]:
        """
        The CPU utilization of a resource pool will not
        exceed this limit, even if there are available resources. Set to `-1` for
        unlimited. Default: `-1`
        """
        return pulumi.get(self, 'memory_limit')

    @property
    @pulumi.getter(name='memoryReservation')
    def memory_reservation(self) -> pulumi.Output[Optional[int]]:
        """
        Amount of CPU (MHz) that is guaranteed
        available to the resource pool. Default: `0`
        """
        return pulumi.get(self, 'memory_reservation')

    @property
    @pulumi.getter(name='memoryShareLevel')
    def memory_share_level(self) -> pulumi.Output[Optional[str]]:
        """
        The CPU allocation level. The level is a
        simplified view of shares. Levels map to a pre-determined set of numeric
        values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
        `low`, `normal`, or `high` are specified values in `memory_shares` will be
        ignored.  Default: `normal`
        """
        return pulumi.get(self, 'memory_share_level')

    @property
    @pulumi.getter(name='memoryShares')
    def memory_shares(self) -> pulumi.Output[int]:
        """
        The number of shares allocated for CPU. Used to
        determine resource allocation in case of resource contention. If this is set,
        `memory_share_level` must be `custom`.
        """
        return pulumi.get(self, 'memory_shares')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource pool.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='parentResourcePoolId')
    def parent_resource_pool_id(self) -> pulumi.Output[str]:
        """
        The managed object ID
        of the parent resource pool. This can be the root resource pool for a cluster
        or standalone host, or a resource pool itself. When moving a resource pool
        from one parent resource pool to another, both must share a common root
        resource pool.
        """
        return pulumi.get(self, 'parent_resource_pool_id')

    @property
    @pulumi.getter(name='scaleDescendantsShares')
    def scale_descendants_shares(self) -> pulumi.Output[Optional[str]]:
        """
        Determines if the shares of all
        descendants of the resource pool are scaled up or down when the shares
        of the resource pool are scaled up or down. Can be one of `disabled` or
        `scaleCpuAndMemoryShares`. Default: `disabled`.
        """
        return pulumi.get(self, 'scale_descendants_shares')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The IDs of any tags to attach to this resource.
        """
        return pulumi.get(self, 'tags')
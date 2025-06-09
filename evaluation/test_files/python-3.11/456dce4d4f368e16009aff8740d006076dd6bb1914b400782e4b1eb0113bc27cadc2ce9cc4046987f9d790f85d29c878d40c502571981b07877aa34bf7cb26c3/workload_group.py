import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['WorkloadGroupArgs', 'WorkloadGroup']

@pulumi.input_type
class WorkloadGroupArgs:

    def __init__(__self__, *, database_name: pulumi.Input[str], max_resource_percent: pulumi.Input[int], min_resource_percent: pulumi.Input[int], min_resource_percent_per_request: pulumi.Input[float], resource_group_name: pulumi.Input[str], server_name: pulumi.Input[str], importance: Optional[pulumi.Input[str]]=None, max_resource_percent_per_request: Optional[pulumi.Input[float]]=None, query_execution_timeout: Optional[pulumi.Input[int]]=None, workload_group_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a WorkloadGroup resource.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[int] max_resource_percent: The workload group cap percentage resource.
        :param pulumi.Input[int] min_resource_percent: The workload group minimum percentage resource.
        :param pulumi.Input[float] min_resource_percent_per_request: The workload group request minimum grant percentage.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] importance: The workload group importance level.
        :param pulumi.Input[float] max_resource_percent_per_request: The workload group request maximum grant percentage.
        :param pulumi.Input[int] query_execution_timeout: The workload group query execution timeout.
        :param pulumi.Input[str] workload_group_name: The name of the workload group.
        """
        pulumi.set(__self__, 'database_name', database_name)
        pulumi.set(__self__, 'max_resource_percent', max_resource_percent)
        pulumi.set(__self__, 'min_resource_percent', min_resource_percent)
        pulumi.set(__self__, 'min_resource_percent_per_request', min_resource_percent_per_request)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'server_name', server_name)
        if importance is not None:
            pulumi.set(__self__, 'importance', importance)
        if max_resource_percent_per_request is not None:
            pulumi.set(__self__, 'max_resource_percent_per_request', max_resource_percent_per_request)
        if query_execution_timeout is not None:
            pulumi.set(__self__, 'query_execution_timeout', query_execution_timeout)
        if workload_group_name is not None:
            pulumi.set(__self__, 'workload_group_name', workload_group_name)

    @property
    @pulumi.getter(name='databaseName')
    def database_name(self) -> pulumi.Input[str]:
        """
        The name of the database.
        """
        return pulumi.get(self, 'database_name')

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'database_name', value)

    @property
    @pulumi.getter(name='maxResourcePercent')
    def max_resource_percent(self) -> pulumi.Input[int]:
        """
        The workload group cap percentage resource.
        """
        return pulumi.get(self, 'max_resource_percent')

    @max_resource_percent.setter
    def max_resource_percent(self, value: pulumi.Input[int]):
        pulumi.set(self, 'max_resource_percent', value)

    @property
    @pulumi.getter(name='minResourcePercent')
    def min_resource_percent(self) -> pulumi.Input[int]:
        """
        The workload group minimum percentage resource.
        """
        return pulumi.get(self, 'min_resource_percent')

    @min_resource_percent.setter
    def min_resource_percent(self, value: pulumi.Input[int]):
        pulumi.set(self, 'min_resource_percent', value)

    @property
    @pulumi.getter(name='minResourcePercentPerRequest')
    def min_resource_percent_per_request(self) -> pulumi.Input[float]:
        """
        The workload group request minimum grant percentage.
        """
        return pulumi.get(self, 'min_resource_percent_per_request')

    @min_resource_percent_per_request.setter
    def min_resource_percent_per_request(self, value: pulumi.Input[float]):
        pulumi.set(self, 'min_resource_percent_per_request', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='serverName')
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, 'server_name')

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'server_name', value)

    @property
    @pulumi.getter
    def importance(self) -> Optional[pulumi.Input[str]]:
        """
        The workload group importance level.
        """
        return pulumi.get(self, 'importance')

    @importance.setter
    def importance(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'importance', value)

    @property
    @pulumi.getter(name='maxResourcePercentPerRequest')
    def max_resource_percent_per_request(self) -> Optional[pulumi.Input[float]]:
        """
        The workload group request maximum grant percentage.
        """
        return pulumi.get(self, 'max_resource_percent_per_request')

    @max_resource_percent_per_request.setter
    def max_resource_percent_per_request(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, 'max_resource_percent_per_request', value)

    @property
    @pulumi.getter(name='queryExecutionTimeout')
    def query_execution_timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The workload group query execution timeout.
        """
        return pulumi.get(self, 'query_execution_timeout')

    @query_execution_timeout.setter
    def query_execution_timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'query_execution_timeout', value)

    @property
    @pulumi.getter(name='workloadGroupName')
    def workload_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the workload group.
        """
        return pulumi.get(self, 'workload_group_name')

    @workload_group_name.setter
    def workload_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'workload_group_name', value)

class WorkloadGroup(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, database_name: Optional[pulumi.Input[str]]=None, importance: Optional[pulumi.Input[str]]=None, max_resource_percent: Optional[pulumi.Input[int]]=None, max_resource_percent_per_request: Optional[pulumi.Input[float]]=None, min_resource_percent: Optional[pulumi.Input[int]]=None, min_resource_percent_per_request: Optional[pulumi.Input[float]]=None, query_execution_timeout: Optional[pulumi.Input[int]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, workload_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Workload group operations for a data warehouse

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] importance: The workload group importance level.
        :param pulumi.Input[int] max_resource_percent: The workload group cap percentage resource.
        :param pulumi.Input[float] max_resource_percent_per_request: The workload group request maximum grant percentage.
        :param pulumi.Input[int] min_resource_percent: The workload group minimum percentage resource.
        :param pulumi.Input[float] min_resource_percent_per_request: The workload group request minimum grant percentage.
        :param pulumi.Input[int] query_execution_timeout: The workload group query execution timeout.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] workload_group_name: The name of the workload group.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WorkloadGroupArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Workload group operations for a data warehouse

        :param str resource_name: The name of the resource.
        :param WorkloadGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkloadGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, database_name: Optional[pulumi.Input[str]]=None, importance: Optional[pulumi.Input[str]]=None, max_resource_percent: Optional[pulumi.Input[int]]=None, max_resource_percent_per_request: Optional[pulumi.Input[float]]=None, min_resource_percent: Optional[pulumi.Input[int]]=None, min_resource_percent_per_request: Optional[pulumi.Input[float]]=None, query_execution_timeout: Optional[pulumi.Input[int]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_name: Optional[pulumi.Input[str]]=None, workload_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkloadGroupArgs.__new__(WorkloadGroupArgs)
            if database_name is None and (not opts.urn):
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__['database_name'] = database_name
            __props__.__dict__['importance'] = importance
            if max_resource_percent is None and (not opts.urn):
                raise TypeError("Missing required property 'max_resource_percent'")
            __props__.__dict__['max_resource_percent'] = max_resource_percent
            __props__.__dict__['max_resource_percent_per_request'] = max_resource_percent_per_request
            if min_resource_percent is None and (not opts.urn):
                raise TypeError("Missing required property 'min_resource_percent'")
            __props__.__dict__['min_resource_percent'] = min_resource_percent
            if min_resource_percent_per_request is None and (not opts.urn):
                raise TypeError("Missing required property 'min_resource_percent_per_request'")
            __props__.__dict__['min_resource_percent_per_request'] = min_resource_percent_per_request
            __props__.__dict__['query_execution_timeout'] = query_execution_timeout
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if server_name is None and (not opts.urn):
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__['server_name'] = server_name
            __props__.__dict__['workload_group_name'] = workload_group_name
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:sql:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20190601preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20200801preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20201101preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20210201preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20210501preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20210801preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20211101:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20211101preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20220201preview:WorkloadGroup'), pulumi.Alias(type_='azure-native:sql/v20220501preview:WorkloadGroup')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WorkloadGroup, __self__).__init__('azure-native:sql/v20200202preview:WorkloadGroup', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'WorkloadGroup':
        """
        Get an existing WorkloadGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = WorkloadGroupArgs.__new__(WorkloadGroupArgs)
        __props__.__dict__['importance'] = None
        __props__.__dict__['max_resource_percent'] = None
        __props__.__dict__['max_resource_percent_per_request'] = None
        __props__.__dict__['min_resource_percent'] = None
        __props__.__dict__['min_resource_percent_per_request'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['query_execution_timeout'] = None
        __props__.__dict__['type'] = None
        return WorkloadGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def importance(self) -> pulumi.Output[Optional[str]]:
        """
        The workload group importance level.
        """
        return pulumi.get(self, 'importance')

    @property
    @pulumi.getter(name='maxResourcePercent')
    def max_resource_percent(self) -> pulumi.Output[int]:
        """
        The workload group cap percentage resource.
        """
        return pulumi.get(self, 'max_resource_percent')

    @property
    @pulumi.getter(name='maxResourcePercentPerRequest')
    def max_resource_percent_per_request(self) -> pulumi.Output[Optional[float]]:
        """
        The workload group request maximum grant percentage.
        """
        return pulumi.get(self, 'max_resource_percent_per_request')

    @property
    @pulumi.getter(name='minResourcePercent')
    def min_resource_percent(self) -> pulumi.Output[int]:
        """
        The workload group minimum percentage resource.
        """
        return pulumi.get(self, 'min_resource_percent')

    @property
    @pulumi.getter(name='minResourcePercentPerRequest')
    def min_resource_percent_per_request(self) -> pulumi.Output[float]:
        """
        The workload group request minimum grant percentage.
        """
        return pulumi.get(self, 'min_resource_percent_per_request')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='queryExecutionTimeout')
    def query_execution_timeout(self) -> pulumi.Output[Optional[int]]:
        """
        The workload group query execution timeout.
        """
        return pulumi.get(self, 'query_execution_timeout')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
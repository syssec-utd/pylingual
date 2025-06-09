import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['RoleArgs', 'Role']

@pulumi.input_type
class RoleArgs:

    def __init__(__self__, *, device_name: pulumi.Input[str], kind: pulumi.Input[Union[str, 'RoleTypes']], resource_group_name: pulumi.Input[str], name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Role resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Union[str, 'RoleTypes']] kind: Role type.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] name: The role name.
        """
        pulumi.set(__self__, 'device_name', device_name)
        pulumi.set(__self__, 'kind', kind)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter(name='deviceName')
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, 'device_name')

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'device_name', value)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[Union[str, 'RoleTypes']]:
        """
        Role type.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: pulumi.Input[Union[str, 'RoleTypes']]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The role name.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)
warnings.warn('Version 2019-07-01 will be removed in v2 of the provider.', DeprecationWarning)

class Role(pulumi.CustomResource):
    warnings.warn('Version 2019-07-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, device_name: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[Union[str, 'RoleTypes']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Compute role.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Union[str, 'RoleTypes']] kind: Role type.
        :param pulumi.Input[str] name: The role name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: RoleArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Compute role.

        :param str resource_name: The name of the resource.
        :param RoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, device_name: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[Union[str, 'RoleTypes']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        pulumi.log.warn('Role is deprecated: Version 2019-07-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleArgs.__new__(RoleArgs)
            if device_name is None and (not opts.urn):
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__['device_name'] = device_name
            if kind is None and (not opts.urn):
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__['kind'] = kind
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:databoxedge:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20190301:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20190801:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20200501preview:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20200901:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20200901preview:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20201201:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20210201:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20210201preview:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20210601:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20210601preview:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20220301:Role'), pulumi.Alias(type_='azure-native:databoxedge/v20220401preview:Role')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Role, __self__).__init__('azure-native:databoxedge/v20190701:Role', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Role':
        """
        Get an existing Role resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = RoleArgs.__new__(RoleArgs)
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['type'] = None
        return Role(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Role type.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['WebAppConnectionStringsArgs', 'WebAppConnectionStrings']

@pulumi.input_type
class WebAppConnectionStringsArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], kind: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[Mapping[str, pulumi.Input['ConnStringValueTypePairArgs']]]]=None):
        """
        The set of arguments for constructing a WebAppConnectionStrings resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[Mapping[str, pulumi.Input['ConnStringValueTypePairArgs']]] properties: Connection strings.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if properties is not None:
            pulumi.set(__self__, 'properties', properties)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the app.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ConnStringValueTypePairArgs']]]]:
        """
        Connection strings.
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ConnStringValueTypePairArgs']]]]):
        pulumi.set(self, 'properties', value)

class WebAppConnectionStrings(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ConnStringValueTypePairArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        String dictionary resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ConnStringValueTypePairArgs']]]] properties: Connection strings.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WebAppConnectionStringsArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        String dictionary resource.

        :param str resource_name: The name of the resource.
        :param WebAppConnectionStringsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppConnectionStringsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ConnStringValueTypePairArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebAppConnectionStringsArgs.__new__(WebAppConnectionStringsArgs)
            __props__.__dict__['kind'] = kind
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:web:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20150801:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20160801:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20180201:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20181101:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20190801:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20200601:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20200901:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20201201:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20210101:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20210115:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20210201:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20210301:WebAppConnectionStrings'), pulumi.Alias(type_='azure-native:web/v20220301:WebAppConnectionStrings')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppConnectionStrings, __self__).__init__('azure-native:web/v20201001:WebAppConnectionStrings', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'WebAppConnectionStrings':
        """
        Get an existing WebAppConnectionStrings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = WebAppConnectionStringsArgs.__new__(WebAppConnectionStringsArgs)
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return WebAppConnectionStrings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Mapping[str, 'outputs.ConnStringValueTypePairResponse']]:
        """
        Connection strings.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
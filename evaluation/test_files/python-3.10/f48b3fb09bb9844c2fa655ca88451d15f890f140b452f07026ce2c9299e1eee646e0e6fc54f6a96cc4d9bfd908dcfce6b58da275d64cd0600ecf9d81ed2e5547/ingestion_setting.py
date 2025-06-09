import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['IngestionSettingArgs', 'IngestionSetting']

@pulumi.input_type
class IngestionSettingArgs:

    def __init__(__self__, *, ingestion_setting_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a IngestionSetting resource.
        :param pulumi.Input[str] ingestion_setting_name: Name of the ingestion setting
        """
        if ingestion_setting_name is not None:
            pulumi.set(__self__, 'ingestion_setting_name', ingestion_setting_name)

    @property
    @pulumi.getter(name='ingestionSettingName')
    def ingestion_setting_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the ingestion setting
        """
        return pulumi.get(self, 'ingestion_setting_name')

    @ingestion_setting_name.setter
    def ingestion_setting_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ingestion_setting_name', value)

class IngestionSetting(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, ingestion_setting_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Configures how to correlate scan data and logs with resources associated with the subscription.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ingestion_setting_name: Name of the ingestion setting
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: Optional[IngestionSettingArgs]=None, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Configures how to correlate scan data and logs with resources associated with the subscription.

        :param str resource_name: The name of the resource.
        :param IngestionSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(IngestionSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, ingestion_setting_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IngestionSettingArgs.__new__(IngestionSettingArgs)
            __props__.__dict__['ingestion_setting_name'] = ingestion_setting_name
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:security:IngestionSetting')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IngestionSetting, __self__).__init__('azure-native:security/v20210115preview:IngestionSetting', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'IngestionSetting':
        """
        Get an existing IngestionSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = IngestionSettingArgs.__new__(IngestionSettingArgs)
        __props__.__dict__['name'] = None
        __props__.__dict__['type'] = None
        return IngestionSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')
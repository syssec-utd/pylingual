import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['WebAppSitePushSettingsSlotArgs', 'WebAppSitePushSettingsSlot']

@pulumi.input_type
class WebAppSitePushSettingsSlotArgs:

    def __init__(__self__, *, is_push_enabled: pulumi.Input[bool], name: pulumi.Input[str], resource_group_name: pulumi.Input[str], slot: pulumi.Input[str], dynamic_tags_json: Optional[pulumi.Input[str]]=None, kind: Optional[pulumi.Input[str]]=None, tag_whitelist_json: Optional[pulumi.Input[str]]=None, tags_requiring_auth: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a WebAppSitePushSettingsSlot resource.
        :param pulumi.Input[bool] is_push_enabled: Gets or sets a flag indicating whether the Push endpoint is enabled.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
        :param pulumi.Input[str] dynamic_tags_json: Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] tag_whitelist_json: Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        :param pulumi.Input[str] tags_requiring_auth: Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
               Tags can consist of alphanumeric characters and the following:
               '_', '@', '#', '.', ':', '-'. 
               Validation should be performed at the PushRequestHandler.
        """
        pulumi.set(__self__, 'is_push_enabled', is_push_enabled)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'slot', slot)
        if dynamic_tags_json is not None:
            pulumi.set(__self__, 'dynamic_tags_json', dynamic_tags_json)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if tag_whitelist_json is not None:
            pulumi.set(__self__, 'tag_whitelist_json', tag_whitelist_json)
        if tags_requiring_auth is not None:
            pulumi.set(__self__, 'tags_requiring_auth', tags_requiring_auth)

    @property
    @pulumi.getter(name='isPushEnabled')
    def is_push_enabled(self) -> pulumi.Input[bool]:
        """
        Gets or sets a flag indicating whether the Push endpoint is enabled.
        """
        return pulumi.get(self, 'is_push_enabled')

    @is_push_enabled.setter
    def is_push_enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, 'is_push_enabled', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of web app.
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
    def slot(self) -> pulumi.Input[str]:
        """
        Name of web app slot. If not specified then will default to production slot.
        """
        return pulumi.get(self, 'slot')

    @slot.setter
    def slot(self, value: pulumi.Input[str]):
        pulumi.set(self, 'slot', value)

    @property
    @pulumi.getter(name='dynamicTagsJson')
    def dynamic_tags_json(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        """
        return pulumi.get(self, 'dynamic_tags_json')

    @dynamic_tags_json.setter
    def dynamic_tags_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dynamic_tags_json', value)

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
    @pulumi.getter(name='tagWhitelistJson')
    def tag_whitelist_json(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        """
        return pulumi.get(self, 'tag_whitelist_json')

    @tag_whitelist_json.setter
    def tag_whitelist_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tag_whitelist_json', value)

    @property
    @pulumi.getter(name='tagsRequiringAuth')
    def tags_requiring_auth(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
        Tags can consist of alphanumeric characters and the following:
        '_', '@', '#', '.', ':', '-'. 
        Validation should be performed at the PushRequestHandler.
        """
        return pulumi.get(self, 'tags_requiring_auth')

    @tags_requiring_auth.setter
    def tags_requiring_auth(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'tags_requiring_auth', value)

class WebAppSitePushSettingsSlot(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, dynamic_tags_json: Optional[pulumi.Input[str]]=None, is_push_enabled: Optional[pulumi.Input[bool]]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, tag_whitelist_json: Optional[pulumi.Input[str]]=None, tags_requiring_auth: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Push settings for the App.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dynamic_tags_json: Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        :param pulumi.Input[bool] is_push_enabled: Gets or sets a flag indicating whether the Push endpoint is enabled.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
        :param pulumi.Input[str] tag_whitelist_json: Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        :param pulumi.Input[str] tags_requiring_auth: Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
               Tags can consist of alphanumeric characters and the following:
               '_', '@', '#', '.', ':', '-'. 
               Validation should be performed at the PushRequestHandler.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: WebAppSitePushSettingsSlotArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Push settings for the App.

        :param str resource_name: The name of the resource.
        :param WebAppSitePushSettingsSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppSitePushSettingsSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, dynamic_tags_json: Optional[pulumi.Input[str]]=None, is_push_enabled: Optional[pulumi.Input[bool]]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, slot: Optional[pulumi.Input[str]]=None, tag_whitelist_json: Optional[pulumi.Input[str]]=None, tags_requiring_auth: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebAppSitePushSettingsSlotArgs.__new__(WebAppSitePushSettingsSlotArgs)
            __props__.__dict__['dynamic_tags_json'] = dynamic_tags_json
            if is_push_enabled is None and (not opts.urn):
                raise TypeError("Missing required property 'is_push_enabled'")
            __props__.__dict__['is_push_enabled'] = is_push_enabled
            __props__.__dict__['kind'] = kind
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if slot is None and (not opts.urn):
                raise TypeError("Missing required property 'slot'")
            __props__.__dict__['slot'] = slot
            __props__.__dict__['tag_whitelist_json'] = tag_whitelist_json
            __props__.__dict__['tags_requiring_auth'] = tags_requiring_auth
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:web:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20160801:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20180201:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20181101:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20190801:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20200601:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20200901:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20201001:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20201201:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20210101:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20210201:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20210301:WebAppSitePushSettingsSlot'), pulumi.Alias(type_='azure-native:web/v20220301:WebAppSitePushSettingsSlot')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSitePushSettingsSlot, __self__).__init__('azure-native:web/v20210115:WebAppSitePushSettingsSlot', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'WebAppSitePushSettingsSlot':
        """
        Get an existing WebAppSitePushSettingsSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = WebAppSitePushSettingsSlotArgs.__new__(WebAppSitePushSettingsSlotArgs)
        __props__.__dict__['dynamic_tags_json'] = None
        __props__.__dict__['is_push_enabled'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['tag_whitelist_json'] = None
        __props__.__dict__['tags_requiring_auth'] = None
        __props__.__dict__['type'] = None
        return WebAppSitePushSettingsSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='dynamicTagsJson')
    def dynamic_tags_json(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        """
        return pulumi.get(self, 'dynamic_tags_json')

    @property
    @pulumi.getter(name='isPushEnabled')
    def is_push_enabled(self) -> pulumi.Output[bool]:
        """
        Gets or sets a flag indicating whether the Push endpoint is enabled.
        """
        return pulumi.get(self, 'is_push_enabled')

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
    @pulumi.getter(name='tagWhitelistJson')
    def tag_whitelist_json(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        """
        return pulumi.get(self, 'tag_whitelist_json')

    @property
    @pulumi.getter(name='tagsRequiringAuth')
    def tags_requiring_auth(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
        Tags can consist of alphanumeric characters and the following:
        '_', '@', '#', '.', ':', '-'. 
        Validation should be performed at the PushRequestHandler.
        """
        return pulumi.get(self, 'tags_requiring_auth')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
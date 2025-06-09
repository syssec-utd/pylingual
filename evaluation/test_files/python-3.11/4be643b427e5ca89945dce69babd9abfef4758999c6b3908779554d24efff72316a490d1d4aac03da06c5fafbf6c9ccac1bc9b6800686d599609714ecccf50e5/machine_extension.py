import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['MachineExtensionArgs', 'MachineExtension']

@pulumi.input_type
class MachineExtensionArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, extension_name: Optional[pulumi.Input[str]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, publisher: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a MachineExtension resource.
        :param pulumi.Input[str] name: The name of the machine where the extension should be created or updated.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param pulumi.Input[bool] auto_upgrade_minor_version: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        :param pulumi.Input[str] extension_name: The name of the machine extension.
        :param pulumi.Input[str] force_update_tag: How the extension handler should be forced to update even if the extension configuration has not changed.
        :param pulumi.Input[str] location: Gets or sets the location.
        :param Any protected_settings: The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher.
        :param Any settings: Json formatted public settings for the extension.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets the Resource tags.
        :param pulumi.Input[str] type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if auto_upgrade_minor_version is not None:
            pulumi.set(__self__, 'auto_upgrade_minor_version', auto_upgrade_minor_version)
        if extension_name is not None:
            pulumi.set(__self__, 'extension_name', extension_name)
        if force_update_tag is not None:
            pulumi.set(__self__, 'force_update_tag', force_update_tag)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if protected_settings is not None:
            pulumi.set(__self__, 'protected_settings', protected_settings)
        if publisher is not None:
            pulumi.set(__self__, 'publisher', publisher)
        if settings is not None:
            pulumi.set(__self__, 'settings', settings)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if type_handler_version is not None:
            pulumi.set(__self__, 'type_handler_version', type_handler_version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the machine where the extension should be created or updated.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The Resource Group Name.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='autoUpgradeMinorVersion')
    def auto_upgrade_minor_version(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        """
        return pulumi.get(self, 'auto_upgrade_minor_version')

    @auto_upgrade_minor_version.setter
    def auto_upgrade_minor_version(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_upgrade_minor_version', value)

    @property
    @pulumi.getter(name='extensionName')
    def extension_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the machine extension.
        """
        return pulumi.get(self, 'extension_name')

    @extension_name.setter
    def extension_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'extension_name', value)

    @property
    @pulumi.getter(name='forceUpdateTag')
    def force_update_tag(self) -> Optional[pulumi.Input[str]]:
        """
        How the extension handler should be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, 'force_update_tag')

    @force_update_tag.setter
    def force_update_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'force_update_tag', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='protectedSettings')
    def protected_settings(self) -> Optional[Any]:
        """
        The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        """
        return pulumi.get(self, 'protected_settings')

    @protected_settings.setter
    def protected_settings(self, value: Optional[Any]):
        pulumi.set(self, 'protected_settings', value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the extension handler publisher.
        """
        return pulumi.get(self, 'publisher')

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'publisher', value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[Any]:
        """
        Json formatted public settings for the extension.
        """
        return pulumi.get(self, 'settings')

    @settings.setter
    def settings(self, value: Optional[Any]):
        pulumi.set(self, 'settings', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Gets or sets the Resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the type of the extension; an example is "CustomScriptExtension".
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='typeHandlerVersion')
    def type_handler_version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, 'type_handler_version')

    @type_handler_version.setter
    def type_handler_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'type_handler_version', value)

class MachineExtension(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, extension_name: Optional[pulumi.Input[str]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, publisher: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Describes a Machine Extension.
        API Version: 2020-10-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_upgrade_minor_version: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        :param pulumi.Input[str] extension_name: The name of the machine extension.
        :param pulumi.Input[str] force_update_tag: How the extension handler should be forced to update even if the extension configuration has not changed.
        :param pulumi.Input[str] location: Gets or sets the location.
        :param pulumi.Input[str] name: The name of the machine where the extension should be created or updated.
        :param Any protected_settings: The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param Any settings: Json formatted public settings for the extension.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets the Resource tags.
        :param pulumi.Input[str] type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: MachineExtensionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Describes a Machine Extension.
        API Version: 2020-10-01-preview.

        :param str resource_name: The name of the resource.
        :param MachineExtensionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineExtensionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, extension_name: Optional[pulumi.Input[str]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, publisher: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MachineExtensionArgs.__new__(MachineExtensionArgs)
            __props__.__dict__['auto_upgrade_minor_version'] = auto_upgrade_minor_version
            __props__.__dict__['extension_name'] = extension_name
            __props__.__dict__['force_update_tag'] = force_update_tag
            __props__.__dict__['location'] = location
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['protected_settings'] = protected_settings
            __props__.__dict__['publisher'] = publisher
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['settings'] = settings
            __props__.__dict__['tags'] = tags
            __props__.__dict__['type'] = type
            __props__.__dict__['type_handler_version'] = type_handler_version
            __props__.__dict__['instance_view'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['system_data'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:connectedvmwarevsphere/v20201001preview:MachineExtension'), pulumi.Alias(type_='azure-native:connectedvmwarevsphere/v20220110preview:MachineExtension')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MachineExtension, __self__).__init__('azure-native:connectedvmwarevsphere:MachineExtension', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'MachineExtension':
        """
        Get an existing MachineExtension resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = MachineExtensionArgs.__new__(MachineExtensionArgs)
        __props__.__dict__['auto_upgrade_minor_version'] = None
        __props__.__dict__['force_update_tag'] = None
        __props__.__dict__['instance_view'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['protected_settings'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['publisher'] = None
        __props__.__dict__['settings'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['type_handler_version'] = None
        return MachineExtension(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='autoUpgradeMinorVersion')
    def auto_upgrade_minor_version(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        """
        return pulumi.get(self, 'auto_upgrade_minor_version')

    @property
    @pulumi.getter(name='forceUpdateTag')
    def force_update_tag(self) -> pulumi.Output[Optional[str]]:
        """
        How the extension handler should be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, 'force_update_tag')

    @property
    @pulumi.getter(name='instanceView')
    def instance_view(self) -> pulumi.Output[Optional['outputs.MachineExtensionPropertiesResponseInstanceView']]:
        """
        The machine extension instance view.
        """
        return pulumi.get(self, 'instance_view')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets or sets the name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='protectedSettings')
    def protected_settings(self) -> pulumi.Output[Optional[Any]]:
        """
        The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        """
        return pulumi.get(self, 'protected_settings')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def publisher(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the extension handler publisher.
        """
        return pulumi.get(self, 'publisher')

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Output[Optional[Any]]:
        """
        Json formatted public settings for the extension.
        """
        return pulumi.get(self, 'settings')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system data.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Gets or sets the Resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Gets or sets the type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='typeHandlerVersion')
    def type_handler_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, 'type_handler_version')
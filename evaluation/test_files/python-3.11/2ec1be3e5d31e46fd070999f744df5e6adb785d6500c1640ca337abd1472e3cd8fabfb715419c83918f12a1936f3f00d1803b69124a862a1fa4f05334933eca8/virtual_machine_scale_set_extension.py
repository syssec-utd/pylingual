import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['VirtualMachineScaleSetExtensionInitArgs', 'VirtualMachineScaleSetExtension']

@pulumi.input_type
class VirtualMachineScaleSetExtensionInitArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], vm_scale_set_name: pulumi.Input[str], auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, provision_after_extensions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, publisher: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None, vmss_extension_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a VirtualMachineScaleSetExtension resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] vm_scale_set_name: The name of the VM scale set where the extension should be create or updated.
        :param pulumi.Input[bool] auto_upgrade_minor_version: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        :param pulumi.Input[str] force_update_tag: If a value is provided and is different from the previous value, the extension handler will be forced to update even if the extension configuration has not changed.
        :param pulumi.Input[str] name: The name of the extension.
        :param Any protected_settings: The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] provision_after_extensions: Collection of extension names after which this extension needs to be provisioned.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher.
        :param Any settings: Json formatted public settings for the extension.
        :param pulumi.Input[str] type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
        :param pulumi.Input[str] vmss_extension_name: The name of the VM scale set extension.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'vm_scale_set_name', vm_scale_set_name)
        if auto_upgrade_minor_version is not None:
            pulumi.set(__self__, 'auto_upgrade_minor_version', auto_upgrade_minor_version)
        if force_update_tag is not None:
            pulumi.set(__self__, 'force_update_tag', force_update_tag)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if protected_settings is not None:
            pulumi.set(__self__, 'protected_settings', protected_settings)
        if provision_after_extensions is not None:
            pulumi.set(__self__, 'provision_after_extensions', provision_after_extensions)
        if publisher is not None:
            pulumi.set(__self__, 'publisher', publisher)
        if settings is not None:
            pulumi.set(__self__, 'settings', settings)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if type_handler_version is not None:
            pulumi.set(__self__, 'type_handler_version', type_handler_version)
        if vmss_extension_name is not None:
            pulumi.set(__self__, 'vmss_extension_name', vmss_extension_name)

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
    @pulumi.getter(name='vmScaleSetName')
    def vm_scale_set_name(self) -> pulumi.Input[str]:
        """
        The name of the VM scale set where the extension should be create or updated.
        """
        return pulumi.get(self, 'vm_scale_set_name')

    @vm_scale_set_name.setter
    def vm_scale_set_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'vm_scale_set_name', value)

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
    @pulumi.getter(name='forceUpdateTag')
    def force_update_tag(self) -> Optional[pulumi.Input[str]]:
        """
        If a value is provided and is different from the previous value, the extension handler will be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, 'force_update_tag')

    @force_update_tag.setter
    def force_update_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'force_update_tag', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the extension.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

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
    @pulumi.getter(name='provisionAfterExtensions')
    def provision_after_extensions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Collection of extension names after which this extension needs to be provisioned.
        """
        return pulumi.get(self, 'provision_after_extensions')

    @provision_after_extensions.setter
    def provision_after_extensions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'provision_after_extensions', value)

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

    @property
    @pulumi.getter(name='vmssExtensionName')
    def vmss_extension_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VM scale set extension.
        """
        return pulumi.get(self, 'vmss_extension_name')

    @vmss_extension_name.setter
    def vmss_extension_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'vmss_extension_name', value)
warnings.warn('Version 2019-12-01 will be removed in v2 of the provider.', DeprecationWarning)

class VirtualMachineScaleSetExtension(pulumi.CustomResource):
    warnings.warn('Version 2019-12-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, provision_after_extensions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, publisher: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None, vm_scale_set_name: Optional[pulumi.Input[str]]=None, vmss_extension_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Describes a Virtual Machine Scale Set Extension.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_upgrade_minor_version: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        :param pulumi.Input[str] force_update_tag: If a value is provided and is different from the previous value, the extension handler will be forced to update even if the extension configuration has not changed.
        :param pulumi.Input[str] name: The name of the extension.
        :param Any protected_settings: The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] provision_after_extensions: Collection of extension names after which this extension needs to be provisioned.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param Any settings: Json formatted public settings for the extension.
        :param pulumi.Input[str] type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
        :param pulumi.Input[str] vm_scale_set_name: The name of the VM scale set where the extension should be create or updated.
        :param pulumi.Input[str] vmss_extension_name: The name of the VM scale set extension.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: VirtualMachineScaleSetExtensionInitArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Describes a Virtual Machine Scale Set Extension.

        :param str resource_name: The name of the resource.
        :param VirtualMachineScaleSetExtensionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualMachineScaleSetExtensionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_upgrade_minor_version: Optional[pulumi.Input[bool]]=None, force_update_tag: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, protected_settings: Optional[Any]=None, provision_after_extensions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, publisher: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, settings: Optional[Any]=None, type: Optional[pulumi.Input[str]]=None, type_handler_version: Optional[pulumi.Input[str]]=None, vm_scale_set_name: Optional[pulumi.Input[str]]=None, vmss_extension_name: Optional[pulumi.Input[str]]=None, __props__=None):
        pulumi.log.warn('VirtualMachineScaleSetExtension is deprecated: Version 2019-12-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VirtualMachineScaleSetExtensionInitArgs.__new__(VirtualMachineScaleSetExtensionInitArgs)
            __props__.__dict__['auto_upgrade_minor_version'] = auto_upgrade_minor_version
            __props__.__dict__['force_update_tag'] = force_update_tag
            __props__.__dict__['name'] = name
            __props__.__dict__['protected_settings'] = protected_settings
            __props__.__dict__['provision_after_extensions'] = provision_after_extensions
            __props__.__dict__['publisher'] = publisher
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['settings'] = settings
            __props__.__dict__['type'] = type
            __props__.__dict__['type_handler_version'] = type_handler_version
            if vm_scale_set_name is None and (not opts.urn):
                raise TypeError("Missing required property 'vm_scale_set_name'")
            __props__.__dict__['vm_scale_set_name'] = vm_scale_set_name
            __props__.__dict__['vmss_extension_name'] = vmss_extension_name
            __props__.__dict__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:compute:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20170330:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20171201:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20180401:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20180601:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20181001:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20190301:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20190701:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20200601:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20201201:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20210301:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20210401:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20210701:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20211101:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20220301:VirtualMachineScaleSetExtension'), pulumi.Alias(type_='azure-native:compute/v20220801:VirtualMachineScaleSetExtension')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualMachineScaleSetExtension, __self__).__init__('azure-native:compute/v20191201:VirtualMachineScaleSetExtension', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'VirtualMachineScaleSetExtension':
        """
        Get an existing VirtualMachineScaleSetExtension resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = VirtualMachineScaleSetExtensionInitArgs.__new__(VirtualMachineScaleSetExtensionInitArgs)
        __props__.__dict__['auto_upgrade_minor_version'] = None
        __props__.__dict__['force_update_tag'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['protected_settings'] = None
        __props__.__dict__['provision_after_extensions'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['publisher'] = None
        __props__.__dict__['settings'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['type_handler_version'] = None
        return VirtualMachineScaleSetExtension(resource_name, opts=opts, __props__=__props__)

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
        If a value is provided and is different from the previous value, the extension handler will be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, 'force_update_tag')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the extension.
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
    @pulumi.getter(name='provisionAfterExtensions')
    def provision_after_extensions(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Collection of extension names after which this extension needs to be provisioned.
        """
        return pulumi.get(self, 'provision_after_extensions')

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
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='typeHandlerVersion')
    def type_handler_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, 'type_handler_version')
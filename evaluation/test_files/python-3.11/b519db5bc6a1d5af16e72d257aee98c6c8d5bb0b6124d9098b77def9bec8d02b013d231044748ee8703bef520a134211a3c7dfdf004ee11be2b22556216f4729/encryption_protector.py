import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['EncryptionProtectorArgs', 'EncryptionProtector']

@pulumi.input_type
class EncryptionProtectorArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], server_key_type: pulumi.Input[Union[str, 'ServerKeyType']], server_name: pulumi.Input[str], auto_rotation_enabled: Optional[pulumi.Input[bool]]=None, encryption_protector_name: Optional[pulumi.Input[str]]=None, server_key_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a EncryptionProtector resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[Union[str, 'ServerKeyType']] server_key_type: The encryption protector type like 'ServiceManaged', 'AzureKeyVault'.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[bool] auto_rotation_enabled: Key auto rotation opt-in flag. Either true or false.
        :param pulumi.Input[str] encryption_protector_name: The name of the encryption protector to be updated.
        :param pulumi.Input[str] server_key_name: The name of the server key.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'server_key_type', server_key_type)
        pulumi.set(__self__, 'server_name', server_name)
        if auto_rotation_enabled is not None:
            pulumi.set(__self__, 'auto_rotation_enabled', auto_rotation_enabled)
        if encryption_protector_name is not None:
            pulumi.set(__self__, 'encryption_protector_name', encryption_protector_name)
        if server_key_name is not None:
            pulumi.set(__self__, 'server_key_name', server_key_name)

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
    @pulumi.getter(name='serverKeyType')
    def server_key_type(self) -> pulumi.Input[Union[str, 'ServerKeyType']]:
        """
        The encryption protector type like 'ServiceManaged', 'AzureKeyVault'.
        """
        return pulumi.get(self, 'server_key_type')

    @server_key_type.setter
    def server_key_type(self, value: pulumi.Input[Union[str, 'ServerKeyType']]):
        pulumi.set(self, 'server_key_type', value)

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
    @pulumi.getter(name='autoRotationEnabled')
    def auto_rotation_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Key auto rotation opt-in flag. Either true or false.
        """
        return pulumi.get(self, 'auto_rotation_enabled')

    @auto_rotation_enabled.setter
    def auto_rotation_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_rotation_enabled', value)

    @property
    @pulumi.getter(name='encryptionProtectorName')
    def encryption_protector_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the encryption protector to be updated.
        """
        return pulumi.get(self, 'encryption_protector_name')

    @encryption_protector_name.setter
    def encryption_protector_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'encryption_protector_name', value)

    @property
    @pulumi.getter(name='serverKeyName')
    def server_key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the server key.
        """
        return pulumi.get(self, 'server_key_name')

    @server_key_name.setter
    def server_key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'server_key_name', value)

class EncryptionProtector(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_rotation_enabled: Optional[pulumi.Input[bool]]=None, encryption_protector_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_key_name: Optional[pulumi.Input[str]]=None, server_key_type: Optional[pulumi.Input[Union[str, 'ServerKeyType']]]=None, server_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The server encryption protector.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_rotation_enabled: Key auto rotation opt-in flag. Either true or false.
        :param pulumi.Input[str] encryption_protector_name: The name of the encryption protector to be updated.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_key_name: The name of the server key.
        :param pulumi.Input[Union[str, 'ServerKeyType']] server_key_type: The encryption protector type like 'ServiceManaged', 'AzureKeyVault'.
        :param pulumi.Input[str] server_name: The name of the server.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: EncryptionProtectorArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The server encryption protector.

        :param str resource_name: The name of the resource.
        :param EncryptionProtectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EncryptionProtectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_rotation_enabled: Optional[pulumi.Input[bool]]=None, encryption_protector_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, server_key_name: Optional[pulumi.Input[str]]=None, server_key_type: Optional[pulumi.Input[Union[str, 'ServerKeyType']]]=None, server_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EncryptionProtectorArgs.__new__(EncryptionProtectorArgs)
            __props__.__dict__['auto_rotation_enabled'] = auto_rotation_enabled
            __props__.__dict__['encryption_protector_name'] = encryption_protector_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['server_key_name'] = server_key_name
            if server_key_type is None and (not opts.urn):
                raise TypeError("Missing required property 'server_key_type'")
            __props__.__dict__['server_key_type'] = server_key_type
            if server_name is None and (not opts.urn):
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__['server_name'] = server_name
            __props__.__dict__['kind'] = None
            __props__.__dict__['location'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['subregion'] = None
            __props__.__dict__['thumbprint'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['uri'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:sql:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20150501preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20200202preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20200801preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20201101preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20210201preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20210501preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20210801preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20211101:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20211101preview:EncryptionProtector'), pulumi.Alias(type_='azure-native:sql/v20220501preview:EncryptionProtector')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EncryptionProtector, __self__).__init__('azure-native:sql/v20220201preview:EncryptionProtector', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'EncryptionProtector':
        """
        Get an existing EncryptionProtector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = EncryptionProtectorArgs.__new__(EncryptionProtectorArgs)
        __props__.__dict__['auto_rotation_enabled'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['server_key_name'] = None
        __props__.__dict__['server_key_type'] = None
        __props__.__dict__['subregion'] = None
        __props__.__dict__['thumbprint'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['uri'] = None
        return EncryptionProtector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='autoRotationEnabled')
    def auto_rotation_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Key auto rotation opt-in flag. Either true or false.
        """
        return pulumi.get(self, 'auto_rotation_enabled')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of encryption protector. This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='serverKeyName')
    def server_key_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the server key.
        """
        return pulumi.get(self, 'server_key_name')

    @property
    @pulumi.getter(name='serverKeyType')
    def server_key_type(self) -> pulumi.Output[str]:
        """
        The encryption protector type like 'ServiceManaged', 'AzureKeyVault'.
        """
        return pulumi.get(self, 'server_key_type')

    @property
    @pulumi.getter
    def subregion(self) -> pulumi.Output[str]:
        """
        Subregion of the encryption protector.
        """
        return pulumi.get(self, 'subregion')

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[str]:
        """
        Thumbprint of the server key.
        """
        return pulumi.get(self, 'thumbprint')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        """
        The URI of the server key.
        """
        return pulumi.get(self, 'uri')
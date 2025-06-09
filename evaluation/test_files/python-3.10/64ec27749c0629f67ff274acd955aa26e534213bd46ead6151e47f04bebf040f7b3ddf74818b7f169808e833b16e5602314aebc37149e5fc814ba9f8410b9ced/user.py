import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:

    def __init__(__self__, *, device_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], encrypted_password: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]=None, name: Optional[pulumi.Input[str]]=None, share_access_rights: Optional[pulumi.Input[Sequence[pulumi.Input['ShareAccessRightArgs']]]]=None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input['AsymmetricEncryptedSecretArgs'] encrypted_password: The password details.
        :param pulumi.Input[str] name: The user name.
        :param pulumi.Input[Sequence[pulumi.Input['ShareAccessRightArgs']]] share_access_rights: List of shares that the user has rights on. This field should not be specified during user creation.
        """
        pulumi.set(__self__, 'device_name', device_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if encrypted_password is not None:
            pulumi.set(__self__, 'encrypted_password', encrypted_password)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if share_access_rights is not None:
            pulumi.set(__self__, 'share_access_rights', share_access_rights)

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
    @pulumi.getter(name='encryptedPassword')
    def encrypted_password(self) -> Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]:
        """
        The password details.
        """
        return pulumi.get(self, 'encrypted_password')

    @encrypted_password.setter
    def encrypted_password(self, value: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]):
        pulumi.set(self, 'encrypted_password', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The user name.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='shareAccessRights')
    def share_access_rights(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ShareAccessRightArgs']]]]:
        """
        List of shares that the user has rights on. This field should not be specified during user creation.
        """
        return pulumi.get(self, 'share_access_rights')

    @share_access_rights.setter
    def share_access_rights(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ShareAccessRightArgs']]]]):
        pulumi.set(self, 'share_access_rights', value)
warnings.warn('Version 2019-03-01 will be removed in v2 of the provider.', DeprecationWarning)

class User(pulumi.CustomResource):
    warnings.warn('Version 2019-03-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, device_name: Optional[pulumi.Input[str]]=None, encrypted_password: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, share_access_rights: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ShareAccessRightArgs']]]]]=None, __props__=None):
        """
        Represents a user who has access to one or more shares on the Data Box Edge/Gateway device.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']] encrypted_password: The password details.
        :param pulumi.Input[str] name: The user name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ShareAccessRightArgs']]]] share_access_rights: List of shares that the user has rights on. This field should not be specified during user creation.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: UserArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Represents a user who has access to one or more shares on the Data Box Edge/Gateway device.

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, device_name: Optional[pulumi.Input[str]]=None, encrypted_password: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, share_access_rights: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ShareAccessRightArgs']]]]]=None, __props__=None):
        pulumi.log.warn('User is deprecated: Version 2019-03-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)
            if device_name is None and (not opts.urn):
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__['device_name'] = device_name
            __props__.__dict__['encrypted_password'] = encrypted_password
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['share_access_rights'] = share_access_rights
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:databoxedge:User'), pulumi.Alias(type_='azure-native:databoxedge/v20190701:User'), pulumi.Alias(type_='azure-native:databoxedge/v20190801:User'), pulumi.Alias(type_='azure-native:databoxedge/v20200501preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20200901:User'), pulumi.Alias(type_='azure-native:databoxedge/v20200901preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20201201:User'), pulumi.Alias(type_='azure-native:databoxedge/v20210201:User'), pulumi.Alias(type_='azure-native:databoxedge/v20210201preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20210601:User'), pulumi.Alias(type_='azure-native:databoxedge/v20210601preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20220301:User'), pulumi.Alias(type_='azure-native:databoxedge/v20220401preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20221201preview:User'), pulumi.Alias(type_='azure-native:databoxedge/v20230101preview:User')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(User, __self__).__init__('azure-native:databoxedge/v20190301:User', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = UserArgs.__new__(UserArgs)
        __props__.__dict__['encrypted_password'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['share_access_rights'] = None
        __props__.__dict__['type'] = None
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='encryptedPassword')
    def encrypted_password(self) -> pulumi.Output[Optional['outputs.AsymmetricEncryptedSecretResponse']]:
        """
        The password details.
        """
        return pulumi.get(self, 'encrypted_password')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='shareAccessRights')
    def share_access_rights(self) -> pulumi.Output[Optional[Sequence['outputs.ShareAccessRightResponse']]]:
        """
        List of shares that the user has rights on. This field should not be specified during user creation.
        """
        return pulumi.get(self, 'share_access_rights')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, 'type')
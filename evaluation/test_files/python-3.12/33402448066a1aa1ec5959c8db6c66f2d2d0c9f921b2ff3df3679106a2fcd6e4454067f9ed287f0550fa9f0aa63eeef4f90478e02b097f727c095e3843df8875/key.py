import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['KeyArgs', 'Key']

@pulumi.input_type
class KeyArgs:

    def __init__(__self__, *, properties: pulumi.Input['KeyPropertiesArgs'], resource_group_name: pulumi.Input[str], vault_name: pulumi.Input[str], key_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Key resource.
        :param pulumi.Input['KeyPropertiesArgs'] properties: The properties of the key to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group which contains the specified key vault.
        :param pulumi.Input[str] vault_name: The name of the key vault which contains the key to be created.
        :param pulumi.Input[str] key_name: The name of the key to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the key.
        """
        pulumi.set(__self__, 'properties', properties)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'vault_name', vault_name)
        if key_name is not None:
            pulumi.set(__self__, 'key_name', key_name)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['KeyPropertiesArgs']:
        """
        The properties of the key to be created.
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: pulumi.Input['KeyPropertiesArgs']):
        pulumi.set(self, 'properties', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group which contains the specified key vault.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='vaultName')
    def vault_name(self) -> pulumi.Input[str]:
        """
        The name of the key vault which contains the key to be created.
        """
        return pulumi.get(self, 'vault_name')

    @vault_name.setter
    def vault_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'vault_name', value)

    @property
    @pulumi.getter(name='keyName')
    def key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the key to be created.
        """
        return pulumi.get(self, 'key_name')

    @key_name.setter
    def key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key_name', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags that will be assigned to the key.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class Key(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, key_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['KeyPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vault_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The key resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_name: The name of the key to be created.
        :param pulumi.Input[pulumi.InputType['KeyPropertiesArgs']] properties: The properties of the key to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group which contains the specified key vault.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags that will be assigned to the key.
        :param pulumi.Input[str] vault_name: The name of the key vault which contains the key to be created.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: KeyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The key resource.

        :param str resource_name: The name of the resource.
        :param KeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, key_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['KeyPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, vault_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = KeyArgs.__new__(KeyArgs)
            __props__.__dict__['key_name'] = key_name
            if properties is None and (not opts.urn):
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            if vault_name is None and (not opts.urn):
                raise TypeError("Missing required property 'vault_name'")
            __props__.__dict__['vault_name'] = vault_name
            __props__.__dict__['attributes'] = None
            __props__.__dict__['curve_name'] = None
            __props__.__dict__['key_ops'] = None
            __props__.__dict__['key_size'] = None
            __props__.__dict__['key_uri'] = None
            __props__.__dict__['key_uri_with_version'] = None
            __props__.__dict__['kty'] = None
            __props__.__dict__['location'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['release_policy'] = None
            __props__.__dict__['rotation_policy'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:keyvault:Key'), pulumi.Alias(type_='azure-native:keyvault/v20190901:Key'), pulumi.Alias(type_='azure-native:keyvault/v20200401preview:Key'), pulumi.Alias(type_='azure-native:keyvault/v20210401preview:Key'), pulumi.Alias(type_='azure-native:keyvault/v20211001:Key'), pulumi.Alias(type_='azure-native:keyvault/v20211101preview:Key'), pulumi.Alias(type_='azure-native:keyvault/v20220201preview:Key'), pulumi.Alias(type_='azure-native:keyvault/v20220701:Key'), pulumi.Alias(type_='azure-native:keyvault/v20221101:Key'), pulumi.Alias(type_='azure-native:keyvault/v20230201:Key')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Key, __self__).__init__('azure-native:keyvault/v20210601preview:Key', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Key':
        """
        Get an existing Key resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = KeyArgs.__new__(KeyArgs)
        __props__.__dict__['attributes'] = None
        __props__.__dict__['curve_name'] = None
        __props__.__dict__['key_ops'] = None
        __props__.__dict__['key_size'] = None
        __props__.__dict__['key_uri'] = None
        __props__.__dict__['key_uri_with_version'] = None
        __props__.__dict__['kty'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['release_policy'] = None
        __props__.__dict__['rotation_policy'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return Key(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Output[Optional['outputs.KeyAttributesResponse']]:
        """
        The attributes of the key.
        """
        return pulumi.get(self, 'attributes')

    @property
    @pulumi.getter(name='curveName')
    def curve_name(self) -> pulumi.Output[Optional[str]]:
        """
        The elliptic curve name. For valid values, see JsonWebKeyCurveName.
        """
        return pulumi.get(self, 'curve_name')

    @property
    @pulumi.getter(name='keyOps')
    def key_ops(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, 'key_ops')

    @property
    @pulumi.getter(name='keySize')
    def key_size(self) -> pulumi.Output[Optional[int]]:
        """
        The key size in bits. For example: 2048, 3072, or 4096 for RSA.
        """
        return pulumi.get(self, 'key_size')

    @property
    @pulumi.getter(name='keyUri')
    def key_uri(self) -> pulumi.Output[str]:
        """
        The URI to retrieve the current version of the key.
        """
        return pulumi.get(self, 'key_uri')

    @property
    @pulumi.getter(name='keyUriWithVersion')
    def key_uri_with_version(self) -> pulumi.Output[str]:
        """
        The URI to retrieve the specific version of the key.
        """
        return pulumi.get(self, 'key_uri_with_version')

    @property
    @pulumi.getter
    def kty(self) -> pulumi.Output[Optional[str]]:
        """
        The type of the key. For valid values, see JsonWebKeyType.
        """
        return pulumi.get(self, 'kty')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Azure location of the key vault resource.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the key vault resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='releasePolicy')
    def release_policy(self) -> pulumi.Output[Optional['outputs.KeyReleasePolicyResponse']]:
        """
        Key release policy in response. It will be used for both output and input. Omitted if empty
        """
        return pulumi.get(self, 'release_policy')

    @property
    @pulumi.getter(name='rotationPolicy')
    def rotation_policy(self) -> pulumi.Output[Optional['outputs.RotationPolicyResponse']]:
        """
        Key rotation policy in response. It will be used for both output and input. Omitted if empty
        """
        return pulumi.get(self, 'rotation_policy')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Tags assigned to the key vault resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type of the key vault resource.
        """
        return pulumi.get(self, 'type')
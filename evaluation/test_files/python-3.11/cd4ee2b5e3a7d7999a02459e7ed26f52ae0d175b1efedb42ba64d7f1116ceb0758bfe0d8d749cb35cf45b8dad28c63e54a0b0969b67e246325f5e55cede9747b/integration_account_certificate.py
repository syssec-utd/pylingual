import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *
__all__ = ['IntegrationAccountCertificateArgs', 'IntegrationAccountCertificate']

@pulumi.input_type
class IntegrationAccountCertificateArgs:

    def __init__(__self__, *, integration_account_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], certificate_name: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input['KeyVaultKeyReferenceArgs']]=None, location: Optional[pulumi.Input[str]]=None, metadata: Optional[Any]=None, public_certificate: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a IntegrationAccountCertificate resource.
        :param pulumi.Input[str] integration_account_name: The integration account name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] certificate_name: The integration account certificate name.
        :param pulumi.Input['KeyVaultKeyReferenceArgs'] key: The key details in the key vault.
        :param pulumi.Input[str] location: The resource location.
        :param Any metadata: The metadata.
        :param pulumi.Input[str] public_certificate: The public certificate.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        pulumi.set(__self__, 'integration_account_name', integration_account_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if certificate_name is not None:
            pulumi.set(__self__, 'certificate_name', certificate_name)
        if key is not None:
            pulumi.set(__self__, 'key', key)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if metadata is not None:
            pulumi.set(__self__, 'metadata', metadata)
        if public_certificate is not None:
            pulumi.set(__self__, 'public_certificate', public_certificate)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='integrationAccountName')
    def integration_account_name(self) -> pulumi.Input[str]:
        """
        The integration account name.
        """
        return pulumi.get(self, 'integration_account_name')

    @integration_account_name.setter
    def integration_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'integration_account_name', value)

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
    @pulumi.getter(name='certificateName')
    def certificate_name(self) -> Optional[pulumi.Input[str]]:
        """
        The integration account certificate name.
        """
        return pulumi.get(self, 'certificate_name')

    @certificate_name.setter
    def certificate_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'certificate_name', value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input['KeyVaultKeyReferenceArgs']]:
        """
        The key details in the key vault.
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: Optional[pulumi.Input['KeyVaultKeyReferenceArgs']]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Any]:
        """
        The metadata.
        """
        return pulumi.get(self, 'metadata')

    @metadata.setter
    def metadata(self, value: Optional[Any]):
        pulumi.set(self, 'metadata', value)

    @property
    @pulumi.getter(name='publicCertificate')
    def public_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The public certificate.
        """
        return pulumi.get(self, 'public_certificate')

    @public_certificate.setter
    def public_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'public_certificate', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class IntegrationAccountCertificate(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, certificate_name: Optional[pulumi.Input[str]]=None, integration_account_name: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[pulumi.InputType['KeyVaultKeyReferenceArgs']]]=None, location: Optional[pulumi.Input[str]]=None, metadata: Optional[Any]=None, public_certificate: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        The integration account certificate.
        API Version: 2019-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_name: The integration account certificate name.
        :param pulumi.Input[str] integration_account_name: The integration account name.
        :param pulumi.Input[pulumi.InputType['KeyVaultKeyReferenceArgs']] key: The key details in the key vault.
        :param pulumi.Input[str] location: The resource location.
        :param Any metadata: The metadata.
        :param pulumi.Input[str] public_certificate: The public certificate.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: IntegrationAccountCertificateArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The integration account certificate.
        API Version: 2019-05-01.

        :param str resource_name: The name of the resource.
        :param IntegrationAccountCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationAccountCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, certificate_name: Optional[pulumi.Input[str]]=None, integration_account_name: Optional[pulumi.Input[str]]=None, key: Optional[pulumi.Input[pulumi.InputType['KeyVaultKeyReferenceArgs']]]=None, location: Optional[pulumi.Input[str]]=None, metadata: Optional[Any]=None, public_certificate: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationAccountCertificateArgs.__new__(IntegrationAccountCertificateArgs)
            __props__.__dict__['certificate_name'] = certificate_name
            if integration_account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'integration_account_name'")
            __props__.__dict__['integration_account_name'] = integration_account_name
            __props__.__dict__['key'] = key
            __props__.__dict__['location'] = location
            __props__.__dict__['metadata'] = metadata
            __props__.__dict__['public_certificate'] = public_certificate
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['changed_time'] = None
            __props__.__dict__['created_time'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:logic/v20150801preview:IntegrationAccountCertificate'), pulumi.Alias(type_='azure-native:logic/v20160601:IntegrationAccountCertificate'), pulumi.Alias(type_='azure-native:logic/v20180701preview:IntegrationAccountCertificate'), pulumi.Alias(type_='azure-native:logic/v20190501:IntegrationAccountCertificate')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IntegrationAccountCertificate, __self__).__init__('azure-native:logic:IntegrationAccountCertificate', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'IntegrationAccountCertificate':
        """
        Get an existing IntegrationAccountCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = IntegrationAccountCertificateArgs.__new__(IntegrationAccountCertificateArgs)
        __props__.__dict__['changed_time'] = None
        __props__.__dict__['created_time'] = None
        __props__.__dict__['key'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['metadata'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['public_certificate'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return IntegrationAccountCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='changedTime')
    def changed_time(self) -> pulumi.Output[str]:
        """
        The changed time.
        """
        return pulumi.get(self, 'changed_time')

    @property
    @pulumi.getter(name='createdTime')
    def created_time(self) -> pulumi.Output[str]:
        """
        The created time.
        """
        return pulumi.get(self, 'created_time')

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[Optional['outputs.KeyVaultKeyReferenceResponse']]:
        """
        The key details in the key vault.
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Any]]:
        """
        The metadata.
        """
        return pulumi.get(self, 'metadata')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='publicCertificate')
    def public_certificate(self) -> pulumi.Output[Optional[str]]:
        """
        The public certificate.
        """
        return pulumi.get(self, 'public_certificate')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Gets the resource type.
        """
        return pulumi.get(self, 'type')
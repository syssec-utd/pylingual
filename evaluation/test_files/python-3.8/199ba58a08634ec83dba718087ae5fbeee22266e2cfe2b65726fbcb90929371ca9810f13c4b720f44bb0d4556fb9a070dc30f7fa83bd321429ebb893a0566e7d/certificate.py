import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['CertificateArgs', 'Certificate']

@pulumi.input_type
class CertificateArgs:

    def __init__(__self__, *, automation_account_name: pulumi.Input[str], base64_value: pulumi.Input[str], name: pulumi.Input[str], resource_group_name: pulumi.Input[str], certificate_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, is_exportable: Optional[pulumi.Input[bool]]=None, thumbprint: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Certificate resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] base64_value: Gets or sets the base64 encoded value of the certificate.
        :param pulumi.Input[str] name: Gets or sets the name of the certificate.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] certificate_name: The parameters supplied to the create or update certificate operation.
        :param pulumi.Input[str] description: Gets or sets the description of the certificate.
        :param pulumi.Input[bool] is_exportable: Gets or sets the is exportable flag of the certificate.
        :param pulumi.Input[str] thumbprint: Gets or sets the thumbprint of the certificate.
        """
        pulumi.set(__self__, 'automation_account_name', automation_account_name)
        pulumi.set(__self__, 'base64_value', base64_value)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if certificate_name is not None:
            pulumi.set(__self__, 'certificate_name', certificate_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if is_exportable is not None:
            pulumi.set(__self__, 'is_exportable', is_exportable)
        if thumbprint is not None:
            pulumi.set(__self__, 'thumbprint', thumbprint)

    @property
    @pulumi.getter(name='automationAccountName')
    def automation_account_name(self) -> pulumi.Input[str]:
        """
        The name of the automation account.
        """
        return pulumi.get(self, 'automation_account_name')

    @automation_account_name.setter
    def automation_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'automation_account_name', value)

    @property
    @pulumi.getter(name='base64Value')
    def base64_value(self) -> pulumi.Input[str]:
        """
        Gets or sets the base64 encoded value of the certificate.
        """
        return pulumi.get(self, 'base64_value')

    @base64_value.setter
    def base64_value(self, value: pulumi.Input[str]):
        pulumi.set(self, 'base64_value', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Gets or sets the name of the certificate.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure Resource group.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='certificateName')
    def certificate_name(self) -> Optional[pulumi.Input[str]]:
        """
        The parameters supplied to the create or update certificate operation.
        """
        return pulumi.get(self, 'certificate_name')

    @certificate_name.setter
    def certificate_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'certificate_name', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the description of the certificate.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='isExportable')
    def is_exportable(self) -> Optional[pulumi.Input[bool]]:
        """
        Gets or sets the is exportable flag of the certificate.
        """
        return pulumi.get(self, 'is_exportable')

    @is_exportable.setter
    def is_exportable(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_exportable', value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the thumbprint of the certificate.
        """
        return pulumi.get(self, 'thumbprint')

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'thumbprint', value)

class Certificate(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, automation_account_name: Optional[pulumi.Input[str]]=None, base64_value: Optional[pulumi.Input[str]]=None, certificate_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, is_exportable: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, thumbprint: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Definition of the certificate.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] base64_value: Gets or sets the base64 encoded value of the certificate.
        :param pulumi.Input[str] certificate_name: The parameters supplied to the create or update certificate operation.
        :param pulumi.Input[str] description: Gets or sets the description of the certificate.
        :param pulumi.Input[bool] is_exportable: Gets or sets the is exportable flag of the certificate.
        :param pulumi.Input[str] name: Gets or sets the name of the certificate.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] thumbprint: Gets or sets the thumbprint of the certificate.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: CertificateArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Definition of the certificate.

        :param str resource_name: The name of the resource.
        :param CertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(CertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, automation_account_name: Optional[pulumi.Input[str]]=None, base64_value: Optional[pulumi.Input[str]]=None, certificate_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, is_exportable: Optional[pulumi.Input[bool]]=None, name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, thumbprint: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CertificateArgs.__new__(CertificateArgs)
            if automation_account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'automation_account_name'")
            __props__.__dict__['automation_account_name'] = automation_account_name
            if base64_value is None and (not opts.urn):
                raise TypeError("Missing required property 'base64_value'")
            __props__.__dict__['base64_value'] = base64_value
            __props__.__dict__['certificate_name'] = certificate_name
            __props__.__dict__['description'] = description
            __props__.__dict__['is_exportable'] = is_exportable
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['thumbprint'] = thumbprint
            __props__.__dict__['creation_time'] = None
            __props__.__dict__['expiry_time'] = None
            __props__.__dict__['last_modified_time'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:automation:Certificate'), pulumi.Alias(type_='azure-native:automation/v20151031:Certificate'), pulumi.Alias(type_='azure-native:automation/v20190601:Certificate'), pulumi.Alias(type_='azure-native:automation/v20220808:Certificate')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Certificate, __self__).__init__('azure-native:automation/v20200113preview:Certificate', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Certificate':
        """
        Get an existing Certificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = CertificateArgs.__new__(CertificateArgs)
        __props__.__dict__['creation_time'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['expiry_time'] = None
        __props__.__dict__['is_exportable'] = None
        __props__.__dict__['last_modified_time'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['thumbprint'] = None
        __props__.__dict__['type'] = None
        return Certificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='creationTime')
    def creation_time(self) -> pulumi.Output[str]:
        """
        Gets the creation time.
        """
        return pulumi.get(self, 'creation_time')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='expiryTime')
    def expiry_time(self) -> pulumi.Output[str]:
        """
        Gets the expiry time of the certificate.
        """
        return pulumi.get(self, 'expiry_time')

    @property
    @pulumi.getter(name='isExportable')
    def is_exportable(self) -> pulumi.Output[bool]:
        """
        Gets the is exportable flag of the certificate.
        """
        return pulumi.get(self, 'is_exportable')

    @property
    @pulumi.getter(name='lastModifiedTime')
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Gets the last modified time.
        """
        return pulumi.get(self, 'last_modified_time')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def thumbprint(self) -> pulumi.Output[str]:
        """
        Gets the thumbprint of the certificate.
        """
        return pulumi.get(self, 'thumbprint')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')
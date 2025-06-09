import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['GatewayHostnameConfigurationArgs', 'GatewayHostnameConfiguration']

@pulumi.input_type
class GatewayHostnameConfigurationArgs:

    def __init__(__self__, *, gateway_id: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_name: pulumi.Input[str], certificate_id: Optional[pulumi.Input[str]]=None, hc_id: Optional[pulumi.Input[str]]=None, hostname: Optional[pulumi.Input[str]]=None, http2_enabled: Optional[pulumi.Input[bool]]=None, negotiate_client_certificate: Optional[pulumi.Input[bool]]=None, tls10_enabled: Optional[pulumi.Input[bool]]=None, tls11_enabled: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a GatewayHostnameConfiguration resource.
        :param pulumi.Input[str] gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] certificate_id: Identifier of Certificate entity that will be used for TLS connection establishment
        :param pulumi.Input[str] hc_id: Gateway hostname configuration identifier. Must be unique in the scope of parent Gateway entity.
        :param pulumi.Input[str] hostname: Hostname value. Supports valid domain name, partial or full wildcard
        :param pulumi.Input[bool] http2_enabled: Specifies if HTTP/2.0 is supported
        :param pulumi.Input[bool] negotiate_client_certificate: Determines whether gateway requests client certificate
        :param pulumi.Input[bool] tls10_enabled: Specifies if TLS 1.0 is supported
        :param pulumi.Input[bool] tls11_enabled: Specifies if TLS 1.1 is supported
        """
        pulumi.set(__self__, 'gateway_id', gateway_id)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_name', service_name)
        if certificate_id is not None:
            pulumi.set(__self__, 'certificate_id', certificate_id)
        if hc_id is not None:
            pulumi.set(__self__, 'hc_id', hc_id)
        if hostname is not None:
            pulumi.set(__self__, 'hostname', hostname)
        if http2_enabled is not None:
            pulumi.set(__self__, 'http2_enabled', http2_enabled)
        if negotiate_client_certificate is not None:
            pulumi.set(__self__, 'negotiate_client_certificate', negotiate_client_certificate)
        if tls10_enabled is not None:
            pulumi.set(__self__, 'tls10_enabled', tls10_enabled)
        if tls11_enabled is not None:
            pulumi.set(__self__, 'tls11_enabled', tls11_enabled)

    @property
    @pulumi.getter(name='gatewayId')
    def gateway_id(self) -> pulumi.Input[str]:
        """
        Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
        """
        return pulumi.get(self, 'gateway_id')

    @gateway_id.setter
    def gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'gateway_id', value)

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
    @pulumi.getter(name='serviceName')
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, 'service_name')

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'service_name', value)

    @property
    @pulumi.getter(name='certificateId')
    def certificate_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of Certificate entity that will be used for TLS connection establishment
        """
        return pulumi.get(self, 'certificate_id')

    @certificate_id.setter
    def certificate_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'certificate_id', value)

    @property
    @pulumi.getter(name='hcId')
    def hc_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gateway hostname configuration identifier. Must be unique in the scope of parent Gateway entity.
        """
        return pulumi.get(self, 'hc_id')

    @hc_id.setter
    def hc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'hc_id', value)

    @property
    @pulumi.getter
    def hostname(self) -> Optional[pulumi.Input[str]]:
        """
        Hostname value. Supports valid domain name, partial or full wildcard
        """
        return pulumi.get(self, 'hostname')

    @hostname.setter
    def hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'hostname', value)

    @property
    @pulumi.getter(name='http2Enabled')
    def http2_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if HTTP/2.0 is supported
        """
        return pulumi.get(self, 'http2_enabled')

    @http2_enabled.setter
    def http2_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'http2_enabled', value)

    @property
    @pulumi.getter(name='negotiateClientCertificate')
    def negotiate_client_certificate(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether gateway requests client certificate
        """
        return pulumi.get(self, 'negotiate_client_certificate')

    @negotiate_client_certificate.setter
    def negotiate_client_certificate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'negotiate_client_certificate', value)

    @property
    @pulumi.getter(name='tls10Enabled')
    def tls10_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if TLS 1.0 is supported
        """
        return pulumi.get(self, 'tls10_enabled')

    @tls10_enabled.setter
    def tls10_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'tls10_enabled', value)

    @property
    @pulumi.getter(name='tls11Enabled')
    def tls11_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies if TLS 1.1 is supported
        """
        return pulumi.get(self, 'tls11_enabled')

    @tls11_enabled.setter
    def tls11_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'tls11_enabled', value)

class GatewayHostnameConfiguration(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, certificate_id: Optional[pulumi.Input[str]]=None, gateway_id: Optional[pulumi.Input[str]]=None, hc_id: Optional[pulumi.Input[str]]=None, hostname: Optional[pulumi.Input[str]]=None, http2_enabled: Optional[pulumi.Input[bool]]=None, negotiate_client_certificate: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, tls10_enabled: Optional[pulumi.Input[bool]]=None, tls11_enabled: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        Gateway hostname configuration details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_id: Identifier of Certificate entity that will be used for TLS connection establishment
        :param pulumi.Input[str] gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
        :param pulumi.Input[str] hc_id: Gateway hostname configuration identifier. Must be unique in the scope of parent Gateway entity.
        :param pulumi.Input[str] hostname: Hostname value. Supports valid domain name, partial or full wildcard
        :param pulumi.Input[bool] http2_enabled: Specifies if HTTP/2.0 is supported
        :param pulumi.Input[bool] negotiate_client_certificate: Determines whether gateway requests client certificate
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[bool] tls10_enabled: Specifies if TLS 1.0 is supported
        :param pulumi.Input[bool] tls11_enabled: Specifies if TLS 1.1 is supported
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: GatewayHostnameConfigurationArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Gateway hostname configuration details.

        :param str resource_name: The name of the resource.
        :param GatewayHostnameConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(GatewayHostnameConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, certificate_id: Optional[pulumi.Input[str]]=None, gateway_id: Optional[pulumi.Input[str]]=None, hc_id: Optional[pulumi.Input[str]]=None, hostname: Optional[pulumi.Input[str]]=None, http2_enabled: Optional[pulumi.Input[bool]]=None, negotiate_client_certificate: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, tls10_enabled: Optional[pulumi.Input[bool]]=None, tls11_enabled: Optional[pulumi.Input[bool]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GatewayHostnameConfigurationArgs.__new__(GatewayHostnameConfigurationArgs)
            __props__.__dict__['certificate_id'] = certificate_id
            if gateway_id is None and (not opts.urn):
                raise TypeError("Missing required property 'gateway_id'")
            __props__.__dict__['gateway_id'] = gateway_id
            __props__.__dict__['hc_id'] = hc_id
            __props__.__dict__['hostname'] = hostname
            __props__.__dict__['http2_enabled'] = http2_enabled
            __props__.__dict__['negotiate_client_certificate'] = negotiate_client_certificate
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__['service_name'] = service_name
            __props__.__dict__['tls10_enabled'] = tls10_enabled
            __props__.__dict__['tls11_enabled'] = tls11_enabled
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:apimanagement:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20191201:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20191201preview:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20200601preview:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20201201:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20210401preview:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20210801:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20211201preview:GatewayHostnameConfiguration'), pulumi.Alias(type_='azure-native:apimanagement/v20220401preview:GatewayHostnameConfiguration')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GatewayHostnameConfiguration, __self__).__init__('azure-native:apimanagement/v20210101preview:GatewayHostnameConfiguration', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'GatewayHostnameConfiguration':
        """
        Get an existing GatewayHostnameConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = GatewayHostnameConfigurationArgs.__new__(GatewayHostnameConfigurationArgs)
        __props__.__dict__['certificate_id'] = None
        __props__.__dict__['hostname'] = None
        __props__.__dict__['http2_enabled'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['negotiate_client_certificate'] = None
        __props__.__dict__['tls10_enabled'] = None
        __props__.__dict__['tls11_enabled'] = None
        __props__.__dict__['type'] = None
        return GatewayHostnameConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='certificateId')
    def certificate_id(self) -> pulumi.Output[Optional[str]]:
        """
        Identifier of Certificate entity that will be used for TLS connection establishment
        """
        return pulumi.get(self, 'certificate_id')

    @property
    @pulumi.getter
    def hostname(self) -> pulumi.Output[Optional[str]]:
        """
        Hostname value. Supports valid domain name, partial or full wildcard
        """
        return pulumi.get(self, 'hostname')

    @property
    @pulumi.getter(name='http2Enabled')
    def http2_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if HTTP/2.0 is supported
        """
        return pulumi.get(self, 'http2_enabled')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='negotiateClientCertificate')
    def negotiate_client_certificate(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines whether gateway requests client certificate
        """
        return pulumi.get(self, 'negotiate_client_certificate')

    @property
    @pulumi.getter(name='tls10Enabled')
    def tls10_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if TLS 1.0 is supported
        """
        return pulumi.get(self, 'tls10_enabled')

    @property
    @pulumi.getter(name='tls11Enabled')
    def tls11_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies if TLS 1.1 is supported
        """
        return pulumi.get(self, 'tls11_enabled')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, 'type')
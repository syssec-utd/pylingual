import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['ApiPortalCustomDomainArgs', 'ApiPortalCustomDomain']

@pulumi.input_type
class ApiPortalCustomDomainArgs:

    def __init__(__self__, *, api_portal_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_name: pulumi.Input[str], domain_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input['ApiPortalCustomDomainPropertiesArgs']]=None):
        """
        The set of arguments for constructing a ApiPortalCustomDomain resource.
        :param pulumi.Input[str] api_portal_name: The name of API portal.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] service_name: The name of the Service resource.
        :param pulumi.Input[str] domain_name: The name of the API portal custom domain.
        :param pulumi.Input['ApiPortalCustomDomainPropertiesArgs'] properties: The properties of custom domain for API portal
        """
        pulumi.set(__self__, 'api_portal_name', api_portal_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_name', service_name)
        if domain_name is not None:
            pulumi.set(__self__, 'domain_name', domain_name)
        if properties is not None:
            pulumi.set(__self__, 'properties', properties)

    @property
    @pulumi.getter(name='apiPortalName')
    def api_portal_name(self) -> pulumi.Input[str]:
        """
        The name of API portal.
        """
        return pulumi.get(self, 'api_portal_name')

    @api_portal_name.setter
    def api_portal_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'api_portal_name', value)

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
    @pulumi.getter(name='serviceName')
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the Service resource.
        """
        return pulumi.get(self, 'service_name')

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'service_name', value)

    @property
    @pulumi.getter(name='domainName')
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API portal custom domain.
        """
        return pulumi.get(self, 'domain_name')

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'domain_name', value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ApiPortalCustomDomainPropertiesArgs']]:
        """
        The properties of custom domain for API portal
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ApiPortalCustomDomainPropertiesArgs']]):
        pulumi.set(self, 'properties', value)

class ApiPortalCustomDomain(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_portal_name: Optional[pulumi.Input[str]]=None, domain_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['ApiPortalCustomDomainPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Custom domain of the API portal

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_portal_name: The name of API portal.
        :param pulumi.Input[str] domain_name: The name of the API portal custom domain.
        :param pulumi.Input[pulumi.InputType['ApiPortalCustomDomainPropertiesArgs']] properties: The properties of custom domain for API portal
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] service_name: The name of the Service resource.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ApiPortalCustomDomainArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Custom domain of the API portal

        :param str resource_name: The name of the resource.
        :param ApiPortalCustomDomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ApiPortalCustomDomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_portal_name: Optional[pulumi.Input[str]]=None, domain_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['ApiPortalCustomDomainPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiPortalCustomDomainArgs.__new__(ApiPortalCustomDomainArgs)
            if api_portal_name is None and (not opts.urn):
                raise TypeError("Missing required property 'api_portal_name'")
            __props__.__dict__['api_portal_name'] = api_portal_name
            __props__.__dict__['domain_name'] = domain_name
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__['service_name'] = service_name
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:appplatform:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20220101preview:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20220301preview:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20220901preview:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20221101preview:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20221201:ApiPortalCustomDomain'), pulumi.Alias(type_='azure-native:appplatform/v20230101preview:ApiPortalCustomDomain')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApiPortalCustomDomain, __self__).__init__('azure-native:appplatform/v20220501preview:ApiPortalCustomDomain', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ApiPortalCustomDomain':
        """
        Get an existing ApiPortalCustomDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ApiPortalCustomDomainArgs.__new__(ApiPortalCustomDomainArgs)
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return ApiPortalCustomDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ApiPortalCustomDomainPropertiesResponse']:
        """
        The properties of custom domain for API portal
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')
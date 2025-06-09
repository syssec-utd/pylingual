import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['ProductApiArgs', 'ProductApi']

@pulumi.input_type
class ProductApiArgs:

    def __init__(__self__, *, product_id: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_name: pulumi.Input[str], api_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a ProductApi resource.
        :param pulumi.Input[str] product_id: Product identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        """
        pulumi.set(__self__, 'product_id', product_id)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_name', service_name)
        if api_id is not None:
            pulumi.set(__self__, 'api_id', api_id)

    @property
    @pulumi.getter(name='productId')
    def product_id(self) -> pulumi.Input[str]:
        """
        Product identifier. Must be unique in the current API Management service instance.
        """
        return pulumi.get(self, 'product_id')

    @product_id.setter
    def product_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'product_id', value)

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
    @pulumi.getter(name='apiId')
    def api_id(self) -> Optional[pulumi.Input[str]]:
        """
        API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        """
        return pulumi.get(self, 'api_id')

    @api_id.setter
    def api_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_id', value)

class ProductApi(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_id: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Api details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] product_id: Product identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ProductApiArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Api details.

        :param str resource_name: The name of the resource.
        :param ProductApiArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ProductApiArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_id: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProductApiArgs.__new__(ProductApiArgs)
            __props__.__dict__['api_id'] = api_id
            if product_id is None and (not opts.urn):
                raise TypeError("Missing required property 'product_id'")
            __props__.__dict__['product_id'] = product_id
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__['service_name'] = service_name
            __props__.__dict__['api_revision'] = None
            __props__.__dict__['api_revision_description'] = None
            __props__.__dict__['api_type'] = None
            __props__.__dict__['api_version'] = None
            __props__.__dict__['api_version_description'] = None
            __props__.__dict__['api_version_set'] = None
            __props__.__dict__['api_version_set_id'] = None
            __props__.__dict__['authentication_settings'] = None
            __props__.__dict__['description'] = None
            __props__.__dict__['display_name'] = None
            __props__.__dict__['is_current'] = None
            __props__.__dict__['is_online'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['path'] = None
            __props__.__dict__['protocols'] = None
            __props__.__dict__['service_url'] = None
            __props__.__dict__['source_api_id'] = None
            __props__.__dict__['subscription_key_parameter_names'] = None
            __props__.__dict__['subscription_required'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:apimanagement:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20170301:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20180101:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20180601preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20191201:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20191201preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20200601preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20201201:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20210101preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20210401preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20210801:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20211201preview:ProductApi'), pulumi.Alias(type_='azure-native:apimanagement/v20220401preview:ProductApi')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ProductApi, __self__).__init__('azure-native:apimanagement/v20190101:ProductApi', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ProductApi':
        """
        Get an existing ProductApi resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ProductApiArgs.__new__(ProductApiArgs)
        __props__.__dict__['api_revision'] = None
        __props__.__dict__['api_revision_description'] = None
        __props__.__dict__['api_type'] = None
        __props__.__dict__['api_version'] = None
        __props__.__dict__['api_version_description'] = None
        __props__.__dict__['api_version_set'] = None
        __props__.__dict__['api_version_set_id'] = None
        __props__.__dict__['authentication_settings'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['is_current'] = None
        __props__.__dict__['is_online'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['path'] = None
        __props__.__dict__['protocols'] = None
        __props__.__dict__['service_url'] = None
        __props__.__dict__['source_api_id'] = None
        __props__.__dict__['subscription_key_parameter_names'] = None
        __props__.__dict__['subscription_required'] = None
        __props__.__dict__['type'] = None
        return ProductApi(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='apiRevision')
    def api_revision(self) -> pulumi.Output[Optional[str]]:
        """
        Describes the Revision of the Api. If no value is provided, default revision 1 is created
        """
        return pulumi.get(self, 'api_revision')

    @property
    @pulumi.getter(name='apiRevisionDescription')
    def api_revision_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Api Revision.
        """
        return pulumi.get(self, 'api_revision_description')

    @property
    @pulumi.getter(name='apiType')
    def api_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of API.
        """
        return pulumi.get(self, 'api_type')

    @property
    @pulumi.getter(name='apiVersion')
    def api_version(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the Version identifier of the API if the API is versioned
        """
        return pulumi.get(self, 'api_version')

    @property
    @pulumi.getter(name='apiVersionDescription')
    def api_version_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the Api Version.
        """
        return pulumi.get(self, 'api_version_description')

    @property
    @pulumi.getter(name='apiVersionSet')
    def api_version_set(self) -> pulumi.Output[Optional['outputs.ApiVersionSetContractDetailsResponse']]:
        """
        Version set details
        """
        return pulumi.get(self, 'api_version_set')

    @property
    @pulumi.getter(name='apiVersionSetId')
    def api_version_set_id(self) -> pulumi.Output[Optional[str]]:
        """
        A resource identifier for the related ApiVersionSet.
        """
        return pulumi.get(self, 'api_version_set_id')

    @property
    @pulumi.getter(name='authenticationSettings')
    def authentication_settings(self) -> pulumi.Output[Optional['outputs.AuthenticationSettingsContractResponse']]:
        """
        Collection of authentication settings included into this API.
        """
        return pulumi.get(self, 'authentication_settings')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the API. May include HTML formatting tags.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        API name. Must be 1 to 300 characters long.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='isCurrent')
    def is_current(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates if API revision is current api revision.
        """
        return pulumi.get(self, 'is_current')

    @property
    @pulumi.getter(name='isOnline')
    def is_online(self) -> pulumi.Output[bool]:
        """
        Indicates if API revision is accessible via the gateway.
        """
        return pulumi.get(self, 'is_online')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def path(self) -> pulumi.Output[str]:
        """
        Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        """
        return pulumi.get(self, 'path')

    @property
    @pulumi.getter
    def protocols(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Describes on which protocols the operations in this API can be invoked.
        """
        return pulumi.get(self, 'protocols')

    @property
    @pulumi.getter(name='serviceUrl')
    def service_url(self) -> pulumi.Output[Optional[str]]:
        """
        Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        """
        return pulumi.get(self, 'service_url')

    @property
    @pulumi.getter(name='sourceApiId')
    def source_api_id(self) -> pulumi.Output[Optional[str]]:
        """
        API identifier of the source API.
        """
        return pulumi.get(self, 'source_api_id')

    @property
    @pulumi.getter(name='subscriptionKeyParameterNames')
    def subscription_key_parameter_names(self) -> pulumi.Output[Optional['outputs.SubscriptionKeyParameterNamesContractResponse']]:
        """
        Protocols over which API is made available.
        """
        return pulumi.get(self, 'subscription_key_parameter_names')

    @property
    @pulumi.getter(name='subscriptionRequired')
    def subscription_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether an API or Product subscription is required for accessing the API.
        """
        return pulumi.get(self, 'subscription_required')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, 'type')
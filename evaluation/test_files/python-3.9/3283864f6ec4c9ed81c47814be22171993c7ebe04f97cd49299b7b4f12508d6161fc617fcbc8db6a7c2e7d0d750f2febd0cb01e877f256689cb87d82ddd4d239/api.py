import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ApiArgs', 'Api']

@pulumi.input_type
class ApiArgs:

    def __init__(__self__, *, path: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_name: pulumi.Input[str], api_id: Optional[pulumi.Input[str]]=None, api_revision: Optional[pulumi.Input[str]]=None, api_revision_description: Optional[pulumi.Input[str]]=None, api_type: Optional[pulumi.Input[Union[str, 'ApiType']]]=None, api_version: Optional[pulumi.Input[str]]=None, api_version_description: Optional[pulumi.Input[str]]=None, api_version_set: Optional[pulumi.Input['ApiVersionSetContractDetailsArgs']]=None, api_version_set_id: Optional[pulumi.Input[str]]=None, authentication_settings: Optional[pulumi.Input['AuthenticationSettingsContractArgs']]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, format: Optional[pulumi.Input[Union[str, 'ContentFormat']]]=None, is_current: Optional[pulumi.Input[bool]]=None, protocols: Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]]=None, service_url: Optional[pulumi.Input[str]]=None, soap_api_type: Optional[pulumi.Input[Union[str, 'SoapApiType']]]=None, source_api_id: Optional[pulumi.Input[str]]=None, subscription_key_parameter_names: Optional[pulumi.Input['SubscriptionKeyParameterNamesContractArgs']]=None, subscription_required: Optional[pulumi.Input[bool]]=None, value: Optional[pulumi.Input[str]]=None, wsdl_selector: Optional[pulumi.Input['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]=None):
        """
        The set of arguments for constructing a Api resource.
        :param pulumi.Input[str] path: Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] api_revision: Describes the Revision of the Api. If no value is provided, default revision 1 is created
        :param pulumi.Input[str] api_revision_description: Description of the Api Revision.
        :param pulumi.Input[Union[str, 'ApiType']] api_type: Type of API.
        :param pulumi.Input[str] api_version: Indicates the Version identifier of the API if the API is versioned
        :param pulumi.Input[str] api_version_description: Description of the Api Version.
        :param pulumi.Input['ApiVersionSetContractDetailsArgs'] api_version_set: Version set details
        :param pulumi.Input[str] api_version_set_id: A resource identifier for the related ApiVersionSet.
        :param pulumi.Input['AuthenticationSettingsContractArgs'] authentication_settings: Collection of authentication settings included into this API.
        :param pulumi.Input[str] description: Description of the API. May include HTML formatting tags.
        :param pulumi.Input[str] display_name: API name. Must be 1 to 300 characters long.
        :param pulumi.Input[Union[str, 'ContentFormat']] format: Format of the Content in which the API is getting imported.
        :param pulumi.Input[bool] is_current: Indicates if API revision is current api revision.
        :param pulumi.Input[Sequence[pulumi.Input['Protocol']]] protocols: Describes on which protocols the operations in this API can be invoked.
        :param pulumi.Input[str] service_url: Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        :param pulumi.Input[Union[str, 'SoapApiType']] soap_api_type: Type of Api to create. 
                * `http` creates a SOAP to REST API 
                * `soap` creates a SOAP pass-through API .
        :param pulumi.Input[str] source_api_id: API identifier of the source API.
        :param pulumi.Input['SubscriptionKeyParameterNamesContractArgs'] subscription_key_parameter_names: Protocols over which API is made available.
        :param pulumi.Input[bool] subscription_required: Specifies whether an API or Product subscription is required for accessing the API.
        :param pulumi.Input[str] value: Content value when Importing an API.
        :param pulumi.Input['ApiCreateOrUpdatePropertiesWsdlSelectorArgs'] wsdl_selector: Criteria to limit import of WSDL to a subset of the document.
        """
        pulumi.set(__self__, 'path', path)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_name', service_name)
        if api_id is not None:
            pulumi.set(__self__, 'api_id', api_id)
        if api_revision is not None:
            pulumi.set(__self__, 'api_revision', api_revision)
        if api_revision_description is not None:
            pulumi.set(__self__, 'api_revision_description', api_revision_description)
        if api_type is not None:
            pulumi.set(__self__, 'api_type', api_type)
        if api_version is not None:
            pulumi.set(__self__, 'api_version', api_version)
        if api_version_description is not None:
            pulumi.set(__self__, 'api_version_description', api_version_description)
        if api_version_set is not None:
            pulumi.set(__self__, 'api_version_set', api_version_set)
        if api_version_set_id is not None:
            pulumi.set(__self__, 'api_version_set_id', api_version_set_id)
        if authentication_settings is not None:
            pulumi.set(__self__, 'authentication_settings', authentication_settings)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if format is not None:
            pulumi.set(__self__, 'format', format)
        if is_current is not None:
            pulumi.set(__self__, 'is_current', is_current)
        if protocols is not None:
            pulumi.set(__self__, 'protocols', protocols)
        if service_url is not None:
            pulumi.set(__self__, 'service_url', service_url)
        if soap_api_type is not None:
            pulumi.set(__self__, 'soap_api_type', soap_api_type)
        if source_api_id is not None:
            pulumi.set(__self__, 'source_api_id', source_api_id)
        if subscription_key_parameter_names is not None:
            pulumi.set(__self__, 'subscription_key_parameter_names', subscription_key_parameter_names)
        if subscription_required is not None:
            pulumi.set(__self__, 'subscription_required', subscription_required)
        if value is not None:
            pulumi.set(__self__, 'value', value)
        if wsdl_selector is not None:
            pulumi.set(__self__, 'wsdl_selector', wsdl_selector)

    @property
    @pulumi.getter
    def path(self) -> pulumi.Input[str]:
        """
        Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        """
        return pulumi.get(self, 'path')

    @path.setter
    def path(self, value: pulumi.Input[str]):
        pulumi.set(self, 'path', value)

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

    @property
    @pulumi.getter(name='apiRevision')
    def api_revision(self) -> Optional[pulumi.Input[str]]:
        """
        Describes the Revision of the Api. If no value is provided, default revision 1 is created
        """
        return pulumi.get(self, 'api_revision')

    @api_revision.setter
    def api_revision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_revision', value)

    @property
    @pulumi.getter(name='apiRevisionDescription')
    def api_revision_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Api Revision.
        """
        return pulumi.get(self, 'api_revision_description')

    @api_revision_description.setter
    def api_revision_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_revision_description', value)

    @property
    @pulumi.getter(name='apiType')
    def api_type(self) -> Optional[pulumi.Input[Union[str, 'ApiType']]]:
        """
        Type of API.
        """
        return pulumi.get(self, 'api_type')

    @api_type.setter
    def api_type(self, value: Optional[pulumi.Input[Union[str, 'ApiType']]]):
        pulumi.set(self, 'api_type', value)

    @property
    @pulumi.getter(name='apiVersion')
    def api_version(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the Version identifier of the API if the API is versioned
        """
        return pulumi.get(self, 'api_version')

    @api_version.setter
    def api_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_version', value)

    @property
    @pulumi.getter(name='apiVersionDescription')
    def api_version_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the Api Version.
        """
        return pulumi.get(self, 'api_version_description')

    @api_version_description.setter
    def api_version_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_version_description', value)

    @property
    @pulumi.getter(name='apiVersionSet')
    def api_version_set(self) -> Optional[pulumi.Input['ApiVersionSetContractDetailsArgs']]:
        """
        Version set details
        """
        return pulumi.get(self, 'api_version_set')

    @api_version_set.setter
    def api_version_set(self, value: Optional[pulumi.Input['ApiVersionSetContractDetailsArgs']]):
        pulumi.set(self, 'api_version_set', value)

    @property
    @pulumi.getter(name='apiVersionSetId')
    def api_version_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        A resource identifier for the related ApiVersionSet.
        """
        return pulumi.get(self, 'api_version_set_id')

    @api_version_set_id.setter
    def api_version_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_version_set_id', value)

    @property
    @pulumi.getter(name='authenticationSettings')
    def authentication_settings(self) -> Optional[pulumi.Input['AuthenticationSettingsContractArgs']]:
        """
        Collection of authentication settings included into this API.
        """
        return pulumi.get(self, 'authentication_settings')

    @authentication_settings.setter
    def authentication_settings(self, value: Optional[pulumi.Input['AuthenticationSettingsContractArgs']]):
        pulumi.set(self, 'authentication_settings', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the API. May include HTML formatting tags.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        API name. Must be 1 to 300 characters long.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def format(self) -> Optional[pulumi.Input[Union[str, 'ContentFormat']]]:
        """
        Format of the Content in which the API is getting imported.
        """
        return pulumi.get(self, 'format')

    @format.setter
    def format(self, value: Optional[pulumi.Input[Union[str, 'ContentFormat']]]):
        pulumi.set(self, 'format', value)

    @property
    @pulumi.getter(name='isCurrent')
    def is_current(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if API revision is current api revision.
        """
        return pulumi.get(self, 'is_current')

    @is_current.setter
    def is_current(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'is_current', value)

    @property
    @pulumi.getter
    def protocols(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]]:
        """
        Describes on which protocols the operations in this API can be invoked.
        """
        return pulumi.get(self, 'protocols')

    @protocols.setter
    def protocols(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]]):
        pulumi.set(self, 'protocols', value)

    @property
    @pulumi.getter(name='serviceUrl')
    def service_url(self) -> Optional[pulumi.Input[str]]:
        """
        Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        """
        return pulumi.get(self, 'service_url')

    @service_url.setter
    def service_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'service_url', value)

    @property
    @pulumi.getter(name='soapApiType')
    def soap_api_type(self) -> Optional[pulumi.Input[Union[str, 'SoapApiType']]]:
        """
        Type of Api to create. 
         * `http` creates a SOAP to REST API 
         * `soap` creates a SOAP pass-through API .
        """
        return pulumi.get(self, 'soap_api_type')

    @soap_api_type.setter
    def soap_api_type(self, value: Optional[pulumi.Input[Union[str, 'SoapApiType']]]):
        pulumi.set(self, 'soap_api_type', value)

    @property
    @pulumi.getter(name='sourceApiId')
    def source_api_id(self) -> Optional[pulumi.Input[str]]:
        """
        API identifier of the source API.
        """
        return pulumi.get(self, 'source_api_id')

    @source_api_id.setter
    def source_api_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'source_api_id', value)

    @property
    @pulumi.getter(name='subscriptionKeyParameterNames')
    def subscription_key_parameter_names(self) -> Optional[pulumi.Input['SubscriptionKeyParameterNamesContractArgs']]:
        """
        Protocols over which API is made available.
        """
        return pulumi.get(self, 'subscription_key_parameter_names')

    @subscription_key_parameter_names.setter
    def subscription_key_parameter_names(self, value: Optional[pulumi.Input['SubscriptionKeyParameterNamesContractArgs']]):
        pulumi.set(self, 'subscription_key_parameter_names', value)

    @property
    @pulumi.getter(name='subscriptionRequired')
    def subscription_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether an API or Product subscription is required for accessing the API.
        """
        return pulumi.get(self, 'subscription_required')

    @subscription_required.setter
    def subscription_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'subscription_required', value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Content value when Importing an API.
        """
        return pulumi.get(self, 'value')

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'value', value)

    @property
    @pulumi.getter(name='wsdlSelector')
    def wsdl_selector(self) -> Optional[pulumi.Input['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]:
        """
        Criteria to limit import of WSDL to a subset of the document.
        """
        return pulumi.get(self, 'wsdl_selector')

    @wsdl_selector.setter
    def wsdl_selector(self, value: Optional[pulumi.Input['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]):
        pulumi.set(self, 'wsdl_selector', value)

class Api(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_id: Optional[pulumi.Input[str]]=None, api_revision: Optional[pulumi.Input[str]]=None, api_revision_description: Optional[pulumi.Input[str]]=None, api_type: Optional[pulumi.Input[Union[str, 'ApiType']]]=None, api_version: Optional[pulumi.Input[str]]=None, api_version_description: Optional[pulumi.Input[str]]=None, api_version_set: Optional[pulumi.Input[pulumi.InputType['ApiVersionSetContractDetailsArgs']]]=None, api_version_set_id: Optional[pulumi.Input[str]]=None, authentication_settings: Optional[pulumi.Input[pulumi.InputType['AuthenticationSettingsContractArgs']]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, format: Optional[pulumi.Input[Union[str, 'ContentFormat']]]=None, is_current: Optional[pulumi.Input[bool]]=None, path: Optional[pulumi.Input[str]]=None, protocols: Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, service_url: Optional[pulumi.Input[str]]=None, soap_api_type: Optional[pulumi.Input[Union[str, 'SoapApiType']]]=None, source_api_id: Optional[pulumi.Input[str]]=None, subscription_key_parameter_names: Optional[pulumi.Input[pulumi.InputType['SubscriptionKeyParameterNamesContractArgs']]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, value: Optional[pulumi.Input[str]]=None, wsdl_selector: Optional[pulumi.Input[pulumi.InputType['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]]=None, __props__=None):
        """
        Api details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_id: API revision identifier. Must be unique in the current API Management service instance. Non-current revision has ;rev=n as a suffix where n is the revision number.
        :param pulumi.Input[str] api_revision: Describes the Revision of the Api. If no value is provided, default revision 1 is created
        :param pulumi.Input[str] api_revision_description: Description of the Api Revision.
        :param pulumi.Input[Union[str, 'ApiType']] api_type: Type of API.
        :param pulumi.Input[str] api_version: Indicates the Version identifier of the API if the API is versioned
        :param pulumi.Input[str] api_version_description: Description of the Api Version.
        :param pulumi.Input[pulumi.InputType['ApiVersionSetContractDetailsArgs']] api_version_set: Version set details
        :param pulumi.Input[str] api_version_set_id: A resource identifier for the related ApiVersionSet.
        :param pulumi.Input[pulumi.InputType['AuthenticationSettingsContractArgs']] authentication_settings: Collection of authentication settings included into this API.
        :param pulumi.Input[str] description: Description of the API. May include HTML formatting tags.
        :param pulumi.Input[str] display_name: API name. Must be 1 to 300 characters long.
        :param pulumi.Input[Union[str, 'ContentFormat']] format: Format of the Content in which the API is getting imported.
        :param pulumi.Input[bool] is_current: Indicates if API revision is current api revision.
        :param pulumi.Input[str] path: Relative URL uniquely identifying this API and all of its resource paths within the API Management service instance. It is appended to the API endpoint base URL specified during the service instance creation to form a public URL for this API.
        :param pulumi.Input[Sequence[pulumi.Input['Protocol']]] protocols: Describes on which protocols the operations in this API can be invoked.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] service_url: Absolute URL of the backend service implementing this API. Cannot be more than 2000 characters long.
        :param pulumi.Input[Union[str, 'SoapApiType']] soap_api_type: Type of Api to create. 
                * `http` creates a SOAP to REST API 
                * `soap` creates a SOAP pass-through API .
        :param pulumi.Input[str] source_api_id: API identifier of the source API.
        :param pulumi.Input[pulumi.InputType['SubscriptionKeyParameterNamesContractArgs']] subscription_key_parameter_names: Protocols over which API is made available.
        :param pulumi.Input[bool] subscription_required: Specifies whether an API or Product subscription is required for accessing the API.
        :param pulumi.Input[str] value: Content value when Importing an API.
        :param pulumi.Input[pulumi.InputType['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']] wsdl_selector: Criteria to limit import of WSDL to a subset of the document.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ApiArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Api details.

        :param str resource_name: The name of the resource.
        :param ApiArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ApiArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_id: Optional[pulumi.Input[str]]=None, api_revision: Optional[pulumi.Input[str]]=None, api_revision_description: Optional[pulumi.Input[str]]=None, api_type: Optional[pulumi.Input[Union[str, 'ApiType']]]=None, api_version: Optional[pulumi.Input[str]]=None, api_version_description: Optional[pulumi.Input[str]]=None, api_version_set: Optional[pulumi.Input[pulumi.InputType['ApiVersionSetContractDetailsArgs']]]=None, api_version_set_id: Optional[pulumi.Input[str]]=None, authentication_settings: Optional[pulumi.Input[pulumi.InputType['AuthenticationSettingsContractArgs']]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, format: Optional[pulumi.Input[Union[str, 'ContentFormat']]]=None, is_current: Optional[pulumi.Input[bool]]=None, path: Optional[pulumi.Input[str]]=None, protocols: Optional[pulumi.Input[Sequence[pulumi.Input['Protocol']]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, service_url: Optional[pulumi.Input[str]]=None, soap_api_type: Optional[pulumi.Input[Union[str, 'SoapApiType']]]=None, source_api_id: Optional[pulumi.Input[str]]=None, subscription_key_parameter_names: Optional[pulumi.Input[pulumi.InputType['SubscriptionKeyParameterNamesContractArgs']]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, value: Optional[pulumi.Input[str]]=None, wsdl_selector: Optional[pulumi.Input[pulumi.InputType['ApiCreateOrUpdatePropertiesWsdlSelectorArgs']]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApiArgs.__new__(ApiArgs)
            __props__.__dict__['api_id'] = api_id
            __props__.__dict__['api_revision'] = api_revision
            __props__.__dict__['api_revision_description'] = api_revision_description
            __props__.__dict__['api_type'] = api_type
            __props__.__dict__['api_version'] = api_version
            __props__.__dict__['api_version_description'] = api_version_description
            __props__.__dict__['api_version_set'] = api_version_set
            __props__.__dict__['api_version_set_id'] = api_version_set_id
            __props__.__dict__['authentication_settings'] = authentication_settings
            __props__.__dict__['description'] = description
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['format'] = format
            __props__.__dict__['is_current'] = is_current
            if path is None and (not opts.urn):
                raise TypeError("Missing required property 'path'")
            __props__.__dict__['path'] = path
            __props__.__dict__['protocols'] = protocols
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__['service_name'] = service_name
            __props__.__dict__['service_url'] = service_url
            __props__.__dict__['soap_api_type'] = soap_api_type
            __props__.__dict__['source_api_id'] = source_api_id
            __props__.__dict__['subscription_key_parameter_names'] = subscription_key_parameter_names
            __props__.__dict__['subscription_required'] = subscription_required
            __props__.__dict__['value'] = value
            __props__.__dict__['wsdl_selector'] = wsdl_selector
            __props__.__dict__['is_online'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:apimanagement:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20160707:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20161010:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20170301:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20180101:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20180601preview:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20190101:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20191201:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20200601preview:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20201201:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20210101preview:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20210401preview:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20210801:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20211201preview:Api'), pulumi.Alias(type_='azure-native:apimanagement/v20220401preview:Api')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Api, __self__).__init__('azure-native:apimanagement/v20191201preview:Api', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Api':
        """
        Get an existing Api resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ApiArgs.__new__(ApiArgs)
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
        return Api(resource_name, opts=opts, __props__=__props__)

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
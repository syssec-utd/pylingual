import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['GetPartnerRegistrationResult', 'AwaitableGetPartnerRegistrationResult', 'get_partner_registration', 'get_partner_registration_output']

@pulumi.output_type
class GetPartnerRegistrationResult:
    """
    Information about a partner registration.
    """

    def __init__(__self__, authorized_azure_subscription_ids=None, customer_service_uri=None, id=None, location=None, logo_uri=None, long_description=None, name=None, partner_customer_service_extension=None, partner_customer_service_number=None, partner_name=None, partner_resource_type_description=None, partner_resource_type_display_name=None, partner_resource_type_name=None, provisioning_state=None, setup_uri=None, system_data=None, tags=None, type=None, visibility_state=None):
        if authorized_azure_subscription_ids and (not isinstance(authorized_azure_subscription_ids, list)):
            raise TypeError("Expected argument 'authorized_azure_subscription_ids' to be a list")
        pulumi.set(__self__, 'authorized_azure_subscription_ids', authorized_azure_subscription_ids)
        if customer_service_uri and (not isinstance(customer_service_uri, str)):
            raise TypeError("Expected argument 'customer_service_uri' to be a str")
        pulumi.set(__self__, 'customer_service_uri', customer_service_uri)
        if id and (not isinstance(id, str)):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, 'id', id)
        if location and (not isinstance(location, str)):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, 'location', location)
        if logo_uri and (not isinstance(logo_uri, str)):
            raise TypeError("Expected argument 'logo_uri' to be a str")
        pulumi.set(__self__, 'logo_uri', logo_uri)
        if long_description and (not isinstance(long_description, str)):
            raise TypeError("Expected argument 'long_description' to be a str")
        pulumi.set(__self__, 'long_description', long_description)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if partner_customer_service_extension and (not isinstance(partner_customer_service_extension, str)):
            raise TypeError("Expected argument 'partner_customer_service_extension' to be a str")
        pulumi.set(__self__, 'partner_customer_service_extension', partner_customer_service_extension)
        if partner_customer_service_number and (not isinstance(partner_customer_service_number, str)):
            raise TypeError("Expected argument 'partner_customer_service_number' to be a str")
        pulumi.set(__self__, 'partner_customer_service_number', partner_customer_service_number)
        if partner_name and (not isinstance(partner_name, str)):
            raise TypeError("Expected argument 'partner_name' to be a str")
        pulumi.set(__self__, 'partner_name', partner_name)
        if partner_resource_type_description and (not isinstance(partner_resource_type_description, str)):
            raise TypeError("Expected argument 'partner_resource_type_description' to be a str")
        pulumi.set(__self__, 'partner_resource_type_description', partner_resource_type_description)
        if partner_resource_type_display_name and (not isinstance(partner_resource_type_display_name, str)):
            raise TypeError("Expected argument 'partner_resource_type_display_name' to be a str")
        pulumi.set(__self__, 'partner_resource_type_display_name', partner_resource_type_display_name)
        if partner_resource_type_name and (not isinstance(partner_resource_type_name, str)):
            raise TypeError("Expected argument 'partner_resource_type_name' to be a str")
        pulumi.set(__self__, 'partner_resource_type_name', partner_resource_type_name)
        if provisioning_state and (not isinstance(provisioning_state, str)):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        if setup_uri and (not isinstance(setup_uri, str)):
            raise TypeError("Expected argument 'setup_uri' to be a str")
        pulumi.set(__self__, 'setup_uri', setup_uri)
        if system_data and (not isinstance(system_data, dict)):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, 'system_data', system_data)
        if tags and (not isinstance(tags, dict)):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, 'tags', tags)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if visibility_state and (not isinstance(visibility_state, str)):
            raise TypeError("Expected argument 'visibility_state' to be a str")
        pulumi.set(__self__, 'visibility_state', visibility_state)

    @property
    @pulumi.getter(name='authorizedAzureSubscriptionIds')
    def authorized_azure_subscription_ids(self) -> Optional[Sequence[str]]:
        """
        List of Azure subscription Ids that are authorized to create a partner namespace
        associated with this partner registration. This is an optional property. Creating
        partner namespaces is always permitted under the same Azure subscription as the one used
        for creating the partner registration.
        """
        return pulumi.get(self, 'authorized_azure_subscription_ids')

    @property
    @pulumi.getter(name='customerServiceUri')
    def customer_service_uri(self) -> Optional[str]:
        """
        The extension of the customer service URI of the publisher.
        """
        return pulumi.get(self, 'customer_service_uri')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Location of the resource.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='logoUri')
    def logo_uri(self) -> Optional[str]:
        """
        URI of the logo.
        """
        return pulumi.get(self, 'logo_uri')

    @property
    @pulumi.getter(name='longDescription')
    def long_description(self) -> Optional[str]:
        """
        Long description for the custom scenarios and integration to be displayed in the portal if needed.
        Length of this description should not exceed 2048 characters.
        """
        return pulumi.get(self, 'long_description')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='partnerCustomerServiceExtension')
    def partner_customer_service_extension(self) -> Optional[str]:
        """
        The extension of the customer service number of the publisher. Only digits are allowed and number of digits should not exceed 10.
        """
        return pulumi.get(self, 'partner_customer_service_extension')

    @property
    @pulumi.getter(name='partnerCustomerServiceNumber')
    def partner_customer_service_number(self) -> Optional[str]:
        """
        The customer service number of the publisher. The expected phone format should start with a '+' sign 
        followed by the country code. The remaining digits are then followed. Only digits and spaces are allowed and its
        length cannot exceed 16 digits including country code. Examples of valid phone numbers are: +1 515 123 4567 and
        +966 7 5115 2471. Examples of invalid phone numbers are: +1 (515) 123-4567, 1 515 123 4567 and +966 121 5115 24 7 551 1234 43
        """
        return pulumi.get(self, 'partner_customer_service_number')

    @property
    @pulumi.getter(name='partnerName')
    def partner_name(self) -> Optional[str]:
        """
        Official name of the partner name. For example: "Contoso".
        """
        return pulumi.get(self, 'partner_name')

    @property
    @pulumi.getter(name='partnerResourceTypeDescription')
    def partner_resource_type_description(self) -> Optional[str]:
        """
        Short description of the partner resource type. The length of this description should not exceed 256 characters.
        """
        return pulumi.get(self, 'partner_resource_type_description')

    @property
    @pulumi.getter(name='partnerResourceTypeDisplayName')
    def partner_resource_type_display_name(self) -> Optional[str]:
        """
        Display name of the partner resource type.
        """
        return pulumi.get(self, 'partner_resource_type_display_name')

    @property
    @pulumi.getter(name='partnerResourceTypeName')
    def partner_resource_type_name(self) -> Optional[str]:
        """
        Name of the partner resource type.
        """
        return pulumi.get(self, 'partner_resource_type_name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the partner registration.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='setupUri')
    def setup_uri(self) -> Optional[str]:
        """
        URI of the partner website that can be used by Azure customers to setup Event Grid
        integration on an event source.
        """
        return pulumi.get(self, 'setup_uri')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to Partner Registration resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags of the resource.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='visibilityState')
    def visibility_state(self) -> Optional[str]:
        """
        Visibility state of the partner registration.
        """
        return pulumi.get(self, 'visibility_state')

class AwaitableGetPartnerRegistrationResult(GetPartnerRegistrationResult):

    def __await__(self):
        if False:
            yield self
        return GetPartnerRegistrationResult(authorized_azure_subscription_ids=self.authorized_azure_subscription_ids, customer_service_uri=self.customer_service_uri, id=self.id, location=self.location, logo_uri=self.logo_uri, long_description=self.long_description, name=self.name, partner_customer_service_extension=self.partner_customer_service_extension, partner_customer_service_number=self.partner_customer_service_number, partner_name=self.partner_name, partner_resource_type_description=self.partner_resource_type_description, partner_resource_type_display_name=self.partner_resource_type_display_name, partner_resource_type_name=self.partner_resource_type_name, provisioning_state=self.provisioning_state, setup_uri=self.setup_uri, system_data=self.system_data, tags=self.tags, type=self.type, visibility_state=self.visibility_state)

def get_partner_registration(partner_registration_name: Optional[str]=None, resource_group_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetPartnerRegistrationResult:
    """
    Information about a partner registration.
    API Version: 2021-06-01-preview.


    :param str partner_registration_name: Name of the partner registration.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    __args__ = dict()
    __args__['partnerRegistrationName'] = partner_registration_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid:getPartnerRegistration', __args__, opts=opts, typ=GetPartnerRegistrationResult).value
    return AwaitableGetPartnerRegistrationResult(authorized_azure_subscription_ids=__ret__.authorized_azure_subscription_ids, customer_service_uri=__ret__.customer_service_uri, id=__ret__.id, location=__ret__.location, logo_uri=__ret__.logo_uri, long_description=__ret__.long_description, name=__ret__.name, partner_customer_service_extension=__ret__.partner_customer_service_extension, partner_customer_service_number=__ret__.partner_customer_service_number, partner_name=__ret__.partner_name, partner_resource_type_description=__ret__.partner_resource_type_description, partner_resource_type_display_name=__ret__.partner_resource_type_display_name, partner_resource_type_name=__ret__.partner_resource_type_name, provisioning_state=__ret__.provisioning_state, setup_uri=__ret__.setup_uri, system_data=__ret__.system_data, tags=__ret__.tags, type=__ret__.type, visibility_state=__ret__.visibility_state)

@_utilities.lift_output_func(get_partner_registration)
def get_partner_registration_output(partner_registration_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetPartnerRegistrationResult]:
    """
    Information about a partner registration.
    API Version: 2021-06-01-preview.


    :param str partner_registration_name: Name of the partner registration.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    ...
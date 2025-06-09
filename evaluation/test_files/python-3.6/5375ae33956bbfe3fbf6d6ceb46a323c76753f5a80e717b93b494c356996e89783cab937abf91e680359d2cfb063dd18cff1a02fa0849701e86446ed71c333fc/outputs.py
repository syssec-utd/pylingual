import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['EventHandlerResponse', 'LiveTraceCategoryResponse', 'LiveTraceConfigurationResponse', 'ManagedIdentityResponse', 'ManagedIdentitySettingsResponse', 'NetworkACLResponse', 'PrivateEndpointACLResponse', 'PrivateEndpointConnectionResponse', 'PrivateEndpointResponse', 'PrivateLinkServiceConnectionStateResponse', 'ResourceLogCategoryResponse', 'ResourceLogConfigurationResponse', 'ResourceSkuResponse', 'SharedPrivateLinkResourceResponse', 'SystemDataResponse', 'UpstreamAuthSettingsResponse', 'UserAssignedIdentityPropertyResponse', 'WebPubSubHubPropertiesResponse', 'WebPubSubNetworkACLsResponse', 'WebPubSubTlsSettingsResponse']

@pulumi.output_type
class EventHandlerResponse(dict):
    """
    Properties of event handler.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'urlTemplate':
            suggest = 'url_template'
        elif key == 'systemEvents':
            suggest = 'system_events'
        elif key == 'userEventPattern':
            suggest = 'user_event_pattern'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventHandlerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventHandlerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        EventHandlerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, url_template: str, auth: Optional['outputs.UpstreamAuthSettingsResponse']=None, system_events: Optional[Sequence[str]]=None, user_event_pattern: Optional[str]=None):
        """
        Properties of event handler.
        :param str url_template: Gets or sets the EventHandler URL template. You can use a predefined parameter {hub} and {event} inside the template, the value of the EventHandler URL is dynamically calculated when the client request comes in.
               For example, UrlTemplate can be `http://example.com/api/{hub}/{event}`. The host part can't contains parameters.
        :param 'UpstreamAuthSettingsResponse' auth: Upstream auth settings. If not set, no auth is used for upstream messages.
        :param Sequence[str] system_events: Gets ot sets the list of system events.
        :param str user_event_pattern: Gets or sets the matching pattern for event names.
               There are 3 kind of patterns supported:
                   1. "*", it to matches any event name
                   2. Combine multiple events with ",", for example "event1,event2", it matches event "event1" and "event2"
                   3. The single event name, for example, "event1", it matches "event1"
        """
        pulumi.set(__self__, 'url_template', url_template)
        if auth is not None:
            pulumi.set(__self__, 'auth', auth)
        if system_events is not None:
            pulumi.set(__self__, 'system_events', system_events)
        if user_event_pattern is not None:
            pulumi.set(__self__, 'user_event_pattern', user_event_pattern)

    @property
    @pulumi.getter(name='urlTemplate')
    def url_template(self) -> str:
        """
        Gets or sets the EventHandler URL template. You can use a predefined parameter {hub} and {event} inside the template, the value of the EventHandler URL is dynamically calculated when the client request comes in.
        For example, UrlTemplate can be `http://example.com/api/{hub}/{event}`. The host part can't contains parameters.
        """
        return pulumi.get(self, 'url_template')

    @property
    @pulumi.getter
    def auth(self) -> Optional['outputs.UpstreamAuthSettingsResponse']:
        """
        Upstream auth settings. If not set, no auth is used for upstream messages.
        """
        return pulumi.get(self, 'auth')

    @property
    @pulumi.getter(name='systemEvents')
    def system_events(self) -> Optional[Sequence[str]]:
        """
        Gets ot sets the list of system events.
        """
        return pulumi.get(self, 'system_events')

    @property
    @pulumi.getter(name='userEventPattern')
    def user_event_pattern(self) -> Optional[str]:
        """
        Gets or sets the matching pattern for event names.
        There are 3 kind of patterns supported:
            1. "*", it to matches any event name
            2. Combine multiple events with ",", for example "event1,event2", it matches event "event1" and "event2"
            3. The single event name, for example, "event1", it matches "event1"
        """
        return pulumi.get(self, 'user_event_pattern')

@pulumi.output_type
class LiveTraceCategoryResponse(dict):
    """
    Live trace category configuration of a Microsoft.SignalRService resource.
    """

    def __init__(__self__, *, enabled: Optional[str]=None, name: Optional[str]=None):
        """
        Live trace category configuration of a Microsoft.SignalRService resource.
        :param str enabled: Indicates whether or the live trace category is enabled.
               Available values: true, false.
               Case insensitive.
        :param str name: Gets or sets the live trace category's name.
               Available values: ConnectivityLogs, MessagingLogs.
               Case insensitive.
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[str]:
        """
        Indicates whether or the live trace category is enabled.
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the live trace category's name.
        Available values: ConnectivityLogs, MessagingLogs.
        Case insensitive.
        """
        return pulumi.get(self, 'name')

@pulumi.output_type
class LiveTraceConfigurationResponse(dict):
    """
    Live trace configuration of a Microsoft.SignalRService resource.
    """

    def __init__(__self__, *, categories: Optional[Sequence['outputs.LiveTraceCategoryResponse']]=None, enabled: Optional[str]=None):
        """
        Live trace configuration of a Microsoft.SignalRService resource.
        :param Sequence['LiveTraceCategoryResponse'] categories: Gets or sets the list of category configurations.
        :param str enabled: Indicates whether or not enable live trace.
               When it's set to true, live trace client can connect to the service.
               Otherwise, live trace client can't connect to the service, so that you are unable to receive any log, no matter what you configure in "categories".
               Available values: true, false.
               Case insensitive.
        """
        if categories is not None:
            pulumi.set(__self__, 'categories', categories)
        if enabled is None:
            enabled = 'false'
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)

    @property
    @pulumi.getter
    def categories(self) -> Optional[Sequence['outputs.LiveTraceCategoryResponse']]:
        """
        Gets or sets the list of category configurations.
        """
        return pulumi.get(self, 'categories')

    @property
    @pulumi.getter
    def enabled(self) -> Optional[str]:
        """
        Indicates whether or not enable live trace.
        When it's set to true, live trace client can connect to the service.
        Otherwise, live trace client can't connect to the service, so that you are unable to receive any log, no matter what you configure in "categories".
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

@pulumi.output_type
class ManagedIdentityResponse(dict):
    """
    A class represent managed identities used for request and response
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'principalId':
            suggest = 'principal_id'
        elif key == 'tenantId':
            suggest = 'tenant_id'
        elif key == 'userAssignedIdentities':
            suggest = 'user_assigned_identities'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedIdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedIdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ManagedIdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, principal_id: str, tenant_id: str, type: Optional[str]=None, user_assigned_identities: Optional[Mapping[str, 'outputs.UserAssignedIdentityPropertyResponse']]=None):
        """
        A class represent managed identities used for request and response
        :param str principal_id: Get the principal id for the system assigned identity.
               Only be used in response.
        :param str tenant_id: Get the tenant id for the system assigned identity.
               Only be used in response
        :param str type: Represents the identity type: systemAssigned, userAssigned, None
        :param Mapping[str, 'UserAssignedIdentityPropertyResponse'] user_assigned_identities: Get or set the user assigned identities
        """
        pulumi.set(__self__, 'principal_id', principal_id)
        pulumi.set(__self__, 'tenant_id', tenant_id)
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, 'user_assigned_identities', user_assigned_identities)

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> str:
        """
        Get the principal id for the system assigned identity.
        Only be used in response.
        """
        return pulumi.get(self, 'principal_id')

    @property
    @pulumi.getter(name='tenantId')
    def tenant_id(self) -> str:
        """
        Get the tenant id for the system assigned identity.
        Only be used in response
        """
        return pulumi.get(self, 'tenant_id')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Represents the identity type: systemAssigned, userAssigned, None
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userAssignedIdentities')
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserAssignedIdentityPropertyResponse']]:
        """
        Get or set the user assigned identities
        """
        return pulumi.get(self, 'user_assigned_identities')

@pulumi.output_type
class ManagedIdentitySettingsResponse(dict):
    """
    Managed identity settings for upstream.
    """

    def __init__(__self__, *, resource: Optional[str]=None):
        """
        Managed identity settings for upstream.
        :param str resource: The Resource indicating the App ID URI of the target resource.
               It also appears in the aud (audience) claim of the issued token.
        """
        if resource is not None:
            pulumi.set(__self__, 'resource', resource)

    @property
    @pulumi.getter
    def resource(self) -> Optional[str]:
        """
        The Resource indicating the App ID URI of the target resource.
        It also appears in the aud (audience) claim of the issued token.
        """
        return pulumi.get(self, 'resource')

@pulumi.output_type
class NetworkACLResponse(dict):
    """
    Network ACL
    """

    def __init__(__self__, *, allow: Optional[Sequence[str]]=None, deny: Optional[Sequence[str]]=None):
        """
        Network ACL
        :param Sequence[str] allow: Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        :param Sequence[str] deny: Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        if allow is not None:
            pulumi.set(__self__, 'allow', allow)
        if deny is not None:
            pulumi.set(__self__, 'deny', deny)

    @property
    @pulumi.getter
    def allow(self) -> Optional[Sequence[str]]:
        """
        Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'allow')

    @property
    @pulumi.getter
    def deny(self) -> Optional[Sequence[str]]:
        """
        Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'deny')

@pulumi.output_type
class PrivateEndpointACLResponse(dict):
    """
    ACL for a private endpoint
    """

    def __init__(__self__, *, name: str, allow: Optional[Sequence[str]]=None, deny: Optional[Sequence[str]]=None):
        """
        ACL for a private endpoint
        :param str name: Name of the private endpoint connection
        :param Sequence[str] allow: Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        :param Sequence[str] deny: Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        pulumi.set(__self__, 'name', name)
        if allow is not None:
            pulumi.set(__self__, 'allow', allow)
        if deny is not None:
            pulumi.set(__self__, 'deny', deny)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the private endpoint connection
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def allow(self) -> Optional[Sequence[str]]:
        """
        Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'allow')

    @property
    @pulumi.getter
    def deny(self) -> Optional[Sequence[str]]:
        """
        Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'deny')

@pulumi.output_type
class PrivateEndpointConnectionResponse(dict):
    """
    A private endpoint connection to an azure resource
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'groupIds':
            suggest = 'group_ids'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'systemData':
            suggest = 'system_data'
        elif key == 'privateEndpoint':
            suggest = 'private_endpoint'
        elif key == 'privateLinkServiceConnectionState':
            suggest = 'private_link_service_connection_state'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateEndpointConnectionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        PrivateEndpointConnectionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, group_ids: Sequence[str], id: str, name: str, provisioning_state: str, system_data: 'outputs.SystemDataResponse', type: str, private_endpoint: Optional['outputs.PrivateEndpointResponse']=None, private_link_service_connection_state: Optional['outputs.PrivateLinkServiceConnectionStateResponse']=None):
        """
        A private endpoint connection to an azure resource
        :param Sequence[str] group_ids: Group IDs
        :param str id: Fully qualified resource Id for the resource.
        :param str name: The name of the resource.
        :param str provisioning_state: Provisioning state of the resource.
        :param 'SystemDataResponse' system_data: Metadata pertaining to creation and last modification of the resource.
        :param str type: The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        :param 'PrivateEndpointResponse' private_endpoint: Private endpoint
        :param 'PrivateLinkServiceConnectionStateResponse' private_link_service_connection_state: Connection state of the private endpoint connection
        """
        pulumi.set(__self__, 'group_ids', group_ids)
        pulumi.set(__self__, 'id', id)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'system_data', system_data)
        pulumi.set(__self__, 'type', type)
        if private_endpoint is not None:
            pulumi.set(__self__, 'private_endpoint', private_endpoint)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, 'private_link_service_connection_state', private_link_service_connection_state)

    @property
    @pulumi.getter(name='groupIds')
    def group_ids(self) -> Sequence[str]:
        """
        Group IDs
        """
        return pulumi.get(self, 'group_ids')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        Private endpoint
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> Optional['outputs.PrivateLinkServiceConnectionStateResponse']:
        """
        Connection state of the private endpoint connection
        """
        return pulumi.get(self, 'private_link_service_connection_state')

@pulumi.output_type
class PrivateEndpointResponse(dict):
    """
    Private endpoint
    """

    def __init__(__self__, *, id: Optional[str]=None):
        """
        Private endpoint
        :param str id: Full qualified Id of the private endpoint
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Full qualified Id of the private endpoint
        """
        return pulumi.get(self, 'id')

@pulumi.output_type
class PrivateLinkServiceConnectionStateResponse(dict):
    """
    Connection state of the private endpoint connection
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'actionsRequired':
            suggest = 'actions_required'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PrivateLinkServiceConnectionStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        PrivateLinkServiceConnectionStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, actions_required: Optional[str]=None, description: Optional[str]=None, status: Optional[str]=None):
        """
        Connection state of the private endpoint connection
        :param str actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param str description: The reason for approval/rejection of the connection.
        :param str status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, 'actions_required', actions_required)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter(name='actionsRequired')
    def actions_required(self) -> Optional[str]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, 'actions_required')

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, 'status')

@pulumi.output_type
class ResourceLogCategoryResponse(dict):
    """
    Resource log category configuration of a Microsoft.SignalRService resource.
    """

    def __init__(__self__, *, enabled: Optional[str]=None, name: Optional[str]=None):
        """
        Resource log category configuration of a Microsoft.SignalRService resource.
        :param str enabled: Indicates whether or the resource log category is enabled.
               Available values: true, false.
               Case insensitive.
        :param str name: Gets or sets the resource log category's name.
               Available values: ConnectivityLogs, MessagingLogs.
               Case insensitive.
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[str]:
        """
        Indicates whether or the resource log category is enabled.
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Gets or sets the resource log category's name.
        Available values: ConnectivityLogs, MessagingLogs.
        Case insensitive.
        """
        return pulumi.get(self, 'name')

@pulumi.output_type
class ResourceLogConfigurationResponse(dict):
    """
    Resource log configuration of a Microsoft.SignalRService resource.
    """

    def __init__(__self__, *, categories: Optional[Sequence['outputs.ResourceLogCategoryResponse']]=None):
        """
        Resource log configuration of a Microsoft.SignalRService resource.
        :param Sequence['ResourceLogCategoryResponse'] categories: Gets or sets the list of category configurations.
        """
        if categories is not None:
            pulumi.set(__self__, 'categories', categories)

    @property
    @pulumi.getter
    def categories(self) -> Optional[Sequence['outputs.ResourceLogCategoryResponse']]:
        """
        Gets or sets the list of category configurations.
        """
        return pulumi.get(self, 'categories')

@pulumi.output_type
class ResourceSkuResponse(dict):
    """
    The billing information of the resource.
    """

    def __init__(__self__, *, family: str, name: str, size: str, capacity: Optional[int]=None, tier: Optional[str]=None):
        """
        The billing information of the resource.
        :param str family: Not used. Retained for future use.
        :param str name: The name of the SKU. Required.
               
               Allowed values: Standard_S1, Free_F1
        :param str size: Not used. Retained for future use.
        :param int capacity: Optional, integer. The unit count of the resource. 1 by default.
               
               If present, following values are allowed:
                   Free: 1
                   Standard: 1,2,5,10,20,50,100
        :param str tier: Optional tier of this particular SKU. 'Standard' or 'Free'. 
               
               `Basic` is deprecated, use `Standard` instead.
        """
        pulumi.set(__self__, 'family', family)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'size', size)
        if capacity is not None:
            pulumi.set(__self__, 'capacity', capacity)
        if tier is not None:
            pulumi.set(__self__, 'tier', tier)

    @property
    @pulumi.getter
    def family(self) -> str:
        """
        Not used. Retained for future use.
        """
        return pulumi.get(self, 'family')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU. Required.
        
        Allowed values: Standard_S1, Free_F1
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def size(self) -> str:
        """
        Not used. Retained for future use.
        """
        return pulumi.get(self, 'size')

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        Optional, integer. The unit count of the resource. 1 by default.
        
        If present, following values are allowed:
            Free: 1
            Standard: 1,2,5,10,20,50,100
        """
        return pulumi.get(self, 'capacity')

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        Optional tier of this particular SKU. 'Standard' or 'Free'. 
        
        `Basic` is deprecated, use `Standard` instead.
        """
        return pulumi.get(self, 'tier')

@pulumi.output_type
class SharedPrivateLinkResourceResponse(dict):
    """
    Describes a Shared Private Link Resource
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'groupId':
            suggest = 'group_id'
        elif key == 'privateLinkResourceId':
            suggest = 'private_link_resource_id'
        elif key == 'provisioningState':
            suggest = 'provisioning_state'
        elif key == 'systemData':
            suggest = 'system_data'
        elif key == 'requestMessage':
            suggest = 'request_message'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SharedPrivateLinkResourceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SharedPrivateLinkResourceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SharedPrivateLinkResourceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, group_id: str, id: str, name: str, private_link_resource_id: str, provisioning_state: str, status: str, system_data: 'outputs.SystemDataResponse', type: str, request_message: Optional[str]=None):
        """
        Describes a Shared Private Link Resource
        :param str group_id: The group id from the provider of resource the shared private link resource is for
        :param str id: Fully qualified resource Id for the resource.
        :param str name: The name of the resource.
        :param str private_link_resource_id: The resource id of the resource the shared private link resource is for
        :param str provisioning_state: Provisioning state of the resource.
        :param str status: Status of the shared private link resource
        :param 'SystemDataResponse' system_data: Metadata pertaining to creation and last modification of the resource.
        :param str type: The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        :param str request_message: The request message for requesting approval of the shared private link resource
        """
        pulumi.set(__self__, 'group_id', group_id)
        pulumi.set(__self__, 'id', id)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'private_link_resource_id', private_link_resource_id)
        pulumi.set(__self__, 'provisioning_state', provisioning_state)
        pulumi.set(__self__, 'status', status)
        pulumi.set(__self__, 'system_data', system_data)
        pulumi.set(__self__, 'type', type)
        if request_message is not None:
            pulumi.set(__self__, 'request_message', request_message)

    @property
    @pulumi.getter(name='groupId')
    def group_id(self) -> str:
        """
        The group id from the provider of resource the shared private link resource is for
        """
        return pulumi.get(self, 'group_id')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource.
        """
        return pulumi.get(self, 'id')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateLinkResourceId')
    def private_link_resource_id(self) -> str:
        """
        The resource id of the resource the shared private link resource is for
        """
        return pulumi.get(self, 'private_link_resource_id')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the shared private link resource
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='requestMessage')
    def request_message(self) -> Optional[str]:
        """
        The request message for requesting approval of the shared private link resource
        """
        return pulumi.get(self, 'request_message')

@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'createdAt':
            suggest = 'created_at'
        elif key == 'createdBy':
            suggest = 'created_by'
        elif key == 'createdByType':
            suggest = 'created_by_type'
        elif key == 'lastModifiedAt':
            suggest = 'last_modified_at'
        elif key == 'lastModifiedBy':
            suggest = 'last_modified_by'
        elif key == 'lastModifiedByType':
            suggest = 'last_modified_by_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, created_at: Optional[str]=None, created_by: Optional[str]=None, created_by_type: Optional[str]=None, last_modified_at: Optional[str]=None, last_modified_by: Optional[str]=None, last_modified_by_type: Optional[str]=None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, 'created_at', created_at)
        if created_by is not None:
            pulumi.set(__self__, 'created_by', created_by)
        if created_by_type is not None:
            pulumi.set(__self__, 'created_by_type', created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, 'last_modified_at', last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, 'last_modified_by', last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, 'last_modified_by_type', last_modified_by_type)

    @property
    @pulumi.getter(name='createdAt')
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, 'created_at')

    @property
    @pulumi.getter(name='createdBy')
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, 'created_by')

    @property
    @pulumi.getter(name='createdByType')
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, 'created_by_type')

    @property
    @pulumi.getter(name='lastModifiedAt')
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, 'last_modified_at')

    @property
    @pulumi.getter(name='lastModifiedBy')
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, 'last_modified_by')

    @property
    @pulumi.getter(name='lastModifiedByType')
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, 'last_modified_by_type')

@pulumi.output_type
class UpstreamAuthSettingsResponse(dict):
    """
    Upstream auth settings. If not set, no auth is used for upstream messages.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'managedIdentity':
            suggest = 'managed_identity'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UpstreamAuthSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UpstreamAuthSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UpstreamAuthSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, managed_identity: Optional['outputs.ManagedIdentitySettingsResponse']=None, type: Optional[str]=None):
        """
        Upstream auth settings. If not set, no auth is used for upstream messages.
        :param 'ManagedIdentitySettingsResponse' managed_identity: Managed identity settings for upstream.
        :param str type: Upstream auth type enum.
        """
        if managed_identity is not None:
            pulumi.set(__self__, 'managed_identity', managed_identity)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='managedIdentity')
    def managed_identity(self) -> Optional['outputs.ManagedIdentitySettingsResponse']:
        """
        Managed identity settings for upstream.
        """
        return pulumi.get(self, 'managed_identity')

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Upstream auth type enum.
        """
        return pulumi.get(self, 'type')

@pulumi.output_type
class UserAssignedIdentityPropertyResponse(dict):
    """
    Properties of user assigned identity.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientId':
            suggest = 'client_id'
        elif key == 'principalId':
            suggest = 'principal_id'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserAssignedIdentityPropertyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserAssignedIdentityPropertyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        UserAssignedIdentityPropertyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_id: str, principal_id: str):
        """
        Properties of user assigned identity.
        :param str client_id: Get the client id for the user assigned identity
        :param str principal_id: Get the principal id for the user assigned identity
        """
        pulumi.set(__self__, 'client_id', client_id)
        pulumi.set(__self__, 'principal_id', principal_id)

    @property
    @pulumi.getter(name='clientId')
    def client_id(self) -> str:
        """
        Get the client id for the user assigned identity
        """
        return pulumi.get(self, 'client_id')

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> str:
        """
        Get the principal id for the user assigned identity
        """
        return pulumi.get(self, 'principal_id')

@pulumi.output_type
class WebPubSubHubPropertiesResponse(dict):
    """
    Properties of a hub.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'anonymousConnectPolicy':
            suggest = 'anonymous_connect_policy'
        elif key == 'eventHandlers':
            suggest = 'event_handlers'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebPubSubHubPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebPubSubHubPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        WebPubSubHubPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, anonymous_connect_policy: Optional[str]=None, event_handlers: Optional[Sequence['outputs.EventHandlerResponse']]=None):
        """
        Properties of a hub.
        :param str anonymous_connect_policy: The settings for configuring if anonymous connections are allowed for this hub: "allow" or "deny". Default to "deny".
        :param Sequence['EventHandlerResponse'] event_handlers: Event handler of a hub.
        """
        if anonymous_connect_policy is None:
            anonymous_connect_policy = 'deny'
        if anonymous_connect_policy is not None:
            pulumi.set(__self__, 'anonymous_connect_policy', anonymous_connect_policy)
        if event_handlers is not None:
            pulumi.set(__self__, 'event_handlers', event_handlers)

    @property
    @pulumi.getter(name='anonymousConnectPolicy')
    def anonymous_connect_policy(self) -> Optional[str]:
        """
        The settings for configuring if anonymous connections are allowed for this hub: "allow" or "deny". Default to "deny".
        """
        return pulumi.get(self, 'anonymous_connect_policy')

    @property
    @pulumi.getter(name='eventHandlers')
    def event_handlers(self) -> Optional[Sequence['outputs.EventHandlerResponse']]:
        """
        Event handler of a hub.
        """
        return pulumi.get(self, 'event_handlers')

@pulumi.output_type
class WebPubSubNetworkACLsResponse(dict):
    """
    Network ACLs for the resource
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'defaultAction':
            suggest = 'default_action'
        elif key == 'privateEndpoints':
            suggest = 'private_endpoints'
        elif key == 'publicNetwork':
            suggest = 'public_network'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebPubSubNetworkACLsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebPubSubNetworkACLsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        WebPubSubNetworkACLsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, default_action: Optional[str]=None, private_endpoints: Optional[Sequence['outputs.PrivateEndpointACLResponse']]=None, public_network: Optional['outputs.NetworkACLResponse']=None):
        """
        Network ACLs for the resource
        :param str default_action: Azure Networking ACL Action.
        :param Sequence['PrivateEndpointACLResponse'] private_endpoints: ACLs for requests from private endpoints
        :param 'NetworkACLResponse' public_network: Network ACL
        """
        if default_action is not None:
            pulumi.set(__self__, 'default_action', default_action)
        if private_endpoints is not None:
            pulumi.set(__self__, 'private_endpoints', private_endpoints)
        if public_network is not None:
            pulumi.set(__self__, 'public_network', public_network)

    @property
    @pulumi.getter(name='defaultAction')
    def default_action(self) -> Optional[str]:
        """
        Azure Networking ACL Action.
        """
        return pulumi.get(self, 'default_action')

    @property
    @pulumi.getter(name='privateEndpoints')
    def private_endpoints(self) -> Optional[Sequence['outputs.PrivateEndpointACLResponse']]:
        """
        ACLs for requests from private endpoints
        """
        return pulumi.get(self, 'private_endpoints')

    @property
    @pulumi.getter(name='publicNetwork')
    def public_network(self) -> Optional['outputs.NetworkACLResponse']:
        """
        Network ACL
        """
        return pulumi.get(self, 'public_network')

@pulumi.output_type
class WebPubSubTlsSettingsResponse(dict):
    """
    TLS settings for the resource
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientCertEnabled':
            suggest = 'client_cert_enabled'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebPubSubTlsSettingsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebPubSubTlsSettingsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        WebPubSubTlsSettingsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_cert_enabled: Optional[bool]=None):
        """
        TLS settings for the resource
        :param bool client_cert_enabled: Request client certificate during TLS handshake if enabled
        """
        if client_cert_enabled is None:
            client_cert_enabled = True
        if client_cert_enabled is not None:
            pulumi.set(__self__, 'client_cert_enabled', client_cert_enabled)

    @property
    @pulumi.getter(name='clientCertEnabled')
    def client_cert_enabled(self) -> Optional[bool]:
        """
        Request client certificate during TLS handshake if enabled
        """
        return pulumi.get(self, 'client_cert_enabled')
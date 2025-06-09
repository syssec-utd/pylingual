import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['EventHandlerArgs', 'EventHubEndpointArgs', 'EventListenerArgs', 'EventNameFilterArgs', 'LiveTraceCategoryArgs', 'LiveTraceConfigurationArgs', 'ManagedIdentitySettingsArgs', 'ManagedIdentityArgs', 'NetworkACLArgs', 'PrivateEndpointACLArgs', 'PrivateEndpointArgs', 'PrivateLinkServiceConnectionStateArgs', 'ResourceLogCategoryArgs', 'ResourceLogConfigurationArgs', 'ResourceReferenceArgs', 'ResourceSkuArgs', 'UpstreamAuthSettingsArgs', 'WebPubSubHubPropertiesArgs', 'WebPubSubNetworkACLsArgs', 'WebPubSubTlsSettingsArgs']

@pulumi.input_type
class EventHandlerArgs:

    def __init__(__self__, *, url_template: pulumi.Input[str], auth: Optional[pulumi.Input['UpstreamAuthSettingsArgs']]=None, system_events: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, user_event_pattern: Optional[pulumi.Input[str]]=None):
        """
        Properties of event handler.
        :param pulumi.Input[str] url_template: Gets or sets the EventHandler URL template. You can use a predefined parameter {hub} and {event} inside the template, the value of the EventHandler URL is dynamically calculated when the client request comes in.
               For example, UrlTemplate can be `http://example.com/api/{hub}/{event}`. The host part can't contains parameters.
        :param pulumi.Input['UpstreamAuthSettingsArgs'] auth: Upstream auth settings. If not set, no auth is used for upstream messages.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] system_events: Gets or sets the list of system events.
        :param pulumi.Input[str] user_event_pattern: Gets or sets the matching pattern for event names.
               There are 3 kinds of patterns supported:
                   1. "*", it matches any event name
                   2. Combine multiple events with ",", for example "event1,event2", it matches event "event1" and "event2"
                   3. A single event name, for example, "event1", it matches "event1"
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
    def url_template(self) -> pulumi.Input[str]:
        """
        Gets or sets the EventHandler URL template. You can use a predefined parameter {hub} and {event} inside the template, the value of the EventHandler URL is dynamically calculated when the client request comes in.
        For example, UrlTemplate can be `http://example.com/api/{hub}/{event}`. The host part can't contains parameters.
        """
        return pulumi.get(self, 'url_template')

    @url_template.setter
    def url_template(self, value: pulumi.Input[str]):
        pulumi.set(self, 'url_template', value)

    @property
    @pulumi.getter
    def auth(self) -> Optional[pulumi.Input['UpstreamAuthSettingsArgs']]:
        """
        Upstream auth settings. If not set, no auth is used for upstream messages.
        """
        return pulumi.get(self, 'auth')

    @auth.setter
    def auth(self, value: Optional[pulumi.Input['UpstreamAuthSettingsArgs']]):
        pulumi.set(self, 'auth', value)

    @property
    @pulumi.getter(name='systemEvents')
    def system_events(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Gets or sets the list of system events.
        """
        return pulumi.get(self, 'system_events')

    @system_events.setter
    def system_events(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'system_events', value)

    @property
    @pulumi.getter(name='userEventPattern')
    def user_event_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the matching pattern for event names.
        There are 3 kinds of patterns supported:
            1. "*", it matches any event name
            2. Combine multiple events with ",", for example "event1,event2", it matches event "event1" and "event2"
            3. A single event name, for example, "event1", it matches "event1"
        """
        return pulumi.get(self, 'user_event_pattern')

    @user_event_pattern.setter
    def user_event_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_event_pattern', value)

@pulumi.input_type
class EventHubEndpointArgs:

    def __init__(__self__, *, event_hub_name: pulumi.Input[str], fully_qualified_namespace: pulumi.Input[str], type: pulumi.Input[str]):
        """
        An Event Hub endpoint. 
        The managed identity of Web PubSub service must be enabled, and the identity should have the "Azure Event Hubs Data sender" role to access Event Hub.
        :param pulumi.Input[str] event_hub_name: The name of the Event Hub.
        :param pulumi.Input[str] fully_qualified_namespace: The fully qualified namespace name of the Event Hub resource. For example, "example.servicebus.windows.net".
        :param pulumi.Input[str] type: 
               Expected value is 'EventHub'.
        """
        pulumi.set(__self__, 'event_hub_name', event_hub_name)
        pulumi.set(__self__, 'fully_qualified_namespace', fully_qualified_namespace)
        pulumi.set(__self__, 'type', 'EventHub')

    @property
    @pulumi.getter(name='eventHubName')
    def event_hub_name(self) -> pulumi.Input[str]:
        """
        The name of the Event Hub.
        """
        return pulumi.get(self, 'event_hub_name')

    @event_hub_name.setter
    def event_hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'event_hub_name', value)

    @property
    @pulumi.getter(name='fullyQualifiedNamespace')
    def fully_qualified_namespace(self) -> pulumi.Input[str]:
        """
        The fully qualified namespace name of the Event Hub resource. For example, "example.servicebus.windows.net".
        """
        return pulumi.get(self, 'fully_qualified_namespace')

    @fully_qualified_namespace.setter
    def fully_qualified_namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, 'fully_qualified_namespace', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """

        Expected value is 'EventHub'.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class EventListenerArgs:

    def __init__(__self__, *, endpoint: pulumi.Input['EventHubEndpointArgs'], filter: pulumi.Input['EventNameFilterArgs']):
        """
        A setting defines which kinds of events should be sent to which endpoint.
        :param pulumi.Input['EventHubEndpointArgs'] endpoint: An endpoint specifying where Web PubSub should send events to.
        :param pulumi.Input['EventNameFilterArgs'] filter: A base class for event filter which determines whether an event should be sent to an event listener.
        """
        pulumi.set(__self__, 'endpoint', endpoint)
        pulumi.set(__self__, 'filter', filter)

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Input['EventHubEndpointArgs']:
        """
        An endpoint specifying where Web PubSub should send events to.
        """
        return pulumi.get(self, 'endpoint')

    @endpoint.setter
    def endpoint(self, value: pulumi.Input['EventHubEndpointArgs']):
        pulumi.set(self, 'endpoint', value)

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Input['EventNameFilterArgs']:
        """
        A base class for event filter which determines whether an event should be sent to an event listener.
        """
        return pulumi.get(self, 'filter')

    @filter.setter
    def filter(self, value: pulumi.Input['EventNameFilterArgs']):
        pulumi.set(self, 'filter', value)

@pulumi.input_type
class EventNameFilterArgs:

    def __init__(__self__, *, type: pulumi.Input[str], system_events: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, user_event_pattern: Optional[pulumi.Input[str]]=None):
        """
        Filter events by their name.
        :param pulumi.Input[str] type: 
               Expected value is 'EventName'.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] system_events: Gets or sets a list of system events. Supported events: "connected" and "disconnected". Blocking event "connect" is not supported because it requires a response.
        :param pulumi.Input[str] user_event_pattern: Gets or sets a matching pattern for event names.
               There are 3 kinds of patterns supported:
                   1. "*", it matches any event name
                   2. Combine multiple events with ",", for example "event1,event2", it matches events "event1" and "event2"
                   3. A single event name, for example, "event1", it matches "event1"
        """
        pulumi.set(__self__, 'type', 'EventName')
        if system_events is not None:
            pulumi.set(__self__, 'system_events', system_events)
        if user_event_pattern is not None:
            pulumi.set(__self__, 'user_event_pattern', user_event_pattern)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """

        Expected value is 'EventName'.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='systemEvents')
    def system_events(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Gets or sets a list of system events. Supported events: "connected" and "disconnected". Blocking event "connect" is not supported because it requires a response.
        """
        return pulumi.get(self, 'system_events')

    @system_events.setter
    def system_events(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'system_events', value)

    @property
    @pulumi.getter(name='userEventPattern')
    def user_event_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets a matching pattern for event names.
        There are 3 kinds of patterns supported:
            1. "*", it matches any event name
            2. Combine multiple events with ",", for example "event1,event2", it matches events "event1" and "event2"
            3. A single event name, for example, "event1", it matches "event1"
        """
        return pulumi.get(self, 'user_event_pattern')

    @user_event_pattern.setter
    def user_event_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_event_pattern', value)

@pulumi.input_type
class LiveTraceCategoryArgs:

    def __init__(__self__, *, enabled: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None):
        """
        Live trace category configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[str] enabled: Indicates whether or the live trace category is enabled.
               Available values: true, false.
               Case insensitive.
        :param pulumi.Input[str] name: Gets or sets the live trace category's name.
               Available values: ConnectivityLogs, MessagingLogs.
               Case insensitive.
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates whether or the live trace category is enabled.
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the live trace category's name.
        Available values: ConnectivityLogs, MessagingLogs.
        Case insensitive.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

@pulumi.input_type
class LiveTraceConfigurationArgs:

    def __init__(__self__, *, categories: Optional[pulumi.Input[Sequence[pulumi.Input['LiveTraceCategoryArgs']]]]=None, enabled: Optional[pulumi.Input[str]]=None):
        """
        Live trace configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[Sequence[pulumi.Input['LiveTraceCategoryArgs']]] categories: Gets or sets the list of category configurations.
        :param pulumi.Input[str] enabled: Indicates whether or not enable live trace.
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
    def categories(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LiveTraceCategoryArgs']]]]:
        """
        Gets or sets the list of category configurations.
        """
        return pulumi.get(self, 'categories')

    @categories.setter
    def categories(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LiveTraceCategoryArgs']]]]):
        pulumi.set(self, 'categories', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates whether or not enable live trace.
        When it's set to true, live trace client can connect to the service.
        Otherwise, live trace client can't connect to the service, so that you are unable to receive any log, no matter what you configure in "categories".
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'enabled', value)

@pulumi.input_type
class ManagedIdentitySettingsArgs:

    def __init__(__self__, *, resource: Optional[pulumi.Input[str]]=None):
        """
        Managed identity settings for upstream.
        :param pulumi.Input[str] resource: The Resource indicating the App ID URI of the target resource.
               It also appears in the aud (audience) claim of the issued token.
        """
        if resource is not None:
            pulumi.set(__self__, 'resource', resource)

    @property
    @pulumi.getter
    def resource(self) -> Optional[pulumi.Input[str]]:
        """
        The Resource indicating the App ID URI of the target resource.
        It also appears in the aud (audience) claim of the issued token.
        """
        return pulumi.get(self, 'resource')

    @resource.setter
    def resource(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource', value)

@pulumi.input_type
class ManagedIdentityArgs:

    def __init__(__self__, *, type: Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]]=None, user_assigned_identities: Optional[pulumi.Input[Mapping[str, Any]]]=None):
        """
        A class represent managed identities used for request and response
        :param pulumi.Input[Union[str, 'ManagedIdentityType']] type: Represents the identity type: systemAssigned, userAssigned, None
        :param pulumi.Input[Mapping[str, Any]] user_assigned_identities: Get or set the user assigned identities
        """
        if type is not None:
            pulumi.set(__self__, 'type', type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, 'user_assigned_identities', user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]]:
        """
        Represents the identity type: systemAssigned, userAssigned, None
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ManagedIdentityType']]]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='userAssignedIdentities')
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Get or set the user assigned identities
        """
        return pulumi.get(self, 'user_assigned_identities')

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, 'user_assigned_identities', value)

@pulumi.input_type
class NetworkACLArgs:

    def __init__(__self__, *, allow: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]=None, deny: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]=None):
        """
        Network ACL
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]] allow: Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]] deny: Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        if allow is not None:
            pulumi.set(__self__, 'allow', allow)
        if deny is not None:
            pulumi.set(__self__, 'deny', deny)

    @property
    @pulumi.getter
    def allow(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]:
        """
        Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'allow')

    @allow.setter
    def allow(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]):
        pulumi.set(self, 'allow', value)

    @property
    @pulumi.getter
    def deny(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]:
        """
        Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'deny')

    @deny.setter
    def deny(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]):
        pulumi.set(self, 'deny', value)

@pulumi.input_type
class PrivateEndpointACLArgs:

    def __init__(__self__, *, name: pulumi.Input[str], allow: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]=None, deny: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]=None):
        """
        ACL for a private endpoint
        :param pulumi.Input[str] name: Name of the private endpoint connection
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]] allow: Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]] deny: Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        pulumi.set(__self__, 'name', name)
        if allow is not None:
            pulumi.set(__self__, 'allow', allow)
        if deny is not None:
            pulumi.set(__self__, 'deny', deny)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the private endpoint connection
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def allow(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]:
        """
        Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'allow')

    @allow.setter
    def allow(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]):
        pulumi.set(self, 'allow', value)

    @property
    @pulumi.getter
    def deny(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]:
        """
        Denied request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
        """
        return pulumi.get(self, 'deny')

    @deny.setter
    def deny(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WebPubSubRequestType']]]]]):
        pulumi.set(self, 'deny', value)

@pulumi.input_type
class PrivateEndpointArgs:

    def __init__(__self__, *, id: Optional[pulumi.Input[str]]=None):
        """
        Private endpoint
        :param pulumi.Input[str] id: Full qualified Id of the private endpoint
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Full qualified Id of the private endpoint
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:

    def __init__(__self__, *, actions_required: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, status: Optional[pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']]]=None):
        """
        Connection state of the private endpoint connection
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, 'actions_required', actions_required)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter(name='actionsRequired')
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, 'actions_required')

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'actions_required', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateLinkServiceConnectionStatus']]]):
        pulumi.set(self, 'status', value)

@pulumi.input_type
class ResourceLogCategoryArgs:

    def __init__(__self__, *, enabled: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None):
        """
        Resource log category configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[str] enabled: Indicates whether or the resource log category is enabled.
               Available values: true, false.
               Case insensitive.
        :param pulumi.Input[str] name: Gets or sets the resource log category's name.
               Available values: ConnectivityLogs, MessagingLogs.
               Case insensitive.
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if name is not None:
            pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates whether or the resource log category is enabled.
        Available values: true, false.
        Case insensitive.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the resource log category's name.
        Available values: ConnectivityLogs, MessagingLogs.
        Case insensitive.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

@pulumi.input_type
class ResourceLogConfigurationArgs:

    def __init__(__self__, *, categories: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceLogCategoryArgs']]]]=None):
        """
        Resource log configuration of a Microsoft.SignalRService resource.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceLogCategoryArgs']]] categories: Gets or sets the list of category configurations.
        """
        if categories is not None:
            pulumi.set(__self__, 'categories', categories)

    @property
    @pulumi.getter
    def categories(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceLogCategoryArgs']]]]:
        """
        Gets or sets the list of category configurations.
        """
        return pulumi.get(self, 'categories')

    @categories.setter
    def categories(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceLogCategoryArgs']]]]):
        pulumi.set(self, 'categories', value)

@pulumi.input_type
class ResourceReferenceArgs:

    def __init__(__self__, *, id: Optional[pulumi.Input[str]]=None):
        """
        Reference to a resource.
        :param pulumi.Input[str] id: Resource ID.
        """
        if id is not None:
            pulumi.set(__self__, 'id', id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

@pulumi.input_type
class ResourceSkuArgs:

    def __init__(__self__, *, name: pulumi.Input[str], capacity: Optional[pulumi.Input[int]]=None, tier: Optional[pulumi.Input[Union[str, 'WebPubSubSkuTier']]]=None):
        """
        The billing information of the resource.
        :param pulumi.Input[str] name: The name of the SKU. Required.
               
               Allowed values: Standard_S1, Free_F1, Premium_P1
        :param pulumi.Input[int] capacity: Optional, integer. The unit count of the resource. 1 by default.
               
               If present, following values are allowed:
                   Free: 1;
                   Standard: 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100;
                   Premium:  1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100;
        :param pulumi.Input[Union[str, 'WebPubSubSkuTier']] tier: Optional tier of this particular SKU. 'Standard' or 'Free'. 
               
               `Basic` is deprecated, use `Standard` instead.
        """
        pulumi.set(__self__, 'name', name)
        if capacity is not None:
            pulumi.set(__self__, 'capacity', capacity)
        if tier is not None:
            pulumi.set(__self__, 'tier', tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SKU. Required.
        
        Allowed values: Standard_S1, Free_F1, Premium_P1
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        Optional, integer. The unit count of the resource. 1 by default.
        
        If present, following values are allowed:
            Free: 1;
            Standard: 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100;
            Premium:  1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100;
        """
        return pulumi.get(self, 'capacity')

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'capacity', value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'WebPubSubSkuTier']]]:
        """
        Optional tier of this particular SKU. 'Standard' or 'Free'. 
        
        `Basic` is deprecated, use `Standard` instead.
        """
        return pulumi.get(self, 'tier')

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'WebPubSubSkuTier']]]):
        pulumi.set(self, 'tier', value)

@pulumi.input_type
class UpstreamAuthSettingsArgs:

    def __init__(__self__, *, managed_identity: Optional[pulumi.Input['ManagedIdentitySettingsArgs']]=None, type: Optional[pulumi.Input[Union[str, 'UpstreamAuthType']]]=None):
        """
        Upstream auth settings. If not set, no auth is used for upstream messages.
        :param pulumi.Input['ManagedIdentitySettingsArgs'] managed_identity: Managed identity settings for upstream.
        :param pulumi.Input[Union[str, 'UpstreamAuthType']] type: Upstream auth type enum.
        """
        if managed_identity is not None:
            pulumi.set(__self__, 'managed_identity', managed_identity)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='managedIdentity')
    def managed_identity(self) -> Optional[pulumi.Input['ManagedIdentitySettingsArgs']]:
        """
        Managed identity settings for upstream.
        """
        return pulumi.get(self, 'managed_identity')

    @managed_identity.setter
    def managed_identity(self, value: Optional[pulumi.Input['ManagedIdentitySettingsArgs']]):
        pulumi.set(self, 'managed_identity', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'UpstreamAuthType']]]:
        """
        Upstream auth type enum.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'UpstreamAuthType']]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class WebPubSubHubPropertiesArgs:

    def __init__(__self__, *, anonymous_connect_policy: Optional[pulumi.Input[str]]=None, event_handlers: Optional[pulumi.Input[Sequence[pulumi.Input['EventHandlerArgs']]]]=None, event_listeners: Optional[pulumi.Input[Sequence[pulumi.Input['EventListenerArgs']]]]=None):
        """
        Properties of a hub.
        :param pulumi.Input[str] anonymous_connect_policy: The settings for configuring if anonymous connections are allowed for this hub: "allow" or "deny". Default to "deny".
        :param pulumi.Input[Sequence[pulumi.Input['EventHandlerArgs']]] event_handlers: Event handler of a hub.
        :param pulumi.Input[Sequence[pulumi.Input['EventListenerArgs']]] event_listeners: Event listener settings for forwarding your client events to listeners.
               Event listener is transparent to Web PubSub clients, and it doesn't return any result to clients nor interrupt the lifetime of clients.
               One event can be sent to multiple listeners, as long as it matches the filters in those listeners. The order of the array elements doesn't matter.
               Maximum count of event listeners among all hubs is 10.
        """
        if anonymous_connect_policy is None:
            anonymous_connect_policy = 'deny'
        if anonymous_connect_policy is not None:
            pulumi.set(__self__, 'anonymous_connect_policy', anonymous_connect_policy)
        if event_handlers is not None:
            pulumi.set(__self__, 'event_handlers', event_handlers)
        if event_listeners is not None:
            pulumi.set(__self__, 'event_listeners', event_listeners)

    @property
    @pulumi.getter(name='anonymousConnectPolicy')
    def anonymous_connect_policy(self) -> Optional[pulumi.Input[str]]:
        """
        The settings for configuring if anonymous connections are allowed for this hub: "allow" or "deny". Default to "deny".
        """
        return pulumi.get(self, 'anonymous_connect_policy')

    @anonymous_connect_policy.setter
    def anonymous_connect_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'anonymous_connect_policy', value)

    @property
    @pulumi.getter(name='eventHandlers')
    def event_handlers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EventHandlerArgs']]]]:
        """
        Event handler of a hub.
        """
        return pulumi.get(self, 'event_handlers')

    @event_handlers.setter
    def event_handlers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EventHandlerArgs']]]]):
        pulumi.set(self, 'event_handlers', value)

    @property
    @pulumi.getter(name='eventListeners')
    def event_listeners(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EventListenerArgs']]]]:
        """
        Event listener settings for forwarding your client events to listeners.
        Event listener is transparent to Web PubSub clients, and it doesn't return any result to clients nor interrupt the lifetime of clients.
        One event can be sent to multiple listeners, as long as it matches the filters in those listeners. The order of the array elements doesn't matter.
        Maximum count of event listeners among all hubs is 10.
        """
        return pulumi.get(self, 'event_listeners')

    @event_listeners.setter
    def event_listeners(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EventListenerArgs']]]]):
        pulumi.set(self, 'event_listeners', value)

@pulumi.input_type
class WebPubSubNetworkACLsArgs:

    def __init__(__self__, *, default_action: Optional[pulumi.Input[Union[str, 'ACLAction']]]=None, private_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointACLArgs']]]]=None, public_network: Optional[pulumi.Input['NetworkACLArgs']]=None):
        """
        Network ACLs for the resource
        :param pulumi.Input[Union[str, 'ACLAction']] default_action: Azure Networking ACL Action.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateEndpointACLArgs']]] private_endpoints: ACLs for requests from private endpoints
        :param pulumi.Input['NetworkACLArgs'] public_network: Network ACL
        """
        if default_action is not None:
            pulumi.set(__self__, 'default_action', default_action)
        if private_endpoints is not None:
            pulumi.set(__self__, 'private_endpoints', private_endpoints)
        if public_network is not None:
            pulumi.set(__self__, 'public_network', public_network)

    @property
    @pulumi.getter(name='defaultAction')
    def default_action(self) -> Optional[pulumi.Input[Union[str, 'ACLAction']]]:
        """
        Azure Networking ACL Action.
        """
        return pulumi.get(self, 'default_action')

    @default_action.setter
    def default_action(self, value: Optional[pulumi.Input[Union[str, 'ACLAction']]]):
        pulumi.set(self, 'default_action', value)

    @property
    @pulumi.getter(name='privateEndpoints')
    def private_endpoints(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointACLArgs']]]]:
        """
        ACLs for requests from private endpoints
        """
        return pulumi.get(self, 'private_endpoints')

    @private_endpoints.setter
    def private_endpoints(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointACLArgs']]]]):
        pulumi.set(self, 'private_endpoints', value)

    @property
    @pulumi.getter(name='publicNetwork')
    def public_network(self) -> Optional[pulumi.Input['NetworkACLArgs']]:
        """
        Network ACL
        """
        return pulumi.get(self, 'public_network')

    @public_network.setter
    def public_network(self, value: Optional[pulumi.Input['NetworkACLArgs']]):
        pulumi.set(self, 'public_network', value)

@pulumi.input_type
class WebPubSubTlsSettingsArgs:

    def __init__(__self__, *, client_cert_enabled: Optional[pulumi.Input[bool]]=None):
        """
        TLS settings for the resource
        :param pulumi.Input[bool] client_cert_enabled: Request client certificate during TLS handshake if enabled
        """
        if client_cert_enabled is None:
            client_cert_enabled = True
        if client_cert_enabled is not None:
            pulumi.set(__self__, 'client_cert_enabled', client_cert_enabled)

    @property
    @pulumi.getter(name='clientCertEnabled')
    def client_cert_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Request client certificate during TLS handshake if enabled
        """
        return pulumi.get(self, 'client_cert_enabled')

    @client_cert_enabled.setter
    def client_cert_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'client_cert_enabled', value)
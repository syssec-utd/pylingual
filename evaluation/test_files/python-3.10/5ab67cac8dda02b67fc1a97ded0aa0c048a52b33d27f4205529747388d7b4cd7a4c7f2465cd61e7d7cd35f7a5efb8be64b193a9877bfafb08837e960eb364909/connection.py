import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ConnectionArgs', 'Connection']

@pulumi.input_type
class ConnectionArgs:

    def __init__(__self__, *, application_endpoint: pulumi.Input['ApplicationEndpointArgs'], type: pulumi.Input['ConnectionType'], connection_id: Optional[pulumi.Input[str]]=None, connectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_name: Optional[pulumi.Input[str]]=None, gateway: Optional[pulumi.Input['GatewayArgs']]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Connection resource.
        :param pulumi.Input['ApplicationEndpointArgs'] application_endpoint: Address of the remote application endpoint for the BeyondCorp Connection.
        :param pulumi.Input['ConnectionType'] type: The type of network connectivity used by the connection.
        :param pulumi.Input[str] connection_id: Optional. User-settable connection resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connectors: Optional. List of [google.cloud.beyondcorp.v1main.Connector.name] that are authorised to be associated with this Connection.
        :param pulumi.Input[str] display_name: Optional. An arbitrary user-provided name for the connection. Cannot exceed 64 characters.
        :param pulumi.Input['GatewayArgs'] gateway: Optional. Gateway used by the connection.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: Unique resource name of the connection. The name is ignored when creating a connection.
        :param pulumi.Input[str] request_id: Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[str] validate_only: Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        pulumi.set(__self__, 'application_endpoint', application_endpoint)
        pulumi.set(__self__, 'type', type)
        if connection_id is not None:
            pulumi.set(__self__, 'connection_id', connection_id)
        if connectors is not None:
            pulumi.set(__self__, 'connectors', connectors)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if gateway is not None:
            pulumi.set(__self__, 'gateway', gateway)
        if labels is not None:
            pulumi.set(__self__, 'labels', labels)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if request_id is not None:
            pulumi.set(__self__, 'request_id', request_id)
        if validate_only is not None:
            pulumi.set(__self__, 'validate_only', validate_only)

    @property
    @pulumi.getter(name='applicationEndpoint')
    def application_endpoint(self) -> pulumi.Input['ApplicationEndpointArgs']:
        """
        Address of the remote application endpoint for the BeyondCorp Connection.
        """
        return pulumi.get(self, 'application_endpoint')

    @application_endpoint.setter
    def application_endpoint(self, value: pulumi.Input['ApplicationEndpointArgs']):
        pulumi.set(self, 'application_endpoint', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['ConnectionType']:
        """
        The type of network connectivity used by the connection.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input['ConnectionType']):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='connectionId')
    def connection_id(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-settable connection resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter.
        """
        return pulumi.get(self, 'connection_id')

    @connection_id.setter
    def connection_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'connection_id', value)

    @property
    @pulumi.getter
    def connectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Optional. List of [google.cloud.beyondcorp.v1main.Connector.name] that are authorised to be associated with this Connection.
        """
        return pulumi.get(self, 'connectors')

    @connectors.setter
    def connectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'connectors', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. An arbitrary user-provided name for the connection. Cannot exceed 64 characters.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def gateway(self) -> Optional[pulumi.Input['GatewayArgs']]:
        """
        Optional. Gateway used by the connection.
        """
        return pulumi.get(self, 'gateway')

    @gateway.setter
    def gateway(self, value: Optional[pulumi.Input['GatewayArgs']]):
        pulumi.set(self, 'gateway', value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Optional. Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, 'labels')

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'labels', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique resource name of the connection. The name is ignored when creating a connection.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter(name='requestId')
    def request_id(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, 'request_id')

    @request_id.setter
    def request_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'request_id', value)

    @property
    @pulumi.getter(name='validateOnly')
    def validate_only(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        return pulumi.get(self, 'validate_only')

    @validate_only.setter
    def validate_only(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'validate_only', value)

class Connection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_endpoint: Optional[pulumi.Input[pulumi.InputType['ApplicationEndpointArgs']]]=None, connection_id: Optional[pulumi.Input[str]]=None, connectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_name: Optional[pulumi.Input[str]]=None, gateway: Optional[pulumi.Input[pulumi.InputType['GatewayArgs']]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input['ConnectionType']]=None, validate_only: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Creates a new Connection in a given project and location.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ApplicationEndpointArgs']] application_endpoint: Address of the remote application endpoint for the BeyondCorp Connection.
        :param pulumi.Input[str] connection_id: Optional. User-settable connection resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connectors: Optional. List of [google.cloud.beyondcorp.v1main.Connector.name] that are authorised to be associated with this Connection.
        :param pulumi.Input[str] display_name: Optional. An arbitrary user-provided name for the connection. Cannot exceed 64 characters.
        :param pulumi.Input[pulumi.InputType['GatewayArgs']] gateway: Optional. Gateway used by the connection.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] labels: Optional. Resource labels to represent user provided metadata.
        :param pulumi.Input[str] name: Unique resource name of the connection. The name is ignored when creating a connection.
        :param pulumi.Input[str] request_id: Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input['ConnectionType'] type: The type of network connectivity used by the connection.
        :param pulumi.Input[str] validate_only: Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ConnectionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a new Connection in a given project and location.

        :param str resource_name: The name of the resource.
        :param ConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_endpoint: Optional[pulumi.Input[pulumi.InputType['ApplicationEndpointArgs']]]=None, connection_id: Optional[pulumi.Input[str]]=None, connectors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, display_name: Optional[pulumi.Input[str]]=None, gateway: Optional[pulumi.Input[pulumi.InputType['GatewayArgs']]]=None, labels: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input['ConnectionType']]=None, validate_only: Optional[pulumi.Input[str]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        else:
            opts = copy.copy(opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectionArgs.__new__(ConnectionArgs)
            if application_endpoint is None and (not opts.urn):
                raise TypeError("Missing required property 'application_endpoint'")
            __props__.__dict__['application_endpoint'] = application_endpoint
            __props__.__dict__['connection_id'] = connection_id
            __props__.__dict__['connectors'] = connectors
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['gateway'] = gateway
            __props__.__dict__['labels'] = labels
            __props__.__dict__['location'] = location
            __props__.__dict__['name'] = name
            __props__.__dict__['project'] = project
            __props__.__dict__['request_id'] = request_id
            if type is None and (not opts.urn):
                raise TypeError("Missing required property 'type'")
            __props__.__dict__['type'] = type
            __props__.__dict__['validate_only'] = validate_only
            __props__.__dict__['create_time'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['uid'] = None
            __props__.__dict__['update_time'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['location', 'project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Connection, __self__).__init__('google-native:beyondcorp/v1alpha:Connection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Connection':
        """
        Get an existing Connection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ConnectionArgs.__new__(ConnectionArgs)
        __props__.__dict__['application_endpoint'] = None
        __props__.__dict__['connection_id'] = None
        __props__.__dict__['connectors'] = None
        __props__.__dict__['create_time'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['gateway'] = None
        __props__.__dict__['labels'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['request_id'] = None
        __props__.__dict__['state'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['uid'] = None
        __props__.__dict__['update_time'] = None
        __props__.__dict__['validate_only'] = None
        return Connection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='applicationEndpoint')
    def application_endpoint(self) -> pulumi.Output['outputs.ApplicationEndpointResponse']:
        """
        Address of the remote application endpoint for the BeyondCorp Connection.
        """
        return pulumi.get(self, 'application_endpoint')

    @property
    @pulumi.getter(name='connectionId')
    def connection_id(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. User-settable connection resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter.
        """
        return pulumi.get(self, 'connection_id')

    @property
    @pulumi.getter
    def connectors(self) -> pulumi.Output[Sequence[str]]:
        """
        Optional. List of [google.cloud.beyondcorp.v1main.Connector.name] that are authorised to be associated with this Connection.
        """
        return pulumi.get(self, 'connectors')

    @property
    @pulumi.getter(name='createTime')
    def create_time(self) -> pulumi.Output[str]:
        """
        Timestamp when the resource was created.
        """
        return pulumi.get(self, 'create_time')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        Optional. An arbitrary user-provided name for the connection. Cannot exceed 64 characters.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def gateway(self) -> pulumi.Output['outputs.GatewayResponse']:
        """
        Optional. Gateway used by the connection.
        """
        return pulumi.get(self, 'gateway')

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Optional. Resource labels to represent user provided metadata.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Unique resource name of the connection. The name is ignored when creating a connection.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter(name='requestId')
    def request_id(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        """
        return pulumi.get(self, 'request_id')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the connection.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of network connectivity used by the connection.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def uid(self) -> pulumi.Output[str]:
        """
        A unique identifier for the instance generated by the system.
        """
        return pulumi.get(self, 'uid')

    @property
    @pulumi.getter(name='updateTime')
    def update_time(self) -> pulumi.Output[str]:
        """
        Timestamp when the resource was last modified.
        """
        return pulumi.get(self, 'update_time')

    @property
    @pulumi.getter(name='validateOnly')
    def validate_only(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        return pulumi.get(self, 'validate_only')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['ClientConnectorServiceArgs', 'ClientConnectorService']

@pulumi.input_type
class ClientConnectorServiceArgs:

    def __init__(__self__, *, egress: pulumi.Input['EgressArgs'], ingress: pulumi.Input['IngressArgs'], client_connector_service_id: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a ClientConnectorService resource.
        :param pulumi.Input['EgressArgs'] egress: The details of the egress settings.
        :param pulumi.Input['IngressArgs'] ingress: The details of the ingress settings.
        :param pulumi.Input[str] client_connector_service_id: Optional. User-settable client connector service resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter. A random system generated name will be assigned if not specified by the user.
        :param pulumi.Input[str] display_name: Optional. User-provided name. The display name should follow certain format. * Must be 6 to 30 characters in length. * Can only contain lowercase letters, numbers, and hyphens. * Must start with a letter.
        :param pulumi.Input[str] name: Name of resource. The name is ignored during creation.
        :param pulumi.Input[str] request_id: Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[bool] validate_only: Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        pulumi.set(__self__, 'egress', egress)
        pulumi.set(__self__, 'ingress', ingress)
        if client_connector_service_id is not None:
            pulumi.set(__self__, 'client_connector_service_id', client_connector_service_id)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
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
    @pulumi.getter
    def egress(self) -> pulumi.Input['EgressArgs']:
        """
        The details of the egress settings.
        """
        return pulumi.get(self, 'egress')

    @egress.setter
    def egress(self, value: pulumi.Input['EgressArgs']):
        pulumi.set(self, 'egress', value)

    @property
    @pulumi.getter
    def ingress(self) -> pulumi.Input['IngressArgs']:
        """
        The details of the ingress settings.
        """
        return pulumi.get(self, 'ingress')

    @ingress.setter
    def ingress(self, value: pulumi.Input['IngressArgs']):
        pulumi.set(self, 'ingress', value)

    @property
    @pulumi.getter(name='clientConnectorServiceId')
    def client_connector_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-settable client connector service resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter. A random system generated name will be assigned if not specified by the user.
        """
        return pulumi.get(self, 'client_connector_service_id')

    @client_connector_service_id.setter
    def client_connector_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'client_connector_service_id', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-provided name. The display name should follow certain format. * Must be 6 to 30 characters in length. * Can only contain lowercase letters, numbers, and hyphens. * Must start with a letter.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

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
        Name of resource. The name is ignored during creation.
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
    def validate_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        return pulumi.get(self, 'validate_only')

    @validate_only.setter
    def validate_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'validate_only', value)

class ClientConnectorService(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_connector_service_id: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, egress: Optional[pulumi.Input[pulumi.InputType['EgressArgs']]]=None, ingress: Optional[pulumi.Input[pulumi.InputType['IngressArgs']]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        Creates a new ClientConnectorService in a given project and location.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] client_connector_service_id: Optional. User-settable client connector service resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter. A random system generated name will be assigned if not specified by the user.
        :param pulumi.Input[str] display_name: Optional. User-provided name. The display name should follow certain format. * Must be 6 to 30 characters in length. * Can only contain lowercase letters, numbers, and hyphens. * Must start with a letter.
        :param pulumi.Input[pulumi.InputType['EgressArgs']] egress: The details of the egress settings.
        :param pulumi.Input[pulumi.InputType['IngressArgs']] ingress: The details of the ingress settings.
        :param pulumi.Input[str] name: Name of resource. The name is ignored during creation.
        :param pulumi.Input[str] request_id: Optional. An optional request ID to identify requests. Specify a unique request ID so that if you must retry your request, the server will know to ignore the request if it has already been completed. The server will guarantee that for at least 60 minutes since the first request. For example, consider a situation where you make an initial request and t he request times out. If you make the request again with the same request ID, the server can check if original operation with the same request ID was received, and if so, will ignore the second request. This prevents clients from accidentally creating duplicate commitments. The request ID must be a valid UUID with the exception that zero UUID is not supported (00000000-0000-0000-0000-000000000000).
        :param pulumi.Input[bool] validate_only: Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ClientConnectorServiceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a new ClientConnectorService in a given project and location.

        :param str resource_name: The name of the resource.
        :param ClientConnectorServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ClientConnectorServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, client_connector_service_id: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, egress: Optional[pulumi.Input[pulumi.InputType['EgressArgs']]]=None, ingress: Optional[pulumi.Input[pulumi.InputType['IngressArgs']]]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, request_id: Optional[pulumi.Input[str]]=None, validate_only: Optional[pulumi.Input[bool]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClientConnectorServiceArgs.__new__(ClientConnectorServiceArgs)
            __props__.__dict__['client_connector_service_id'] = client_connector_service_id
            __props__.__dict__['display_name'] = display_name
            if egress is None and (not opts.urn):
                raise TypeError("Missing required property 'egress'")
            __props__.__dict__['egress'] = egress
            if ingress is None and (not opts.urn):
                raise TypeError("Missing required property 'ingress'")
            __props__.__dict__['ingress'] = ingress
            __props__.__dict__['location'] = location
            __props__.__dict__['name'] = name
            __props__.__dict__['project'] = project
            __props__.__dict__['request_id'] = request_id
            __props__.__dict__['validate_only'] = validate_only
            __props__.__dict__['create_time'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['update_time'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['location', 'project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(ClientConnectorService, __self__).__init__('google-native:beyondcorp/v1alpha:ClientConnectorService', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ClientConnectorService':
        """
        Get an existing ClientConnectorService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ClientConnectorServiceArgs.__new__(ClientConnectorServiceArgs)
        __props__.__dict__['client_connector_service_id'] = None
        __props__.__dict__['create_time'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['egress'] = None
        __props__.__dict__['ingress'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['request_id'] = None
        __props__.__dict__['state'] = None
        __props__.__dict__['update_time'] = None
        __props__.__dict__['validate_only'] = None
        return ClientConnectorService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='clientConnectorServiceId')
    def client_connector_service_id(self) -> pulumi.Output[Optional[str]]:
        """
        Optional. User-settable client connector service resource ID. * Must start with a letter. * Must contain between 4-63 characters from `/a-z-/`. * Must end with a number or a letter. A random system generated name will be assigned if not specified by the user.
        """
        return pulumi.get(self, 'client_connector_service_id')

    @property
    @pulumi.getter(name='createTime')
    def create_time(self) -> pulumi.Output[str]:
        """
        [Output only] Create time stamp.
        """
        return pulumi.get(self, 'create_time')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        Optional. User-provided name. The display name should follow certain format. * Must be 6 to 30 characters in length. * Can only contain lowercase letters, numbers, and hyphens. * Must start with a letter.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def egress(self) -> pulumi.Output['outputs.EgressResponse']:
        """
        The details of the egress settings.
        """
        return pulumi.get(self, 'egress')

    @property
    @pulumi.getter
    def ingress(self) -> pulumi.Output['outputs.IngressResponse']:
        """
        The details of the ingress settings.
        """
        return pulumi.get(self, 'ingress')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of resource. The name is ignored during creation.
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
        The operational state of the ClientConnectorService.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter(name='updateTime')
    def update_time(self) -> pulumi.Output[str]:
        """
        [Output only] Update time stamp.
        """
        return pulumi.get(self, 'update_time')

    @property
    @pulumi.getter(name='validateOnly')
    def validate_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Optional. If set, validates request by executing a dry-run which would not alter the resource in any way.
        """
        return pulumi.get(self, 'validate_only')
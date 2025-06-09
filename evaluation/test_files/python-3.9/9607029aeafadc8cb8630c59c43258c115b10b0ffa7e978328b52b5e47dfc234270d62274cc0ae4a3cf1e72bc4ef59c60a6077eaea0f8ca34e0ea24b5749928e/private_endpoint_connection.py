import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['PrivateEndpointConnectionInitArgs', 'PrivateEndpointConnection']

@pulumi.input_type
class PrivateEndpointConnectionInitArgs:

    def __init__(__self__, *, namespace_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], private_endpoint: Optional[pulumi.Input['PrivateEndpointArgs']]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input['ConnectionStateArgs']]=None, provisioning_state: Optional[pulumi.Input[Union[str, 'EndPointProvisioningState']]]=None):
        """
        The set of arguments for constructing a PrivateEndpointConnection resource.
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input['PrivateEndpointArgs'] private_endpoint: The Private Endpoint resource for this Connection.
        :param pulumi.Input[str] private_endpoint_connection_name: The PrivateEndpointConnection name
        :param pulumi.Input['ConnectionStateArgs'] private_link_service_connection_state: Details about the state of the connection.
        :param pulumi.Input[Union[str, 'EndPointProvisioningState']] provisioning_state: Provisioning state of the Private Endpoint Connection.
        """
        pulumi.set(__self__, 'namespace_name', namespace_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if private_endpoint is not None:
            pulumi.set(__self__, 'private_endpoint', private_endpoint)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, 'private_endpoint_connection_name', private_endpoint_connection_name)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, 'private_link_service_connection_state', private_link_service_connection_state)
        if provisioning_state is not None:
            pulumi.set(__self__, 'provisioning_state', provisioning_state)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The Namespace name
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the azure subscription.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> Optional[pulumi.Input['PrivateEndpointArgs']]:
        """
        The Private Endpoint resource for this Connection.
        """
        return pulumi.get(self, 'private_endpoint')

    @private_endpoint.setter
    def private_endpoint(self, value: Optional[pulumi.Input['PrivateEndpointArgs']]):
        pulumi.set(self, 'private_endpoint', value)

    @property
    @pulumi.getter(name='privateEndpointConnectionName')
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The PrivateEndpointConnection name
        """
        return pulumi.get(self, 'private_endpoint_connection_name')

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_connection_name', value)

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> Optional[pulumi.Input['ConnectionStateArgs']]:
        """
        Details about the state of the connection.
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: Optional[pulumi.Input['ConnectionStateArgs']]):
        pulumi.set(self, 'private_link_service_connection_state', value)

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'EndPointProvisioningState']]]:
        """
        Provisioning state of the Private Endpoint Connection.
        """
        return pulumi.get(self, 'provisioning_state')

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'EndPointProvisioningState']]]):
        pulumi.set(self, 'provisioning_state', value)

class PrivateEndpointConnection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, namespace_name: Optional[pulumi.Input[str]]=None, private_endpoint: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointArgs']]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['ConnectionStateArgs']]]=None, provisioning_state: Optional[pulumi.Input[Union[str, 'EndPointProvisioningState']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Properties of the PrivateEndpointConnection.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[pulumi.InputType['PrivateEndpointArgs']] private_endpoint: The Private Endpoint resource for this Connection.
        :param pulumi.Input[str] private_endpoint_connection_name: The PrivateEndpointConnection name
        :param pulumi.Input[pulumi.InputType['ConnectionStateArgs']] private_link_service_connection_state: Details about the state of the connection.
        :param pulumi.Input[Union[str, 'EndPointProvisioningState']] provisioning_state: Provisioning state of the Private Endpoint Connection.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PrivateEndpointConnectionInitArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Properties of the PrivateEndpointConnection.

        :param str resource_name: The name of the resource.
        :param PrivateEndpointConnectionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(PrivateEndpointConnectionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, namespace_name: Optional[pulumi.Input[str]]=None, private_endpoint: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointArgs']]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['ConnectionStateArgs']]]=None, provisioning_state: Optional[pulumi.Input[Union[str, 'EndPointProvisioningState']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateEndpointConnectionInitArgs.__new__(PrivateEndpointConnectionInitArgs)
            if namespace_name is None and (not opts.urn):
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__['namespace_name'] = namespace_name
            __props__.__dict__['private_endpoint'] = private_endpoint
            __props__.__dict__['private_endpoint_connection_name'] = private_endpoint_connection_name
            __props__.__dict__['private_link_service_connection_state'] = private_link_service_connection_state
            __props__.__dict__['provisioning_state'] = provisioning_state
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['location'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:eventhub:PrivateEndpointConnection'), pulumi.Alias(type_='azure-native:eventhub/v20180101preview:PrivateEndpointConnection'), pulumi.Alias(type_='azure-native:eventhub/v20210101preview:PrivateEndpointConnection'), pulumi.Alias(type_='azure-native:eventhub/v20210601preview:PrivateEndpointConnection'), pulumi.Alias(type_='azure-native:eventhub/v20220101preview:PrivateEndpointConnection'), pulumi.Alias(type_='azure-native:eventhub/v20221001preview:PrivateEndpointConnection')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateEndpointConnection, __self__).__init__('azure-native:eventhub/v20211101:PrivateEndpointConnection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'PrivateEndpointConnection':
        """
        Get an existing PrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = PrivateEndpointConnectionInitArgs.__new__(PrivateEndpointConnectionInitArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['private_endpoint'] = None
        __props__.__dict__['private_link_service_connection_state'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return PrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> pulumi.Output[Optional['outputs.PrivateEndpointResponse']]:
        """
        The Private Endpoint resource for this Connection.
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> pulumi.Output[Optional['outputs.ConnectionStateResponse']]:
        """
        Details about the state of the connection.
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provisioning state of the Private Endpoint Connection.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.EventHub/Namespaces" or "Microsoft.EventHub/Namespaces/EventHubs"
        """
        return pulumi.get(self, 'type')
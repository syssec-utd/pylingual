import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['StaticSitePrivateEndpointConnectionArgs', 'StaticSitePrivateEndpointConnection']

@pulumi.input_type
class StaticSitePrivateEndpointConnectionArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], kind: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input['PrivateLinkConnectionStateArgs']]=None):
        """
        The set of arguments for constructing a StaticSitePrivateEndpointConnection resource.
        :param pulumi.Input[str] name: Name of the static site.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] private_endpoint_connection_name: Name of the private endpoint connection.
        :param pulumi.Input['PrivateLinkConnectionStateArgs'] private_link_service_connection_state: The state of a private link connection
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if kind is not None:
            pulumi.set(__self__, 'kind', kind)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, 'private_endpoint_connection_name', private_endpoint_connection_name)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, 'private_link_service_connection_state', private_link_service_connection_state)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the static site.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'kind', value)

    @property
    @pulumi.getter(name='privateEndpointConnectionName')
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the private endpoint connection.
        """
        return pulumi.get(self, 'private_endpoint_connection_name')

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_connection_name', value)

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> Optional[pulumi.Input['PrivateLinkConnectionStateArgs']]:
        """
        The state of a private link connection
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: Optional[pulumi.Input['PrivateLinkConnectionStateArgs']]):
        pulumi.set(self, 'private_link_service_connection_state', value)

class StaticSitePrivateEndpointConnection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['PrivateLinkConnectionStateArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Remote Private Endpoint Connection ARM resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the static site.
        :param pulumi.Input[str] private_endpoint_connection_name: Name of the private endpoint connection.
        :param pulumi.Input[pulumi.InputType['PrivateLinkConnectionStateArgs']] private_link_service_connection_state: The state of a private link connection
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: StaticSitePrivateEndpointConnectionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Remote Private Endpoint Connection ARM resource.

        :param str resource_name: The name of the resource.
        :param StaticSitePrivateEndpointConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(StaticSitePrivateEndpointConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, kind: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['PrivateLinkConnectionStateArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StaticSitePrivateEndpointConnectionArgs.__new__(StaticSitePrivateEndpointConnectionArgs)
            __props__.__dict__['kind'] = kind
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['private_endpoint_connection_name'] = private_endpoint_connection_name
            __props__.__dict__['private_link_service_connection_state'] = private_link_service_connection_state
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['ip_addresses'] = None
            __props__.__dict__['private_endpoint'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:web:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20201201:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20210101:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20210115:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20210201:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20210301:StaticSitePrivateEndpointConnection'), pulumi.Alias(type_='azure-native:web/v20220301:StaticSitePrivateEndpointConnection')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StaticSitePrivateEndpointConnection, __self__).__init__('azure-native:web/v20220901:StaticSitePrivateEndpointConnection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'StaticSitePrivateEndpointConnection':
        """
        Get an existing StaticSitePrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = StaticSitePrivateEndpointConnectionArgs.__new__(StaticSitePrivateEndpointConnectionArgs)
        __props__.__dict__['ip_addresses'] = None
        __props__.__dict__['kind'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['private_endpoint'] = None
        __props__.__dict__['private_link_service_connection_state'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['type'] = None
        return StaticSitePrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='ipAddresses')
    def ip_addresses(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Private IPAddresses mapped to the remote private endpoint
        """
        return pulumi.get(self, 'ip_addresses')

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> pulumi.Output[Optional['outputs.ArmIdWrapperResponse']]:
        """
        PrivateEndpoint of a remote private endpoint connection
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> pulumi.Output[Optional['outputs.PrivateLinkConnectionStateResponse']]:
        """
        The state of a private link connection
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['MHSMPrivateEndpointConnectionArgs', 'MHSMPrivateEndpointConnection']

@pulumi.input_type
class MHSMPrivateEndpointConnectionArgs:

    def __init__(__self__, *, name: pulumi.Input[str], resource_group_name: pulumi.Input[str], location: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input['MHSMPrivateLinkServiceConnectionStateArgs']]=None, sku: Optional[pulumi.Input['ManagedHsmSkuArgs']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a MHSMPrivateEndpointConnection resource.
        :param pulumi.Input[str] name: Name of the managed HSM Pool
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the managed HSM pool.
        :param pulumi.Input[str] location: The supported Azure location where the managed HSM Pool should be created.
        :param pulumi.Input[str] private_endpoint_connection_name: Name of the private endpoint connection associated with the managed hsm pool.
        :param pulumi.Input['MHSMPrivateLinkServiceConnectionStateArgs'] private_link_service_connection_state: Approval state of the private link connection.
        :param pulumi.Input['ManagedHsmSkuArgs'] sku: SKU details
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, 'private_endpoint_connection_name', private_endpoint_connection_name)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, 'private_link_service_connection_state', private_link_service_connection_state)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the managed HSM Pool
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group that contains the managed HSM pool.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The supported Azure location where the managed HSM Pool should be created.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='privateEndpointConnectionName')
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the private endpoint connection associated with the managed hsm pool.
        """
        return pulumi.get(self, 'private_endpoint_connection_name')

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'private_endpoint_connection_name', value)

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> Optional[pulumi.Input['MHSMPrivateLinkServiceConnectionStateArgs']]:
        """
        Approval state of the private link connection.
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: Optional[pulumi.Input['MHSMPrivateLinkServiceConnectionStateArgs']]):
        pulumi.set(self, 'private_link_service_connection_state', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ManagedHsmSkuArgs']]:
        """
        SKU details
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ManagedHsmSkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class MHSMPrivateEndpointConnection(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['MHSMPrivateLinkServiceConnectionStateArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ManagedHsmSkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Private endpoint connection resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The supported Azure location where the managed HSM Pool should be created.
        :param pulumi.Input[str] name: Name of the managed HSM Pool
        :param pulumi.Input[str] private_endpoint_connection_name: Name of the private endpoint connection associated with the managed hsm pool.
        :param pulumi.Input[pulumi.InputType['MHSMPrivateLinkServiceConnectionStateArgs']] private_link_service_connection_state: Approval state of the private link connection.
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the managed HSM pool.
        :param pulumi.Input[pulumi.InputType['ManagedHsmSkuArgs']] sku: SKU details
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: MHSMPrivateEndpointConnectionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Private endpoint connection resource.

        :param str resource_name: The name of the resource.
        :param MHSMPrivateEndpointConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(MHSMPrivateEndpointConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, location: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, private_endpoint_connection_name: Optional[pulumi.Input[str]]=None, private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['MHSMPrivateLinkServiceConnectionStateArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['ManagedHsmSkuArgs']]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MHSMPrivateEndpointConnectionArgs.__new__(MHSMPrivateEndpointConnectionArgs)
            __props__.__dict__['location'] = location
            if name is None and (not opts.urn):
                raise TypeError("Missing required property 'name'")
            __props__.__dict__['name'] = name
            __props__.__dict__['private_endpoint_connection_name'] = private_endpoint_connection_name
            __props__.__dict__['private_link_service_connection_state'] = private_link_service_connection_state
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['tags'] = tags
            __props__.__dict__['etag'] = None
            __props__.__dict__['private_endpoint'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:keyvault:MHSMPrivateEndpointConnection'), pulumi.Alias(type_='azure-native:keyvault/v20210601preview:MHSMPrivateEndpointConnection'), pulumi.Alias(type_='azure-native:keyvault/v20211001:MHSMPrivateEndpointConnection'), pulumi.Alias(type_='azure-native:keyvault/v20211101preview:MHSMPrivateEndpointConnection'), pulumi.Alias(type_='azure-native:keyvault/v20220701:MHSMPrivateEndpointConnection')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MHSMPrivateEndpointConnection, __self__).__init__('azure-native:keyvault/v20210401preview:MHSMPrivateEndpointConnection', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'MHSMPrivateEndpointConnection':
        """
        Get an existing MHSMPrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = MHSMPrivateEndpointConnectionArgs.__new__(MHSMPrivateEndpointConnectionArgs)
        __props__.__dict__['etag'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['private_endpoint'] = None
        __props__.__dict__['private_link_service_connection_state'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return MHSMPrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Modified whenever there is a change in the state of private endpoint connection.
        """
        return pulumi.get(self, 'etag')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The supported Azure location where the managed HSM Pool should be created.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the managed HSM Pool.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='privateEndpoint')
    def private_endpoint(self) -> pulumi.Output[Optional['outputs.MHSMPrivateEndpointResponse']]:
        """
        Properties of the private endpoint object.
        """
        return pulumi.get(self, 'private_endpoint')

    @property
    @pulumi.getter(name='privateLinkServiceConnectionState')
    def private_link_service_connection_state(self) -> pulumi.Output[Optional['outputs.MHSMPrivateLinkServiceConnectionStateResponse']]:
        """
        Approval state of the private link connection.
        """
        return pulumi.get(self, 'private_link_service_connection_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the private endpoint connection.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ManagedHsmSkuResponse']]:
        """
        SKU details
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the key vault resource.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type of the managed HSM Pool.
        """
        return pulumi.get(self, 'type')
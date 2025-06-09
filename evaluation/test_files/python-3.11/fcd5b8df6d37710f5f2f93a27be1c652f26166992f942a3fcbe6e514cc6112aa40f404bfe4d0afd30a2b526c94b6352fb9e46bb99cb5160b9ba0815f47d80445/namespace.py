import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['NamespaceArgs', 'Namespace']

@pulumi.input_type
class NamespaceArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], create_acs_namespace: Optional[pulumi.Input[bool]]=None, enabled: Optional[pulumi.Input[bool]]=None, location: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input['SkuArgs']]=None, status: Optional[pulumi.Input['NamespaceState']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a Namespace resource.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[bool] create_acs_namespace: Indicates whether to create an ACS namespace.
        :param pulumi.Input[bool] enabled: Specifies whether this instance is enabled.
        :param pulumi.Input[str] location: Namespace location.
        :param pulumi.Input[str] namespace_name: The namespace name.
        :param pulumi.Input['SkuArgs'] sku: SKU of the namespace.
        :param pulumi.Input['NamespaceState'] status: State of the namespace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Namespace tags.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if create_acs_namespace is not None:
            pulumi.set(__self__, 'create_acs_namespace', create_acs_namespace)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if namespace_name is not None:
            pulumi.set(__self__, 'namespace_name', namespace_name)
        if sku is not None:
            pulumi.set(__self__, 'sku', sku)
        if status is not None:
            pulumi.set(__self__, 'status', status)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Resource group within the Azure subscription.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='createACSNamespace')
    def create_acs_namespace(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to create an ACS namespace.
        """
        return pulumi.get(self, 'create_acs_namespace')

    @create_acs_namespace.setter
    def create_acs_namespace(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'create_acs_namespace', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether this instance is enabled.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace name.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        SKU of the namespace.
        """
        return pulumi.get(self, 'sku')

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, 'sku', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['NamespaceState']]:
        """
        State of the namespace.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input['NamespaceState']]):
        pulumi.set(self, 'status', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Namespace tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)
warnings.warn('Version 2014-09-01 will be removed in v2 of the provider.', DeprecationWarning)

class Namespace(pulumi.CustomResource):
    warnings.warn('Version 2014-09-01 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, create_acs_namespace: Optional[pulumi.Input[bool]]=None, enabled: Optional[pulumi.Input[bool]]=None, location: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, status: Optional[pulumi.Input['NamespaceState']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Description of a namespace resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] create_acs_namespace: Indicates whether to create an ACS namespace.
        :param pulumi.Input[bool] enabled: Specifies whether this instance is enabled.
        :param pulumi.Input[str] location: Namespace location.
        :param pulumi.Input[str] namespace_name: The namespace name.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: SKU of the namespace.
        :param pulumi.Input['NamespaceState'] status: State of the namespace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Namespace tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: NamespaceArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Description of a namespace resource.

        :param str resource_name: The name of the resource.
        :param NamespaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NamespaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, create_acs_namespace: Optional[pulumi.Input[bool]]=None, enabled: Optional[pulumi.Input[bool]]=None, location: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]]=None, status: Optional[pulumi.Input['NamespaceState']]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        pulumi.log.warn('Namespace is deprecated: Version 2014-09-01 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NamespaceArgs.__new__(NamespaceArgs)
            __props__.__dict__['create_acs_namespace'] = create_acs_namespace
            __props__.__dict__['enabled'] = enabled
            __props__.__dict__['location'] = location
            __props__.__dict__['namespace_name'] = namespace_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sku'] = sku
            __props__.__dict__['status'] = status
            __props__.__dict__['tags'] = tags
            __props__.__dict__['created_at'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['service_bus_endpoint'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['updated_at'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:servicebus:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20150801:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20170401:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20180101preview:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20210101preview:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20210601preview:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20211101:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20220101preview:Namespace'), pulumi.Alias(type_='azure-native:servicebus/v20221001preview:Namespace')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Namespace, __self__).__init__('azure-native:servicebus/v20140901:Namespace', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Namespace':
        """
        Get an existing Namespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = NamespaceArgs.__new__(NamespaceArgs)
        __props__.__dict__['create_acs_namespace'] = None
        __props__.__dict__['created_at'] = None
        __props__.__dict__['enabled'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['service_bus_endpoint'] = None
        __props__.__dict__['sku'] = None
        __props__.__dict__['status'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['updated_at'] = None
        return Namespace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='createACSNamespace')
    def create_acs_namespace(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether to create an ACS namespace.
        """
        return pulumi.get(self, 'create_acs_namespace')

    @property
    @pulumi.getter(name='createdAt')
    def created_at(self) -> pulumi.Output[str]:
        """
        The time the namespace was created.
        """
        return pulumi.get(self, 'created_at')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether this instance is enabled.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the namespace.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='serviceBusEndpoint')
    def service_bus_endpoint(self) -> pulumi.Output[str]:
        """
        Endpoint you can use to perform Service Bus operations.
        """
        return pulumi.get(self, 'service_bus_endpoint')

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        SKU of the namespace.
        """
        return pulumi.get(self, 'sku')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        State of the namespace.
        """
        return pulumi.get(self, 'status')

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
        Resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='updatedAt')
    def updated_at(self) -> pulumi.Output[str]:
        """
        The time the namespace was updated.
        """
        return pulumi.get(self, 'updated_at')
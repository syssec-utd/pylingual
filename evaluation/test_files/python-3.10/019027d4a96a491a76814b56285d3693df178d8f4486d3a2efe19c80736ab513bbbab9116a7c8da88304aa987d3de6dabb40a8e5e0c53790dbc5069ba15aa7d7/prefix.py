import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['PrefixArgs', 'Prefix']

@pulumi.input_type
class PrefixArgs:

    def __init__(__self__, *, peering_service_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], peering_service_prefix_key: Optional[pulumi.Input[str]]=None, prefix: Optional[pulumi.Input[str]]=None, prefix_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Prefix resource.
        :param pulumi.Input[str] peering_service_name: The name of the peering service.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] peering_service_prefix_key: The peering service prefix key
        :param pulumi.Input[str] prefix: The prefix from which your traffic originates.
        :param pulumi.Input[str] prefix_name: The name of the prefix.
        """
        pulumi.set(__self__, 'peering_service_name', peering_service_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if peering_service_prefix_key is not None:
            pulumi.set(__self__, 'peering_service_prefix_key', peering_service_prefix_key)
        if prefix is not None:
            pulumi.set(__self__, 'prefix', prefix)
        if prefix_name is not None:
            pulumi.set(__self__, 'prefix_name', prefix_name)

    @property
    @pulumi.getter(name='peeringServiceName')
    def peering_service_name(self) -> pulumi.Input[str]:
        """
        The name of the peering service.
        """
        return pulumi.get(self, 'peering_service_name')

    @peering_service_name.setter
    def peering_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'peering_service_name', value)

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
    @pulumi.getter(name='peeringServicePrefixKey')
    def peering_service_prefix_key(self) -> Optional[pulumi.Input[str]]:
        """
        The peering service prefix key
        """
        return pulumi.get(self, 'peering_service_prefix_key')

    @peering_service_prefix_key.setter
    def peering_service_prefix_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'peering_service_prefix_key', value)

    @property
    @pulumi.getter
    def prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The prefix from which your traffic originates.
        """
        return pulumi.get(self, 'prefix')

    @prefix.setter
    def prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'prefix', value)

    @property
    @pulumi.getter(name='prefixName')
    def prefix_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the prefix.
        """
        return pulumi.get(self, 'prefix_name')

    @prefix_name.setter
    def prefix_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'prefix_name', value)

class Prefix(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, peering_service_name: Optional[pulumi.Input[str]]=None, peering_service_prefix_key: Optional[pulumi.Input[str]]=None, prefix: Optional[pulumi.Input[str]]=None, prefix_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The peering service prefix class.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] peering_service_name: The name of the peering service.
        :param pulumi.Input[str] peering_service_prefix_key: The peering service prefix key
        :param pulumi.Input[str] prefix: The prefix from which your traffic originates.
        :param pulumi.Input[str] prefix_name: The name of the prefix.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PrefixArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The peering service prefix class.

        :param str resource_name: The name of the resource.
        :param PrefixArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(PrefixArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, peering_service_name: Optional[pulumi.Input[str]]=None, peering_service_prefix_key: Optional[pulumi.Input[str]]=None, prefix: Optional[pulumi.Input[str]]=None, prefix_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrefixArgs.__new__(PrefixArgs)
            if peering_service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'peering_service_name'")
            __props__.__dict__['peering_service_name'] = peering_service_name
            __props__.__dict__['peering_service_prefix_key'] = peering_service_prefix_key
            __props__.__dict__['prefix'] = prefix
            __props__.__dict__['prefix_name'] = prefix_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['error_message'] = None
            __props__.__dict__['events'] = None
            __props__.__dict__['learned_type'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['prefix_validation_state'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:peering:Prefix'), pulumi.Alias(type_='azure-native:peering/v20190801preview:Prefix'), pulumi.Alias(type_='azure-native:peering/v20190901preview:Prefix'), pulumi.Alias(type_='azure-native:peering/v20200101preview:Prefix'), pulumi.Alias(type_='azure-native:peering/v20200401:Prefix'), pulumi.Alias(type_='azure-native:peering/v20201001:Prefix'), pulumi.Alias(type_='azure-native:peering/v20210101:Prefix'), pulumi.Alias(type_='azure-native:peering/v20210601:Prefix'), pulumi.Alias(type_='azure-native:peering/v20220101:Prefix'), pulumi.Alias(type_='azure-native:peering/v20220601:Prefix')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Prefix, __self__).__init__('azure-native:peering/v20221001:Prefix', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Prefix':
        """
        Get an existing Prefix resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = PrefixArgs.__new__(PrefixArgs)
        __props__.__dict__['error_message'] = None
        __props__.__dict__['events'] = None
        __props__.__dict__['learned_type'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['peering_service_prefix_key'] = None
        __props__.__dict__['prefix'] = None
        __props__.__dict__['prefix_validation_state'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['type'] = None
        return Prefix(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='errorMessage')
    def error_message(self) -> pulumi.Output[str]:
        """
        The error message for validation state
        """
        return pulumi.get(self, 'error_message')

    @property
    @pulumi.getter
    def events(self) -> pulumi.Output[Sequence['outputs.PeeringServicePrefixEventResponse']]:
        """
        The list of events for peering service prefix
        """
        return pulumi.get(self, 'events')

    @property
    @pulumi.getter(name='learnedType')
    def learned_type(self) -> pulumi.Output[str]:
        """
        The prefix learned type
        """
        return pulumi.get(self, 'learned_type')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='peeringServicePrefixKey')
    def peering_service_prefix_key(self) -> pulumi.Output[Optional[str]]:
        """
        The peering service prefix key
        """
        return pulumi.get(self, 'peering_service_prefix_key')

    @property
    @pulumi.getter
    def prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The prefix from which your traffic originates.
        """
        return pulumi.get(self, 'prefix')

    @property
    @pulumi.getter(name='prefixValidationState')
    def prefix_validation_state(self) -> pulumi.Output[str]:
        """
        The prefix validation state
        """
        return pulumi.get(self, 'prefix_validation_state')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')
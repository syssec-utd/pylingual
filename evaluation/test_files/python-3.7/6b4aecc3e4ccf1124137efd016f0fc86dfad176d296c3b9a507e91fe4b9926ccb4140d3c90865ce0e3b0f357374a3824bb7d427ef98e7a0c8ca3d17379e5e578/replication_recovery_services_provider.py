import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['ReplicationRecoveryServicesProviderArgs', 'ReplicationRecoveryServicesProvider']

@pulumi.input_type
class ReplicationRecoveryServicesProviderArgs:

    def __init__(__self__, *, fabric_name: pulumi.Input[str], properties: pulumi.Input['AddRecoveryServicesProviderInputPropertiesArgs'], resource_group_name: pulumi.Input[str], resource_name: pulumi.Input[str], provider_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a ReplicationRecoveryServicesProvider resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input['AddRecoveryServicesProviderInputPropertiesArgs'] properties: The properties of an add provider request.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input[str] provider_name: Recovery services provider name.
        """
        pulumi.set(__self__, 'fabric_name', fabric_name)
        pulumi.set(__self__, 'properties', properties)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'resource_name', resource_name)
        if provider_name is not None:
            pulumi.set(__self__, 'provider_name', provider_name)

    @property
    @pulumi.getter(name='fabricName')
    def fabric_name(self) -> pulumi.Input[str]:
        """
        Fabric name.
        """
        return pulumi.get(self, 'fabric_name')

    @fabric_name.setter
    def fabric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'fabric_name', value)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['AddRecoveryServicesProviderInputPropertiesArgs']:
        """
        The properties of an add provider request.
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: pulumi.Input['AddRecoveryServicesProviderInputPropertiesArgs']):
        pulumi.set(self, 'properties', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the recovery services vault is present.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='resourceName')
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the recovery services vault.
        """
        return pulumi.get(self, 'resource_name')

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_name', value)

    @property
    @pulumi.getter(name='providerName')
    def provider_name(self) -> Optional[pulumi.Input[str]]:
        """
        Recovery services provider name.
        """
        return pulumi.get(self, 'provider_name')

    @provider_name.setter
    def provider_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'provider_name', value)
warnings.warn('Version 2018-01-10 will be removed in v2 of the provider.', DeprecationWarning)

class ReplicationRecoveryServicesProvider(pulumi.CustomResource):
    warnings.warn('Version 2018-01-10 will be removed in v2 of the provider.', DeprecationWarning)

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, fabric_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['AddRecoveryServicesProviderInputPropertiesArgs']]]=None, provider_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name_: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Provider details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input[pulumi.InputType['AddRecoveryServicesProviderInputPropertiesArgs']] properties: The properties of an add provider request.
        :param pulumi.Input[str] provider_name: Recovery services provider name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ReplicationRecoveryServicesProviderArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Provider details.

        :param str resource_name: The name of the resource.
        :param ReplicationRecoveryServicesProviderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ReplicationRecoveryServicesProviderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, fabric_name: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['AddRecoveryServicesProviderInputPropertiesArgs']]]=None, provider_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name_: Optional[pulumi.Input[str]]=None, __props__=None):
        pulumi.log.warn('ReplicationRecoveryServicesProvider is deprecated: Version 2018-01-10 will be removed in v2 of the provider.')
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationRecoveryServicesProviderArgs.__new__(ReplicationRecoveryServicesProviderArgs)
            if fabric_name is None and (not opts.urn):
                raise TypeError("Missing required property 'fabric_name'")
            __props__.__dict__['fabric_name'] = fabric_name
            if properties is None and (not opts.urn):
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__['properties'] = properties
            __props__.__dict__['provider_name'] = provider_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if resource_name_ is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__['resource_name'] = resource_name_
            __props__.__dict__['location'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:recoveryservices:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20180710:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210210:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210301:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210401:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210601:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210701:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20210801:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20211001:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20211101:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20211201:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220101:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220201:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220301:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220401:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220501:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220801:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20220910:ReplicationRecoveryServicesProvider'), pulumi.Alias(type_='azure-native:recoveryservices/v20221001:ReplicationRecoveryServicesProvider')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationRecoveryServicesProvider, __self__).__init__('azure-native:recoveryservices/v20180110:ReplicationRecoveryServicesProvider', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ReplicationRecoveryServicesProvider':
        """
        Get an existing ReplicationRecoveryServicesProvider resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ReplicationRecoveryServicesProviderArgs.__new__(ReplicationRecoveryServicesProviderArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['type'] = None
        return ReplicationRecoveryServicesProvider(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.RecoveryServicesProviderPropertiesResponse']:
        """
        Provider properties.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource Type
        """
        return pulumi.get(self, 'type')
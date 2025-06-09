import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['IntegrationAccountBatchConfigurationArgs', 'IntegrationAccountBatchConfiguration']

@pulumi.input_type
class IntegrationAccountBatchConfigurationArgs:

    def __init__(__self__, *, integration_account_name: pulumi.Input[str], properties: pulumi.Input['BatchConfigurationPropertiesArgs'], resource_group_name: pulumi.Input[str], batch_configuration_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a IntegrationAccountBatchConfiguration resource.
        :param pulumi.Input[str] integration_account_name: The integration account name.
        :param pulumi.Input['BatchConfigurationPropertiesArgs'] properties: The batch configuration properties.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] batch_configuration_name: The batch configuration name.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        pulumi.set(__self__, 'integration_account_name', integration_account_name)
        pulumi.set(__self__, 'properties', properties)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if batch_configuration_name is not None:
            pulumi.set(__self__, 'batch_configuration_name', batch_configuration_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='integrationAccountName')
    def integration_account_name(self) -> pulumi.Input[str]:
        """
        The integration account name.
        """
        return pulumi.get(self, 'integration_account_name')

    @integration_account_name.setter
    def integration_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'integration_account_name', value)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['BatchConfigurationPropertiesArgs']:
        """
        The batch configuration properties.
        """
        return pulumi.get(self, 'properties')

    @properties.setter
    def properties(self, value: pulumi.Input['BatchConfigurationPropertiesArgs']):
        pulumi.set(self, 'properties', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='batchConfigurationName')
    def batch_configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        The batch configuration name.
        """
        return pulumi.get(self, 'batch_configuration_name')

    @batch_configuration_name.setter
    def batch_configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'batch_configuration_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'tags', value)

class IntegrationAccountBatchConfiguration(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, batch_configuration_name: Optional[pulumi.Input[str]]=None, integration_account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['BatchConfigurationPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        The batch configuration resource definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] batch_configuration_name: The batch configuration name.
        :param pulumi.Input[str] integration_account_name: The integration account name.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[pulumi.InputType['BatchConfigurationPropertiesArgs']] properties: The batch configuration properties.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: IntegrationAccountBatchConfigurationArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The batch configuration resource definition.

        :param str resource_name: The name of the resource.
        :param IntegrationAccountBatchConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IntegrationAccountBatchConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, batch_configuration_name: Optional[pulumi.Input[str]]=None, integration_account_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, properties: Optional[pulumi.Input[pulumi.InputType['BatchConfigurationPropertiesArgs']]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IntegrationAccountBatchConfigurationArgs.__new__(IntegrationAccountBatchConfigurationArgs)
            __props__.__dict__['batch_configuration_name'] = batch_configuration_name
            if integration_account_name is None and (not opts.urn):
                raise TypeError("Missing required property 'integration_account_name'")
            __props__.__dict__['integration_account_name'] = integration_account_name
            __props__.__dict__['location'] = location
            if properties is None and (not opts.urn):
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__['properties'] = properties
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:logic:IntegrationAccountBatchConfiguration'), pulumi.Alias(type_='azure-native:logic/v20180701preview:IntegrationAccountBatchConfiguration'), pulumi.Alias(type_='azure-native:logic/v20190501:IntegrationAccountBatchConfiguration')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IntegrationAccountBatchConfiguration, __self__).__init__('azure-native:logic/v20160601:IntegrationAccountBatchConfiguration', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'IntegrationAccountBatchConfiguration':
        """
        Get an existing IntegrationAccountBatchConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = IntegrationAccountBatchConfigurationArgs.__new__(IntegrationAccountBatchConfigurationArgs)
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['properties'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        return IntegrationAccountBatchConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.BatchConfigurationPropertiesResponse']:
        """
        The batch configuration properties.
        """
        return pulumi.get(self, 'properties')

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, 'tags')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Gets the resource type.
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['BlueprintArgs', 'Blueprint']

@pulumi.input_type
class BlueprintArgs:

    def __init__(__self__, *, resource_scope: pulumi.Input[str], target_scope: pulumi.Input[Union[str, 'BlueprintTargetScope']], blueprint_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionArgs']]]]=None, resource_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input['ResourceGroupDefinitionArgs']]]]=None, versions: Optional[Any]=None):
        """
        The set of arguments for constructing a Blueprint resource.
        :param pulumi.Input[str] resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
        :param pulumi.Input[Union[str, 'BlueprintTargetScope']] target_scope: The scope where this blueprint definition can be assigned.
        :param pulumi.Input[str] blueprint_name: Name of the blueprint definition.
        :param pulumi.Input[str] description: Multi-line explain this resource.
        :param pulumi.Input[str] display_name: One-liner string explain this resource.
        :param pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionArgs']]] parameters: Parameters required by this blueprint definition.
        :param pulumi.Input[Mapping[str, pulumi.Input['ResourceGroupDefinitionArgs']]] resource_groups: Resource group placeholders defined by this blueprint definition.
        :param Any versions: Published versions of this blueprint definition.
        """
        pulumi.set(__self__, 'resource_scope', resource_scope)
        pulumi.set(__self__, 'target_scope', target_scope)
        if blueprint_name is not None:
            pulumi.set(__self__, 'blueprint_name', blueprint_name)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if parameters is not None:
            pulumi.set(__self__, 'parameters', parameters)
        if resource_groups is not None:
            pulumi.set(__self__, 'resource_groups', resource_groups)
        if versions is not None:
            pulumi.set(__self__, 'versions', versions)

    @property
    @pulumi.getter(name='resourceScope')
    def resource_scope(self) -> pulumi.Input[str]:
        """
        The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
        """
        return pulumi.get(self, 'resource_scope')

    @resource_scope.setter
    def resource_scope(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_scope', value)

    @property
    @pulumi.getter(name='targetScope')
    def target_scope(self) -> pulumi.Input[Union[str, 'BlueprintTargetScope']]:
        """
        The scope where this blueprint definition can be assigned.
        """
        return pulumi.get(self, 'target_scope')

    @target_scope.setter
    def target_scope(self, value: pulumi.Input[Union[str, 'BlueprintTargetScope']]):
        pulumi.set(self, 'target_scope', value)

    @property
    @pulumi.getter(name='blueprintName')
    def blueprint_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the blueprint definition.
        """
        return pulumi.get(self, 'blueprint_name')

    @blueprint_name.setter
    def blueprint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'blueprint_name', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionArgs']]]]:
        """
        Parameters required by this blueprint definition.
        """
        return pulumi.get(self, 'parameters')

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionArgs']]]]):
        pulumi.set(self, 'parameters', value)

    @property
    @pulumi.getter(name='resourceGroups')
    def resource_groups(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ResourceGroupDefinitionArgs']]]]:
        """
        Resource group placeholders defined by this blueprint definition.
        """
        return pulumi.get(self, 'resource_groups')

    @resource_groups.setter
    def resource_groups(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ResourceGroupDefinitionArgs']]]]):
        pulumi.set(self, 'resource_groups', value)

    @property
    @pulumi.getter
    def versions(self) -> Optional[Any]:
        """
        Published versions of this blueprint definition.
        """
        return pulumi.get(self, 'versions')

    @versions.setter
    def versions(self, value: Optional[Any]):
        pulumi.set(self, 'versions', value)

class Blueprint(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, blueprint_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionArgs']]]]]=None, resource_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ResourceGroupDefinitionArgs']]]]]=None, resource_scope: Optional[pulumi.Input[str]]=None, target_scope: Optional[pulumi.Input[Union[str, 'BlueprintTargetScope']]]=None, versions: Optional[Any]=None, __props__=None):
        """
        Represents a Blueprint definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blueprint_name: Name of the blueprint definition.
        :param pulumi.Input[str] description: Multi-line explain this resource.
        :param pulumi.Input[str] display_name: One-liner string explain this resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionArgs']]]] parameters: Parameters required by this blueprint definition.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ResourceGroupDefinitionArgs']]]] resource_groups: Resource group placeholders defined by this blueprint definition.
        :param pulumi.Input[str] resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
        :param pulumi.Input[Union[str, 'BlueprintTargetScope']] target_scope: The scope where this blueprint definition can be assigned.
        :param Any versions: Published versions of this blueprint definition.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: BlueprintArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Represents a Blueprint definition.

        :param str resource_name: The name of the resource.
        :param BlueprintArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(BlueprintArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, blueprint_name: Optional[pulumi.Input[str]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionArgs']]]]]=None, resource_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ResourceGroupDefinitionArgs']]]]]=None, resource_scope: Optional[pulumi.Input[str]]=None, target_scope: Optional[pulumi.Input[Union[str, 'BlueprintTargetScope']]]=None, versions: Optional[Any]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BlueprintArgs.__new__(BlueprintArgs)
            __props__.__dict__['blueprint_name'] = blueprint_name
            __props__.__dict__['description'] = description
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['parameters'] = parameters
            __props__.__dict__['resource_groups'] = resource_groups
            if resource_scope is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_scope'")
            __props__.__dict__['resource_scope'] = resource_scope
            if target_scope is None and (not opts.urn):
                raise TypeError("Missing required property 'target_scope'")
            __props__.__dict__['target_scope'] = target_scope
            __props__.__dict__['versions'] = versions
            __props__.__dict__['layout'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['status'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:blueprint:Blueprint')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Blueprint, __self__).__init__('azure-native:blueprint/v20181101preview:Blueprint', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Blueprint':
        """
        Get an existing Blueprint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = BlueprintArgs.__new__(BlueprintArgs)
        __props__.__dict__['description'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['layout'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['parameters'] = None
        __props__.__dict__['resource_groups'] = None
        __props__.__dict__['status'] = None
        __props__.__dict__['target_scope'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['versions'] = None
        return Blueprint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def layout(self) -> pulumi.Output[Any]:
        """
        Layout view of the blueprint definition for UI reference.
        """
        return pulumi.get(self, 'layout')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of this resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ParameterDefinitionResponse']]]:
        """
        Parameters required by this blueprint definition.
        """
        return pulumi.get(self, 'parameters')

    @property
    @pulumi.getter(name='resourceGroups')
    def resource_groups(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ResourceGroupDefinitionResponse']]]:
        """
        Resource group placeholders defined by this blueprint definition.
        """
        return pulumi.get(self, 'resource_groups')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.BlueprintStatusResponse']:
        """
        Status of the blueprint. This field is readonly.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter(name='targetScope')
    def target_scope(self) -> pulumi.Output[str]:
        """
        The scope where this blueprint definition can be assigned.
        """
        return pulumi.get(self, 'target_scope')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of this resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter
    def versions(self) -> pulumi.Output[Optional[Any]]:
        """
        Published versions of this blueprint definition.
        """
        return pulumi.get(self, 'versions')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['TrustedAccessRoleBindingArgs', 'TrustedAccessRoleBinding']

@pulumi.input_type
class TrustedAccessRoleBindingArgs:

    def __init__(__self__, *, resource_group_name: pulumi.Input[str], resource_name: pulumi.Input[str], roles: pulumi.Input[Sequence[pulumi.Input[str]]], source_resource_id: pulumi.Input[str], trusted_access_role_binding_name: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a TrustedAccessRoleBinding resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name: The name of the managed cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list of roles to bind, each item is a resource type qualified role name. For example: 'Microsoft.MachineLearningServices/workspaces/reader'.
        :param pulumi.Input[str] source_resource_id: The ARM resource ID of source resource that trusted access is configured for.
        :param pulumi.Input[str] trusted_access_role_binding_name: The name of trusted access role binding.
        """
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'resource_name', resource_name)
        pulumi.set(__self__, 'roles', roles)
        pulumi.set(__self__, 'source_resource_id', source_resource_id)
        if trusted_access_role_binding_name is not None:
            pulumi.set(__self__, 'trusted_access_role_binding_name', trusted_access_role_binding_name)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='resourceName')
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the managed cluster resource.
        """
        return pulumi.get(self, 'resource_name')

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_name', value)

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of roles to bind, each item is a resource type qualified role name. For example: 'Microsoft.MachineLearningServices/workspaces/reader'.
        """
        return pulumi.get(self, 'roles')

    @roles.setter
    def roles(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'roles', value)

    @property
    @pulumi.getter(name='sourceResourceId')
    def source_resource_id(self) -> pulumi.Input[str]:
        """
        The ARM resource ID of source resource that trusted access is configured for.
        """
        return pulumi.get(self, 'source_resource_id')

    @source_resource_id.setter
    def source_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'source_resource_id', value)

    @property
    @pulumi.getter(name='trustedAccessRoleBindingName')
    def trusted_access_role_binding_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of trusted access role binding.
        """
        return pulumi.get(self, 'trusted_access_role_binding_name')

    @trusted_access_role_binding_name.setter
    def trusted_access_role_binding_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'trusted_access_role_binding_name', value)

class TrustedAccessRoleBinding(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name_: Optional[pulumi.Input[str]]=None, roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, source_resource_id: Optional[pulumi.Input[str]]=None, trusted_access_role_binding_name: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Defines binding between a resource and role

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the managed cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] roles: A list of roles to bind, each item is a resource type qualified role name. For example: 'Microsoft.MachineLearningServices/workspaces/reader'.
        :param pulumi.Input[str] source_resource_id: The ARM resource ID of source resource that trusted access is configured for.
        :param pulumi.Input[str] trusted_access_role_binding_name: The name of trusted access role binding.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: TrustedAccessRoleBindingArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Defines binding between a resource and role

        :param str resource_name: The name of the resource.
        :param TrustedAccessRoleBindingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrustedAccessRoleBindingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name_: Optional[pulumi.Input[str]]=None, roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, source_resource_id: Optional[pulumi.Input[str]]=None, trusted_access_role_binding_name: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrustedAccessRoleBindingArgs.__new__(TrustedAccessRoleBindingArgs)
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if resource_name_ is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__['resource_name'] = resource_name_
            if roles is None and (not opts.urn):
                raise TypeError("Missing required property 'roles'")
            __props__.__dict__['roles'] = roles
            if source_resource_id is None and (not opts.urn):
                raise TypeError("Missing required property 'source_resource_id'")
            __props__.__dict__['source_resource_id'] = source_resource_id
            __props__.__dict__['trusted_access_role_binding_name'] = trusted_access_role_binding_name
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:containerservice:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220402preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220502preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220702preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220802preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220803preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20220902preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20221002preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20221102preview:TrustedAccessRoleBinding'), pulumi.Alias(type_='azure-native:containerservice/v20230102preview:TrustedAccessRoleBinding')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(TrustedAccessRoleBinding, __self__).__init__('azure-native:containerservice/v20220602preview:TrustedAccessRoleBinding', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'TrustedAccessRoleBinding':
        """
        Get an existing TrustedAccessRoleBinding resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = TrustedAccessRoleBindingArgs.__new__(TrustedAccessRoleBindingArgs)
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['roles'] = None
        __props__.__dict__['source_resource_id'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        return TrustedAccessRoleBinding(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='provisioningState')
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The current provisioning state of trusted access role binding.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of roles to bind, each item is a resource type qualified role name. For example: 'Microsoft.MachineLearningServices/workspaces/reader'.
        """
        return pulumi.get(self, 'roles')

    @property
    @pulumi.getter(name='sourceResourceId')
    def source_resource_id(self) -> pulumi.Output[str]:
        """
        The ARM resource ID of source resource that trusted access is configured for.
        """
        return pulumi.get(self, 'source_resource_id')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, 'type')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['OrganizationPolicyArgs', 'OrganizationPolicy']

@pulumi.input_type
class OrganizationPolicyArgs:

    def __init__(__self__, *, organization_id: pulumi.Input[str], alternate: Optional[pulumi.Input['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']]=None, name: Optional[pulumi.Input[str]]=None, spec: Optional[pulumi.Input['GoogleCloudOrgpolicyV2PolicySpecArgs']]=None):
        """
        The set of arguments for constructing a OrganizationPolicy resource.
        :param pulumi.Input['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs'] alternate: Deprecated.
        :param pulumi.Input[str] name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * `projects/{project_number}/policies/{constraint_name}` * `folders/{folder_id}/policies/{constraint_name}` * `organizations/{organization_id}/policies/{constraint_name}` For example, "projects/123/policies/compute.disableSerialPortAccess". Note: `projects/{project_id}/policies/{constraint_name}` is also an acceptable name for API requests, but responses will return the name using the equivalent project number.
        :param pulumi.Input['GoogleCloudOrgpolicyV2PolicySpecArgs'] spec: Basic information about the Organization Policy.
        """
        pulumi.set(__self__, 'organization_id', organization_id)
        if alternate is not None:
            warnings.warn('Deprecated.', DeprecationWarning)
            pulumi.log.warn('alternate is deprecated: Deprecated.')
        if alternate is not None:
            pulumi.set(__self__, 'alternate', alternate)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if spec is not None:
            pulumi.set(__self__, 'spec', spec)

    @property
    @pulumi.getter(name='organizationId')
    def organization_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, 'organization_id')

    @organization_id.setter
    def organization_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'organization_id', value)

    @property
    @pulumi.getter
    def alternate(self) -> Optional[pulumi.Input['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']]:
        """
        Deprecated.
        """
        return pulumi.get(self, 'alternate')

    @alternate.setter
    def alternate(self, value: Optional[pulumi.Input['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']]):
        pulumi.set(self, 'alternate', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * `projects/{project_number}/policies/{constraint_name}` * `folders/{folder_id}/policies/{constraint_name}` * `organizations/{organization_id}/policies/{constraint_name}` For example, "projects/123/policies/compute.disableSerialPortAccess". Note: `projects/{project_id}/policies/{constraint_name}` is also an acceptable name for API requests, but responses will return the name using the equivalent project number.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def spec(self) -> Optional[pulumi.Input['GoogleCloudOrgpolicyV2PolicySpecArgs']]:
        """
        Basic information about the Organization Policy.
        """
        return pulumi.get(self, 'spec')

    @spec.setter
    def spec(self, value: Optional[pulumi.Input['GoogleCloudOrgpolicyV2PolicySpecArgs']]):
        pulumi.set(self, 'spec', value)

class OrganizationPolicy(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, alternate: Optional[pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']]]=None, name: Optional[pulumi.Input[str]]=None, organization_id: Optional[pulumi.Input[str]]=None, spec: Optional[pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2PolicySpecArgs']]]=None, __props__=None):
        """
        Creates a Policy. Returns a `google.rpc.Status` with `google.rpc.Code.NOT_FOUND` if the constraint does not exist. Returns a `google.rpc.Status` with `google.rpc.Code.ALREADY_EXISTS` if the policy already exists on the given Cloud resource.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']] alternate: Deprecated.
        :param pulumi.Input[str] name: Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * `projects/{project_number}/policies/{constraint_name}` * `folders/{folder_id}/policies/{constraint_name}` * `organizations/{organization_id}/policies/{constraint_name}` For example, "projects/123/policies/compute.disableSerialPortAccess". Note: `projects/{project_id}/policies/{constraint_name}` is also an acceptable name for API requests, but responses will return the name using the equivalent project number.
        :param pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2PolicySpecArgs']] spec: Basic information about the Organization Policy.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: OrganizationPolicyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates a Policy. Returns a `google.rpc.Status` with `google.rpc.Code.NOT_FOUND` if the constraint does not exist. Returns a `google.rpc.Status` with `google.rpc.Code.ALREADY_EXISTS` if the policy already exists on the given Cloud resource.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param OrganizationPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, alternate: Optional[pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2AlternatePolicySpecArgs']]]=None, name: Optional[pulumi.Input[str]]=None, organization_id: Optional[pulumi.Input[str]]=None, spec: Optional[pulumi.Input[pulumi.InputType['GoogleCloudOrgpolicyV2PolicySpecArgs']]]=None, __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        else:
            opts = copy.copy(opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationPolicyArgs.__new__(OrganizationPolicyArgs)
            if alternate is not None and (not opts.urn):
                warnings.warn('Deprecated.', DeprecationWarning)
                pulumi.log.warn('alternate is deprecated: Deprecated.')
            __props__.__dict__['alternate'] = alternate
            __props__.__dict__['name'] = name
            if organization_id is None and (not opts.urn):
                raise TypeError("Missing required property 'organization_id'")
            __props__.__dict__['organization_id'] = organization_id
            __props__.__dict__['spec'] = spec
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['organization_id'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(OrganizationPolicy, __self__).__init__('google-native:orgpolicy/v2:OrganizationPolicy', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'OrganizationPolicy':
        """
        Get an existing OrganizationPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = OrganizationPolicyArgs.__new__(OrganizationPolicyArgs)
        __props__.__dict__['alternate'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['organization_id'] = None
        __props__.__dict__['spec'] = None
        return OrganizationPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def alternate(self) -> pulumi.Output['outputs.GoogleCloudOrgpolicyV2AlternatePolicySpecResponse']:
        """
        Deprecated.
        """
        return pulumi.get(self, 'alternate')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Immutable. The resource name of the Policy. Must be one of the following forms, where constraint_name is the name of the constraint which this Policy configures: * `projects/{project_number}/policies/{constraint_name}` * `folders/{folder_id}/policies/{constraint_name}` * `organizations/{organization_id}/policies/{constraint_name}` For example, "projects/123/policies/compute.disableSerialPortAccess". Note: `projects/{project_id}/policies/{constraint_name}` is also an acceptable name for API requests, but responses will return the name using the equivalent project number.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='organizationId')
    def organization_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'organization_id')

    @property
    @pulumi.getter
    def spec(self) -> pulumi.Output['outputs.GoogleCloudOrgpolicyV2PolicySpecResponse']:
        """
        Basic information about the Organization Policy.
        """
        return pulumi.get(self, 'spec')
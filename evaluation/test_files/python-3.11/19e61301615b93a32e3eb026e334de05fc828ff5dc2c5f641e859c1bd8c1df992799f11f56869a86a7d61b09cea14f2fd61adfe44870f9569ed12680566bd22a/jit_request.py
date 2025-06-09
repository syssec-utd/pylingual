import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['JitRequestArgs', 'JitRequest']

@pulumi.input_type
class JitRequestArgs:

    def __init__(__self__, *, application_resource_id: pulumi.Input[str], jit_authorization_policies: pulumi.Input[Sequence[pulumi.Input['JitAuthorizationPoliciesArgs']]], jit_scheduling_policy: pulumi.Input['JitSchedulingPolicyArgs'], resource_group_name: pulumi.Input[str], jit_request_name: Optional[pulumi.Input[str]]=None, location: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None):
        """
        The set of arguments for constructing a JitRequest resource.
        :param pulumi.Input[str] application_resource_id: The parent application id.
        :param pulumi.Input[Sequence[pulumi.Input['JitAuthorizationPoliciesArgs']]] jit_authorization_policies: The JIT authorization policies.
        :param pulumi.Input['JitSchedulingPolicyArgs'] jit_scheduling_policy: The JIT request properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] jit_request_name: The name of the JIT request.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, 'application_resource_id', application_resource_id)
        pulumi.set(__self__, 'jit_authorization_policies', jit_authorization_policies)
        pulumi.set(__self__, 'jit_scheduling_policy', jit_scheduling_policy)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if jit_request_name is not None:
            pulumi.set(__self__, 'jit_request_name', jit_request_name)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='applicationResourceId')
    def application_resource_id(self) -> pulumi.Input[str]:
        """
        The parent application id.
        """
        return pulumi.get(self, 'application_resource_id')

    @application_resource_id.setter
    def application_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'application_resource_id', value)

    @property
    @pulumi.getter(name='jitAuthorizationPolicies')
    def jit_authorization_policies(self) -> pulumi.Input[Sequence[pulumi.Input['JitAuthorizationPoliciesArgs']]]:
        """
        The JIT authorization policies.
        """
        return pulumi.get(self, 'jit_authorization_policies')

    @jit_authorization_policies.setter
    def jit_authorization_policies(self, value: pulumi.Input[Sequence[pulumi.Input['JitAuthorizationPoliciesArgs']]]):
        pulumi.set(self, 'jit_authorization_policies', value)

    @property
    @pulumi.getter(name='jitSchedulingPolicy')
    def jit_scheduling_policy(self) -> pulumi.Input['JitSchedulingPolicyArgs']:
        """
        The JIT request properties.
        """
        return pulumi.get(self, 'jit_scheduling_policy')

    @jit_scheduling_policy.setter
    def jit_scheduling_policy(self, value: pulumi.Input['JitSchedulingPolicyArgs']):
        pulumi.set(self, 'jit_scheduling_policy', value)

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
    @pulumi.getter(name='jitRequestName')
    def jit_request_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the JIT request.
        """
        return pulumi.get(self, 'jit_request_name')

    @jit_request_name.setter
    def jit_request_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'jit_request_name', value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'location', value)

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

class JitRequest(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_resource_id: Optional[pulumi.Input[str]]=None, jit_authorization_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JitAuthorizationPoliciesArgs']]]]]=None, jit_request_name: Optional[pulumi.Input[str]]=None, jit_scheduling_policy: Optional[pulumi.Input[pulumi.InputType['JitSchedulingPolicyArgs']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        """
        Information about JIT request definition.
        API Version: 2019-07-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_resource_id: The parent application id.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JitAuthorizationPoliciesArgs']]]] jit_authorization_policies: The JIT authorization policies.
        :param pulumi.Input[str] jit_request_name: The name of the JIT request.
        :param pulumi.Input[pulumi.InputType['JitSchedulingPolicyArgs']] jit_scheduling_policy: The JIT request properties.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: JitRequestArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Information about JIT request definition.
        API Version: 2019-07-01.

        :param str resource_name: The name of the resource.
        :param JitRequestArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JitRequestArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, application_resource_id: Optional[pulumi.Input[str]]=None, jit_authorization_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['JitAuthorizationPoliciesArgs']]]]]=None, jit_request_name: Optional[pulumi.Input[str]]=None, jit_scheduling_policy: Optional[pulumi.Input[pulumi.InputType['JitSchedulingPolicyArgs']]]=None, location: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = JitRequestArgs.__new__(JitRequestArgs)
            if application_resource_id is None and (not opts.urn):
                raise TypeError("Missing required property 'application_resource_id'")
            __props__.__dict__['application_resource_id'] = application_resource_id
            if jit_authorization_policies is None and (not opts.urn):
                raise TypeError("Missing required property 'jit_authorization_policies'")
            __props__.__dict__['jit_authorization_policies'] = jit_authorization_policies
            __props__.__dict__['jit_request_name'] = jit_request_name
            if jit_scheduling_policy is None and (not opts.urn):
                raise TypeError("Missing required property 'jit_scheduling_policy'")
            __props__.__dict__['jit_scheduling_policy'] = jit_scheduling_policy
            __props__.__dict__['location'] = location
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['tags'] = tags
            __props__.__dict__['created_by'] = None
            __props__.__dict__['jit_request_state'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['provisioning_state'] = None
            __props__.__dict__['publisher_tenant_id'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['updated_by'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:solutions/v20180301:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20180601:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20180901preview:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20190701:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20200821preview:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20210201preview:JitRequest'), pulumi.Alias(type_='azure-native:solutions/v20210701:JitRequest')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(JitRequest, __self__).__init__('azure-native:solutions:JitRequest', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'JitRequest':
        """
        Get an existing JitRequest resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = JitRequestArgs.__new__(JitRequestArgs)
        __props__.__dict__['application_resource_id'] = None
        __props__.__dict__['created_by'] = None
        __props__.__dict__['jit_authorization_policies'] = None
        __props__.__dict__['jit_request_state'] = None
        __props__.__dict__['jit_scheduling_policy'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['provisioning_state'] = None
        __props__.__dict__['publisher_tenant_id'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['updated_by'] = None
        return JitRequest(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='applicationResourceId')
    def application_resource_id(self) -> pulumi.Output[str]:
        """
        The parent application id.
        """
        return pulumi.get(self, 'application_resource_id')

    @property
    @pulumi.getter(name='createdBy')
    def created_by(self) -> pulumi.Output['outputs.ApplicationClientDetailsResponse']:
        """
        The client entity that created the JIT request.
        """
        return pulumi.get(self, 'created_by')

    @property
    @pulumi.getter(name='jitAuthorizationPolicies')
    def jit_authorization_policies(self) -> pulumi.Output[Sequence['outputs.JitAuthorizationPoliciesResponse']]:
        """
        The JIT authorization policies.
        """
        return pulumi.get(self, 'jit_authorization_policies')

    @property
    @pulumi.getter(name='jitRequestState')
    def jit_request_state(self) -> pulumi.Output[str]:
        """
        The JIT request state.
        """
        return pulumi.get(self, 'jit_request_state')

    @property
    @pulumi.getter(name='jitSchedulingPolicy')
    def jit_scheduling_policy(self) -> pulumi.Output['outputs.JitSchedulingPolicyResponse']:
        """
        The JIT request properties.
        """
        return pulumi.get(self, 'jit_scheduling_policy')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
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
        The JIT request provisioning state.
        """
        return pulumi.get(self, 'provisioning_state')

    @property
    @pulumi.getter(name='publisherTenantId')
    def publisher_tenant_id(self) -> pulumi.Output[str]:
        """
        The publisher tenant id.
        """
        return pulumi.get(self, 'publisher_tenant_id')

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
    @pulumi.getter(name='updatedBy')
    def updated_by(self) -> pulumi.Output['outputs.ApplicationClientDetailsResponse']:
        """
        The client entity that last updated the JIT request.
        """
        return pulumi.get(self, 'updated_by')
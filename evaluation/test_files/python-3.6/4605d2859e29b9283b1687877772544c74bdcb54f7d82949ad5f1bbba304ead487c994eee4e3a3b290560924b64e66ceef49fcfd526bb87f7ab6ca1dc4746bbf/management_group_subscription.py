import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
__all__ = ['ManagementGroupSubscriptionArgs', 'ManagementGroupSubscription']

@pulumi.input_type
class ManagementGroupSubscriptionArgs:

    def __init__(__self__, *, group_id: pulumi.Input[str], subscription_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a ManagementGroupSubscription resource.
        :param pulumi.Input[str] group_id: Management Group ID.
        :param pulumi.Input[str] subscription_id: Subscription ID.
        """
        pulumi.set(__self__, 'group_id', group_id)
        if subscription_id is not None:
            pulumi.set(__self__, 'subscription_id', subscription_id)

    @property
    @pulumi.getter(name='groupId')
    def group_id(self) -> pulumi.Input[str]:
        """
        Management Group ID.
        """
        return pulumi.get(self, 'group_id')

    @group_id.setter
    def group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'group_id', value)

    @property
    @pulumi.getter(name='subscriptionId')
    def subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        Subscription ID.
        """
        return pulumi.get(self, 'subscription_id')

    @subscription_id.setter
    def subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'subscription_id', value)

class ManagementGroupSubscription(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, group_id: Optional[pulumi.Input[str]]=None, subscription_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The details of subscription under management group.
        API Version: 2020-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group_id: Management Group ID.
        :param pulumi.Input[str] subscription_id: Subscription ID.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ManagementGroupSubscriptionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The details of subscription under management group.
        API Version: 2020-05-01.

        :param str resource_name: The name of the resource.
        :param ManagementGroupSubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(ManagementGroupSubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, group_id: Optional[pulumi.Input[str]]=None, subscription_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagementGroupSubscriptionArgs.__new__(ManagementGroupSubscriptionArgs)
            if group_id is None and (not opts.urn):
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__['group_id'] = group_id
            __props__.__dict__['subscription_id'] = subscription_id
            __props__.__dict__['display_name'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['parent'] = None
            __props__.__dict__['state'] = None
            __props__.__dict__['tenant'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:management/v20200501:ManagementGroupSubscription'), pulumi.Alias(type_='azure-native:management/v20201001:ManagementGroupSubscription'), pulumi.Alias(type_='azure-native:management/v20210401:ManagementGroupSubscription')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagementGroupSubscription, __self__).__init__('azure-native:management:ManagementGroupSubscription', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ManagementGroupSubscription':
        """
        Get an existing ManagementGroupSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ManagementGroupSubscriptionArgs.__new__(ManagementGroupSubscriptionArgs)
        __props__.__dict__['display_name'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['parent'] = None
        __props__.__dict__['state'] = None
        __props__.__dict__['tenant'] = None
        __props__.__dict__['type'] = None
        return ManagementGroupSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The friendly name of the subscription.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The stringified id of the subscription. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def parent(self) -> pulumi.Output[Optional['outputs.DescendantParentGroupInfoResponse']]:
        """
        The ID of the parent management group.
        """
        return pulumi.get(self, 'parent')

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        """
        The state of the subscription.
        """
        return pulumi.get(self, 'state')

    @property
    @pulumi.getter
    def tenant(self) -> pulumi.Output[Optional[str]]:
        """
        The AAD Tenant ID associated with the subscription. For example, 00000000-0000-0000-0000-000000000000
        """
        return pulumi.get(self, 'tenant')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.  For example, Microsoft.Management/managementGroups/subscriptions
        """
        return pulumi.get(self, 'type')
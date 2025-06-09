import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
__all__ = ['NotificationRecipientUserArgs', 'NotificationRecipientUser']

@pulumi.input_type
class NotificationRecipientUserArgs:

    def __init__(__self__, *, notification_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], service_name: pulumi.Input[str], user_id: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a NotificationRecipientUser resource.
        :param pulumi.Input[str] notification_name: Notification Name Identifier.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] user_id: User identifier. Must be unique in the current API Management service instance.
        """
        pulumi.set(__self__, 'notification_name', notification_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        pulumi.set(__self__, 'service_name', service_name)
        if user_id is not None:
            pulumi.set(__self__, 'user_id', user_id)

    @property
    @pulumi.getter(name='notificationName')
    def notification_name(self) -> pulumi.Input[str]:
        """
        Notification Name Identifier.
        """
        return pulumi.get(self, 'notification_name')

    @notification_name.setter
    def notification_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'notification_name', value)

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
    @pulumi.getter(name='serviceName')
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, 'service_name')

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'service_name', value)

    @property
    @pulumi.getter(name='userId')
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        User identifier. Must be unique in the current API Management service instance.
        """
        return pulumi.get(self, 'user_id')

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_id', value)

class NotificationRecipientUser(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, notification_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, user_id: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Recipient User details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] notification_name: Notification Name Identifier.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] user_id: User identifier. Must be unique in the current API Management service instance.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: NotificationRecipientUserArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Recipient User details.

        :param str resource_name: The name of the resource.
        :param NotificationRecipientUserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(NotificationRecipientUserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, notification_name: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, service_name: Optional[pulumi.Input[str]]=None, user_id: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NotificationRecipientUserArgs.__new__(NotificationRecipientUserArgs)
            if notification_name is None and (not opts.urn):
                raise TypeError("Missing required property 'notification_name'")
            __props__.__dict__['notification_name'] = notification_name
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            if service_name is None and (not opts.urn):
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__['service_name'] = service_name
            __props__.__dict__['user_id'] = user_id
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:apimanagement:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20170301:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20180101:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20180601preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20190101:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20191201:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20191201preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20200601preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20201201:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20210401preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20210801:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20211201preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20220401preview:NotificationRecipientUser'), pulumi.Alias(type_='azure-native:apimanagement/v20220801:NotificationRecipientUser')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NotificationRecipientUser, __self__).__init__('azure-native:apimanagement/v20210101preview:NotificationRecipientUser', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'NotificationRecipientUser':
        """
        Get an existing NotificationRecipientUser resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = NotificationRecipientUserArgs.__new__(NotificationRecipientUserArgs)
        __props__.__dict__['name'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['user_id'] = None
        return NotificationRecipientUser(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userId')
    def user_id(self) -> pulumi.Output[Optional[str]]:
        """
        API Management UserId subscribed to notification.
        """
        return pulumi.get(self, 'user_id')
import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *
__all__ = ['ActionGroupArgs', 'ActionGroup']

@pulumi.input_type
class ActionGroupArgs:

    def __init__(__self__, *, enabled: pulumi.Input[bool], group_short_name: pulumi.Input[str], resource_group_name: pulumi.Input[str], action_group_name: Optional[pulumi.Input[str]]=None, arm_role_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['ArmRoleReceiverArgs']]]]=None, automation_runbook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRunbookReceiverArgs']]]]=None, azure_app_push_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['AzureAppPushReceiverArgs']]]]=None, azure_function_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFunctionReceiverArgs']]]]=None, email_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['EmailReceiverArgs']]]]=None, itsm_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['ItsmReceiverArgs']]]]=None, location: Optional[pulumi.Input[str]]=None, logic_app_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['LogicAppReceiverArgs']]]]=None, sms_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['SmsReceiverArgs']]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, voice_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['VoiceReceiverArgs']]]]=None, webhook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input['WebhookReceiverArgs']]]]=None):
        """
        The set of arguments for constructing a ActionGroup resource.
        :param pulumi.Input[bool] enabled: Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
        :param pulumi.Input[str] group_short_name: The short name of the action group. This will be used in SMS messages.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] action_group_name: The name of the action group.
        :param pulumi.Input[Sequence[pulumi.Input['ArmRoleReceiverArgs']]] arm_role_receivers: The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
        :param pulumi.Input[Sequence[pulumi.Input['AutomationRunbookReceiverArgs']]] automation_runbook_receivers: The list of AutomationRunbook receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['AzureAppPushReceiverArgs']]] azure_app_push_receivers: The list of AzureAppPush receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['AzureFunctionReceiverArgs']]] azure_function_receivers: The list of azure function receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['EmailReceiverArgs']]] email_receivers: The list of email receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['ItsmReceiverArgs']]] itsm_receivers: The list of ITSM receivers that are part of this action group.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Sequence[pulumi.Input['LogicAppReceiverArgs']]] logic_app_receivers: The list of logic app receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['SmsReceiverArgs']]] sms_receivers: The list of SMS receivers that are part of this action group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input['VoiceReceiverArgs']]] voice_receivers: The list of voice receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input['WebhookReceiverArgs']]] webhook_receivers: The list of webhook receivers that are part of this action group.
        """
        if enabled is None:
            enabled = True
        pulumi.set(__self__, 'enabled', enabled)
        pulumi.set(__self__, 'group_short_name', group_short_name)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if action_group_name is not None:
            pulumi.set(__self__, 'action_group_name', action_group_name)
        if arm_role_receivers is not None:
            pulumi.set(__self__, 'arm_role_receivers', arm_role_receivers)
        if automation_runbook_receivers is not None:
            pulumi.set(__self__, 'automation_runbook_receivers', automation_runbook_receivers)
        if azure_app_push_receivers is not None:
            pulumi.set(__self__, 'azure_app_push_receivers', azure_app_push_receivers)
        if azure_function_receivers is not None:
            pulumi.set(__self__, 'azure_function_receivers', azure_function_receivers)
        if email_receivers is not None:
            pulumi.set(__self__, 'email_receivers', email_receivers)
        if itsm_receivers is not None:
            pulumi.set(__self__, 'itsm_receivers', itsm_receivers)
        if location is not None:
            pulumi.set(__self__, 'location', location)
        if logic_app_receivers is not None:
            pulumi.set(__self__, 'logic_app_receivers', logic_app_receivers)
        if sms_receivers is not None:
            pulumi.set(__self__, 'sms_receivers', sms_receivers)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)
        if voice_receivers is not None:
            pulumi.set(__self__, 'voice_receivers', voice_receivers)
        if webhook_receivers is not None:
            pulumi.set(__self__, 'webhook_receivers', webhook_receivers)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='groupShortName')
    def group_short_name(self) -> pulumi.Input[str]:
        """
        The short name of the action group. This will be used in SMS messages.
        """
        return pulumi.get(self, 'group_short_name')

    @group_short_name.setter
    def group_short_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'group_short_name', value)

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
    @pulumi.getter(name='actionGroupName')
    def action_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the action group.
        """
        return pulumi.get(self, 'action_group_name')

    @action_group_name.setter
    def action_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'action_group_name', value)

    @property
    @pulumi.getter(name='armRoleReceivers')
    def arm_role_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ArmRoleReceiverArgs']]]]:
        """
        The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
        """
        return pulumi.get(self, 'arm_role_receivers')

    @arm_role_receivers.setter
    def arm_role_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ArmRoleReceiverArgs']]]]):
        pulumi.set(self, 'arm_role_receivers', value)

    @property
    @pulumi.getter(name='automationRunbookReceivers')
    def automation_runbook_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRunbookReceiverArgs']]]]:
        """
        The list of AutomationRunbook receivers that are part of this action group.
        """
        return pulumi.get(self, 'automation_runbook_receivers')

    @automation_runbook_receivers.setter
    def automation_runbook_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AutomationRunbookReceiverArgs']]]]):
        pulumi.set(self, 'automation_runbook_receivers', value)

    @property
    @pulumi.getter(name='azureAppPushReceivers')
    def azure_app_push_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureAppPushReceiverArgs']]]]:
        """
        The list of AzureAppPush receivers that are part of this action group.
        """
        return pulumi.get(self, 'azure_app_push_receivers')

    @azure_app_push_receivers.setter
    def azure_app_push_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureAppPushReceiverArgs']]]]):
        pulumi.set(self, 'azure_app_push_receivers', value)

    @property
    @pulumi.getter(name='azureFunctionReceivers')
    def azure_function_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AzureFunctionReceiverArgs']]]]:
        """
        The list of azure function receivers that are part of this action group.
        """
        return pulumi.get(self, 'azure_function_receivers')

    @azure_function_receivers.setter
    def azure_function_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AzureFunctionReceiverArgs']]]]):
        pulumi.set(self, 'azure_function_receivers', value)

    @property
    @pulumi.getter(name='emailReceivers')
    def email_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EmailReceiverArgs']]]]:
        """
        The list of email receivers that are part of this action group.
        """
        return pulumi.get(self, 'email_receivers')

    @email_receivers.setter
    def email_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EmailReceiverArgs']]]]):
        pulumi.set(self, 'email_receivers', value)

    @property
    @pulumi.getter(name='itsmReceivers')
    def itsm_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ItsmReceiverArgs']]]]:
        """
        The list of ITSM receivers that are part of this action group.
        """
        return pulumi.get(self, 'itsm_receivers')

    @itsm_receivers.setter
    def itsm_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ItsmReceiverArgs']]]]):
        pulumi.set(self, 'itsm_receivers', value)

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
    @pulumi.getter(name='logicAppReceivers')
    def logic_app_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LogicAppReceiverArgs']]]]:
        """
        The list of logic app receivers that are part of this action group.
        """
        return pulumi.get(self, 'logic_app_receivers')

    @logic_app_receivers.setter
    def logic_app_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LogicAppReceiverArgs']]]]):
        pulumi.set(self, 'logic_app_receivers', value)

    @property
    @pulumi.getter(name='smsReceivers')
    def sms_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SmsReceiverArgs']]]]:
        """
        The list of SMS receivers that are part of this action group.
        """
        return pulumi.get(self, 'sms_receivers')

    @sms_receivers.setter
    def sms_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SmsReceiverArgs']]]]):
        pulumi.set(self, 'sms_receivers', value)

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

    @property
    @pulumi.getter(name='voiceReceivers')
    def voice_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VoiceReceiverArgs']]]]:
        """
        The list of voice receivers that are part of this action group.
        """
        return pulumi.get(self, 'voice_receivers')

    @voice_receivers.setter
    def voice_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VoiceReceiverArgs']]]]):
        pulumi.set(self, 'voice_receivers', value)

    @property
    @pulumi.getter(name='webhookReceivers')
    def webhook_receivers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WebhookReceiverArgs']]]]:
        """
        The list of webhook receivers that are part of this action group.
        """
        return pulumi.get(self, 'webhook_receivers')

    @webhook_receivers.setter
    def webhook_receivers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WebhookReceiverArgs']]]]):
        pulumi.set(self, 'webhook_receivers', value)

class ActionGroup(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, action_group_name: Optional[pulumi.Input[str]]=None, arm_role_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ArmRoleReceiverArgs']]]]]=None, automation_runbook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AutomationRunbookReceiverArgs']]]]]=None, azure_app_push_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureAppPushReceiverArgs']]]]]=None, azure_function_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFunctionReceiverArgs']]]]]=None, email_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EmailReceiverArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, group_short_name: Optional[pulumi.Input[str]]=None, itsm_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ItsmReceiverArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, logic_app_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LogicAppReceiverArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sms_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SmsReceiverArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, voice_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VoiceReceiverArgs']]]]]=None, webhook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookReceiverArgs']]]]]=None, __props__=None):
        """
        An action group resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action_group_name: The name of the action group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ArmRoleReceiverArgs']]]] arm_role_receivers: The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AutomationRunbookReceiverArgs']]]] automation_runbook_receivers: The list of AutomationRunbook receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureAppPushReceiverArgs']]]] azure_app_push_receivers: The list of AzureAppPush receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFunctionReceiverArgs']]]] azure_function_receivers: The list of azure function receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EmailReceiverArgs']]]] email_receivers: The list of email receivers that are part of this action group.
        :param pulumi.Input[bool] enabled: Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
        :param pulumi.Input[str] group_short_name: The short name of the action group. This will be used in SMS messages.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ItsmReceiverArgs']]]] itsm_receivers: The list of ITSM receivers that are part of this action group.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LogicAppReceiverArgs']]]] logic_app_receivers: The list of logic app receivers that are part of this action group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SmsReceiverArgs']]]] sms_receivers: The list of SMS receivers that are part of this action group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VoiceReceiverArgs']]]] voice_receivers: The list of voice receivers that are part of this action group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookReceiverArgs']]]] webhook_receivers: The list of webhook receivers that are part of this action group.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ActionGroupArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        An action group resource.

        :param str resource_name: The name of the resource.
        :param ActionGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ActionGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, action_group_name: Optional[pulumi.Input[str]]=None, arm_role_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ArmRoleReceiverArgs']]]]]=None, automation_runbook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AutomationRunbookReceiverArgs']]]]]=None, azure_app_push_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureAppPushReceiverArgs']]]]]=None, azure_function_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AzureFunctionReceiverArgs']]]]]=None, email_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EmailReceiverArgs']]]]]=None, enabled: Optional[pulumi.Input[bool]]=None, group_short_name: Optional[pulumi.Input[str]]=None, itsm_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ItsmReceiverArgs']]]]]=None, location: Optional[pulumi.Input[str]]=None, logic_app_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LogicAppReceiverArgs']]]]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, sms_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SmsReceiverArgs']]]]]=None, tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, voice_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VoiceReceiverArgs']]]]]=None, webhook_receivers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookReceiverArgs']]]]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ActionGroupArgs.__new__(ActionGroupArgs)
            __props__.__dict__['action_group_name'] = action_group_name
            __props__.__dict__['arm_role_receivers'] = arm_role_receivers
            __props__.__dict__['automation_runbook_receivers'] = automation_runbook_receivers
            __props__.__dict__['azure_app_push_receivers'] = azure_app_push_receivers
            __props__.__dict__['azure_function_receivers'] = azure_function_receivers
            __props__.__dict__['email_receivers'] = email_receivers
            if enabled is None:
                enabled = True
            if enabled is None and (not opts.urn):
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__['enabled'] = enabled
            if group_short_name is None and (not opts.urn):
                raise TypeError("Missing required property 'group_short_name'")
            __props__.__dict__['group_short_name'] = group_short_name
            __props__.__dict__['itsm_receivers'] = itsm_receivers
            __props__.__dict__['location'] = location
            __props__.__dict__['logic_app_receivers'] = logic_app_receivers
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['sms_receivers'] = sms_receivers
            __props__.__dict__['tags'] = tags
            __props__.__dict__['voice_receivers'] = voice_receivers
            __props__.__dict__['webhook_receivers'] = webhook_receivers
            __props__.__dict__['name'] = None
            __props__.__dict__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:insights:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20170401:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20180301:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20180901:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20190301:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20210901:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20220401:ActionGroup'), pulumi.Alias(type_='azure-native:insights/v20220601:ActionGroup')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ActionGroup, __self__).__init__('azure-native:insights/v20190601:ActionGroup', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'ActionGroup':
        """
        Get an existing ActionGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = ActionGroupArgs.__new__(ActionGroupArgs)
        __props__.__dict__['arm_role_receivers'] = None
        __props__.__dict__['automation_runbook_receivers'] = None
        __props__.__dict__['azure_app_push_receivers'] = None
        __props__.__dict__['azure_function_receivers'] = None
        __props__.__dict__['email_receivers'] = None
        __props__.__dict__['enabled'] = None
        __props__.__dict__['group_short_name'] = None
        __props__.__dict__['itsm_receivers'] = None
        __props__.__dict__['location'] = None
        __props__.__dict__['logic_app_receivers'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['sms_receivers'] = None
        __props__.__dict__['tags'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['voice_receivers'] = None
        __props__.__dict__['webhook_receivers'] = None
        return ActionGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='armRoleReceivers')
    def arm_role_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.ArmRoleReceiverResponse']]]:
        """
        The list of ARM role receivers that are part of this action group. Roles are Azure RBAC roles and only built-in roles are supported.
        """
        return pulumi.get(self, 'arm_role_receivers')

    @property
    @pulumi.getter(name='automationRunbookReceivers')
    def automation_runbook_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.AutomationRunbookReceiverResponse']]]:
        """
        The list of AutomationRunbook receivers that are part of this action group.
        """
        return pulumi.get(self, 'automation_runbook_receivers')

    @property
    @pulumi.getter(name='azureAppPushReceivers')
    def azure_app_push_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.AzureAppPushReceiverResponse']]]:
        """
        The list of AzureAppPush receivers that are part of this action group.
        """
        return pulumi.get(self, 'azure_app_push_receivers')

    @property
    @pulumi.getter(name='azureFunctionReceivers')
    def azure_function_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.AzureFunctionReceiverResponse']]]:
        """
        The list of azure function receivers that are part of this action group.
        """
        return pulumi.get(self, 'azure_function_receivers')

    @property
    @pulumi.getter(name='emailReceivers')
    def email_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.EmailReceiverResponse']]]:
        """
        The list of email receivers that are part of this action group.
        """
        return pulumi.get(self, 'email_receivers')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        """
        Indicates whether this action group is enabled. If an action group is not enabled, then none of its receivers will receive communications.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter(name='groupShortName')
    def group_short_name(self) -> pulumi.Output[str]:
        """
        The short name of the action group. This will be used in SMS messages.
        """
        return pulumi.get(self, 'group_short_name')

    @property
    @pulumi.getter(name='itsmReceivers')
    def itsm_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.ItsmReceiverResponse']]]:
        """
        The list of ITSM receivers that are part of this action group.
        """
        return pulumi.get(self, 'itsm_receivers')

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='logicAppReceivers')
    def logic_app_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.LogicAppReceiverResponse']]]:
        """
        The list of logic app receivers that are part of this action group.
        """
        return pulumi.get(self, 'logic_app_receivers')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='smsReceivers')
    def sms_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.SmsReceiverResponse']]]:
        """
        The list of SMS receivers that are part of this action group.
        """
        return pulumi.get(self, 'sms_receivers')

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
        Azure resource type
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='voiceReceivers')
    def voice_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.VoiceReceiverResponse']]]:
        """
        The list of voice receivers that are part of this action group.
        """
        return pulumi.get(self, 'voice_receivers')

    @property
    @pulumi.getter(name='webhookReceivers')
    def webhook_receivers(self) -> pulumi.Output[Optional[Sequence['outputs.WebhookReceiverResponse']]]:
        """
        The list of webhook receivers that are part of this action group.
        """
        return pulumi.get(self, 'webhook_receivers')
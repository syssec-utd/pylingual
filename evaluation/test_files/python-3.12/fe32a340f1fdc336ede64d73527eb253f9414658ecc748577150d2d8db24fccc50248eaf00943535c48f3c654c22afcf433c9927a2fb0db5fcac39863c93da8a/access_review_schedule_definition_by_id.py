import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['AccessReviewScheduleDefinitionByIdArgs', 'AccessReviewScheduleDefinitionById']

@pulumi.input_type
class AccessReviewScheduleDefinitionByIdArgs:

    def __init__(__self__, *, auto_apply_decisions_enabled: Optional[pulumi.Input[bool]]=None, backup_reviewers: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]=None, default_decision: Optional[pulumi.Input[Union[str, 'DefaultDecisionType']]]=None, default_decision_enabled: Optional[pulumi.Input[bool]]=None, description_for_admins: Optional[pulumi.Input[str]]=None, description_for_reviewers: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, end_date: Optional[pulumi.Input[str]]=None, expand_nested_memberships: Optional[pulumi.Input[bool]]=None, inactive_duration: Optional[pulumi.Input[str]]=None, instance_duration_in_days: Optional[pulumi.Input[int]]=None, instances: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewInstanceArgs']]]]=None, interval: Optional[pulumi.Input[int]]=None, justification_required_on_approval: Optional[pulumi.Input[bool]]=None, mail_notifications_enabled: Optional[pulumi.Input[bool]]=None, number_of_occurrences: Optional[pulumi.Input[int]]=None, recommendation_look_back_duration: Optional[pulumi.Input[str]]=None, recommendations_enabled: Optional[pulumi.Input[bool]]=None, reminder_notifications_enabled: Optional[pulumi.Input[bool]]=None, reviewers: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]=None, schedule_definition_id: Optional[pulumi.Input[str]]=None, start_date: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']]]=None):
        """
        The set of arguments for constructing a AccessReviewScheduleDefinitionById resource.
        :param pulumi.Input[bool] auto_apply_decisions_enabled: Flag to indicate whether auto-apply capability, to automatically change the target object access resource, is enabled. If not enabled, a user must, after the review completes, apply the access review.
        :param pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]] backup_reviewers: This is the collection of backup reviewers.
        :param pulumi.Input[Union[str, 'DefaultDecisionType']] default_decision: This specifies the behavior for the autoReview feature when an access review completes.
        :param pulumi.Input[bool] default_decision_enabled: Flag to indicate whether reviewers are required to provide a justification when reviewing access.
        :param pulumi.Input[str] description_for_admins: The description provided by the access review creator and visible to admins.
        :param pulumi.Input[str] description_for_reviewers: The description provided by the access review creator to be shown to reviewers.
        :param pulumi.Input[str] display_name: The display name for the schedule definition.
        :param pulumi.Input[str] end_date: The DateTime when the review is scheduled to end. Required if type is endDate
        :param pulumi.Input[bool] expand_nested_memberships: Flag to indicate whether to expand nested memberships or not.
        :param pulumi.Input[str] inactive_duration: Duration users are inactive for. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        :param pulumi.Input[int] instance_duration_in_days: The duration in days for an instance.
        :param pulumi.Input[Sequence[pulumi.Input['AccessReviewInstanceArgs']]] instances: This is the collection of instances returned when one does an expand on it.
        :param pulumi.Input[int] interval: The interval for recurrence. For a quarterly review, the interval is 3 for type : absoluteMonthly.
        :param pulumi.Input[bool] justification_required_on_approval: Flag to indicate whether the reviewer is required to pass justification when recording a decision.
        :param pulumi.Input[bool] mail_notifications_enabled: Flag to indicate whether sending mails to reviewers and the review creator is enabled.
        :param pulumi.Input[int] number_of_occurrences: The number of times to repeat the access review. Required and must be positive if type is numbered.
        :param pulumi.Input[str] recommendation_look_back_duration: Recommendations for access reviews are calculated by looking back at 30 days of data(w.r.t the start date of the review) by default. However, in some scenarios, customers want to change how far back to look at and want to configure 60 days, 90 days, etc. instead. This setting allows customers to configure this duration. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        :param pulumi.Input[bool] recommendations_enabled: Flag to indicate whether showing recommendations to reviewers is enabled.
        :param pulumi.Input[bool] reminder_notifications_enabled: Flag to indicate whether sending reminder emails to reviewers are enabled.
        :param pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]] reviewers: This is the collection of reviewers.
        :param pulumi.Input[str] schedule_definition_id: The id of the access review schedule definition.
        :param pulumi.Input[str] start_date: The DateTime when the review is scheduled to be start. This could be a date in the future. Required on create.
        :param pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']] type: The recurrence range type. The possible values are: endDate, noEnd, numbered.
        """
        if auto_apply_decisions_enabled is not None:
            pulumi.set(__self__, 'auto_apply_decisions_enabled', auto_apply_decisions_enabled)
        if backup_reviewers is not None:
            pulumi.set(__self__, 'backup_reviewers', backup_reviewers)
        if default_decision is not None:
            pulumi.set(__self__, 'default_decision', default_decision)
        if default_decision_enabled is not None:
            pulumi.set(__self__, 'default_decision_enabled', default_decision_enabled)
        if description_for_admins is not None:
            pulumi.set(__self__, 'description_for_admins', description_for_admins)
        if description_for_reviewers is not None:
            pulumi.set(__self__, 'description_for_reviewers', description_for_reviewers)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if end_date is not None:
            pulumi.set(__self__, 'end_date', end_date)
        if expand_nested_memberships is not None:
            pulumi.set(__self__, 'expand_nested_memberships', expand_nested_memberships)
        if inactive_duration is not None:
            pulumi.set(__self__, 'inactive_duration', inactive_duration)
        if instance_duration_in_days is not None:
            pulumi.set(__self__, 'instance_duration_in_days', instance_duration_in_days)
        if instances is not None:
            pulumi.set(__self__, 'instances', instances)
        if interval is not None:
            pulumi.set(__self__, 'interval', interval)
        if justification_required_on_approval is not None:
            pulumi.set(__self__, 'justification_required_on_approval', justification_required_on_approval)
        if mail_notifications_enabled is not None:
            pulumi.set(__self__, 'mail_notifications_enabled', mail_notifications_enabled)
        if number_of_occurrences is not None:
            pulumi.set(__self__, 'number_of_occurrences', number_of_occurrences)
        if recommendation_look_back_duration is not None:
            pulumi.set(__self__, 'recommendation_look_back_duration', recommendation_look_back_duration)
        if recommendations_enabled is not None:
            pulumi.set(__self__, 'recommendations_enabled', recommendations_enabled)
        if reminder_notifications_enabled is not None:
            pulumi.set(__self__, 'reminder_notifications_enabled', reminder_notifications_enabled)
        if reviewers is not None:
            pulumi.set(__self__, 'reviewers', reviewers)
        if schedule_definition_id is not None:
            pulumi.set(__self__, 'schedule_definition_id', schedule_definition_id)
        if start_date is not None:
            pulumi.set(__self__, 'start_date', start_date)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter(name='autoApplyDecisionsEnabled')
    def auto_apply_decisions_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether auto-apply capability, to automatically change the target object access resource, is enabled. If not enabled, a user must, after the review completes, apply the access review.
        """
        return pulumi.get(self, 'auto_apply_decisions_enabled')

    @auto_apply_decisions_enabled.setter
    def auto_apply_decisions_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_apply_decisions_enabled', value)

    @property
    @pulumi.getter(name='backupReviewers')
    def backup_reviewers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]:
        """
        This is the collection of backup reviewers.
        """
        return pulumi.get(self, 'backup_reviewers')

    @backup_reviewers.setter
    def backup_reviewers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]):
        pulumi.set(self, 'backup_reviewers', value)

    @property
    @pulumi.getter(name='defaultDecision')
    def default_decision(self) -> Optional[pulumi.Input[Union[str, 'DefaultDecisionType']]]:
        """
        This specifies the behavior for the autoReview feature when an access review completes.
        """
        return pulumi.get(self, 'default_decision')

    @default_decision.setter
    def default_decision(self, value: Optional[pulumi.Input[Union[str, 'DefaultDecisionType']]]):
        pulumi.set(self, 'default_decision', value)

    @property
    @pulumi.getter(name='defaultDecisionEnabled')
    def default_decision_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether reviewers are required to provide a justification when reviewing access.
        """
        return pulumi.get(self, 'default_decision_enabled')

    @default_decision_enabled.setter
    def default_decision_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'default_decision_enabled', value)

    @property
    @pulumi.getter(name='descriptionForAdmins')
    def description_for_admins(self) -> Optional[pulumi.Input[str]]:
        """
        The description provided by the access review creator and visible to admins.
        """
        return pulumi.get(self, 'description_for_admins')

    @description_for_admins.setter
    def description_for_admins(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description_for_admins', value)

    @property
    @pulumi.getter(name='descriptionForReviewers')
    def description_for_reviewers(self) -> Optional[pulumi.Input[str]]:
        """
        The description provided by the access review creator to be shown to reviewers.
        """
        return pulumi.get(self, 'description_for_reviewers')

    @description_for_reviewers.setter
    def description_for_reviewers(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description_for_reviewers', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name for the schedule definition.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='endDate')
    def end_date(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review is scheduled to end. Required if type is endDate
        """
        return pulumi.get(self, 'end_date')

    @end_date.setter
    def end_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'end_date', value)

    @property
    @pulumi.getter(name='expandNestedMemberships')
    def expand_nested_memberships(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether to expand nested memberships or not.
        """
        return pulumi.get(self, 'expand_nested_memberships')

    @expand_nested_memberships.setter
    def expand_nested_memberships(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'expand_nested_memberships', value)

    @property
    @pulumi.getter(name='inactiveDuration')
    def inactive_duration(self) -> Optional[pulumi.Input[str]]:
        """
        Duration users are inactive for. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        """
        return pulumi.get(self, 'inactive_duration')

    @inactive_duration.setter
    def inactive_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'inactive_duration', value)

    @property
    @pulumi.getter(name='instanceDurationInDays')
    def instance_duration_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        The duration in days for an instance.
        """
        return pulumi.get(self, 'instance_duration_in_days')

    @instance_duration_in_days.setter
    def instance_duration_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'instance_duration_in_days', value)

    @property
    @pulumi.getter
    def instances(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewInstanceArgs']]]]:
        """
        This is the collection of instances returned when one does an expand on it.
        """
        return pulumi.get(self, 'instances')

    @instances.setter
    def instances(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewInstanceArgs']]]]):
        pulumi.set(self, 'instances', value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        """
        The interval for recurrence. For a quarterly review, the interval is 3 for type : absoluteMonthly.
        """
        return pulumi.get(self, 'interval')

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'interval', value)

    @property
    @pulumi.getter(name='justificationRequiredOnApproval')
    def justification_required_on_approval(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether the reviewer is required to pass justification when recording a decision.
        """
        return pulumi.get(self, 'justification_required_on_approval')

    @justification_required_on_approval.setter
    def justification_required_on_approval(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'justification_required_on_approval', value)

    @property
    @pulumi.getter(name='mailNotificationsEnabled')
    def mail_notifications_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether sending mails to reviewers and the review creator is enabled.
        """
        return pulumi.get(self, 'mail_notifications_enabled')

    @mail_notifications_enabled.setter
    def mail_notifications_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'mail_notifications_enabled', value)

    @property
    @pulumi.getter(name='numberOfOccurrences')
    def number_of_occurrences(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times to repeat the access review. Required and must be positive if type is numbered.
        """
        return pulumi.get(self, 'number_of_occurrences')

    @number_of_occurrences.setter
    def number_of_occurrences(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'number_of_occurrences', value)

    @property
    @pulumi.getter(name='recommendationLookBackDuration')
    def recommendation_look_back_duration(self) -> Optional[pulumi.Input[str]]:
        """
        Recommendations for access reviews are calculated by looking back at 30 days of data(w.r.t the start date of the review) by default. However, in some scenarios, customers want to change how far back to look at and want to configure 60 days, 90 days, etc. instead. This setting allows customers to configure this duration. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        """
        return pulumi.get(self, 'recommendation_look_back_duration')

    @recommendation_look_back_duration.setter
    def recommendation_look_back_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'recommendation_look_back_duration', value)

    @property
    @pulumi.getter(name='recommendationsEnabled')
    def recommendations_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether showing recommendations to reviewers is enabled.
        """
        return pulumi.get(self, 'recommendations_enabled')

    @recommendations_enabled.setter
    def recommendations_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'recommendations_enabled', value)

    @property
    @pulumi.getter(name='reminderNotificationsEnabled')
    def reminder_notifications_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether sending reminder emails to reviewers are enabled.
        """
        return pulumi.get(self, 'reminder_notifications_enabled')

    @reminder_notifications_enabled.setter
    def reminder_notifications_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'reminder_notifications_enabled', value)

    @property
    @pulumi.getter
    def reviewers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]:
        """
        This is the collection of reviewers.
        """
        return pulumi.get(self, 'reviewers')

    @reviewers.setter
    def reviewers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AccessReviewReviewerArgs']]]]):
        pulumi.set(self, 'reviewers', value)

    @property
    @pulumi.getter(name='scheduleDefinitionId')
    def schedule_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the access review schedule definition.
        """
        return pulumi.get(self, 'schedule_definition_id')

    @schedule_definition_id.setter
    def schedule_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'schedule_definition_id', value)

    @property
    @pulumi.getter(name='startDate')
    def start_date(self) -> Optional[pulumi.Input[str]]:
        """
        The DateTime when the review is scheduled to be start. This could be a date in the future. Required on create.
        """
        return pulumi.get(self, 'start_date')

    @start_date.setter
    def start_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'start_date', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']]]:
        """
        The recurrence range type. The possible values are: endDate, noEnd, numbered.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']]]):
        pulumi.set(self, 'type', value)

class AccessReviewScheduleDefinitionById(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_apply_decisions_enabled: Optional[pulumi.Input[bool]]=None, backup_reviewers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]]]=None, default_decision: Optional[pulumi.Input[Union[str, 'DefaultDecisionType']]]=None, default_decision_enabled: Optional[pulumi.Input[bool]]=None, description_for_admins: Optional[pulumi.Input[str]]=None, description_for_reviewers: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, end_date: Optional[pulumi.Input[str]]=None, expand_nested_memberships: Optional[pulumi.Input[bool]]=None, inactive_duration: Optional[pulumi.Input[str]]=None, instance_duration_in_days: Optional[pulumi.Input[int]]=None, instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewInstanceArgs']]]]]=None, interval: Optional[pulumi.Input[int]]=None, justification_required_on_approval: Optional[pulumi.Input[bool]]=None, mail_notifications_enabled: Optional[pulumi.Input[bool]]=None, number_of_occurrences: Optional[pulumi.Input[int]]=None, recommendation_look_back_duration: Optional[pulumi.Input[str]]=None, recommendations_enabled: Optional[pulumi.Input[bool]]=None, reminder_notifications_enabled: Optional[pulumi.Input[bool]]=None, reviewers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]]]=None, schedule_definition_id: Optional[pulumi.Input[str]]=None, start_date: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']]]=None, __props__=None):
        """
        Access Review Schedule Definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_apply_decisions_enabled: Flag to indicate whether auto-apply capability, to automatically change the target object access resource, is enabled. If not enabled, a user must, after the review completes, apply the access review.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]] backup_reviewers: This is the collection of backup reviewers.
        :param pulumi.Input[Union[str, 'DefaultDecisionType']] default_decision: This specifies the behavior for the autoReview feature when an access review completes.
        :param pulumi.Input[bool] default_decision_enabled: Flag to indicate whether reviewers are required to provide a justification when reviewing access.
        :param pulumi.Input[str] description_for_admins: The description provided by the access review creator and visible to admins.
        :param pulumi.Input[str] description_for_reviewers: The description provided by the access review creator to be shown to reviewers.
        :param pulumi.Input[str] display_name: The display name for the schedule definition.
        :param pulumi.Input[str] end_date: The DateTime when the review is scheduled to end. Required if type is endDate
        :param pulumi.Input[bool] expand_nested_memberships: Flag to indicate whether to expand nested memberships or not.
        :param pulumi.Input[str] inactive_duration: Duration users are inactive for. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        :param pulumi.Input[int] instance_duration_in_days: The duration in days for an instance.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewInstanceArgs']]]] instances: This is the collection of instances returned when one does an expand on it.
        :param pulumi.Input[int] interval: The interval for recurrence. For a quarterly review, the interval is 3 for type : absoluteMonthly.
        :param pulumi.Input[bool] justification_required_on_approval: Flag to indicate whether the reviewer is required to pass justification when recording a decision.
        :param pulumi.Input[bool] mail_notifications_enabled: Flag to indicate whether sending mails to reviewers and the review creator is enabled.
        :param pulumi.Input[int] number_of_occurrences: The number of times to repeat the access review. Required and must be positive if type is numbered.
        :param pulumi.Input[str] recommendation_look_back_duration: Recommendations for access reviews are calculated by looking back at 30 days of data(w.r.t the start date of the review) by default. However, in some scenarios, customers want to change how far back to look at and want to configure 60 days, 90 days, etc. instead. This setting allows customers to configure this duration. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        :param pulumi.Input[bool] recommendations_enabled: Flag to indicate whether showing recommendations to reviewers is enabled.
        :param pulumi.Input[bool] reminder_notifications_enabled: Flag to indicate whether sending reminder emails to reviewers are enabled.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]] reviewers: This is the collection of reviewers.
        :param pulumi.Input[str] schedule_definition_id: The id of the access review schedule definition.
        :param pulumi.Input[str] start_date: The DateTime when the review is scheduled to be start. This could be a date in the future. Required on create.
        :param pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']] type: The recurrence range type. The possible values are: endDate, noEnd, numbered.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: Optional[AccessReviewScheduleDefinitionByIdArgs]=None, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Access Review Schedule Definition.

        :param str resource_name: The name of the resource.
        :param AccessReviewScheduleDefinitionByIdArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessReviewScheduleDefinitionByIdArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, auto_apply_decisions_enabled: Optional[pulumi.Input[bool]]=None, backup_reviewers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]]]=None, default_decision: Optional[pulumi.Input[Union[str, 'DefaultDecisionType']]]=None, default_decision_enabled: Optional[pulumi.Input[bool]]=None, description_for_admins: Optional[pulumi.Input[str]]=None, description_for_reviewers: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, end_date: Optional[pulumi.Input[str]]=None, expand_nested_memberships: Optional[pulumi.Input[bool]]=None, inactive_duration: Optional[pulumi.Input[str]]=None, instance_duration_in_days: Optional[pulumi.Input[int]]=None, instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewInstanceArgs']]]]]=None, interval: Optional[pulumi.Input[int]]=None, justification_required_on_approval: Optional[pulumi.Input[bool]]=None, mail_notifications_enabled: Optional[pulumi.Input[bool]]=None, number_of_occurrences: Optional[pulumi.Input[int]]=None, recommendation_look_back_duration: Optional[pulumi.Input[str]]=None, recommendations_enabled: Optional[pulumi.Input[bool]]=None, reminder_notifications_enabled: Optional[pulumi.Input[bool]]=None, reviewers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AccessReviewReviewerArgs']]]]]=None, schedule_definition_id: Optional[pulumi.Input[str]]=None, start_date: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[Union[str, 'AccessReviewRecurrenceRangeType']]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessReviewScheduleDefinitionByIdArgs.__new__(AccessReviewScheduleDefinitionByIdArgs)
            __props__.__dict__['auto_apply_decisions_enabled'] = auto_apply_decisions_enabled
            __props__.__dict__['backup_reviewers'] = backup_reviewers
            __props__.__dict__['default_decision'] = default_decision
            __props__.__dict__['default_decision_enabled'] = default_decision_enabled
            __props__.__dict__['description_for_admins'] = description_for_admins
            __props__.__dict__['description_for_reviewers'] = description_for_reviewers
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['end_date'] = end_date
            __props__.__dict__['expand_nested_memberships'] = expand_nested_memberships
            __props__.__dict__['inactive_duration'] = inactive_duration
            __props__.__dict__['instance_duration_in_days'] = instance_duration_in_days
            __props__.__dict__['instances'] = instances
            __props__.__dict__['interval'] = interval
            __props__.__dict__['justification_required_on_approval'] = justification_required_on_approval
            __props__.__dict__['mail_notifications_enabled'] = mail_notifications_enabled
            __props__.__dict__['number_of_occurrences'] = number_of_occurrences
            __props__.__dict__['recommendation_look_back_duration'] = recommendation_look_back_duration
            __props__.__dict__['recommendations_enabled'] = recommendations_enabled
            __props__.__dict__['reminder_notifications_enabled'] = reminder_notifications_enabled
            __props__.__dict__['reviewers'] = reviewers
            __props__.__dict__['schedule_definition_id'] = schedule_definition_id
            __props__.__dict__['start_date'] = start_date
            __props__.__dict__['type'] = type
            __props__.__dict__['assignment_state'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['principal_id'] = None
            __props__.__dict__['principal_name'] = None
            __props__.__dict__['principal_type'] = None
            __props__.__dict__['resource_id'] = None
            __props__.__dict__['reviewers_type'] = None
            __props__.__dict__['role_definition_id'] = None
            __props__.__dict__['status'] = None
            __props__.__dict__['user_principal_name'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:authorization:AccessReviewScheduleDefinitionById'), pulumi.Alias(type_='azure-native:authorization/v20180501preview:AccessReviewScheduleDefinitionById'), pulumi.Alias(type_='azure-native:authorization/v20210301preview:AccessReviewScheduleDefinitionById'), pulumi.Alias(type_='azure-native:authorization/v20210701preview:AccessReviewScheduleDefinitionById'), pulumi.Alias(type_='azure-native:authorization/v20211201preview:AccessReviewScheduleDefinitionById')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AccessReviewScheduleDefinitionById, __self__).__init__('azure-native:authorization/v20211116preview:AccessReviewScheduleDefinitionById', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'AccessReviewScheduleDefinitionById':
        """
        Get an existing AccessReviewScheduleDefinitionById resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = AccessReviewScheduleDefinitionByIdArgs.__new__(AccessReviewScheduleDefinitionByIdArgs)
        __props__.__dict__['assignment_state'] = None
        __props__.__dict__['auto_apply_decisions_enabled'] = None
        __props__.__dict__['backup_reviewers'] = None
        __props__.__dict__['default_decision'] = None
        __props__.__dict__['default_decision_enabled'] = None
        __props__.__dict__['description_for_admins'] = None
        __props__.__dict__['description_for_reviewers'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['end_date'] = None
        __props__.__dict__['expand_nested_memberships'] = None
        __props__.__dict__['inactive_duration'] = None
        __props__.__dict__['instance_duration_in_days'] = None
        __props__.__dict__['instances'] = None
        __props__.__dict__['interval'] = None
        __props__.__dict__['justification_required_on_approval'] = None
        __props__.__dict__['mail_notifications_enabled'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['number_of_occurrences'] = None
        __props__.__dict__['principal_id'] = None
        __props__.__dict__['principal_name'] = None
        __props__.__dict__['principal_type'] = None
        __props__.__dict__['recommendation_look_back_duration'] = None
        __props__.__dict__['recommendations_enabled'] = None
        __props__.__dict__['reminder_notifications_enabled'] = None
        __props__.__dict__['resource_id'] = None
        __props__.__dict__['reviewers'] = None
        __props__.__dict__['reviewers_type'] = None
        __props__.__dict__['role_definition_id'] = None
        __props__.__dict__['start_date'] = None
        __props__.__dict__['status'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['user_principal_name'] = None
        return AccessReviewScheduleDefinitionById(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='assignmentState')
    def assignment_state(self) -> pulumi.Output[str]:
        """
        The role assignment state eligible/active to review
        """
        return pulumi.get(self, 'assignment_state')

    @property
    @pulumi.getter(name='autoApplyDecisionsEnabled')
    def auto_apply_decisions_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether auto-apply capability, to automatically change the target object access resource, is enabled. If not enabled, a user must, after the review completes, apply the access review.
        """
        return pulumi.get(self, 'auto_apply_decisions_enabled')

    @property
    @pulumi.getter(name='backupReviewers')
    def backup_reviewers(self) -> pulumi.Output[Optional[Sequence['outputs.AccessReviewReviewerResponse']]]:
        """
        This is the collection of backup reviewers.
        """
        return pulumi.get(self, 'backup_reviewers')

    @property
    @pulumi.getter(name='defaultDecision')
    def default_decision(self) -> pulumi.Output[Optional[str]]:
        """
        This specifies the behavior for the autoReview feature when an access review completes.
        """
        return pulumi.get(self, 'default_decision')

    @property
    @pulumi.getter(name='defaultDecisionEnabled')
    def default_decision_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether reviewers are required to provide a justification when reviewing access.
        """
        return pulumi.get(self, 'default_decision_enabled')

    @property
    @pulumi.getter(name='descriptionForAdmins')
    def description_for_admins(self) -> pulumi.Output[Optional[str]]:
        """
        The description provided by the access review creator and visible to admins.
        """
        return pulumi.get(self, 'description_for_admins')

    @property
    @pulumi.getter(name='descriptionForReviewers')
    def description_for_reviewers(self) -> pulumi.Output[Optional[str]]:
        """
        The description provided by the access review creator to be shown to reviewers.
        """
        return pulumi.get(self, 'description_for_reviewers')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The display name for the schedule definition.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='endDate')
    def end_date(self) -> pulumi.Output[Optional[str]]:
        """
        The DateTime when the review is scheduled to end. Required if type is endDate
        """
        return pulumi.get(self, 'end_date')

    @property
    @pulumi.getter(name='expandNestedMemberships')
    def expand_nested_memberships(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether to expand nested memberships or not.
        """
        return pulumi.get(self, 'expand_nested_memberships')

    @property
    @pulumi.getter(name='inactiveDuration')
    def inactive_duration(self) -> pulumi.Output[Optional[str]]:
        """
        Duration users are inactive for. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        """
        return pulumi.get(self, 'inactive_duration')

    @property
    @pulumi.getter(name='instanceDurationInDays')
    def instance_duration_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        The duration in days for an instance.
        """
        return pulumi.get(self, 'instance_duration_in_days')

    @property
    @pulumi.getter
    def instances(self) -> pulumi.Output[Optional[Sequence['outputs.AccessReviewInstanceResponse']]]:
        """
        This is the collection of instances returned when one does an expand on it.
        """
        return pulumi.get(self, 'instances')

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Output[Optional[int]]:
        """
        The interval for recurrence. For a quarterly review, the interval is 3 for type : absoluteMonthly.
        """
        return pulumi.get(self, 'interval')

    @property
    @pulumi.getter(name='justificationRequiredOnApproval')
    def justification_required_on_approval(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether the reviewer is required to pass justification when recording a decision.
        """
        return pulumi.get(self, 'justification_required_on_approval')

    @property
    @pulumi.getter(name='mailNotificationsEnabled')
    def mail_notifications_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether sending mails to reviewers and the review creator is enabled.
        """
        return pulumi.get(self, 'mail_notifications_enabled')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The access review schedule definition unique id.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='numberOfOccurrences')
    def number_of_occurrences(self) -> pulumi.Output[Optional[int]]:
        """
        The number of times to repeat the access review. Required and must be positive if type is numbered.
        """
        return pulumi.get(self, 'number_of_occurrences')

    @property
    @pulumi.getter(name='principalId')
    def principal_id(self) -> pulumi.Output[str]:
        """
        The identity id
        """
        return pulumi.get(self, 'principal_id')

    @property
    @pulumi.getter(name='principalName')
    def principal_name(self) -> pulumi.Output[str]:
        """
        The identity display name
        """
        return pulumi.get(self, 'principal_name')

    @property
    @pulumi.getter(name='principalType')
    def principal_type(self) -> pulumi.Output[str]:
        """
        The identity type user/servicePrincipal to review
        """
        return pulumi.get(self, 'principal_type')

    @property
    @pulumi.getter(name='recommendationLookBackDuration')
    def recommendation_look_back_duration(self) -> pulumi.Output[Optional[str]]:
        """
        Recommendations for access reviews are calculated by looking back at 30 days of data(w.r.t the start date of the review) by default. However, in some scenarios, customers want to change how far back to look at and want to configure 60 days, 90 days, etc. instead. This setting allows customers to configure this duration. The value should be in ISO  8601 format (http://en.wikipedia.org/wiki/ISO_8601#Durations).This code can be used to convert TimeSpan to a valid interval string: XmlConvert.ToString(new TimeSpan(hours, minutes, seconds))
        """
        return pulumi.get(self, 'recommendation_look_back_duration')

    @property
    @pulumi.getter(name='recommendationsEnabled')
    def recommendations_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether showing recommendations to reviewers is enabled.
        """
        return pulumi.get(self, 'recommendations_enabled')

    @property
    @pulumi.getter(name='reminderNotificationsEnabled')
    def reminder_notifications_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether sending reminder emails to reviewers are enabled.
        """
        return pulumi.get(self, 'reminder_notifications_enabled')

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> pulumi.Output[str]:
        """
        ResourceId in which this review is getting created
        """
        return pulumi.get(self, 'resource_id')

    @property
    @pulumi.getter
    def reviewers(self) -> pulumi.Output[Optional[Sequence['outputs.AccessReviewReviewerResponse']]]:
        """
        This is the collection of reviewers.
        """
        return pulumi.get(self, 'reviewers')

    @property
    @pulumi.getter(name='reviewersType')
    def reviewers_type(self) -> pulumi.Output[str]:
        """
        This field specifies the type of reviewers for a review. Usually for a review, reviewers are explicitly assigned. However, in some cases, the reviewers may not be assigned and instead be chosen dynamically. For example managers review or self review.
        """
        return pulumi.get(self, 'reviewers_type')

    @property
    @pulumi.getter(name='roleDefinitionId')
    def role_definition_id(self) -> pulumi.Output[str]:
        """
        This is used to indicate the role being reviewed
        """
        return pulumi.get(self, 'role_definition_id')

    @property
    @pulumi.getter(name='startDate')
    def start_date(self) -> pulumi.Output[Optional[str]]:
        """
        The DateTime when the review is scheduled to be start. This could be a date in the future. Required on create.
        """
        return pulumi.get(self, 'start_date')

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        This read-only field specifies the status of an accessReview.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userPrincipalName')
    def user_principal_name(self) -> pulumi.Output[str]:
        """
        The user principal name(if valid)
        """
        return pulumi.get(self, 'user_principal_name')
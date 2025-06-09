import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['GoogleCloudBillingBudgetsV1beta1AllUpdatesRuleResponse', 'GoogleCloudBillingBudgetsV1beta1BudgetAmountResponse', 'GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse', 'GoogleCloudBillingBudgetsV1beta1FilterResponse', 'GoogleCloudBillingBudgetsV1beta1LastPeriodAmountResponse', 'GoogleCloudBillingBudgetsV1beta1ThresholdRuleResponse', 'GoogleTypeDateResponse', 'GoogleTypeMoneyResponse']

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1AllUpdatesRuleResponse(dict):
    """
    AllUpdatesRule defines notifications that are sent based on budget spend and thresholds.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'disableDefaultIamRecipients':
            suggest = 'disable_default_iam_recipients'
        elif key == 'monitoringNotificationChannels':
            suggest = 'monitoring_notification_channels'
        elif key == 'pubsubTopic':
            suggest = 'pubsub_topic'
        elif key == 'schemaVersion':
            suggest = 'schema_version'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudBillingBudgetsV1beta1AllUpdatesRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudBillingBudgetsV1beta1AllUpdatesRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleCloudBillingBudgetsV1beta1AllUpdatesRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, disable_default_iam_recipients: bool, monitoring_notification_channels: Sequence[str], pubsub_topic: str, schema_version: str):
        """
        AllUpdatesRule defines notifications that are sent based on budget spend and thresholds.
        :param bool disable_default_iam_recipients: Optional. When set to true, disables default notifications sent when a threshold is exceeded. Default notifications are sent to those with Billing Account Administrator and Billing Account User IAM roles for the target account.
        :param Sequence[str] monitoring_notification_channels: Optional. Targets to send notifications to when a threshold is exceeded. This is in addition to default recipients who have billing account IAM roles. The value is the full REST resource name of a monitoring notification channel with the form `projects/{project_id}/notificationChannels/{channel_id}`. A maximum of 5 channels are allowed. See https://cloud.google.com/billing/docs/how-to/budgets-notification-recipients for more details.
        :param str pubsub_topic: Optional. The name of the Pub/Sub topic where budget related messages will be published, in the form `projects/{project_id}/topics/{topic_id}`. Updates are sent at regular intervals to the topic. The topic needs to be created before the budget is created; see https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications for more details. Caller is expected to have `pubsub.topics.setIamPolicy` permission on the topic when it's set for a budget, otherwise, the API call will fail with PERMISSION_DENIED. See https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#permissions_required_for_this_task for more details on Pub/Sub roles and permissions.
        :param str schema_version: Optional. Required when AllUpdatesRule.pubsub_topic is set. The schema version of the notification sent to AllUpdatesRule.pubsub_topic. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format.
        """
        pulumi.set(__self__, 'disable_default_iam_recipients', disable_default_iam_recipients)
        pulumi.set(__self__, 'monitoring_notification_channels', monitoring_notification_channels)
        pulumi.set(__self__, 'pubsub_topic', pubsub_topic)
        pulumi.set(__self__, 'schema_version', schema_version)

    @property
    @pulumi.getter(name='disableDefaultIamRecipients')
    def disable_default_iam_recipients(self) -> bool:
        """
        Optional. When set to true, disables default notifications sent when a threshold is exceeded. Default notifications are sent to those with Billing Account Administrator and Billing Account User IAM roles for the target account.
        """
        return pulumi.get(self, 'disable_default_iam_recipients')

    @property
    @pulumi.getter(name='monitoringNotificationChannels')
    def monitoring_notification_channels(self) -> Sequence[str]:
        """
        Optional. Targets to send notifications to when a threshold is exceeded. This is in addition to default recipients who have billing account IAM roles. The value is the full REST resource name of a monitoring notification channel with the form `projects/{project_id}/notificationChannels/{channel_id}`. A maximum of 5 channels are allowed. See https://cloud.google.com/billing/docs/how-to/budgets-notification-recipients for more details.
        """
        return pulumi.get(self, 'monitoring_notification_channels')

    @property
    @pulumi.getter(name='pubsubTopic')
    def pubsub_topic(self) -> str:
        """
        Optional. The name of the Pub/Sub topic where budget related messages will be published, in the form `projects/{project_id}/topics/{topic_id}`. Updates are sent at regular intervals to the topic. The topic needs to be created before the budget is created; see https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications for more details. Caller is expected to have `pubsub.topics.setIamPolicy` permission on the topic when it's set for a budget, otherwise, the API call will fail with PERMISSION_DENIED. See https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#permissions_required_for_this_task for more details on Pub/Sub roles and permissions.
        """
        return pulumi.get(self, 'pubsub_topic')

    @property
    @pulumi.getter(name='schemaVersion')
    def schema_version(self) -> str:
        """
        Optional. Required when AllUpdatesRule.pubsub_topic is set. The schema version of the notification sent to AllUpdatesRule.pubsub_topic. Only "1.0" is accepted. It represents the JSON schema as defined in https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format.
        """
        return pulumi.get(self, 'schema_version')

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1BudgetAmountResponse(dict):
    """
    The budgeted amount for each usage period.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'lastPeriodAmount':
            suggest = 'last_period_amount'
        elif key == 'specifiedAmount':
            suggest = 'specified_amount'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudBillingBudgetsV1beta1BudgetAmountResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudBillingBudgetsV1beta1BudgetAmountResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleCloudBillingBudgetsV1beta1BudgetAmountResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, last_period_amount: 'outputs.GoogleCloudBillingBudgetsV1beta1LastPeriodAmountResponse', specified_amount: 'outputs.GoogleTypeMoneyResponse'):
        """
        The budgeted amount for each usage period.
        :param 'GoogleCloudBillingBudgetsV1beta1LastPeriodAmountResponse' last_period_amount: Use the last period's actual spend as the budget for the present period. LastPeriodAmount can only be set when the budget's time period is a Filter.calendar_period. It cannot be set in combination with Filter.custom_period.
        :param 'GoogleTypeMoneyResponse' specified_amount: A specified amount to use as the budget. `currency_code` is optional. If specified when creating a budget, it must match the currency of the billing account. If specified when updating a budget, it must match the currency_code of the existing budget. The `currency_code` is provided on output.
        """
        pulumi.set(__self__, 'last_period_amount', last_period_amount)
        pulumi.set(__self__, 'specified_amount', specified_amount)

    @property
    @pulumi.getter(name='lastPeriodAmount')
    def last_period_amount(self) -> 'outputs.GoogleCloudBillingBudgetsV1beta1LastPeriodAmountResponse':
        """
        Use the last period's actual spend as the budget for the present period. LastPeriodAmount can only be set when the budget's time period is a Filter.calendar_period. It cannot be set in combination with Filter.custom_period.
        """
        return pulumi.get(self, 'last_period_amount')

    @property
    @pulumi.getter(name='specifiedAmount')
    def specified_amount(self) -> 'outputs.GoogleTypeMoneyResponse':
        """
        A specified amount to use as the budget. `currency_code` is optional. If specified when creating a budget, it must match the currency of the billing account. If specified when updating a budget, it must match the currency_code of the existing budget. The `currency_code` is provided on output.
        """
        return pulumi.get(self, 'specified_amount')

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse(dict):
    """
    All date times begin at 12 AM US and Canadian Pacific Time (UTC-8).
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'endDate':
            suggest = 'end_date'
        elif key == 'startDate':
            suggest = 'start_date'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, end_date: 'outputs.GoogleTypeDateResponse', start_date: 'outputs.GoogleTypeDateResponse'):
        """
        All date times begin at 12 AM US and Canadian Pacific Time (UTC-8).
        :param 'GoogleTypeDateResponse' end_date: Optional. The end date of the time period. Budgets with elapsed end date won't be processed. If unset, specifies to track all usage incurred since the start_date.
        :param 'GoogleTypeDateResponse' start_date: The start date must be after January 1, 2017.
        """
        pulumi.set(__self__, 'end_date', end_date)
        pulumi.set(__self__, 'start_date', start_date)

    @property
    @pulumi.getter(name='endDate')
    def end_date(self) -> 'outputs.GoogleTypeDateResponse':
        """
        Optional. The end date of the time period. Budgets with elapsed end date won't be processed. If unset, specifies to track all usage incurred since the start_date.
        """
        return pulumi.get(self, 'end_date')

    @property
    @pulumi.getter(name='startDate')
    def start_date(self) -> 'outputs.GoogleTypeDateResponse':
        """
        The start date must be after January 1, 2017.
        """
        return pulumi.get(self, 'start_date')

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1FilterResponse(dict):
    """
    A filter for a budget, limiting the scope of the cost to calculate.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'calendarPeriod':
            suggest = 'calendar_period'
        elif key == 'creditTypes':
            suggest = 'credit_types'
        elif key == 'creditTypesTreatment':
            suggest = 'credit_types_treatment'
        elif key == 'customPeriod':
            suggest = 'custom_period'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudBillingBudgetsV1beta1FilterResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudBillingBudgetsV1beta1FilterResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleCloudBillingBudgetsV1beta1FilterResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, calendar_period: str, credit_types: Sequence[str], credit_types_treatment: str, custom_period: 'outputs.GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse', labels: Mapping[str, str], projects: Sequence[str], services: Sequence[str], subaccounts: Sequence[str]):
        """
        A filter for a budget, limiting the scope of the cost to calculate.
        :param str calendar_period: Optional. Specifies to track usage for recurring calendar period. For example, assume that CalendarPeriod.QUARTER is set. The budget will track usage from April 1 to June 30, when the current calendar month is April, May, June. After that, it will track usage from July 1 to September 30 when the current calendar month is July, August, September, so on.
        :param Sequence[str] credit_types: Optional. If Filter.credit_types_treatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See [a list of acceptable credit type values](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables#credits-type). If Filter.credit_types_treatment is **not** INCLUDE_SPECIFIED_CREDITS, this field must be empty.
        :param str credit_types_treatment: Optional. If not set, default behavior is `INCLUDE_ALL_CREDITS`.
        :param 'GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse' custom_period: Optional. Specifies to track usage from any start date (required) to any end date (optional). This time period is static, it does not recur.
        :param Mapping[str, str] labels: Optional. A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. If omitted, the report will include all labeled and unlabeled usage. An object containing a single `"key": value` pair. Example: `{ "name": "wrench" }`. _Currently, multiple entries or multiple values per entry are not allowed._
        :param Sequence[str] projects: Optional. A set of projects of the form `projects/{project}`, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on.
        :param Sequence[str] services: Optional. A set of services of the form `services/{service_id}`, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api.
        :param Sequence[str] subaccounts: Optional. A set of subaccounts of the form `billingAccounts/{account_id}`, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If omitted, the report will include usage from the parent account and all subaccounts, if they exist.
        """
        pulumi.set(__self__, 'calendar_period', calendar_period)
        pulumi.set(__self__, 'credit_types', credit_types)
        pulumi.set(__self__, 'credit_types_treatment', credit_types_treatment)
        pulumi.set(__self__, 'custom_period', custom_period)
        pulumi.set(__self__, 'labels', labels)
        pulumi.set(__self__, 'projects', projects)
        pulumi.set(__self__, 'services', services)
        pulumi.set(__self__, 'subaccounts', subaccounts)

    @property
    @pulumi.getter(name='calendarPeriod')
    def calendar_period(self) -> str:
        """
        Optional. Specifies to track usage for recurring calendar period. For example, assume that CalendarPeriod.QUARTER is set. The budget will track usage from April 1 to June 30, when the current calendar month is April, May, June. After that, it will track usage from July 1 to September 30 when the current calendar month is July, August, September, so on.
        """
        return pulumi.get(self, 'calendar_period')

    @property
    @pulumi.getter(name='creditTypes')
    def credit_types(self) -> Sequence[str]:
        """
        Optional. If Filter.credit_types_treatment is INCLUDE_SPECIFIED_CREDITS, this is a list of credit types to be subtracted from gross cost to determine the spend for threshold calculations. See [a list of acceptable credit type values](https://cloud.google.com/billing/docs/how-to/export-data-bigquery-tables#credits-type). If Filter.credit_types_treatment is **not** INCLUDE_SPECIFIED_CREDITS, this field must be empty.
        """
        return pulumi.get(self, 'credit_types')

    @property
    @pulumi.getter(name='creditTypesTreatment')
    def credit_types_treatment(self) -> str:
        """
        Optional. If not set, default behavior is `INCLUDE_ALL_CREDITS`.
        """
        return pulumi.get(self, 'credit_types_treatment')

    @property
    @pulumi.getter(name='customPeriod')
    def custom_period(self) -> 'outputs.GoogleCloudBillingBudgetsV1beta1CustomPeriodResponse':
        """
        Optional. Specifies to track usage from any start date (required) to any end date (optional). This time period is static, it does not recur.
        """
        return pulumi.get(self, 'custom_period')

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Optional. A single label and value pair specifying that usage from only this set of labeled resources should be included in the budget. If omitted, the report will include all labeled and unlabeled usage. An object containing a single `"key": value` pair. Example: `{ "name": "wrench" }`. _Currently, multiple entries or multiple values per entry are not allowed._
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter
    def projects(self) -> Sequence[str]:
        """
        Optional. A set of projects of the form `projects/{project}`, specifying that usage from only this set of projects should be included in the budget. If omitted, the report will include all usage for the billing account, regardless of which project the usage occurred on.
        """
        return pulumi.get(self, 'projects')

    @property
    @pulumi.getter
    def services(self) -> Sequence[str]:
        """
        Optional. A set of services of the form `services/{service_id}`, specifying that usage from only this set of services should be included in the budget. If omitted, the report will include usage for all the services. The service names are available through the Catalog API: https://cloud.google.com/billing/v1/how-tos/catalog-api.
        """
        return pulumi.get(self, 'services')

    @property
    @pulumi.getter
    def subaccounts(self) -> Sequence[str]:
        """
        Optional. A set of subaccounts of the form `billingAccounts/{account_id}`, specifying that usage from only this set of subaccounts should be included in the budget. If a subaccount is set to the name of the parent account, usage from the parent account will be included. If omitted, the report will include usage from the parent account and all subaccounts, if they exist.
        """
        return pulumi.get(self, 'subaccounts')

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1LastPeriodAmountResponse(dict):
    """
    Describes a budget amount targeted to the last Filter.calendar_period spend. At this time, the amount is automatically 100% of the last calendar period's spend; that is, there are no other options yet. Future configuration options will be described here (for example, configuring a percentage of last period's spend). LastPeriodAmount cannot be set for a budget configured with a Filter.custom_period.
    """

    def __init__(__self__):
        """
        Describes a budget amount targeted to the last Filter.calendar_period spend. At this time, the amount is automatically 100% of the last calendar period's spend; that is, there are no other options yet. Future configuration options will be described here (for example, configuring a percentage of last period's spend). LastPeriodAmount cannot be set for a budget configured with a Filter.custom_period.
        """
        pass

@pulumi.output_type
class GoogleCloudBillingBudgetsV1beta1ThresholdRuleResponse(dict):
    """
    ThresholdRule contains the definition of a threshold. Threshold rules define the triggering events used to generate a budget notification email. When a threshold is crossed (spend exceeds the specified percentages of the budget), budget alert emails are sent to the email recipients you specify in the [NotificationsRule](#notificationsrule). Threshold rules also affect the fields included in the [JSON data object](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format) sent to a Pub/Sub topic. Threshold rules are _required_ if using email notifications. Threshold rules are _optional_ if only setting a [`pubsubTopic` NotificationsRule](#NotificationsRule), unless you want your JSON data object to include data about the thresholds you set. For more information, see [set budget threshold rules and actions](https://cloud.google.com/billing/docs/how-to/budgets#budget-actions).
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'spendBasis':
            suggest = 'spend_basis'
        elif key == 'thresholdPercent':
            suggest = 'threshold_percent'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleCloudBillingBudgetsV1beta1ThresholdRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleCloudBillingBudgetsV1beta1ThresholdRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleCloudBillingBudgetsV1beta1ThresholdRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, spend_basis: str, threshold_percent: float):
        """
        ThresholdRule contains the definition of a threshold. Threshold rules define the triggering events used to generate a budget notification email. When a threshold is crossed (spend exceeds the specified percentages of the budget), budget alert emails are sent to the email recipients you specify in the [NotificationsRule](#notificationsrule). Threshold rules also affect the fields included in the [JSON data object](https://cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications#notification_format) sent to a Pub/Sub topic. Threshold rules are _required_ if using email notifications. Threshold rules are _optional_ if only setting a [`pubsubTopic` NotificationsRule](#NotificationsRule), unless you want your JSON data object to include data about the thresholds you set. For more information, see [set budget threshold rules and actions](https://cloud.google.com/billing/docs/how-to/budgets#budget-actions).
        :param str spend_basis: Optional. The type of basis used to determine if spend has passed the threshold. Behavior defaults to CURRENT_SPEND if not set.
        :param float threshold_percent: Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Validation: non-negative number.
        """
        pulumi.set(__self__, 'spend_basis', spend_basis)
        pulumi.set(__self__, 'threshold_percent', threshold_percent)

    @property
    @pulumi.getter(name='spendBasis')
    def spend_basis(self) -> str:
        """
        Optional. The type of basis used to determine if spend has passed the threshold. Behavior defaults to CURRENT_SPEND if not set.
        """
        return pulumi.get(self, 'spend_basis')

    @property
    @pulumi.getter(name='thresholdPercent')
    def threshold_percent(self) -> float:
        """
        Send an alert when this threshold is exceeded. This is a 1.0-based percentage, so 0.5 = 50%. Validation: non-negative number.
        """
        return pulumi.get(self, 'threshold_percent')

@pulumi.output_type
class GoogleTypeDateResponse(dict):
    """
    Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following: * A full date, with non-zero year, month, and day values. * A month and day, with a zero year (for example, an anniversary). * A year on its own, with a zero month and a zero day. * A year and month, with a zero day (for example, a credit card expiration date). Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp
    """

    def __init__(__self__, *, day: int, month: int, year: int):
        """
        Represents a whole or partial calendar date, such as a birthday. The time of day and time zone are either specified elsewhere or are insignificant. The date is relative to the Gregorian Calendar. This can represent one of the following: * A full date, with non-zero year, month, and day values. * A month and day, with a zero year (for example, an anniversary). * A year on its own, with a zero month and a zero day. * A year and month, with a zero day (for example, a credit card expiration date). Related types: * google.type.TimeOfDay * google.type.DateTime * google.protobuf.Timestamp
        :param int day: Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.
        :param int month: Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.
        :param int year: Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.
        """
        pulumi.set(__self__, 'day', day)
        pulumi.set(__self__, 'month', month)
        pulumi.set(__self__, 'year', year)

    @property
    @pulumi.getter
    def day(self) -> int:
        """
        Day of a month. Must be from 1 to 31 and valid for the year and month, or 0 to specify a year by itself or a year and month where the day isn't significant.
        """
        return pulumi.get(self, 'day')

    @property
    @pulumi.getter
    def month(self) -> int:
        """
        Month of a year. Must be from 1 to 12, or 0 to specify a year without a month and day.
        """
        return pulumi.get(self, 'month')

    @property
    @pulumi.getter
    def year(self) -> int:
        """
        Year of the date. Must be from 1 to 9999, or 0 to specify a date without a year.
        """
        return pulumi.get(self, 'year')

@pulumi.output_type
class GoogleTypeMoneyResponse(dict):
    """
    Represents an amount of money with its currency type.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'currencyCode':
            suggest = 'currency_code'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GoogleTypeMoneyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GoogleTypeMoneyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        GoogleTypeMoneyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, currency_code: str, nanos: int, units: str):
        """
        Represents an amount of money with its currency type.
        :param str currency_code: The three-letter currency code defined in ISO 4217.
        :param int nanos: Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If `units` is positive, `nanos` must be positive or zero. If `units` is zero, `nanos` can be positive, zero, or negative. If `units` is negative, `nanos` must be negative or zero. For example $-1.75 is represented as `units`=-1 and `nanos`=-750,000,000.
        :param str units: The whole units of the amount. For example if `currencyCode` is `"USD"`, then 1 unit is one US dollar.
        """
        pulumi.set(__self__, 'currency_code', currency_code)
        pulumi.set(__self__, 'nanos', nanos)
        pulumi.set(__self__, 'units', units)

    @property
    @pulumi.getter(name='currencyCode')
    def currency_code(self) -> str:
        """
        The three-letter currency code defined in ISO 4217.
        """
        return pulumi.get(self, 'currency_code')

    @property
    @pulumi.getter
    def nanos(self) -> int:
        """
        Number of nano (10^-9) units of the amount. The value must be between -999,999,999 and +999,999,999 inclusive. If `units` is positive, `nanos` must be positive or zero. If `units` is zero, `nanos` can be positive, zero, or negative. If `units` is negative, `nanos` must be negative or zero. For example $-1.75 is represented as `units`=-1 and `nanos`=-750,000,000.
        """
        return pulumi.get(self, 'nanos')

    @property
    @pulumi.getter
    def units(self) -> str:
        """
        The whole units of the amount. For example if `currencyCode` is `"USD"`, then 1 unit is one US dollar.
        """
        return pulumi.get(self, 'units')
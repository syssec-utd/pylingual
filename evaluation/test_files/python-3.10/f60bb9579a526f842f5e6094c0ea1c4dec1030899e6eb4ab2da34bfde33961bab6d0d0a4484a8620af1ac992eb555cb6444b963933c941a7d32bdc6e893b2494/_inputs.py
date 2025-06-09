import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['ExportDatasetConfigurationArgs', 'ExportDatasetArgs', 'ExportDefinitionArgs', 'ExportDeliveryDestinationArgs', 'ExportDeliveryInfoArgs', 'ExportRecurrencePeriodArgs', 'ExportScheduleArgs', 'ExportTimePeriodArgs', 'FileDestinationArgs', 'KpiPropertiesArgs', 'NotificationPropertiesArgs', 'PivotPropertiesArgs', 'ReportConfigAggregationArgs', 'ReportConfigComparisonExpressionArgs', 'ReportConfigDatasetConfigurationArgs', 'ReportConfigDatasetArgs', 'ReportConfigFilterArgs', 'ReportConfigGroupingArgs', 'ReportConfigSortingArgs', 'ReportConfigTimePeriodArgs', 'SchedulePropertiesArgs']

@pulumi.input_type
class ExportDatasetConfigurationArgs:

    def __init__(__self__, *, columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The export dataset configuration. Allows columns to be selected for the export. If not provided then the export will include all available columns.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] columns: Array of column names to be included in the export. If not provided then the export will include all available columns. The available columns can vary by customer channel (see examples).
        """
        if columns is not None:
            pulumi.set(__self__, 'columns', columns)

    @property
    @pulumi.getter
    def columns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of column names to be included in the export. If not provided then the export will include all available columns. The available columns can vary by customer channel (see examples).
        """
        return pulumi.get(self, 'columns')

    @columns.setter
    def columns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'columns', value)

@pulumi.input_type
class ExportDatasetArgs:

    def __init__(__self__, *, configuration: Optional[pulumi.Input['ExportDatasetConfigurationArgs']]=None, granularity: Optional[pulumi.Input[Union[str, 'GranularityType']]]=None):
        """
        The definition for data in the export.
        :param pulumi.Input['ExportDatasetConfigurationArgs'] configuration: The export dataset configuration.
        :param pulumi.Input[Union[str, 'GranularityType']] granularity: The granularity of rows in the export. Currently only 'Daily' is supported.
        """
        if configuration is not None:
            pulumi.set(__self__, 'configuration', configuration)
        if granularity is not None:
            pulumi.set(__self__, 'granularity', granularity)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input['ExportDatasetConfigurationArgs']]:
        """
        The export dataset configuration.
        """
        return pulumi.get(self, 'configuration')

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['ExportDatasetConfigurationArgs']]):
        pulumi.set(self, 'configuration', value)

    @property
    @pulumi.getter
    def granularity(self) -> Optional[pulumi.Input[Union[str, 'GranularityType']]]:
        """
        The granularity of rows in the export. Currently only 'Daily' is supported.
        """
        return pulumi.get(self, 'granularity')

    @granularity.setter
    def granularity(self, value: Optional[pulumi.Input[Union[str, 'GranularityType']]]):
        pulumi.set(self, 'granularity', value)

@pulumi.input_type
class ExportDefinitionArgs:

    def __init__(__self__, *, timeframe: pulumi.Input[Union[str, 'TimeframeType']], type: pulumi.Input[Union[str, 'ExportType']], data_set: Optional[pulumi.Input['ExportDatasetArgs']]=None, time_period: Optional[pulumi.Input['ExportTimePeriodArgs']]=None):
        """
        The definition of an export.
        :param pulumi.Input[Union[str, 'TimeframeType']] timeframe: The time frame for pulling data for the export. If custom, then a specific time period must be provided.
        :param pulumi.Input[Union[str, 'ExportType']] type: The type of the export. Note that 'Usage' is equivalent to 'ActualCost' and is applicable to exports that do not yet provide data for charges or amortization for service reservations.
        :param pulumi.Input['ExportDatasetArgs'] data_set: The definition for data in the export.
        :param pulumi.Input['ExportTimePeriodArgs'] time_period: Has time period for pulling data for the export.
        """
        pulumi.set(__self__, 'timeframe', timeframe)
        pulumi.set(__self__, 'type', type)
        if data_set is not None:
            pulumi.set(__self__, 'data_set', data_set)
        if time_period is not None:
            pulumi.set(__self__, 'time_period', time_period)

    @property
    @pulumi.getter
    def timeframe(self) -> pulumi.Input[Union[str, 'TimeframeType']]:
        """
        The time frame for pulling data for the export. If custom, then a specific time period must be provided.
        """
        return pulumi.get(self, 'timeframe')

    @timeframe.setter
    def timeframe(self, value: pulumi.Input[Union[str, 'TimeframeType']]):
        pulumi.set(self, 'timeframe', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'ExportType']]:
        """
        The type of the export. Note that 'Usage' is equivalent to 'ActualCost' and is applicable to exports that do not yet provide data for charges or amortization for service reservations.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'ExportType']]):
        pulumi.set(self, 'type', value)

    @property
    @pulumi.getter(name='dataSet')
    def data_set(self) -> Optional[pulumi.Input['ExportDatasetArgs']]:
        """
        The definition for data in the export.
        """
        return pulumi.get(self, 'data_set')

    @data_set.setter
    def data_set(self, value: Optional[pulumi.Input['ExportDatasetArgs']]):
        pulumi.set(self, 'data_set', value)

    @property
    @pulumi.getter(name='timePeriod')
    def time_period(self) -> Optional[pulumi.Input['ExportTimePeriodArgs']]:
        """
        Has time period for pulling data for the export.
        """
        return pulumi.get(self, 'time_period')

    @time_period.setter
    def time_period(self, value: Optional[pulumi.Input['ExportTimePeriodArgs']]):
        pulumi.set(self, 'time_period', value)

@pulumi.input_type
class ExportDeliveryDestinationArgs:

    def __init__(__self__, *, container: pulumi.Input[str], resource_id: Optional[pulumi.Input[str]]=None, root_folder_path: Optional[pulumi.Input[str]]=None, sas_token: Optional[pulumi.Input[str]]=None, storage_account: Optional[pulumi.Input[str]]=None):
        """
        This represents the blob storage account location where exports of costs will be delivered. There are two ways to configure the destination. The approach recommended for most customers is to specify the resourceId of the storage account. This requires a one-time registration of the account's subscription with the Microsoft.CostManagementExports resource provider in order to give Cost Management services access to the storage. When creating an export in the Azure portal this registration is performed automatically but API users may need to register the subscription explicitly (for more information see https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-supported-services ). Another way to configure the destination is available ONLY to Partners with a Microsoft Partner Agreement plan who are global admins of their billing account. These Partners, instead of specifying the resourceId of a storage account, can specify the storage account name along with a SAS token for the account. This allows exports of costs to a storage account in any tenant. The SAS token should be created for the blob service with Service/Container/Object resource types and with Read/Write/Delete/List/Add/Create permissions (for more information see https://docs.microsoft.com/en-us/azure/cost-management-billing/costs/export-cost-data-storage-account-sas-key ).
        :param pulumi.Input[str] container: The name of the container where exports will be uploaded. If the container does not exist it will be created.
        :param pulumi.Input[str] resource_id: The resource id of the storage account where exports will be delivered. This is not required if a sasToken and storageAccount are specified.
        :param pulumi.Input[str] root_folder_path: The name of the directory where exports will be uploaded.
        :param pulumi.Input[str] sas_token: A SAS token for the storage account. For a restricted set of Azure customers this together with storageAccount can be specified instead of resourceId. Note: the value returned by the API for this property will always be obfuscated. Returning this same obfuscated value will not result in the SAS token being updated. To update this value a new SAS token must be specified.
        :param pulumi.Input[str] storage_account: The storage account where exports will be uploaded. For a restricted set of Azure customers this together with sasToken can be specified instead of resourceId.
        """
        pulumi.set(__self__, 'container', container)
        if resource_id is not None:
            pulumi.set(__self__, 'resource_id', resource_id)
        if root_folder_path is not None:
            pulumi.set(__self__, 'root_folder_path', root_folder_path)
        if sas_token is not None:
            pulumi.set(__self__, 'sas_token', sas_token)
        if storage_account is not None:
            pulumi.set(__self__, 'storage_account', storage_account)

    @property
    @pulumi.getter
    def container(self) -> pulumi.Input[str]:
        """
        The name of the container where exports will be uploaded. If the container does not exist it will be created.
        """
        return pulumi.get(self, 'container')

    @container.setter
    def container(self, value: pulumi.Input[str]):
        pulumi.set(self, 'container', value)

    @property
    @pulumi.getter(name='resourceId')
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource id of the storage account where exports will be delivered. This is not required if a sasToken and storageAccount are specified.
        """
        return pulumi.get(self, 'resource_id')

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_id', value)

    @property
    @pulumi.getter(name='rootFolderPath')
    def root_folder_path(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the directory where exports will be uploaded.
        """
        return pulumi.get(self, 'root_folder_path')

    @root_folder_path.setter
    def root_folder_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'root_folder_path', value)

    @property
    @pulumi.getter(name='sasToken')
    def sas_token(self) -> Optional[pulumi.Input[str]]:
        """
        A SAS token for the storage account. For a restricted set of Azure customers this together with storageAccount can be specified instead of resourceId. Note: the value returned by the API for this property will always be obfuscated. Returning this same obfuscated value will not result in the SAS token being updated. To update this value a new SAS token must be specified.
        """
        return pulumi.get(self, 'sas_token')

    @sas_token.setter
    def sas_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'sas_token', value)

    @property
    @pulumi.getter(name='storageAccount')
    def storage_account(self) -> Optional[pulumi.Input[str]]:
        """
        The storage account where exports will be uploaded. For a restricted set of Azure customers this together with sasToken can be specified instead of resourceId.
        """
        return pulumi.get(self, 'storage_account')

    @storage_account.setter
    def storage_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'storage_account', value)

@pulumi.input_type
class ExportDeliveryInfoArgs:

    def __init__(__self__, *, destination: pulumi.Input['ExportDeliveryDestinationArgs']):
        """
        The delivery information associated with a export.
        :param pulumi.Input['ExportDeliveryDestinationArgs'] destination: Has destination for the export being delivered.
        """
        pulumi.set(__self__, 'destination', destination)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input['ExportDeliveryDestinationArgs']:
        """
        Has destination for the export being delivered.
        """
        return pulumi.get(self, 'destination')

    @destination.setter
    def destination(self, value: pulumi.Input['ExportDeliveryDestinationArgs']):
        pulumi.set(self, 'destination', value)

@pulumi.input_type
class ExportRecurrencePeriodArgs:

    def __init__(__self__, *, from_: pulumi.Input[str], to: Optional[pulumi.Input[str]]=None):
        """
        The start and end date for recurrence schedule.
        :param pulumi.Input[str] from_: The start date of recurrence.
        :param pulumi.Input[str] to: The end date of recurrence.
        """
        pulumi.set(__self__, 'from_', from_)
        if to is not None:
            pulumi.set(__self__, 'to', to)

    @property
    @pulumi.getter(name='from')
    def from_(self) -> pulumi.Input[str]:
        """
        The start date of recurrence.
        """
        return pulumi.get(self, 'from_')

    @from_.setter
    def from_(self, value: pulumi.Input[str]):
        pulumi.set(self, 'from_', value)

    @property
    @pulumi.getter
    def to(self) -> Optional[pulumi.Input[str]]:
        """
        The end date of recurrence.
        """
        return pulumi.get(self, 'to')

    @to.setter
    def to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'to', value)

@pulumi.input_type
class ExportScheduleArgs:

    def __init__(__self__, *, recurrence: Optional[pulumi.Input[Union[str, 'RecurrenceType']]]=None, recurrence_period: Optional[pulumi.Input['ExportRecurrencePeriodArgs']]=None, status: Optional[pulumi.Input[Union[str, 'StatusType']]]=None):
        """
        The schedule associated with the export.
        :param pulumi.Input[Union[str, 'RecurrenceType']] recurrence: The schedule recurrence.
        :param pulumi.Input['ExportRecurrencePeriodArgs'] recurrence_period: Has start and end date of the recurrence. The start date must be in future. If present, the end date must be greater than start date.
        :param pulumi.Input[Union[str, 'StatusType']] status: The status of the export's schedule. If 'Inactive', the export's schedule is paused.
        """
        if recurrence is not None:
            pulumi.set(__self__, 'recurrence', recurrence)
        if recurrence_period is not None:
            pulumi.set(__self__, 'recurrence_period', recurrence_period)
        if status is not None:
            pulumi.set(__self__, 'status', status)

    @property
    @pulumi.getter
    def recurrence(self) -> Optional[pulumi.Input[Union[str, 'RecurrenceType']]]:
        """
        The schedule recurrence.
        """
        return pulumi.get(self, 'recurrence')

    @recurrence.setter
    def recurrence(self, value: Optional[pulumi.Input[Union[str, 'RecurrenceType']]]):
        pulumi.set(self, 'recurrence', value)

    @property
    @pulumi.getter(name='recurrencePeriod')
    def recurrence_period(self) -> Optional[pulumi.Input['ExportRecurrencePeriodArgs']]:
        """
        Has start and end date of the recurrence. The start date must be in future. If present, the end date must be greater than start date.
        """
        return pulumi.get(self, 'recurrence_period')

    @recurrence_period.setter
    def recurrence_period(self, value: Optional[pulumi.Input['ExportRecurrencePeriodArgs']]):
        pulumi.set(self, 'recurrence_period', value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'StatusType']]]:
        """
        The status of the export's schedule. If 'Inactive', the export's schedule is paused.
        """
        return pulumi.get(self, 'status')

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'StatusType']]]):
        pulumi.set(self, 'status', value)

@pulumi.input_type
class ExportTimePeriodArgs:

    def __init__(__self__, *, from_: pulumi.Input[str], to: pulumi.Input[str]):
        """
        The date range for data in the export. This should only be specified with timeFrame set to 'Custom'. The maximum date range is 3 months.
        :param pulumi.Input[str] from_: The start date for export data.
        :param pulumi.Input[str] to: The end date for export data.
        """
        pulumi.set(__self__, 'from_', from_)
        pulumi.set(__self__, 'to', to)

    @property
    @pulumi.getter(name='from')
    def from_(self) -> pulumi.Input[str]:
        """
        The start date for export data.
        """
        return pulumi.get(self, 'from_')

    @from_.setter
    def from_(self, value: pulumi.Input[str]):
        pulumi.set(self, 'from_', value)

    @property
    @pulumi.getter
    def to(self) -> pulumi.Input[str]:
        """
        The end date for export data.
        """
        return pulumi.get(self, 'to')

    @to.setter
    def to(self, value: pulumi.Input[str]):
        pulumi.set(self, 'to', value)

@pulumi.input_type
class FileDestinationArgs:

    def __init__(__self__, *, file_formats: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'FileFormat']]]]]=None):
        """
        Destination of the view data. This is optional. Currently only CSV format is supported.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'FileFormat']]]] file_formats: Destination of the view data. Currently only CSV format is supported.
        """
        if file_formats is not None:
            pulumi.set(__self__, 'file_formats', file_formats)

    @property
    @pulumi.getter(name='fileFormats')
    def file_formats(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'FileFormat']]]]]:
        """
        Destination of the view data. Currently only CSV format is supported.
        """
        return pulumi.get(self, 'file_formats')

    @file_formats.setter
    def file_formats(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'FileFormat']]]]]):
        pulumi.set(self, 'file_formats', value)

@pulumi.input_type
class KpiPropertiesArgs:

    def __init__(__self__, *, enabled: Optional[pulumi.Input[bool]]=None, id: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[Union[str, 'KpiTypeType']]]=None):
        """
        Each KPI must contain a 'type' and 'enabled' key.
        :param pulumi.Input[bool] enabled: show the KPI in the UI?
        :param pulumi.Input[str] id: ID of resource related to metric (budget).
        :param pulumi.Input[Union[str, 'KpiTypeType']] type: KPI type (Forecast, Budget).
        """
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if id is not None:
            pulumi.set(__self__, 'id', id)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        show the KPI in the UI?
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of resource related to metric (budget).
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'KpiTypeType']]]:
        """
        KPI type (Forecast, Budget).
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'KpiTypeType']]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class NotificationPropertiesArgs:

    def __init__(__self__, *, subject: pulumi.Input[str], to: pulumi.Input[Sequence[pulumi.Input[str]]], language: Optional[pulumi.Input[str]]=None, message: Optional[pulumi.Input[str]]=None, regional_format: Optional[pulumi.Input[str]]=None):
        """
        The properties of the scheduled action notification.
        :param pulumi.Input[str] subject: Subject of the email. Length is limited to 70 characters.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] to: Array of email addresses.
        :param pulumi.Input[str] language: Locale of the email.
        :param pulumi.Input[str] message: Optional message to be added in the email. Length is limited to 250 characters.
        :param pulumi.Input[str] regional_format: Regional format used for formatting date/time and currency values in the email.
        """
        pulumi.set(__self__, 'subject', subject)
        pulumi.set(__self__, 'to', to)
        if language is not None:
            pulumi.set(__self__, 'language', language)
        if message is not None:
            pulumi.set(__self__, 'message', message)
        if regional_format is not None:
            pulumi.set(__self__, 'regional_format', regional_format)

    @property
    @pulumi.getter
    def subject(self) -> pulumi.Input[str]:
        """
        Subject of the email. Length is limited to 70 characters.
        """
        return pulumi.get(self, 'subject')

    @subject.setter
    def subject(self, value: pulumi.Input[str]):
        pulumi.set(self, 'subject', value)

    @property
    @pulumi.getter
    def to(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Array of email addresses.
        """
        return pulumi.get(self, 'to')

    @to.setter
    def to(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'to', value)

    @property
    @pulumi.getter
    def language(self) -> Optional[pulumi.Input[str]]:
        """
        Locale of the email.
        """
        return pulumi.get(self, 'language')

    @language.setter
    def language(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'language', value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Optional message to be added in the email. Length is limited to 250 characters.
        """
        return pulumi.get(self, 'message')

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'message', value)

    @property
    @pulumi.getter(name='regionalFormat')
    def regional_format(self) -> Optional[pulumi.Input[str]]:
        """
        Regional format used for formatting date/time and currency values in the email.
        """
        return pulumi.get(self, 'regional_format')

    @regional_format.setter
    def regional_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'regional_format', value)

@pulumi.input_type
class PivotPropertiesArgs:

    def __init__(__self__, *, name: Optional[pulumi.Input[str]]=None, type: Optional[pulumi.Input[Union[str, 'PivotTypeType']]]=None):
        """
        Each pivot must contain a 'type' and 'name'.
        :param pulumi.Input[str] name: Data field to show in view.
        :param pulumi.Input[Union[str, 'PivotTypeType']] type: Data type to show in view.
        """
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if type is not None:
            pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Data field to show in view.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'PivotTypeType']]]:
        """
        Data type to show in view.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'PivotTypeType']]]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class ReportConfigAggregationArgs:

    def __init__(__self__, *, function: pulumi.Input[Union[str, 'FunctionType']], name: pulumi.Input[str]):
        """
        The aggregation expression to be used in the report.
        :param pulumi.Input[Union[str, 'FunctionType']] function: The name of the aggregation function to use.
        :param pulumi.Input[str] name: The name of the column to aggregate.
        """
        pulumi.set(__self__, 'function', function)
        pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def function(self) -> pulumi.Input[Union[str, 'FunctionType']]:
        """
        The name of the aggregation function to use.
        """
        return pulumi.get(self, 'function')

    @function.setter
    def function(self, value: pulumi.Input[Union[str, 'FunctionType']]):
        pulumi.set(self, 'function', value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the column to aggregate.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

@pulumi.input_type
class ReportConfigComparisonExpressionArgs:

    def __init__(__self__, *, name: pulumi.Input[str], operator: pulumi.Input[Union[str, 'OperatorType']], values: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        The comparison expression to be used in the report.
        :param pulumi.Input[str] name: The name of the column to use in comparison.
        :param pulumi.Input[Union[str, 'OperatorType']] operator: The operator to use for comparison.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: Array of values to use for comparison
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'operator', operator)
        pulumi.set(__self__, 'values', values)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the column to use in comparison.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def operator(self) -> pulumi.Input[Union[str, 'OperatorType']]:
        """
        The operator to use for comparison.
        """
        return pulumi.get(self, 'operator')

    @operator.setter
    def operator(self, value: pulumi.Input[Union[str, 'OperatorType']]):
        pulumi.set(self, 'operator', value)

    @property
    @pulumi.getter
    def values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Array of values to use for comparison
        """
        return pulumi.get(self, 'values')

    @values.setter
    def values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, 'values', value)

@pulumi.input_type
class ReportConfigDatasetConfigurationArgs:

    def __init__(__self__, *, columns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None):
        """
        The configuration of dataset in the report.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] columns: Array of column names to be included in the report. Any valid report column name is allowed. If not provided, then report includes all columns.
        """
        if columns is not None:
            pulumi.set(__self__, 'columns', columns)

    @property
    @pulumi.getter
    def columns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of column names to be included in the report. Any valid report column name is allowed. If not provided, then report includes all columns.
        """
        return pulumi.get(self, 'columns')

    @columns.setter
    def columns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'columns', value)

@pulumi.input_type
class ReportConfigDatasetArgs:

    def __init__(__self__, *, aggregation: Optional[pulumi.Input[Mapping[str, pulumi.Input['ReportConfigAggregationArgs']]]]=None, configuration: Optional[pulumi.Input['ReportConfigDatasetConfigurationArgs']]=None, filter: Optional[pulumi.Input['ReportConfigFilterArgs']]=None, granularity: Optional[pulumi.Input[Union[str, 'ReportGranularityType']]]=None, grouping: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigGroupingArgs']]]]=None, sorting: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigSortingArgs']]]]=None):
        """
        The definition of data present in the report.
        :param pulumi.Input[Mapping[str, pulumi.Input['ReportConfigAggregationArgs']]] aggregation: Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the aggregated column. Report can have up to 2 aggregation clauses.
        :param pulumi.Input['ReportConfigDatasetConfigurationArgs'] configuration: Has configuration information for the data in the report. The configuration will be ignored if aggregation and grouping are provided.
        :param pulumi.Input['ReportConfigFilterArgs'] filter: Has filter expression to use in the report.
        :param pulumi.Input[Union[str, 'ReportGranularityType']] granularity: The granularity of rows in the report.
        :param pulumi.Input[Sequence[pulumi.Input['ReportConfigGroupingArgs']]] grouping: Array of group by expression to use in the report. Report can have up to 2 group by clauses.
        :param pulumi.Input[Sequence[pulumi.Input['ReportConfigSortingArgs']]] sorting: Array of order by expression to use in the report.
        """
        if aggregation is not None:
            pulumi.set(__self__, 'aggregation', aggregation)
        if configuration is not None:
            pulumi.set(__self__, 'configuration', configuration)
        if filter is not None:
            pulumi.set(__self__, 'filter', filter)
        if granularity is not None:
            pulumi.set(__self__, 'granularity', granularity)
        if grouping is not None:
            pulumi.set(__self__, 'grouping', grouping)
        if sorting is not None:
            pulumi.set(__self__, 'sorting', sorting)

    @property
    @pulumi.getter
    def aggregation(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ReportConfigAggregationArgs']]]]:
        """
        Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the aggregated column. Report can have up to 2 aggregation clauses.
        """
        return pulumi.get(self, 'aggregation')

    @aggregation.setter
    def aggregation(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ReportConfigAggregationArgs']]]]):
        pulumi.set(self, 'aggregation', value)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[pulumi.Input['ReportConfigDatasetConfigurationArgs']]:
        """
        Has configuration information for the data in the report. The configuration will be ignored if aggregation and grouping are provided.
        """
        return pulumi.get(self, 'configuration')

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['ReportConfigDatasetConfigurationArgs']]):
        pulumi.set(self, 'configuration', value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['ReportConfigFilterArgs']]:
        """
        Has filter expression to use in the report.
        """
        return pulumi.get(self, 'filter')

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['ReportConfigFilterArgs']]):
        pulumi.set(self, 'filter', value)

    @property
    @pulumi.getter
    def granularity(self) -> Optional[pulumi.Input[Union[str, 'ReportGranularityType']]]:
        """
        The granularity of rows in the report.
        """
        return pulumi.get(self, 'granularity')

    @granularity.setter
    def granularity(self, value: Optional[pulumi.Input[Union[str, 'ReportGranularityType']]]):
        pulumi.set(self, 'granularity', value)

    @property
    @pulumi.getter
    def grouping(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigGroupingArgs']]]]:
        """
        Array of group by expression to use in the report. Report can have up to 2 group by clauses.
        """
        return pulumi.get(self, 'grouping')

    @grouping.setter
    def grouping(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigGroupingArgs']]]]):
        pulumi.set(self, 'grouping', value)

    @property
    @pulumi.getter
    def sorting(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigSortingArgs']]]]:
        """
        Array of order by expression to use in the report.
        """
        return pulumi.get(self, 'sorting')

    @sorting.setter
    def sorting(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigSortingArgs']]]]):
        pulumi.set(self, 'sorting', value)

@pulumi.input_type
class ReportConfigFilterArgs:

    def __init__(__self__, *, and_: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]=None, dimensions: Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]=None, or_: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]=None, tags: Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]=None):
        """
        The filter expression to be used in the report.
        :param pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]] and_: The logical "AND" expression. Must have at least 2 items.
        :param pulumi.Input['ReportConfigComparisonExpressionArgs'] dimensions: Has comparison expression for a dimension
        :param pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]] or_: The logical "OR" expression. Must have at least 2 items.
        :param pulumi.Input['ReportConfigComparisonExpressionArgs'] tags: Has comparison expression for a tag
        """
        if and_ is not None:
            pulumi.set(__self__, 'and_', and_)
        if dimensions is not None:
            pulumi.set(__self__, 'dimensions', dimensions)
        if or_ is not None:
            pulumi.set(__self__, 'or_', or_)
        if tags is not None:
            pulumi.set(__self__, 'tags', tags)

    @property
    @pulumi.getter(name='and')
    def and_(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]:
        """
        The logical "AND" expression. Must have at least 2 items.
        """
        return pulumi.get(self, 'and_')

    @and_.setter
    def and_(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]):
        pulumi.set(self, 'and_', value)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]:
        """
        Has comparison expression for a dimension
        """
        return pulumi.get(self, 'dimensions')

    @dimensions.setter
    def dimensions(self, value: Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]):
        pulumi.set(self, 'dimensions', value)

    @property
    @pulumi.getter(name='or')
    def or_(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]:
        """
        The logical "OR" expression. Must have at least 2 items.
        """
        return pulumi.get(self, 'or_')

    @or_.setter
    def or_(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ReportConfigFilterArgs']]]]):
        pulumi.set(self, 'or_', value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]:
        """
        Has comparison expression for a tag
        """
        return pulumi.get(self, 'tags')

    @tags.setter
    def tags(self, value: Optional[pulumi.Input['ReportConfigComparisonExpressionArgs']]):
        pulumi.set(self, 'tags', value)

@pulumi.input_type
class ReportConfigGroupingArgs:

    def __init__(__self__, *, name: pulumi.Input[str], type: pulumi.Input[Union[str, 'QueryColumnType']]):
        """
        The group by expression to be used in the report.
        :param pulumi.Input[str] name: The name of the column to group. This version supports subscription lowest possible grain.
        :param pulumi.Input[Union[str, 'QueryColumnType']] type: Has type of the column to group.
        """
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'type', type)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the column to group. This version supports subscription lowest possible grain.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'QueryColumnType']]:
        """
        Has type of the column to group.
        """
        return pulumi.get(self, 'type')

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'QueryColumnType']]):
        pulumi.set(self, 'type', value)

@pulumi.input_type
class ReportConfigSortingArgs:

    def __init__(__self__, *, name: pulumi.Input[str], direction: Optional[pulumi.Input[Union[str, 'ReportConfigSortingType']]]=None):
        """
        The order by expression to be used in the report.
        :param pulumi.Input[str] name: The name of the column to sort.
        :param pulumi.Input[Union[str, 'ReportConfigSortingType']] direction: Direction of sort.
        """
        pulumi.set(__self__, 'name', name)
        if direction is not None:
            pulumi.set(__self__, 'direction', direction)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the column to sort.
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def direction(self) -> Optional[pulumi.Input[Union[str, 'ReportConfigSortingType']]]:
        """
        Direction of sort.
        """
        return pulumi.get(self, 'direction')

    @direction.setter
    def direction(self, value: Optional[pulumi.Input[Union[str, 'ReportConfigSortingType']]]):
        pulumi.set(self, 'direction', value)

@pulumi.input_type
class ReportConfigTimePeriodArgs:

    def __init__(__self__, *, from_: pulumi.Input[str], to: pulumi.Input[str]):
        """
        The start and end date for pulling data for the report.
        :param pulumi.Input[str] from_: The start date to pull data from.
        :param pulumi.Input[str] to: The end date to pull data to.
        """
        pulumi.set(__self__, 'from_', from_)
        pulumi.set(__self__, 'to', to)

    @property
    @pulumi.getter(name='from')
    def from_(self) -> pulumi.Input[str]:
        """
        The start date to pull data from.
        """
        return pulumi.get(self, 'from_')

    @from_.setter
    def from_(self, value: pulumi.Input[str]):
        pulumi.set(self, 'from_', value)

    @property
    @pulumi.getter
    def to(self) -> pulumi.Input[str]:
        """
        The end date to pull data to.
        """
        return pulumi.get(self, 'to')

    @to.setter
    def to(self, value: pulumi.Input[str]):
        pulumi.set(self, 'to', value)

@pulumi.input_type
class SchedulePropertiesArgs:

    def __init__(__self__, *, end_date: pulumi.Input[str], frequency: pulumi.Input[Union[str, 'ScheduleFrequency']], start_date: pulumi.Input[str], day_of_month: Optional[pulumi.Input[int]]=None, days_of_week: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DaysOfWeek']]]]]=None, hour_of_day: Optional[pulumi.Input[int]]=None, weeks_of_month: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeeksOfMonth']]]]]=None):
        """
        The properties of the schedule.
        :param pulumi.Input[str] end_date: The end date and time of the scheduled action (UTC).
        :param pulumi.Input[Union[str, 'ScheduleFrequency']] frequency: Frequency of the schedule.
        :param pulumi.Input[str] start_date: The start date and time of the scheduled action (UTC).
        :param pulumi.Input[int] day_of_month: UTC day on which cost analysis data will be emailed. Must be between 1 and 31. This property is applicable when frequency is Monthly and overrides weeksOfMonth or daysOfWeek.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'DaysOfWeek']]]] days_of_week: Day names in english on which cost analysis data will be emailed. This property is applicable when frequency is Weekly or Monthly.
        :param pulumi.Input[int] hour_of_day: UTC time at which cost analysis data will be emailed.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeeksOfMonth']]]] weeks_of_month: Weeks in which cost analysis data will be emailed. This property is applicable when frequency is Monthly and used in combination with daysOfWeek.
        """
        pulumi.set(__self__, 'end_date', end_date)
        pulumi.set(__self__, 'frequency', frequency)
        pulumi.set(__self__, 'start_date', start_date)
        if day_of_month is not None:
            pulumi.set(__self__, 'day_of_month', day_of_month)
        if days_of_week is not None:
            pulumi.set(__self__, 'days_of_week', days_of_week)
        if hour_of_day is not None:
            pulumi.set(__self__, 'hour_of_day', hour_of_day)
        if weeks_of_month is not None:
            pulumi.set(__self__, 'weeks_of_month', weeks_of_month)

    @property
    @pulumi.getter(name='endDate')
    def end_date(self) -> pulumi.Input[str]:
        """
        The end date and time of the scheduled action (UTC).
        """
        return pulumi.get(self, 'end_date')

    @end_date.setter
    def end_date(self, value: pulumi.Input[str]):
        pulumi.set(self, 'end_date', value)

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Input[Union[str, 'ScheduleFrequency']]:
        """
        Frequency of the schedule.
        """
        return pulumi.get(self, 'frequency')

    @frequency.setter
    def frequency(self, value: pulumi.Input[Union[str, 'ScheduleFrequency']]):
        pulumi.set(self, 'frequency', value)

    @property
    @pulumi.getter(name='startDate')
    def start_date(self) -> pulumi.Input[str]:
        """
        The start date and time of the scheduled action (UTC).
        """
        return pulumi.get(self, 'start_date')

    @start_date.setter
    def start_date(self, value: pulumi.Input[str]):
        pulumi.set(self, 'start_date', value)

    @property
    @pulumi.getter(name='dayOfMonth')
    def day_of_month(self) -> Optional[pulumi.Input[int]]:
        """
        UTC day on which cost analysis data will be emailed. Must be between 1 and 31. This property is applicable when frequency is Monthly and overrides weeksOfMonth or daysOfWeek.
        """
        return pulumi.get(self, 'day_of_month')

    @day_of_month.setter
    def day_of_month(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'day_of_month', value)

    @property
    @pulumi.getter(name='daysOfWeek')
    def days_of_week(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DaysOfWeek']]]]]:
        """
        Day names in english on which cost analysis data will be emailed. This property is applicable when frequency is Weekly or Monthly.
        """
        return pulumi.get(self, 'days_of_week')

    @days_of_week.setter
    def days_of_week(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DaysOfWeek']]]]]):
        pulumi.set(self, 'days_of_week', value)

    @property
    @pulumi.getter(name='hourOfDay')
    def hour_of_day(self) -> Optional[pulumi.Input[int]]:
        """
        UTC time at which cost analysis data will be emailed.
        """
        return pulumi.get(self, 'hour_of_day')

    @hour_of_day.setter
    def hour_of_day(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'hour_of_day', value)

    @property
    @pulumi.getter(name='weeksOfMonth')
    def weeks_of_month(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeeksOfMonth']]]]]:
        """
        Weeks in which cost analysis data will be emailed. This property is applicable when frequency is Monthly and used in combination with daysOfWeek.
        """
        return pulumi.get(self, 'weeks_of_month')

    @weeks_of_month.setter
    def weeks_of_month(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'WeeksOfMonth']]]]]):
        pulumi.set(self, 'weeks_of_month', value)
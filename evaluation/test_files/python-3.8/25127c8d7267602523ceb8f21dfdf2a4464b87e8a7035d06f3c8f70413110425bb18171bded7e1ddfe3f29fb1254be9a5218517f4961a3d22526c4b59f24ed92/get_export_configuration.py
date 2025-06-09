import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['GetExportConfigurationResult', 'AwaitableGetExportConfigurationResult', 'get_export_configuration', 'get_export_configuration_output']

@pulumi.output_type
class GetExportConfigurationResult:
    """
    Properties that define a Continuous Export configuration.
    """

    def __init__(__self__, application_name=None, container_name=None, destination_account_id=None, destination_storage_location_id=None, destination_storage_subscription_id=None, destination_type=None, export_id=None, export_status=None, instrumentation_key=None, is_user_enabled=None, last_gap_time=None, last_success_time=None, last_user_update=None, notification_queue_enabled=None, permanent_error_reason=None, record_types=None, resource_group=None, storage_name=None, subscription_id=None):
        if application_name and (not isinstance(application_name, str)):
            raise TypeError("Expected argument 'application_name' to be a str")
        pulumi.set(__self__, 'application_name', application_name)
        if container_name and (not isinstance(container_name, str)):
            raise TypeError("Expected argument 'container_name' to be a str")
        pulumi.set(__self__, 'container_name', container_name)
        if destination_account_id and (not isinstance(destination_account_id, str)):
            raise TypeError("Expected argument 'destination_account_id' to be a str")
        pulumi.set(__self__, 'destination_account_id', destination_account_id)
        if destination_storage_location_id and (not isinstance(destination_storage_location_id, str)):
            raise TypeError("Expected argument 'destination_storage_location_id' to be a str")
        pulumi.set(__self__, 'destination_storage_location_id', destination_storage_location_id)
        if destination_storage_subscription_id and (not isinstance(destination_storage_subscription_id, str)):
            raise TypeError("Expected argument 'destination_storage_subscription_id' to be a str")
        pulumi.set(__self__, 'destination_storage_subscription_id', destination_storage_subscription_id)
        if destination_type and (not isinstance(destination_type, str)):
            raise TypeError("Expected argument 'destination_type' to be a str")
        pulumi.set(__self__, 'destination_type', destination_type)
        if export_id and (not isinstance(export_id, str)):
            raise TypeError("Expected argument 'export_id' to be a str")
        pulumi.set(__self__, 'export_id', export_id)
        if export_status and (not isinstance(export_status, str)):
            raise TypeError("Expected argument 'export_status' to be a str")
        pulumi.set(__self__, 'export_status', export_status)
        if instrumentation_key and (not isinstance(instrumentation_key, str)):
            raise TypeError("Expected argument 'instrumentation_key' to be a str")
        pulumi.set(__self__, 'instrumentation_key', instrumentation_key)
        if is_user_enabled and (not isinstance(is_user_enabled, str)):
            raise TypeError("Expected argument 'is_user_enabled' to be a str")
        pulumi.set(__self__, 'is_user_enabled', is_user_enabled)
        if last_gap_time and (not isinstance(last_gap_time, str)):
            raise TypeError("Expected argument 'last_gap_time' to be a str")
        pulumi.set(__self__, 'last_gap_time', last_gap_time)
        if last_success_time and (not isinstance(last_success_time, str)):
            raise TypeError("Expected argument 'last_success_time' to be a str")
        pulumi.set(__self__, 'last_success_time', last_success_time)
        if last_user_update and (not isinstance(last_user_update, str)):
            raise TypeError("Expected argument 'last_user_update' to be a str")
        pulumi.set(__self__, 'last_user_update', last_user_update)
        if notification_queue_enabled and (not isinstance(notification_queue_enabled, str)):
            raise TypeError("Expected argument 'notification_queue_enabled' to be a str")
        pulumi.set(__self__, 'notification_queue_enabled', notification_queue_enabled)
        if permanent_error_reason and (not isinstance(permanent_error_reason, str)):
            raise TypeError("Expected argument 'permanent_error_reason' to be a str")
        pulumi.set(__self__, 'permanent_error_reason', permanent_error_reason)
        if record_types and (not isinstance(record_types, str)):
            raise TypeError("Expected argument 'record_types' to be a str")
        pulumi.set(__self__, 'record_types', record_types)
        if resource_group and (not isinstance(resource_group, str)):
            raise TypeError("Expected argument 'resource_group' to be a str")
        pulumi.set(__self__, 'resource_group', resource_group)
        if storage_name and (not isinstance(storage_name, str)):
            raise TypeError("Expected argument 'storage_name' to be a str")
        pulumi.set(__self__, 'storage_name', storage_name)
        if subscription_id and (not isinstance(subscription_id, str)):
            raise TypeError("Expected argument 'subscription_id' to be a str")
        pulumi.set(__self__, 'subscription_id', subscription_id)

    @property
    @pulumi.getter(name='applicationName')
    def application_name(self) -> str:
        """
        The name of the Application Insights component.
        """
        return pulumi.get(self, 'application_name')

    @property
    @pulumi.getter(name='containerName')
    def container_name(self) -> str:
        """
        The name of the destination storage container.
        """
        return pulumi.get(self, 'container_name')

    @property
    @pulumi.getter(name='destinationAccountId')
    def destination_account_id(self) -> str:
        """
        The name of destination account.
        """
        return pulumi.get(self, 'destination_account_id')

    @property
    @pulumi.getter(name='destinationStorageLocationId')
    def destination_storage_location_id(self) -> str:
        """
        The destination account location ID.
        """
        return pulumi.get(self, 'destination_storage_location_id')

    @property
    @pulumi.getter(name='destinationStorageSubscriptionId')
    def destination_storage_subscription_id(self) -> str:
        """
        The destination storage account subscription ID.
        """
        return pulumi.get(self, 'destination_storage_subscription_id')

    @property
    @pulumi.getter(name='destinationType')
    def destination_type(self) -> str:
        """
        The destination type.
        """
        return pulumi.get(self, 'destination_type')

    @property
    @pulumi.getter(name='exportId')
    def export_id(self) -> str:
        """
        The unique ID of the export configuration inside an Application Insights component. It is auto generated when the Continuous Export configuration is created.
        """
        return pulumi.get(self, 'export_id')

    @property
    @pulumi.getter(name='exportStatus')
    def export_status(self) -> str:
        """
        This indicates current Continuous Export configuration status. The possible values are 'Preparing', 'Success', 'Failure'.
        """
        return pulumi.get(self, 'export_status')

    @property
    @pulumi.getter(name='instrumentationKey')
    def instrumentation_key(self) -> str:
        """
        The instrumentation key of the Application Insights component.
        """
        return pulumi.get(self, 'instrumentation_key')

    @property
    @pulumi.getter(name='isUserEnabled')
    def is_user_enabled(self) -> str:
        """
        This will be 'true' if the Continuous Export configuration is enabled, otherwise it will be 'false'.
        """
        return pulumi.get(self, 'is_user_enabled')

    @property
    @pulumi.getter(name='lastGapTime')
    def last_gap_time(self) -> str:
        """
        The last time the Continuous Export configuration started failing.
        """
        return pulumi.get(self, 'last_gap_time')

    @property
    @pulumi.getter(name='lastSuccessTime')
    def last_success_time(self) -> str:
        """
        The last time data was successfully delivered to the destination storage container for this Continuous Export configuration.
        """
        return pulumi.get(self, 'last_success_time')

    @property
    @pulumi.getter(name='lastUserUpdate')
    def last_user_update(self) -> str:
        """
        Last time the Continuous Export configuration was updated.
        """
        return pulumi.get(self, 'last_user_update')

    @property
    @pulumi.getter(name='notificationQueueEnabled')
    def notification_queue_enabled(self) -> Optional[str]:
        """
        Deprecated
        """
        return pulumi.get(self, 'notification_queue_enabled')

    @property
    @pulumi.getter(name='permanentErrorReason')
    def permanent_error_reason(self) -> str:
        """
        This is the reason the Continuous Export configuration started failing. It can be 'AzureStorageNotFound' or 'AzureStorageAccessDenied'.
        """
        return pulumi.get(self, 'permanent_error_reason')

    @property
    @pulumi.getter(name='recordTypes')
    def record_types(self) -> Optional[str]:
        """
        This comma separated list of document types that will be exported. The possible values include 'Requests', 'Event', 'Exceptions', 'Metrics', 'PageViews', 'PageViewPerformance', 'Rdd', 'PerformanceCounters', 'Availability', 'Messages'.
        """
        return pulumi.get(self, 'record_types')

    @property
    @pulumi.getter(name='resourceGroup')
    def resource_group(self) -> str:
        """
        The resource group of the Application Insights component.
        """
        return pulumi.get(self, 'resource_group')

    @property
    @pulumi.getter(name='storageName')
    def storage_name(self) -> str:
        """
        The name of the destination storage account.
        """
        return pulumi.get(self, 'storage_name')

    @property
    @pulumi.getter(name='subscriptionId')
    def subscription_id(self) -> str:
        """
        The subscription of the Application Insights component.
        """
        return pulumi.get(self, 'subscription_id')

class AwaitableGetExportConfigurationResult(GetExportConfigurationResult):

    def __await__(self):
        if False:
            yield self
        return GetExportConfigurationResult(application_name=self.application_name, container_name=self.container_name, destination_account_id=self.destination_account_id, destination_storage_location_id=self.destination_storage_location_id, destination_storage_subscription_id=self.destination_storage_subscription_id, destination_type=self.destination_type, export_id=self.export_id, export_status=self.export_status, instrumentation_key=self.instrumentation_key, is_user_enabled=self.is_user_enabled, last_gap_time=self.last_gap_time, last_success_time=self.last_success_time, last_user_update=self.last_user_update, notification_queue_enabled=self.notification_queue_enabled, permanent_error_reason=self.permanent_error_reason, record_types=self.record_types, resource_group=self.resource_group, storage_name=self.storage_name, subscription_id=self.subscription_id)

def get_export_configuration(export_id: Optional[str]=None, resource_group_name: Optional[str]=None, resource_name: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetExportConfigurationResult:
    """
    Properties that define a Continuous Export configuration.
    API Version: 2015-05-01.


    :param str export_id: The Continuous Export configuration ID. This is unique within a Application Insights component.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the Application Insights component resource.
    """
    __args__ = dict()
    __args__['exportId'] = export_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:insights:getExportConfiguration', __args__, opts=opts, typ=GetExportConfigurationResult).value
    return AwaitableGetExportConfigurationResult(application_name=__ret__.application_name, container_name=__ret__.container_name, destination_account_id=__ret__.destination_account_id, destination_storage_location_id=__ret__.destination_storage_location_id, destination_storage_subscription_id=__ret__.destination_storage_subscription_id, destination_type=__ret__.destination_type, export_id=__ret__.export_id, export_status=__ret__.export_status, instrumentation_key=__ret__.instrumentation_key, is_user_enabled=__ret__.is_user_enabled, last_gap_time=__ret__.last_gap_time, last_success_time=__ret__.last_success_time, last_user_update=__ret__.last_user_update, notification_queue_enabled=__ret__.notification_queue_enabled, permanent_error_reason=__ret__.permanent_error_reason, record_types=__ret__.record_types, resource_group=__ret__.resource_group, storage_name=__ret__.storage_name, subscription_id=__ret__.subscription_id)

@_utilities.lift_output_func(get_export_configuration)
def get_export_configuration_output(export_id: Optional[pulumi.Input[str]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, resource_name: Optional[pulumi.Input[str]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetExportConfigurationResult]:
    """
    Properties that define a Continuous Export configuration.
    API Version: 2015-05-01.


    :param str export_id: The Continuous Export configuration ID. This is unique within a Application Insights component.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the Application Insights component resource.
    """
    ...
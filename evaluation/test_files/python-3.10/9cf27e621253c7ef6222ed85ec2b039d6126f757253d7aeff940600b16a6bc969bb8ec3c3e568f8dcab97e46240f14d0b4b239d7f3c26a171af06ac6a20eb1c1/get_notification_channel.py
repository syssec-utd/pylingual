import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
__all__ = ['GetNotificationChannelResult', 'AwaitableGetNotificationChannelResult', 'get_notification_channel', 'get_notification_channel_output']

@pulumi.output_type
class GetNotificationChannelResult:

    def __init__(__self__, creation_record=None, description=None, display_name=None, enabled=None, labels=None, mutation_records=None, name=None, type=None, user_labels=None, verification_status=None):
        if creation_record and (not isinstance(creation_record, dict)):
            raise TypeError("Expected argument 'creation_record' to be a dict")
        pulumi.set(__self__, 'creation_record', creation_record)
        if description and (not isinstance(description, str)):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, 'description', description)
        if display_name and (not isinstance(display_name, str)):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, 'display_name', display_name)
        if enabled and (not isinstance(enabled, bool)):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, 'enabled', enabled)
        if labels and (not isinstance(labels, dict)):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, 'labels', labels)
        if mutation_records and (not isinstance(mutation_records, list)):
            raise TypeError("Expected argument 'mutation_records' to be a list")
        pulumi.set(__self__, 'mutation_records', mutation_records)
        if name and (not isinstance(name, str)):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, 'name', name)
        if type and (not isinstance(type, str)):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, 'type', type)
        if user_labels and (not isinstance(user_labels, dict)):
            raise TypeError("Expected argument 'user_labels' to be a dict")
        pulumi.set(__self__, 'user_labels', user_labels)
        if verification_status and (not isinstance(verification_status, str)):
            raise TypeError("Expected argument 'verification_status' to be a str")
        pulumi.set(__self__, 'verification_status', verification_status)

    @property
    @pulumi.getter(name='creationRecord')
    def creation_record(self) -> 'outputs.MutationRecordResponse':
        """
        Record of the creation of this channel.
        """
        return pulumi.get(self, 'creation_record')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional human-readable description of this notification channel. This description may provide additional details, beyond the display name, for the channel. This may not exceed 1024 Unicode characters.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        An optional human-readable name for this notification channel. It is recommended that you specify a non-empty and unique name in order to make it easier to identify the channels in your project, though this is not enforced. The display name is limited to 512 Unicode characters.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Whether notifications are forwarded to the described channel. This makes it possible to disable delivery of notifications to a particular channel without removing the channel from all alerting policies that reference the channel. This is a more convenient approach when the change is temporary and you want to receive notifications from the same set of alerting policies on the channel at some point in the future.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Configuration fields that define the channel and its behavior. The permissible and required labels are specified in the NotificationChannelDescriptor.labels of the NotificationChannelDescriptor corresponding to the type field.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter(name='mutationRecords')
    def mutation_records(self) -> Sequence['outputs.MutationRecordResponse']:
        """
        Records of the modification of this channel.
        """
        return pulumi.get(self, 'mutation_records')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The full REST resource name for this channel. The format is: projects/[PROJECT_ID_OR_NUMBER]/notificationChannels/[CHANNEL_ID] The [CHANNEL_ID] is automatically assigned by the server on creation.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the notification channel. This field matches the value of the NotificationChannelDescriptor.type field.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='userLabels')
    def user_labels(self) -> Mapping[str, str]:
        """
        User-supplied key/value data that does not need to conform to the corresponding NotificationChannelDescriptor's schema, unlike the labels field. This field is intended to be used for organizing and identifying the NotificationChannel objects.The field can contain up to 64 entries. Each key and value is limited to 63 Unicode characters or 128 bytes, whichever is smaller. Labels and values can contain only lowercase letters, numerals, underscores, and dashes. Keys must begin with a letter.
        """
        return pulumi.get(self, 'user_labels')

    @property
    @pulumi.getter(name='verificationStatus')
    def verification_status(self) -> str:
        """
        Indicates whether this channel has been verified or not. On a ListNotificationChannels or GetNotificationChannel operation, this field is expected to be populated.If the value is UNVERIFIED, then it indicates that the channel is non-functioning (it both requires verification and lacks verification); otherwise, it is assumed that the channel works.If the channel is neither VERIFIED nor UNVERIFIED, it implies that the channel is of a type that does not require verification or that this specific channel has been exempted from verification because it was created prior to verification being required for channels of this type.This field cannot be modified using a standard UpdateNotificationChannel operation. To change the value of this field, you must call VerifyNotificationChannel.
        """
        return pulumi.get(self, 'verification_status')

class AwaitableGetNotificationChannelResult(GetNotificationChannelResult):

    def __await__(self):
        if False:
            yield self
        return GetNotificationChannelResult(creation_record=self.creation_record, description=self.description, display_name=self.display_name, enabled=self.enabled, labels=self.labels, mutation_records=self.mutation_records, name=self.name, type=self.type, user_labels=self.user_labels, verification_status=self.verification_status)

def get_notification_channel(notification_channel_id: Optional[str]=None, project: Optional[str]=None, opts: Optional[pulumi.InvokeOptions]=None) -> AwaitableGetNotificationChannelResult:
    """
    Gets a single notification channel. The channel includes the relevant configuration details with which the channel was created. However, the response may truncate or omit passwords, API keys, or other private key matter and thus the response may not be 100% identical to the information that was supplied in the call to the create method.
    """
    __args__ = dict()
    __args__['notificationChannelId'] = notification_channel_id
    __args__['project'] = project
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('google-native:monitoring/v3:getNotificationChannel', __args__, opts=opts, typ=GetNotificationChannelResult).value
    return AwaitableGetNotificationChannelResult(creation_record=__ret__.creation_record, description=__ret__.description, display_name=__ret__.display_name, enabled=__ret__.enabled, labels=__ret__.labels, mutation_records=__ret__.mutation_records, name=__ret__.name, type=__ret__.type, user_labels=__ret__.user_labels, verification_status=__ret__.verification_status)

@_utilities.lift_output_func(get_notification_channel)
def get_notification_channel_output(notification_channel_id: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[Optional[str]]]=None, opts: Optional[pulumi.InvokeOptions]=None) -> pulumi.Output[GetNotificationChannelResult]:
    """
    Gets a single notification channel. The channel includes the relevant configuration details with which the channel was created. However, the response may truncate or omit passwords, API keys, or other private key matter and thus the response may not be 100% identical to the information that was supplied in the call to the create method.
    """
    ...
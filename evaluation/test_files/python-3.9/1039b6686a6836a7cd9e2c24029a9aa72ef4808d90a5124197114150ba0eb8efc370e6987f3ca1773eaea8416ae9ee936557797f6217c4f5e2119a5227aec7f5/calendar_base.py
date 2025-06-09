import datetime
import logging
from typing import List, Optional, Set, Tuple, Union
from . import constants
from .enums import AppointmentAuxilaryFlag, AppointmentColor, AppointmentStateFlag, BusyStatus, IconIndex, MeetingRecipientType, ResponseStatus
from .message_base import MessageBase
from .structures.entry_id import EntryID
from .structures.misc_id import GlobalObjectID
from .structures.recurrence_pattern import RecurrencePattern
from .structures.time_zone_definition import TimeZoneDefinition
from .structures.time_zone_struct import TimeZoneStruct
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class CalendarBase(MessageBase):
    """
    Common base for all Appointment and Meeting objects.
    """

    def _genRecipient(self, recipientType, recipientInt: MeetingRecipientType) -> Optional[str]:
        """
        Returns the specified recipient field.
        """
        private = '_' + recipientType
        recipientInt = MeetingRecipientType(recipientInt)
        try:
            return getattr(self, private)
        except AttributeError:
            value = None
            if self.headerInit():
                value = self.header[recipientType]
                if value:
                    value = value.replace(',', self.recipientSeparator)
            if not value:
                if self.headerInit():
                    logger.info(f'Header found, but "{recipientType}" is not included. Will be generated from other streams.')
                foundRecipients = tuple((recipient.formatted for recipient in self.recipients if recipient.type == recipientInt))
                if len(foundRecipients) > 0:
                    value = (self.recipientSeparator + ' ').join(foundRecipients)
            if value:
                value = value.replace(' \r\n\t', ' ').replace('\r\n\t ', ' ').replace('\r\n\t', ' ')
                value = value.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
                while value.find('  ') != -1:
                    value = value.replace('  ', ' ')
            setattr(self, private, value)
            return value

    @property
    def allAttendeesString(self) -> Optional[str]:
        """
        A list of all attendees, excluding the organizer.
        """
        return self._ensureSetNamed('_allAttendeesString', '8238', constants.PSETID_APPOINTMENT)

    @property
    def appointmentAuxilaryFlags(self) -> Optional[Set[AppointmentAuxilaryFlag]]:
        """
        The auxiliary state of the object.
        """
        return self._ensureSetNamed('_appointmentAuxilaryFlags', '8207', constants.PSETID_APPOINTMENT, overrideClass=AppointmentAuxilaryFlag.fromBits)

    @property
    def appointmentColor(self) -> Optional[AppointmentColor]:
        """
        The color to be used when displaying a Calendar object.
        """
        return self._ensureSetNamed('_appointmentColor', '8214', constants.PSETID_APPOINTMENT, overrideClass=AppointmentColor)

    @property
    def appointmentDuration(self) -> Optional[int]:
        """
        The length of the event, in minutes.
        """
        return self._ensureSetNamed('_appointmentDuration', '8213', constants.PSETID_APPOINTMENT)

    @property
    def appointmentEndWhole(self) -> Optional[datetime.datetime]:
        """
        The end date and time of the event in UTC.
        """
        return self._ensureSetNamed('_appointmentEndWhole', '820E', constants.PSETID_APPOINTMENT)

    @property
    def appointmentNotAllowPropose(self) -> bool:
        """
        Indicates that attendees are not allowed to propose a new date and/or
        time for the meeting if True.
        """
        return self._ensureSetNamed('_appointmentNotAllowPropose', '8259', constants.PSETID_APPOINTMENT, overrideClass=bool, preserveNone=False)

    @property
    def appointmentRecur(self) -> Optional[RecurrencePattern]:
        """
        Specifies the dates and times when a recurring series occurs by using
        one of the recurrence patterns and ranges specified in this section.
        """
        return self._ensureSetNamed('_appointmentRecur', '8216', constants.PSETID_APPOINTMENT, overrideClass=RecurrencePattern)

    @property
    def appointmentSequence(self) -> Optional[int]:
        """
        Specified the sequence number of a Meeting object. A meeting object
        begins with the sequence number set to 0 and is incremented each time
        the organizer sends out a Meeting Update object.
        """
        return self._ensureSetNamed('_appointmentSequence', '8201', constants.PSETID_APPOINTMENT)

    @property
    def appointmentStartWhole(self) -> Optional[datetime.datetime]:
        """
        The start date and time of the event in UTC.
        """
        return self._ensureSetNamed('_appointmentStartWhole', '820D', constants.PSETID_APPOINTMENT)

    @property
    def appointmentStateFlags(self) -> Optional[Set[AppointmentStateFlag]]:
        """
        The appointment state of the object.
        """
        return self._ensureSetNamed('_appointmentStateFlags', '8217', constants.PSETID_APPOINTMENT, overrideClass=AppointmentStateFlag.fromBits)

    @property
    def appointmentSubType(self) -> bool:
        """
        Whether the event is an all-day event or not.
        """
        return self._ensureSetNamed('_appointmentSubType', '8215', constants.PSETID_APPOINTMENT, overrideClass=bool, preserveNone=False)

    @property
    def appointmentTimeZoneDefinitionEndDisplay(self) -> Optional[TimeZoneDefinition]:
        """
        Specifies the time zone information for the appointmentEndWhole property
        Used to convert the end date and time to and from UTC.
        """
        return self._ensureSetNamed('_appointmentTimeZoneDefinitionEndDisplay', '825F', constants.PSETID_APPOINTMENT, overrideClass=TimeZoneDefinition)

    @property
    def appointmentTimeZoneDefinitionRecur(self) -> Optional[TimeZoneDefinition]:
        """
        Specified the time zone information that specifies how to convert the
        meeting date and time on a recurring series to and from UTC.
        """
        return self._ensureSetNamed('_appointmentTimeZoneDefinitionRecur', '8260', constants.PSETID_APPOINTMENT, overrideClass=TimeZoneDefinition)

    @property
    def appointmentTimeZoneDefinitionStartDisplay(self) -> Optional[TimeZoneDefinition]:
        """
        Specifies the time zone information for the appointmentStartWhole
        property. Used to convert the start date and time to and from UTC.
        """
        return self._ensureSetNamed('_appointmentTimeZoneDefinitionStartDisplay', '825E', constants.PSETID_APPOINTMENT, overrideClass=TimeZoneDefinition)

    @property
    def appointmentUnsendableRecipients(self) -> Optional[bytes]:
        """
        A list of unsendable attendees.

        I want to return the structure parsed, but my one example does not match
        the specifications. If you have examples, let me know and I can ask you
        to run a verification on it.
        """
        return self._ensureSetNamed('_appointmentUnsendableRecipients', '825D', constants.PSETID_APPOINTMENT)

    @property
    def bcc(self) -> Optional[str]:
        """
        Returns the bcc field, if it exists.
        """
        return self._genRecipient('bcc', MeetingRecipientType.SENDABLE_RESOURCE_OBJECT)

    @property
    def birthdayContactAttributionDisplayName(self) -> Optional[str]:
        """
        Indicated the name of the contact associated with the birthday event.
        """
        return self._ensureSetNamed('_birthdayContactAttributionDisplayName', 'BirthdayContactAttributionDisplayName', constants.PSETID_ADDRESS)

    @property
    def birthdayContactEntryID(self) -> Optional[EntryID]:
        """
        Indicates the EntryID of the contact associated with the birthday event.
        """
        return self._ensureSetNamed('_birthdayContactEntryID', 'BirthdayContactEntryId', constants.PSETID_ADDRESS, overrideClass=EntryID.autoCreate)

    @property
    def birthdayContactPersonGuid(self) -> Optional[bytes]:
        """
        Indicates the person ID's GUID of the contact associated with the
        birthday event.
        """
        return self._ensureSetNamed('_birthdayContactPersonGuid', 'BirthdayContactPersonGuid', constants.PSETID_ADDRESS)

    @property
    def busyStatus(self) -> Optional[BusyStatus]:
        """
        Specified the availability of a user for the event described by the
        object.
        """
        return self._ensureSetNamed('_busyStatus', '8205', constants.PSETID_APPOINTMENT, overrideClass=BusyStatus)

    @property
    def cc(self) -> Optional[str]:
        """
        Returns the cc field, if it exists.
        """
        return self._genRecipient('cc', MeetingRecipientType.SENDABLE_OPTIONAL_ATTENDEE)

    @property
    def ccAttendeesString(self) -> Optional[str]:
        """
        A list of all the sendable attendees, who are also optional attendees.
        """
        return self._ensureSetNamed('_ccAttendeesString', '823C', constants.PSETID_APPOINTMENT)

    @property
    def cleanGlobalObjectID(self) -> Optional[GlobalObjectID]:
        """
        The value of the globalObjectID property for an object that represents
        an Exception object to a recurring series, where the year, month, and
        day fields are all 0.
        """
        return self._ensureSetNamed('_cleanGlobalObjectID', '0023', constants.PSETID_MEETING, overrideClass=GlobalObjectID)

    @property
    def clipEnd(self) -> Optional[datetime.datetime]:
        """
        For single-instance Calendar objects, the end date and time of the
        event in UTC. For a recurring series, midnight in the user's machine
        time zone, on the date of the last instance, then is persisted in UTC,
        unless the recurring series has no end, in which case the value MUST be
        "31 August 4500 11:49 PM".

        Honestly, not sure what this is. [MS-OXOCAL]: PidLidClipEnd.
        """
        return self._ensureSetNamed('_clipEnd', '8236', constants.PSETID_APPOINTMENT)

    @property
    def clipStart(self) -> Optional[datetime.datetime]:
        """
        For single-instance Calendar objects, the start date and time of the
        event in UTC. For a recurring series, midnight in the user's machine
        time zone, on the date of the first instance, then is persisted in UTC.

        Honestly, not sure what this is. [MS-OXOCAL]: PidLidClipStart.
        """
        return self._ensureSetNamed('_clipStart', '8235', constants.PSETID_APPOINTMENT)

    @property
    def commonEnd(self) -> Optional[datetime.datetime]:
        """
        The end date and time of an event. MUST be equal to appointmentEndWhole.
        """
        return self._ensureSetNamed('_commonEnd', '8517', constants.PSETID_COMMON)

    @property
    def commonStart(self) -> Optional[datetime.datetime]:
        """
        The start date and time of an event. MUST be equal to
        appointmentStartWhole.
        """
        return self._ensureSetNamed('_commonStart', '8516', constants.PSETID_COMMON)

    @property
    def endDate(self) -> Optional[datetime.datetime]:
        """
        The end date of the appointment.
        """
        return self._ensureSetProperty('_endDate', '00610040')

    @property
    def globalObjectID(self) -> Optional[GlobalObjectID]:
        """
        The unique identifier or the Calendar object.
        """
        return self._ensureSetNamed('_globalObjectID', '0003', constants.PSETID_MEETING, overrideClass=GlobalObjectID)

    @property
    def iconIndex(self) -> Optional[Union[IconIndex, int]]:
        """
        The icon to use for the object.
        """
        return self._ensureSetProperty('_iconIndex', '10800003', overrideClass=IconIndex.tryMake)

    @property
    def isBirthdayContactWritable(self) -> bool:
        """
        Indicates whether the contact associated with the birthday event is
        writable.
        """
        return self._ensureSetNamed('_isBirthdayContactWritable', 'IsBirthdayContactWritable', constants.PSETID_ADDRESS, overrideClass=bool, preserveNone=False)

    @property
    def isException(self) -> bool:
        """
        Whether the object represents an exception. False indicates that the
        object represents a recurring series or a single-instance object.
        """
        return self._ensureSetNamed('_isException', '000A', constants.PSETID_MEETING, overrideClass=bool, preserveNone=False)

    @property
    def isRecurring(self) -> bool:
        """
        Whether the object is associated with a recurring series.
        """
        return self._ensureSetNamed('_isRecurring', '0005', constants.PSETID_MEETING, overrideClass=bool, preserveNone=False)

    @property
    def keywords(self) -> Optional[List[str]]:
        """
        The color to be used when displaying a Calendar object.
        """
        return self._ensureSet('_keywords', 'Keywords')

    @property
    def linkedTaskItems(self) -> Optional[Tuple[EntryID]]:
        """
        A list of PidTagEntryId properties of Task objects related to the
        Calendar object that are set by a client.
        """
        return self._ensureSetNamed('_linkedTaskItems', '820C', constants.PSETID_APPOINTMENT, overrideClass=lambda x: tuple((EntryID.autoCreate(y) for y in x)))

    @property
    def location(self) -> Optional[str]:
        """
        Returns the location of the meeting.
        """
        return self._ensureSetNamed('_location', '8208', constants.PSETID_APPOINTMENT)

    @property
    def meetingDoNotForward(self) -> bool:
        """
        Whether to allow the meeting to be forwarded. True disallows forwarding.
        """
        return self._ensureSetNamed('_meetingDoNotForward', 'DoNotForward', constants.PS_PUBLIC_STRINGS, overrideClass=bool, preserveNone=False)

    @property
    def meetingWorkspaceUrl(self) -> Optional[str]:
        """
        The URL of the Meeting Workspace, as specified in [MS-MEETS], that is
        associated with a Calendar object.
        """
        return self._ensureSetNamed('_meetingWorkspaceUrl', '8209', constants.PSETID_APPOINTMENT)

    @property
    def nonSendableBcc(self) -> Optional[str]:
        """
        A list of all unsendable attendees who are also resource objects.
        """
        return self._ensureSetNamed('_nonSendableBcc', '8538', constants.PSETID_COMMON)

    @property
    def nonSendableCc(self) -> Optional[str]:
        """
        A list of all unsendable attendees who are also optional attendees.
        """
        return self._ensureSetNamed('_nonSendableCc', '8537', constants.PSETID_COMMON)

    @property
    def nonSendableTo(self) -> Optional[str]:
        """
        A list of all unsendable attendees who are also required attendees.
        """
        return self._ensureSetNamed('_nonSendableTo', '8536', constants.PSETID_COMMON)

    @property
    def nonSendBccTrackStatus(self) -> Optional[List[ResponseStatus]]:
        """
        A ResponseStatus for each of the attendees in nonSendableBcc.
        """
        return self._ensureSetNamed('_nonSendBccTrackStatus', '8545', constants.PSETID_COMMON, overrideClass=lambda x: (ResponseStatus(y) for y in x))

    @property
    def nonSendCcTrackStatus(self) -> Optional[List[ResponseStatus]]:
        """
        A ResponseStatus for each of the attendees in nonSendableCc.
        """
        return self._ensureSetNamed('_nonSendCcTrackStatus', '8544', constants.PSETID_COMMON, overrideClass=lambda x: (ResponseStatus(y) for y in x))

    @property
    def nonSendToTrackStatus(self) -> Optional[List[ResponseStatus]]:
        """
        A ResponseStatus for each of the attendees in nonSendableTo.
        """
        return self._ensureSetNamed('_nonSendToTrackStatus', '8543', constants.PSETID_COMMON, overrideClass=lambda x: (ResponseStatus(y) for y in x))

    @property
    def optionalAttendees(self) -> Optional[str]:
        """
        Returns the optional attendees of the meeting.
        """
        return self._ensureSetNamed('_optionalAttendees', '0007', constants.PSETID_MEETING)

    @property
    def organizer(self) -> Optional[str]:
        """
        The meeting organizer.
        """
        return self._ensureSet('_organizer', '__substg1.0_0042')

    @property
    def ownerAppointmentID(self) -> Optional[int]:
        """
        A quasi-unique value amond all Calendar objects in a user's mailbox.
        Assists a client or server in finding a Calendar object but is not
        guarenteed to be unique amoung all objects.
        """
        return self._ensureSetProperty('_ownerAppointmentID', '00620003')

    @property
    def ownerCriticalChange(self) -> Optional[datetime.datetime]:
        """
        The date and time at which a Meeting Request object was sent by the
        organizer, in UTC.
        """
        return self._ensureSetNamed('_ownerCriticalChange', '001A', constants.PSETID_MEETING)

    @property
    def recurrencePattern(self) -> Optional[str]:
        """
        A description of the recurrence specified by the appointmentRecur
        property.
        """
        return self._ensureSetNamed('_recurrencePattern', '8232', constants.PSETID_APPOINTMENT)

    @property
    def recurring(self) -> bool:
        """
        Specifies whether the object represents a recurring series.
        """
        return self._ensureSetNamed('_recurring', '8223', constants.PSETID_APPOINTMENT, overrideClass=bool, preserveNone=True)

    @property
    def replyRequested(self) -> bool:
        """
        Whether the organizer requests a reply from attendees.
        """
        return self._ensureSetProperty('_replyRequested', '0C17000B', overrideClass=bool, preserveNone=False)

    @property
    def requiredAttendees(self) -> Optional[str]:
        """
        Returns the required attendees of the meeting.
        """
        return self._ensureSetNamed('_requiredAttendees', '0006', constants.PSETID_MEETING)

    @property
    def resourceAttendees(self) -> Optional[str]:
        """
        Returns the resource attendees of the meeting.
        """
        return self._ensureSetNamed('_resourceAttendees', '0008', constants.PSETID_MEETING)

    @property
    def responseRequested(self) -> bool:
        """
        Whether to send Meeting Response objects to the organizer.
        """
        return self._ensureSetProperty('_responseRequested', '0063000B', overrideClass=bool, preserveNone=False)

    @property
    def responseStatus(self) -> ResponseStatus:
        """
        The response status of an attendee.
        """
        return self._ensureSetNamed('_responseStatus', '8218', constants.PSETID_APPOINTMENT, overrideClass=lambda x: ResponseStatus(x or 0), preserveNone=False)

    @property
    def startDate(self) -> Optional[datetime.datetime]:
        """
        The start date of the appointment.
        """
        return self._ensureSetProperty('_startDate', '00600040')

    @property
    def timeZoneDescription(self) -> Optional[str]:
        """
        A human-readable description of the time zone that is represented by the
        data in the timeZoneStruct property.
        """
        return self._ensureSetNamed('_timeZoneDescription', '8234', constants.PSETID_APPOINTMENT)

    @property
    def timeZoneStruct(self) -> Optional[TimeZoneStruct]:
        """
        Set on a recurring series to specify time zone information. Specifies
        how to convert time fields between local time and UTC.
        """
        return self._ensureSetNamed('_timeZoneStruct', '8233', constants.PSETID_APPOINTMENT, overrideClass=TimeZoneStruct)

    @property
    def to(self) -> Optional[str]:
        """
        Returns the to field, if it exists.
        """
        return self._genRecipient('to', MeetingRecipientType.SENDABLE_REQUIRED_ATTENDEE)

    @property
    def toAttendeesString(self) -> Optional[str]:
        """
        A list of all the sendable attendees, who are also required attendees.
        """
        return self._ensureSetNamed('_toAttendeesString', '823B', constants.PSETID_APPOINTMENT)
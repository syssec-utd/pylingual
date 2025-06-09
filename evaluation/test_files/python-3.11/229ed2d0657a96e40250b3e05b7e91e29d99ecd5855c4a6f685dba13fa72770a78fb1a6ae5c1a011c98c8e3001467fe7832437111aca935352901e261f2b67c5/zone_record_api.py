from __future__ import absolute_import, division, print_function
__metaclass__ = type
import abc
from ansible.module_utils import six
from ansible_collections.community.dns.plugins.module_utils.zone import DNSZoneWithRecords

class DNSAPIError(Exception):
    pass

class DNSAPIAuthenticationError(DNSAPIError):
    pass

class NotProvidedType(object):
    pass
NOT_PROVIDED = NotProvidedType()

@six.add_metaclass(abc.ABCMeta)
class ZoneRecordAPI(object):

    @abc.abstractmethod
    def get_zone_by_name(self, name):
        """
        Given a zone name, return the zone contents if found.

        @param name: The zone name (string)
        @return The zone information (DNSZone), or None if not found
        """

    @abc.abstractmethod
    def get_zone_by_id(self, id):
        """
        Given a zone ID, return the zone contents if found.

        @param id: The zone ID
        @return The zone information (DNSZone), or None if not found
        """

    def get_zone_with_records_by_name(self, name, prefix=NOT_PROVIDED, record_type=NOT_PROVIDED):
        """
        Given a zone name, return the zone contents with records if found.

        @param name: The zone name (string)
        @param prefix: The prefix to filter for, if provided. Since None is a valid value,
                       the special constant NOT_PROVIDED indicates that we are not filtering.
        @param record_type: The record type to filter for, if provided
        @return The zone information with records (DNSZoneWithRecords), or None if not found
        """
        zone = self.get_zone_by_name(name)
        if zone is None:
            return None
        return DNSZoneWithRecords(zone, self.get_zone_records(zone.id, prefix=prefix, record_type=record_type))

    def get_zone_with_records_by_id(self, id, prefix=NOT_PROVIDED, record_type=NOT_PROVIDED):
        """
        Given a zone ID, return the zone contents with records if found.

        @param id: The zone ID
        @param prefix: The prefix to filter for, if provided. Since None is a valid value,
                       the special constant NOT_PROVIDED indicates that we are not filtering.
        @param record_type: The record type to filter for, if provided
        @return The zone information with records (DNSZoneWithRecords), or None if not found
        """
        zone = self.get_zone_by_id(id)
        if zone is None:
            return None
        return DNSZoneWithRecords(zone, self.get_zone_records(zone.id, prefix=prefix, record_type=record_type))

    @abc.abstractmethod
    def get_zone_records(self, zone_id, prefix=NOT_PROVIDED, record_type=NOT_PROVIDED):
        """
        Given a zone ID, return a list of records, optionally filtered by the provided criteria.

        @param zone_id: The zone ID
        @param prefix: The prefix to filter for, if provided. Since None is a valid value,
                       the special constant NOT_PROVIDED indicates that we are not filtering.
        @param record_type: The record type to filter for, if provided
        @return A list of DNSrecord objects, or None if zone was not found
        """

    @abc.abstractmethod
    def add_record(self, zone_id, record):
        """
        Adds a new record to an existing zone.

        @param zone_id: The zone ID
        @param record: The DNS record (DNSRecord)
        @return The created DNS record (DNSRecord)
        """

    @abc.abstractmethod
    def update_record(self, zone_id, record):
        """
        Update a record.

        @param zone_id: The zone ID
        @param record: The DNS record (DNSRecord)
        @return The DNS record (DNSRecord)
        """

    @abc.abstractmethod
    def delete_record(self, zone_id, record):
        """
        Delete a record.

        @param zone_id: The zone ID
        @param record: The DNS record (DNSRecord)
        @return True in case of success (boolean)
        """

    def add_records(self, records_per_zone_id, stop_early_on_errors=True):
        """
        Add new records to an existing zone.

        @param records_per_zone_id: Maps a zone ID to a list of DNS records (DNSRecord)
        @param stop_early_on_errors: If set to ``True``, try to stop changes after the first error happens.
                                     This might only work on some APIs.
        @return A dictionary mapping zone IDs to lists of tuples ``(record, created, failed)``.
                Here ``created`` indicates whether the record was created (``True``) or not (``False``).
                If it was created, ``record`` contains the record ID and ``failed`` is ``None``.
                If it was not created, ``failed`` should be a ``DNSAPIError`` instance indicating why
                it was not created. It is possible that the API only creates records if all succeed,
                in that case ``failed`` can be ``None`` even though ``created`` is ``False``.
        """
        results_per_zone_id = {}
        for zone_id, records in records_per_zone_id.items():
            result = []
            results_per_zone_id[zone_id] = result
            for record in records:
                try:
                    result.append((self.add_record(zone_id, record), True, None))
                except DNSAPIError as e:
                    result.append((record, False, e))
                    if stop_early_on_errors:
                        return results_per_zone_id
        return results_per_zone_id

    def update_records(self, records_per_zone_id, stop_early_on_errors=True):
        """
        Update multiple records.

        @param records_per_zone_id: Maps a zone ID to a list of DNS records (DNSRecord)
        @param stop_early_on_errors: If set to ``True``, try to stop changes after the first error happens.
                                     This might only work on some APIs.
        @return A dictionary mapping zone IDs to lists of tuples ``(record, updated, failed)``.
                Here ``updated`` indicates whether the record was updated (``True``) or not (``False``).
                If it was not updated, ``failed`` should be a ``DNSAPIError`` instance. If it was
                updated, ``failed`` should be ``None``.  It is possible that the API only updates
                records if all succeed, in that case ``failed`` can be ``None`` even though
                ``updated`` is ``False``.
        """
        results_per_zone_id = {}
        for zone_id, records in records_per_zone_id.items():
            result = []
            results_per_zone_id[zone_id] = result
            for record in records:
                try:
                    result.append((self.update_record(zone_id, record), True, None))
                except DNSAPIError as e:
                    result.append((record, False, e))
                    if stop_early_on_errors:
                        return results_per_zone_id
        return results_per_zone_id

    def delete_records(self, records_per_zone_id, stop_early_on_errors=True):
        """
        Delete multiple records.

        @param records_per_zone_id: Maps a zone ID to a list of DNS records (DNSRecord)
        @param stop_early_on_errors: If set to ``True``, try to stop changes after the first error happens.
                                     This might only work on some APIs.
        @return A dictionary mapping zone IDs to lists of tuples ``(record, deleted, failed)``.
                In case ``record`` was deleted or not deleted, ``deleted`` is ``True``
                respectively ``False``, and ``failed`` is ``None``. In case an error happened
                while deleting, ``deleted`` is ``False`` and ``failed`` is a ``DNSAPIError``
                instance hopefully providing information on the error.
        """
        results_per_zone_id = {}
        for zone_id, records in records_per_zone_id.items():
            result = []
            results_per_zone_id[zone_id] = result
            for record in records:
                try:
                    result.append((record, self.delete_record(zone_id, record), None))
                except DNSAPIError as e:
                    result.append((record, False, e))
                    if stop_early_on_errors:
                        return results_per_zone_id
        return results_per_zone_id

def filter_records(records, prefix=NOT_PROVIDED, record_type=NOT_PROVIDED):
    """
    Given a list of records, returns a filtered subset.

    @param prefix: The prefix to filter for, if provided. Since None is a valid value,
                   the special constant NOT_PROVIDED indicates that we are not filtering.
    @param record_type: The record type to filter for, if provided
    @return The list of records matching the provided filters.
    """
    if prefix is not NOT_PROVIDED:
        records = [record for record in records if record.prefix == prefix]
    if record_type is not NOT_PROVIDED:
        records = [record for record in records if record.type == record_type]
    return records
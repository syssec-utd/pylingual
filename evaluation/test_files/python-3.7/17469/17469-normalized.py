def create_ns_record(self, name, values, ttl=60):
    """
        Creates a NS record attached to this hosted zone.

        :param str name: The fully qualified name of the record to add.
        :param list values: A list of value strings for the record.
        :keyword int ttl: The time-to-live of the record (in seconds).
        :rtype: tuple
        :returns: A tuple in the form of ``(rrset, change_info)``, where
            ``rrset`` is the newly created NSResourceRecordSet instance.
        """
    self._halt_if_already_deleted()
    values = locals()
    del values['self']
    return self._add_record(NSResourceRecordSet, **values)
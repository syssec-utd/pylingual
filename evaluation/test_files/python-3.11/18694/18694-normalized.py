def create(cls, dump):
    """Create record based on dump."""
    if not dump.data.get('record'):
        try:
            PersistentIdentifier.get(pid_type='recid', pid_value=dump.recid)
        except PIDDoesNotExistError:
            PersistentIdentifier.create('recid', dump.recid, status=PIDStatus.RESERVED)
            db.session.commit()
        return None
    dump.prepare_revisions()
    dump.prepare_pids()
    dump.prepare_files()
    existing_files = []
    if dump.record:
        existing_files = dump.record.get('_files', [])
        record = cls.update_record(revisions=dump.revisions, created=dump.created, record=dump.record)
        pids = dump.missing_pids
    else:
        record = cls.create_record(dump)
        pids = dump.pids
    if pids:
        cls.create_pids(record.id, pids)
    if dump.files:
        cls.create_files(record, dump.files, existing_files)
    if dump.is_deleted(record):
        cls.delete_record(record)
    return record
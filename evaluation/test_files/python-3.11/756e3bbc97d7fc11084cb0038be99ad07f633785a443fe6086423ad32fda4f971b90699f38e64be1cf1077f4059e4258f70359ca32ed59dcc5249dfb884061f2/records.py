from ..record import UnicatRecord
from ..error import UnicatError

def create_record(unicat, parent, ordering):
    success, result = unicat.api.call('/records/create', {'parent': parent.gid, 'ordering': ordering})
    if not success:
        raise UnicatError('create_record', result)
    return UnicatRecord(unicat, result['record'])

def set_record_definition(unicat, record, definition):
    success, result = unicat.api.call('/records/definition/set', {'record': record.gid, 'definition': definition.gid})
    if not success:
        raise UnicatError('set_record_definition', result)
    return UnicatRecord(unicat, result['record'])

def extend_record_definition_add_class(unicat, record, class_):
    success, result = unicat.api.call('/records/definition/classes/add', {'record': record.gid, 'class': class_.gid})
    if not success:
        raise UnicatError('extend_record_definition_add_class', result)
    return UnicatRecord(unicat, result['record'])

def extend_record_definition_add_field(unicat, record, field):
    success, result = unicat.api.call('/records/definition/fields/add', {'record': record.gid, 'field': field.gid})
    if not success:
        raise UnicatError('extend_record_definition_add_field', result)
    return UnicatRecord(unicat, result['record'])

def update_record(unicat, record, localizedfielddata):
    success, result = unicat.api.call('/records/update', {'record': record.gid, 'fields': localizedfielddata})
    if not success:
        raise UnicatError('update_record', result)
    return UnicatRecord(unicat, result['record'], result['report.validation'])

def set_record_channels(unicat, record, channels, enabled):
    success, result = unicat.api.call('/records/channels/set', {'record': record.gid, 'channels': channels, 'enabled': enabled})
    if not success:
        raise UnicatError('set_record_channels', result)
    return UnicatRecord(unicat, result['record'])

def set_record_orderings(unicat, record, orderings):
    success, result = unicat.api.call('/records/orderings/set', {'record': record.gid, 'orderings': orderings})
    if not success:
        raise UnicatError('set_record_orderings', result)
    return UnicatRecord(unicat, result['record'])

def link_record(unicat, parent, record, ordering):
    success, result = unicat.api.call('/records/link', {'parent': parent.gid, 'record': record.gid, 'ordering': ordering})
    if not success:
        raise UnicatError('link_record', result)
    return UnicatRecord(unicat, result['record'])

def delete_record(unicat, record):
    success, result = unicat.api.call('/records/delete', {'record': record.gid})
    if not success:
        raise UnicatError('delete_record', result)
    return UnicatRecord(unicat, result['record'])

def undelete_record(unicat, record):
    success, result = unicat.api.call('/records/undelete', {'record': record.gid})
    if not success:
        raise UnicatError('undelete_record', result)
    return UnicatRecord(unicat, result['record'])

def permanent_delete_record(unicat, record):
    success, result = unicat.api.call('/records/permanent_delete', {'record': record.gid})
    if not success:
        raise UnicatError('permanent_delete_record', result)
    if record.gid in unicat.api.data['records']:
        del unicat.api.data['records'][record.gid]
    return True
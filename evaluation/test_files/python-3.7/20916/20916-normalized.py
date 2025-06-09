def get_record(self, msg_id):
    """Get a specific Task Record, by msg_id."""
    if not msg_id in self._records:
        raise KeyError('No such msg_id %r' % msg_id)
    return copy(self._records[msg_id])
def get_history(self):
    """get all msg_ids, ordered by time submitted."""
    cursor = self._records.find({}, {'msg_id': 1}).sort('submitted')
    return [rec['msg_id'] for rec in cursor]
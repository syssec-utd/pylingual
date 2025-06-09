def get_history(self):
    """get all msg_ids, ordered by time submitted."""
    query = 'SELECT msg_id FROM %s ORDER by submitted ASC' % self.table
    cursor = self._db.execute(query)
    return [tup[0] for tup in cursor.fetchall()]
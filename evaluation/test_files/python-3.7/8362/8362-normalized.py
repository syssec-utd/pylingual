def valid(self):
    """ Check to see if we are still active. """
    if self.finished is not None:
        return False
    with self._db_conn() as conn:
        row = conn.get('\n                SELECT (last_contact > %%(now)s - INTERVAL %%(ttl)s SECOND) AS valid\n                FROM %s\n                WHERE\n                    id = %%(task_id)s\n                    AND execution_id = %%(execution_id)s\n            ' % self._queue.table_name, now=datetime.utcnow(), ttl=self._queue.execution_ttl, task_id=self.task_id, execution_id=self.execution_id)
    return bool(row is not None and row.valid)
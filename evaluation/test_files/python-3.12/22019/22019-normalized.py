def _handle_stranded_msgs(self, eid, uuid):
    """Handle messages known to be on an engine when the engine unregisters.

        It is possible that this will fire prematurely - that is, an engine will
        go down after completing a result, and the client will be notified
        that the result failed and later receive the actual result.
        """
    outstanding = self.queues[eid]
    for msg_id in outstanding:
        self.pending.remove(msg_id)
        self.all_completed.add(msg_id)
        try:
            raise error.EngineError('Engine %r died while running task %r' % (eid, msg_id))
        except:
            content = error.wrap_exception()
        header = {}
        header['engine'] = uuid
        header['date'] = datetime.now()
        rec = dict(result_content=content, result_header=header, result_buffers=[])
        rec['completed'] = header['date']
        rec['engine_uuid'] = uuid
        try:
            self.db.update_record(msg_id, rec)
        except Exception:
            self.log.error('DB Error handling stranded msg %r', msg_id, exc_info=True)
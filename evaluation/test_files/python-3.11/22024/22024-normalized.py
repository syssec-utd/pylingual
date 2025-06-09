def resubmit_task(self, client_id, msg):
    """Resubmit one or more tasks."""

    def finish(reply):
        self.session.send(self.query, 'resubmit_reply', content=reply, ident=client_id)
    content = msg['content']
    msg_ids = content['msg_ids']
    reply = dict(status='ok')
    try:
        records = self.db.find_records({'msg_id': {'$in': msg_ids}}, keys=['header', 'content', 'buffers'])
    except Exception:
        self.log.error('db::db error finding tasks to resubmit', exc_info=True)
        return finish(error.wrap_exception())
    found_ids = [rec['msg_id'] for rec in records]
    pending_ids = [msg_id for msg_id in found_ids if msg_id in self.pending]
    if len(records) > len(msg_ids):
        try:
            raise RuntimeError('DB appears to be in an inconsistent state.More matching records were found than should exist')
        except Exception:
            return finish(error.wrap_exception())
    elif len(records) < len(msg_ids):
        missing = [m for m in msg_ids if m not in found_ids]
        try:
            raise KeyError('No such msg(s): %r' % missing)
        except KeyError:
            return finish(error.wrap_exception())
    elif pending_ids:
        pass
    resubmitted = {}
    for rec in records:
        header = rec['header']
        msg = self.session.msg(header['msg_type'], parent=header)
        msg_id = msg['msg_id']
        msg['content'] = rec['content']
        fresh = msg['header']
        header['msg_id'] = fresh['msg_id']
        header['date'] = fresh['date']
        msg['header'] = header
        self.session.send(self.resubmit, msg, buffers=rec['buffers'])
        resubmitted[rec['msg_id']] = msg_id
        self.pending.add(msg_id)
        msg['buffers'] = rec['buffers']
        try:
            self.db.add_record(msg_id, init_record(msg))
        except Exception:
            self.log.error('db::DB Error updating record: %s', msg_id, exc_info=True)
    finish(dict(status='ok', resubmitted=resubmitted))
    for msg_id, resubmit_id in resubmitted.iteritems():
        try:
            self.db.update_record(msg_id, {'resubmitted': resubmit_id})
        except Exception:
            self.log.error('db::DB Error updating record: %s', msg_id, exc_info=True)
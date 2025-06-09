def disable(self, msgid, scope='package', line=None, ignore_unknown=False):
    """don't output message of the given id"""
    self._set_msg_status(msgid, enable=False, scope=scope, line=line, ignore_unknown=ignore_unknown)
    self._register_by_id_managed_msg(msgid, line)
def _handle_pyout(self, msg):
    """ Handle display hook output.
        """
    self.log.debug('pyout: %s', msg.get('content', ''))
    if not self._hidden and self._is_from_this_session(msg):
        text = msg['content']['data']
        self._append_plain_text(text + '\n', before_prompt=True)
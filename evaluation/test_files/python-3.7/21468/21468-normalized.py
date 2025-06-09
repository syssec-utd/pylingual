def _complete(self):
    """ Performs completion at the current cursor location.
        """
    context = self._get_context()
    if context:
        msg_id = self.kernel_manager.shell_channel.complete('.'.join(context), self._get_input_buffer_cursor_line(), self._get_input_buffer_cursor_column(), self.input_buffer)
        pos = self._get_cursor().position()
        info = self._CompletionRequest(msg_id, pos)
        self._request_info['complete'] = info
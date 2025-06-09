def handle_line_start(self, pos):
    """Record the first non-junk token at the start of a line."""
    if self._line_start > -1:
        return
    check_token_position = pos
    if self._tokens.token(pos) == _ASYNC_TOKEN:
        check_token_position += 1
    self._is_block_opener = self._tokens.token(check_token_position) in _CONTINUATION_BLOCK_OPENERS
    self._line_start = pos
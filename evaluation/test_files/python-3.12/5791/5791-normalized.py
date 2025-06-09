def _hanging_indent_after_bracket(self, bracket, position):
    """Extracts indentation information for a hanging indent

        Case of hanging indent after a bracket (including parenthesis)

        :param str bracket: bracket in question
        :param int position: Position of bracket in self._tokens

        :returns: the state and valid positions for hanging indentation
        :rtype: _ContinuedIndent
        """
    indentation = self._tokens.line_indent(position)
    if self._is_block_opener and self._continuation_string == self._block_indent_string:
        return _ContinuedIndent(HANGING_BLOCK, bracket, position, _Indentations(indentation + self._continuation_string, indentation), _BeforeBlockIndentations(indentation + self._continuation_string, indentation + self._continuation_string * 2))
    if bracket == ':':
        paren_align = self._cont_stack[-1].valid_outdent_strings
        next_align = self._cont_stack[-1].valid_continuation_strings.copy()
        next_align_keys = list(next_align.keys())
        next_align[next_align_keys[0] + self._continuation_string] = True
        return _ContinuedIndent(HANGING_DICT_VALUE, bracket, position, paren_align, next_align)
    return _ContinuedIndent(HANGING, bracket, position, _Indentations(indentation, indentation + self._continuation_string), _Indentations(indentation + self._continuation_string))
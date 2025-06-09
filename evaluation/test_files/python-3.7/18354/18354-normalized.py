def _ast_repetition_group_to_code(self, repetition_group, ignore_whitespace=False, **kwargs):
    """Convert an AST repetition group to python source code."""
    lines = ['zero_or_more(']
    lines.extend(self._indent(self._ast_to_code(repetition_group.expression)))
    lines[-1] += ','
    lines.append(self._indent('ignore_whitespace={}'.format(bool(ignore_whitespace))))
    lines.append(')')
    return lines
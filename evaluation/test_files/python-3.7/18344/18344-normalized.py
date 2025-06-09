def _get_rule_source(self, rule):
    """Gets the variable part of the source code for a rule."""
    p = len(self.input_source) + rule.position
    source = self.input_source[p:p + rule.consumed].rstrip()
    return self._indent(source, depth=self.indent + '   ', skip_first_line=True)
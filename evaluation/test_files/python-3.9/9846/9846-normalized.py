def visit_Dict(self, node):
    """
        Process dict arguments.

        """
    if self.should_check_whitelist(node):
        for key in node.keys:
            if key.s in self.whitelist or key.s.startswith('debug_'):
                continue
            self.violations.append((self.current_logging_call, WHITELIST_VIOLATION.format(key.s)))
    if self.should_check_extra_exception(node):
        for value in node.values:
            self.check_exception_arg(value)
    super(LoggingVisitor, self).generic_visit(node)
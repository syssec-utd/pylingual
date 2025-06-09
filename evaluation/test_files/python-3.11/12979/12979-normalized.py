def _blame_line(self, traceback):
    """Figures out which line in traceback is to blame for the error.
        Returns a 3-tuple of (ErrorKey, StackTraceEntry, [email recipients])"""
    key = None
    blamed_entry = None
    email_recipients = []
    for stack_line in traceback:
        line_type = self._get_line_type(stack_line)
        if line_type == api_ttypes.LineType.THIRDPARTY_WHITELIST:
            return (None, None, None, True)
        elif line_type in [api_ttypes.LineType.DEFAULT, api_ttypes.LineType.KNOWN_ERROR]:
            filepath = self._get_basepath(stack_line.filename)
            entry = api_ttypes.CodeIdentifier(filepath, stack_line.function_name, stack_line.text)
            blamed_entry = entry
            key = api_ttypes.ErrorKey(filepath, stack_line.line_number, stack_line.function_name, stack_line.text)
            if filepath in self.watch_all_errors:
                email_recipients.extend(self.watch_all_errors[filepath])
    return (key, blamed_entry, email_recipients, False)
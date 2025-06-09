def _format_exception_only(self, etype, value):
    """Format the exception part of a traceback.

        The arguments are the exception type and value such as given by
        sys.exc_info()[:2]. The return value is a list of strings, each ending
        in a newline.  Normally, the list contains a single string; however,
        for SyntaxError exceptions, it contains several lines that (when
        printed) display detailed information about where the syntax error
        occurred.  The message indicating which exception occurred is the
        always last string in the list.

        Also lifted nearly verbatim from traceback.py
        """
    have_filedata = False
    Colors = self.Colors
    list = []
    stype = Colors.excName + etype.__name__ + Colors.Normal
    if value is None:
        list.append(str(stype) + '\n')
    else:
        if etype is SyntaxError:
            have_filedata = True
            if not value.filename:
                value.filename = '<string>'
            list.append('%s  File %s"%s"%s, line %s%d%s\n' % (Colors.normalEm, Colors.filenameEm, value.filename, Colors.normalEm, Colors.linenoEm, value.lineno, Colors.Normal))
            if value.text is not None:
                i = 0
                while i < len(value.text) and value.text[i].isspace():
                    i += 1
                list.append('%s    %s%s\n' % (Colors.line, value.text.strip(), Colors.Normal))
                if value.offset is not None:
                    s = '    '
                    for c in value.text[i:value.offset - 1]:
                        if c.isspace():
                            s += c
                        else:
                            s += ' '
                    list.append('%s%s^%s\n' % (Colors.caret, s, Colors.Normal))
        try:
            s = value.msg
        except Exception:
            s = self._some_str(value)
        if s:
            list.append('%s%s:%s %s\n' % (str(stype), Colors.excName, Colors.Normal, s))
        else:
            list.append('%s\n' % str(stype))
    if have_filedata:
        ipinst = ipapi.get()
        if ipinst is not None:
            ipinst.hooks.synchronize_with_editor(value.filename, value.lineno, 0)
    return list
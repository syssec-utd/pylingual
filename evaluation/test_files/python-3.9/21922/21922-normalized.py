def addError(self, test, err, capt=None):
    """Add error output to Xunit report.
        """
    taken = self._timeTaken()
    if issubclass(err[0], SkipTest):
        type = 'skipped'
        self.stats['skipped'] += 1
    else:
        type = 'error'
        self.stats['errors'] += 1
    tb = ''.join(traceback.format_exception(*err))
    id = test.id()
    self.errorlist.append('<testcase classname=%(cls)s name=%(name)s time="%(taken).3f"><%(type)s type=%(errtype)s message=%(message)s><![CDATA[%(tb)s]]></%(type)s></testcase>' % {'cls': self._quoteattr(id_split(id)[0]), 'name': self._quoteattr(id_split(id)[-1]), 'taken': taken, 'type': type, 'errtype': self._quoteattr(nice_classname(err[0])), 'message': self._quoteattr(exc_message(err)), 'tb': escape_cdata(tb)})
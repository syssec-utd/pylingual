def run(self, args):
    """Current line number in source file"""
    if not self.proc.curframe:
        self.errmsg('No line number information available.')
        return
    if len(args) == 3:
        answer = self.lineinfo(args[2])
        if answer[0]:
            (item, filename, lineno) = answer
            if not os.path.isfile(filename):
                filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
            self.msg('Line %s of "%s" <%s>' % (lineno, filename, item))
        return
    filename = self.core.canonic_filename(self.proc.curframe)
    if not os.path.isfile(filename):
        filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
        pass
    filename = self.core.canonic_filename(self.proc.curframe)
    msg1 = 'Line %d of "%s"' % (inspect.getlineno(self.proc.curframe), self.core.filename(filename))
    msg2 = 'at instruction %d' % self.proc.curframe.f_lasti
    if self.proc.event:
        msg2 += ', %s event' % self.proc.event
        pass
    self.msg(Mmisc.wrapped_lines(msg1, msg2, self.settings['width']))
    return False
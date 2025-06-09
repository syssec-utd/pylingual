def event_processor(self, frame, event, event_arg, prompt='trepan3k'):
    """command event processor: reading a commands do something with them."""
    self.frame = frame
    self.event = event
    self.event_arg = event_arg
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    line = linecache.getline(filename, lineno, frame.f_globals)
    if not line:
        opts = {'output': 'plain', 'reload_on_change': self.settings('reload'), 'strip_nl': False}
        m = re.search('^<frozen (.*)>', filename)
        if m and m.group(1):
            filename = pyficache.unmap_file(m.group(1))
        line = pyficache.getline(filename, lineno, opts)
    self.current_source_text = line
    if self.settings('skip') is not None:
        if Mbytecode.is_def_stmt(line, frame):
            return True
        if Mbytecode.is_class_def(line, frame):
            return True
        pass
    self.thread_name = Mthread.current_thread_name()
    self.frame_thread_name = self.thread_name
    self.set_prompt(prompt)
    self.process_commands()
    if filename == '<string>':
        pyficache.remove_remap_file('<string>')
    return True
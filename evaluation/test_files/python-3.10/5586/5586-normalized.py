def check(self, files_or_modules):
    """main checking entry: check a list of files or modules from their
        name.
        """
    for msg in self.msgs_store.messages:
        if not msg.may_be_emitted():
            self._msgs_state[msg.msgid] = False
    if not isinstance(files_or_modules, (list, tuple)):
        files_or_modules = (files_or_modules,)
    if self.config.jobs == 1:
        self._do_check(files_or_modules)
    else:
        self._parallel_check(files_or_modules)
def _cmdRegex(self, cmd_grp=None):
    """Get command regex string and completer dict."""
    cmd_grp = cmd_grp or 'cmd'
    help_opts = ('-h', '--help')
    cmd = self.name()
    names = '|'.join([re.escape(cmd)] + [re.escape(a) for a in self.aliases()])
    opts = []
    for action in self.parser._actions:
        opts += [a for a in action.option_strings if a not in help_opts]
    opts_re = '|'.join([re.escape(o) for o in opts])
    if opts_re:
        opts_re = f'(\\s+(?P<{cmd_grp}_opts>{opts_re}))*'
    help_re = '|'.join([re.escape(o) for o in help_opts])
    help_re = f'(\\s+(?P<HELP_OPTS>{help_re}))*'
    completers = {}
    if opts_re:
        completers[f'{cmd_grp}_opts'] = WordCompleter(opts)
    return tuple([f'(?P<{cmd_grp}>{names}){opts_re}{help_re}', completers])
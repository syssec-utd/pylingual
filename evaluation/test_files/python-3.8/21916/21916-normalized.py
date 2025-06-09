def magic_run_completer(self, event):
    """Complete files that end in .py or .ipy for the %run command.
    """
    comps = arg_split(event.line, strict=False)
    relpath = (len(comps) > 1 and comps[-1] or '').strip('\'"')
    lglob = glob.glob
    isdir = os.path.isdir
    (relpath, tilde_expand, tilde_val) = expand_user(relpath)
    dirs = [f.replace('\\', '/') + '/' for f in lglob(relpath + '*') if isdir(f)]
    if filter(magic_run_re.match, comps):
        pys = [f.replace('\\', '/') for f in lglob('*')]
    else:
        pys = [f.replace('\\', '/') for f in lglob(relpath + '*.py') + lglob(relpath + '*.ipy') + lglob(relpath + '*.pyw')]
    return [compress_user(p, tilde_expand, tilde_val) for p in dirs + pys]
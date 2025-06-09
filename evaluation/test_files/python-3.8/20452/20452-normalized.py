def find_user_code(self, target, raw=True, py_only=False):
    """Get a code string from history, file, url, or a string or macro.

        This is mainly used by magic functions.

        Parameters
        ----------

        target : str

          A string specifying code to retrieve. This will be tried respectively
          as: ranges of input history (see %history for syntax), url,
          correspnding .py file, filename, or an expression evaluating to a
          string or Macro in the user namespace.

        raw : bool
          If true (default), retrieve raw history. Has no effect on the other
          retrieval mechanisms.

        py_only : bool (default False)
          Only try to fetch python code, do not try alternative methods to decode file
          if unicode fails.

        Returns
        -------
        A string of code.

        ValueError is raised if nothing is found, and TypeError if it evaluates
        to an object of another type. In each case, .args[0] is a printable
        message.
        """
    code = self.extract_input_lines(target, raw=raw)
    if code:
        return code
    utarget = unquote_filename(target)
    try:
        if utarget.startswith(('http://', 'https://')):
            return openpy.read_py_url(utarget, skip_encoding_cookie=True)
    except UnicodeDecodeError:
        if not py_only:
            response = urllib.urlopen(target)
            return response.read().decode('latin1')
        raise ValueError("'%s' seem to be unreadable." % utarget)
    potential_target = [target]
    try:
        potential_target.insert(0, get_py_filename(target))
    except IOError:
        pass
    for tgt in potential_target:
        if os.path.isfile(tgt):
            try:
                return openpy.read_py_file(tgt, skip_encoding_cookie=True)
            except UnicodeDecodeError:
                if not py_only:
                    with io_open(tgt, 'r', encoding='latin1') as f:
                        return f.read()
                raise ValueError("'%s' seem to be unreadable." % target)
    try:
        codeobj = eval(target, self.user_ns)
    except Exception:
        raise ValueError("'%s' was not found in history, as a file, url, nor in the user namespace." % target)
    if isinstance(codeobj, basestring):
        return codeobj
    elif isinstance(codeobj, Macro):
        return codeobj.value
    raise TypeError('%s is neither a string nor a macro.' % target, codeobj)
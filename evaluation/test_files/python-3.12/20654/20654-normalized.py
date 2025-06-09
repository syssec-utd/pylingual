def getoutputerror(cmd):
    """Return (standard output, standard error) of executing cmd in a shell.

    Accepts the same arguments as os.system().

    Parameters
    ----------
    cmd : str
      A command to be executed in the system shell.

    Returns
    -------
    stdout : str
    stderr : str
    """
    out_err = process_handler(cmd, lambda p: p.communicate())
    if out_err is None:
        return ('', '')
    out, err = out_err
    return (py3compat.bytes_to_str(out), py3compat.bytes_to_str(err))
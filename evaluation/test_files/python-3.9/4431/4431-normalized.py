def log_stdout_stderr(log, stdout, stderr, comment=''):
    """
    This function polls stdout and stderr streams and writes their contents
    to log
    """
    readable = select.select([stdout], [], [], 0)[0]
    if stderr:
        exceptional = select.select([stderr], [], [], 0)[0]
    else:
        exceptional = []
    log.debug('Selected: %s, %s', readable, exceptional)
    for handle in readable:
        line = handle.read()
        readable.remove(handle)
        if line:
            log.debug('%s stdout: %s', comment, line.strip())
    for handle in exceptional:
        line = handle.read()
        exceptional.remove(handle)
        if line:
            log.warn('%s stderr: %s', comment, line.strip())
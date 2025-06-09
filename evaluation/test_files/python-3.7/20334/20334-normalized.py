def warn(msg, level=2, exit_val=1):
    """Standard warning printer. Gives formatting consistency.

    Output is sent to io.stderr (sys.stderr by default).

    Options:

    -level(2): allows finer control:
      0 -> Do nothing, dummy function.
      1 -> Print message.
      2 -> Print 'WARNING:' + message. (Default level).
      3 -> Print 'ERROR:' + message.
      4 -> Print 'FATAL ERROR:' + message and trigger a sys.exit(exit_val).

    -exit_val (1): exit value returned by sys.exit() for a level 4
    warning. Ignored for all other levels."""
    if level > 0:
        header = ['', '', 'WARNING: ', 'ERROR: ', 'FATAL ERROR: ']
        io.stderr.write('%s%s' % (header[level], msg))
        if level == 4:
            (print >> io.stderr, 'Exiting.\n')
            sys.exit(exit_val)
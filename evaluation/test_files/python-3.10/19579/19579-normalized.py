def chown(path, uid, guid, recursive=True):
    """ alternative to os.chown.
        wraps around unix chown
        example:
            chown('/tmp/test/', bob, bob)

        returns 2-tuple: exitcode and terminal output
    """
    if recursive:
        cmd = 'chown -R %s:%s %s' % (uid, guid, path)
    else:
        cmd = 'chown %s:%s %s' % (uid, guid, path)
    return sh(cmd)
def _try_passwordless_openssh(server, keyfile):
    """Try passwordless login with shell ssh command."""
    if pexpect is None:
        raise ImportError('pexpect unavailable, use paramiko')
    cmd = 'ssh -f ' + server
    if keyfile:
        cmd += ' -i ' + keyfile
    cmd += ' exit'
    p = pexpect.spawn(cmd)
    while True:
        try:
            p.expect('[Pp]assword:', timeout=0.1)
        except pexpect.TIMEOUT:
            continue
        except pexpect.EOF:
            return True
        else:
            return False
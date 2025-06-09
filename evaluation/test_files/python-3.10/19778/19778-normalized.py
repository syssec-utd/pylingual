def dump(filename, dbname, username=None, password=None, host=None, port=None, tempdir='/tmp', mysqldump_path='mysqldump'):
    """Perfoms a mysqldump backup.
    Create a database dump for the given database.
    returns statuscode and shelloutput
    """
    filepath = os.path.join(tempdir, filename)
    cmd = mysqldump_path
    cmd += ' --result-file=' + os.path.join(tempdir, filename)
    if username:
        cmd += ' --user=%s' % username
    if host:
        cmd += ' --host=%s' % host
    if port:
        cmd += ' --port=%s' % port
    if password:
        cmd += ' --password=%s' % password
    cmd += ' ' + dbname
    return sh(cmd)
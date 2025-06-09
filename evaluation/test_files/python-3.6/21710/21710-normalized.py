def filehash(path):
    """Make an MD5 hash of a file, ignoring any differences in line
    ending characters."""
    with open(path, 'rU') as f:
        return md5(py3compat.str_to_bytes(f.read())).hexdigest()
def _find_prefix_path(self, basedir, prefix):
    """Similar to _find_prefix_paths() but only returns the first match"""
    ret = ''
    for ret in self._find_prefix_paths(basedir, prefix):
        break
    if not ret:
        raise IOError('Could not find prefix {} in path {}'.format(prefix, basedir))
    return ret
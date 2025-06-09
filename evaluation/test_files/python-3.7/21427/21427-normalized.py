def wantDirectory(self, dirname):
    """Check if directory is eligible for test discovery"""
    if dirname in self.exclude_dirs:
        log.debug('excluded: %s' % dirname)
        return False
    else:
        return None
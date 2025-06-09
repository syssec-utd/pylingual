def make_init_files(self):
    """Create missing package __init__ files"""
    init_files = []
    for base, dirs, files in walk_egg(self.bdist_dir):
        if base == self.bdist_dir:
            continue
        for name in files:
            if name.endswith('.py'):
                if '__init__.py' not in files:
                    pkg = base[len(self.bdist_dir) + 1:].replace(os.sep, '.')
                    if self.distribution.has_contents_for(pkg):
                        log.warn('Creating missing __init__.py for %s', pkg)
                        filename = os.path.join(base, '__init__.py')
                        if not self.dry_run:
                            f = open(filename, 'w')
                            f.write(NS_PKG_STUB)
                            f.close()
                        init_files.append(filename)
                break
        else:
            dirs[:] = []
    return init_files
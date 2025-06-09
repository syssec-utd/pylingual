def _run_startup_files(self):
    """Run files from profile startup directory"""
    startup_dir = self.profile_dir.startup_dir
    startup_files = glob.glob(os.path.join(startup_dir, '*.py'))
    startup_files += glob.glob(os.path.join(startup_dir, '*.ipy'))
    if not startup_files:
        return
    self.log.debug('Running startup files from %s...', startup_dir)
    try:
        for fname in sorted(startup_files):
            self._exec_file(fname)
    except:
        self.log.warn('Unknown error in handling startup files:')
        self.shell.showtraceback()
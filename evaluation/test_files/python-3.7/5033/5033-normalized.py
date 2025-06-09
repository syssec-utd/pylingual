def _update_references(self, refs):
    """Update references removing old ones."""
    new_refs = [ref.refname for ref in refs]
    for old_ref in self._discover_refs():
        if not old_ref.refname.startswith('refs/heads/'):
            continue
        if old_ref.refname in new_refs:
            continue
        self._update_ref(old_ref, delete=True)
    for new_ref in refs:
        refname = new_ref.refname
        if refname.endswith('^{}'):
            logger.debug('Annotated tag %s ignored for updating in sync process', refname)
            continue
        elif not refname.startswith('refs/heads/') and (not refname.startswith('refs/tags/')):
            logger.debug('Reference %s not needed; ignored for updating in sync process', refname)
            continue
        else:
            self._update_ref(new_ref)
    cmd = ['git', 'remote', 'prune', 'origin']
    self._exec(cmd, cwd=self.dirpath, env=self.gitenv)
def install(self, install_options, global_options=()):
    """Install everything in this set (after having downloaded and unpacked the packages)"""
    to_install = [r for r in self.requirements.values() if not r.satisfied_by]
    if to_install:
        logger.notify('Installing collected packages: %s' % ', '.join([req.name for req in to_install]))
    logger.indent += 2
    try:
        for requirement in to_install:
            if requirement.conflicts_with:
                logger.notify('Found existing installation: %s' % requirement.conflicts_with)
                logger.indent += 2
                try:
                    requirement.uninstall(auto_confirm=True)
                finally:
                    logger.indent -= 2
            try:
                requirement.install(install_options, global_options)
            except:
                if requirement.conflicts_with and (not requirement.install_succeeded):
                    requirement.rollback_uninstall()
                raise
            else:
                if requirement.conflicts_with and requirement.install_succeeded:
                    requirement.commit_uninstall()
            requirement.remove_temporary_source()
    finally:
        logger.indent -= 2
    self.successfully_installed = to_install
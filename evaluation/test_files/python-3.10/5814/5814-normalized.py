def _match_long_opt(self, opt):
    """Disable abbreviations."""
    if opt not in self._long_opt:
        raise optparse.BadOptionError(opt)
    return opt
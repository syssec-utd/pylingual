def patches_after(self, patch):
    """ Returns a list of patches after patch from the patches list """
    return [line.get_patch() for line in self._patchlines_after(patch) if line.get_patch()]
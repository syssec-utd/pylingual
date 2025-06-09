def _set_default_options(self):
    """set different default options with _default dictionary"""
    self.module_names = self._set_option(self.config.module_names)
    all_ancestors = self._set_option(self.config.all_ancestors)
    all_associated = self._set_option(self.config.all_associated)
    (anc_level, association_level) = (0, 0)
    if all_ancestors:
        anc_level = -1
    if all_associated:
        association_level = -1
    if self.config.show_ancestors is not None:
        anc_level = self.config.show_ancestors
    if self.config.show_associated is not None:
        association_level = self.config.show_associated
    (self.anc_level, self.association_level) = (anc_level, association_level)
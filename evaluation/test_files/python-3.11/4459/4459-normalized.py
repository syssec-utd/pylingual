def __add_user_options(self):
    """ override config options with user specified options"""
    if self.options.get('user_options', None):
        self.core.apply_shorthand_options(self.options['user_options'])
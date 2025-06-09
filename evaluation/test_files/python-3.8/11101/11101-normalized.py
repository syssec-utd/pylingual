def write(self, outfile=None, section=None):
    """Write the current config to a file (defaults to user config).

        :param str outfile: The path to the file to write to.
        :param None/str section: The config section to write, or :data:`None`
                                 to write the entire config.
        """
    with io.open(outfile or self.user_config_file(), 'wb') as f:
        self.data.write(outfile=f, section=section)
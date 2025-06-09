def combine(self):
    """Combine together a number of similarly-named coverage data files.

        All coverage data files whose name starts with `data_file` (from the
        coverage() constructor) will be read, and combined together into the
        current measurements.

        """
    aliases = None
    if self.config.paths:
        aliases = PathAliases(self.file_locator)
        for paths in self.config.paths.values():
            result = paths[0]
            for pattern in paths[1:]:
                aliases.add(pattern, result)
    self.data.combine_parallel_data(aliases=aliases)
def sections_list(self, cmd=None):
    """List of config sections used by a command.

        Args:
            cmd (str): command name, set to ``None`` or ``''`` for the bare
                command.

        Returns:
            list of str: list of configuration sections used by that command.
        """
    sections = list(self.common.sections)
    if not cmd:
        if self.bare is not None:
            sections.extend(self.bare.sections)
            return sections
        return []
    sections.extend(self.subcmds[cmd].sections)
    if cmd in self._conf:
        sections.append(cmd)
    return sections
def getsection(self, section):
    """
        Returns the section as a dict. Values are converted to int, float, bool
        as required.

        :param section: section from the config
        :rtype: dict
        """
    if section not in self._sections and section not in self.airflow_defaults._sections:
        return None
    _section = copy.deepcopy(self.airflow_defaults._sections[section])
    if section in self._sections:
        _section.update(copy.deepcopy(self._sections[section]))
    section_prefix = 'AIRFLOW__{S}__'.format(S=section.upper())
    for env_var in sorted(os.environ.keys()):
        if env_var.startswith(section_prefix):
            key = env_var.replace(section_prefix, '').lower()
            _section[key] = self._get_env_var_option(section, key)
    for (key, val) in iteritems(_section):
        try:
            val = int(val)
        except ValueError:
            try:
                val = float(val)
            except ValueError:
                if val.lower() in ('t', 'true'):
                    val = True
                elif val.lower() in ('f', 'false'):
                    val = False
        _section[key] = val
    return _section
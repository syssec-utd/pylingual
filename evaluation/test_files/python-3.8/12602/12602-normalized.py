def _collect_section(self, section):
    """Collects all settings within a section"""
    kwargs = {}
    try:
        if self.parser.has_section(section):
            options = self.parser.options(section)
            for option in options:
                str_val = self.parser.get(section, option)
                val = ast.literal_eval(str_val)
                kwargs[option] = val
        return kwargs
    except:
        raise
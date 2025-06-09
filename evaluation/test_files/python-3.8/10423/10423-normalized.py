def set(self, section, option, value):
    """
        Set method that (1) auto-saves if possible and (2) auto-creates
        sections.
        """
    try:
        super(ExactOnlineConfig, self).set(section, option, value)
    except NoSectionError:
        self.add_section(section)
        super(ExactOnlineConfig, self).set(section, option, value)
    self.save()
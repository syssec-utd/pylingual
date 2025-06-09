def add_sample_tag_value(self, tag_name, new_sample_values):
    """Appends a new format tag-value for all samples.

        Args:
            tag_name: string tag name; must not already exist
            new_sample

        Raises:
            KeyError: if tag_name to be added already exists
        """
    if tag_name in self.format_tags:
        msg = 'New format value [{}] already exists.'.format(tag_name)
        raise KeyError(msg)
    if not self._samples_match(new_sample_values):
        raise KeyError('Sample name values must match existing sample names')
    for sample in self.sample_tag_values.keys():
        value = str(new_sample_values[sample])
        self.sample_tag_values[sample][tag_name] = value
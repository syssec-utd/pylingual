def _fill_sample_count(self, node):
    """Counts and fills sample counts inside call tree."""
    node['sampleCount'] += sum((self._fill_sample_count(child) for child in node['children']))
    return node['sampleCount']
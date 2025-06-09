def describe(self, verbose=True):
    """Return a textual description of the segment."""
    center = titlecase(target_names.get(self.center, 'Unknown center'))
    target = titlecase(target_names.get(self.target, 'Unknown target'))
    text = '{0.start_jd:.2f}..{0.end_jd:.2f}  {1} ({0.center}) -> {2} ({0.target})'.format(self, center, target)
    if verbose:
        text += '\n  frame={0.frame} data_type={0.data_type} source={1}'.format(self, self.source.decode('ascii'))
    return text
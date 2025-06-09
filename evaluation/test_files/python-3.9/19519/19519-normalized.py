def render(self):
    """Render the axes data into the dict data"""
    for (opt, values) in self.data.items():
        if opt == 'ticks':
            self['chxtc'] = '|'.join(values)
        else:
            self['chx%s' % opt[0]] = '|'.join(values)
    return self
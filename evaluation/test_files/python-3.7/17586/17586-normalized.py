def get(self):
    """
        Please don't do this in production environments.
        """
    self.write('Memory Session Object Demo:')
    if 'sv' in self.session:
        current_value = self.session['sv']
        self.write('current sv value is %s, and system will delete this value.<br/>' % self.session['sv'])
        self.session.delete('sv')
        if 'sv' not in self.session:
            self.write('current sv value is empty')
    else:
        self.write('Session data not found')
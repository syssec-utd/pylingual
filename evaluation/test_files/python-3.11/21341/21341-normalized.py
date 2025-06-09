def _make_in_prompt(self, number):
    """ Given a prompt number, returns an HTML In prompt.
        """
    try:
        body = self.in_prompt % number
    except TypeError:
        body = self.in_prompt
    return '<span class="in-prompt">%s</span>' % body
def set_style(self, style):
    """ Sets the style to the specified Pygments style.
        """
    if isinstance(style, basestring):
        style = get_style_by_name(style)
    self._style = style
    self._clear_caches()
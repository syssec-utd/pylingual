from pygame import constants
__all__ = ['StyleType', 'normal', 'fullscreen', 'resizable', 'no_frame', 'hidden', 'shown', 'scaled']

class _Style(object):

    def __init__(self, style: int):
        """
        The window style.
        
        :param style: Style number.
        """
        self.style = style
        if isinstance(style, _Style):
            self.style = style.style
        self.help_docs = ''

    def __str__(self):
        return f'_Style(style={self.style})'

    def __add__(self, other):
        """
        Merge two styles.
        
        :param other: Style type or style number.
        :return: Merged style.
        """
        if isinstance(other, int):
            return _Style(self.style | other)
        if isinstance(other, _Style):
            return _Style(self.style | other.style)
        return self

    def help(self):
        """
        Show help document.
        
        :return: Help document.
        """
        return self.help_docs
StyleType = _Style
normal = _Style(0)
fullscreen = _Style(constants.FULLSCREEN)
resizable = _Style(constants.RESIZABLE)
no_frame = _Style(constants.NOFRAME)
hidden = _Style(constants.HIDDEN)
shown = _Style(constants.SHOWN)
scaled = _Style(constants.SCALED)
normal.help_docs = 'The normal mode'
fullscreen.help_docs = 'Window full screen display'
resizable.help_docs = 'Window resizeable'
no_frame.help_docs = 'Window without borders or controls'
hidden.help_docs = 'Window opens in hidden mode'
shown.help_docs = 'Window opens in shown mode'
scaled.help_docs = 'Window resolution depends on desktop size and zoom shape'
def switch_to_frame(self, frame):
    """
        Switch to the given frame.

        If you use this method you are responsible for making sure you switch back to the parent
        frame when done in the frame changed to. :meth:`frame` is preferred over this method and
        should be used when possible. May not be supported by all drivers.

        Args:
            frame (Element | str): The iframe/frame element to switch to.
        """
    if isinstance(frame, Element):
        self.driver.switch_to_frame(frame)
        self._scopes.append('frame')
    elif frame == 'parent':
        if self._scopes[-1] != 'frame':
            raise ScopeError('`switch_to_frame("parent")` cannot be called from inside a descendant frame\'s `scope` context.')
        self._scopes.pop()
        self.driver.switch_to_frame('parent')
    elif frame == 'top':
        if 'frame' in self._scopes:
            idx = self._scopes.index('frame')
            if any([scope not in ['frame', None] for scope in self._scopes[idx:]]):
                raise ScopeError('`switch_to_frame("top")` cannot be called from inside a descendant frame\'s `scope` context.')
            self._scopes = self._scopes[:idx]
            self.driver.switch_to_frame('top')
    else:
        raise ValueError('You must provide a frame element, "parent", or "top" when calling switch_to_frame')
def drop_tag(self):
    """
        Remove the tag, but not its children or text.  The children and text
        are merged into the parent.

        Example::

            >>> h = fragment_fromstring('<div>Hello <b>World!</b></div>')
            >>> h.find('.//b').drop_tag()
            >>> print(tostring(h, encoding='unicode'))
            <div>Hello World!</div>
        """
    parent = self.getparent()
    assert parent is not None
    previous = self.getprevious()
    if self.text and isinstance(self.tag, basestring):
        if previous is None:
            parent.text = (parent.text or '') + self.text
        else:
            previous.tail = (previous.tail or '') + self.text
    if self.tail:
        if len(self):
            last = self[-1]
            last.tail = (last.tail or '') + self.tail
        elif previous is None:
            parent.text = (parent.text or '') + self.tail
        else:
            previous.tail = (previous.tail or '') + self.tail
    index = parent.index(self)
    parent[index:index + 1] = self[:]
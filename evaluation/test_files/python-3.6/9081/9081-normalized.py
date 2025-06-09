def destroy(self):
    """ A reimplemented destructor.

        This destructor will clear the reference to the toolkit widget
        and set its parent to None.

        """
    widget = self.widget
    if widget is not None:
        parent = widget.getparent()
        if parent is not None:
            parent.remove(widget)
        del self.widget
        d = self.declaration
        try:
            del CACHE[d.ref]
        except KeyError:
            pass
    super(WebComponent, self).destroy()
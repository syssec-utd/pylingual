def draw(self):
    """
        Draws the submenu and its background.
        
        Note that this leaves the OpenGL state set to 2d drawing.
        """
    self.window.set2d()
    if isinstance(self.bg, Layer):
        self.bg._draw()
    elif hasattr(self.bg, 'draw') and callable(self.bg.draw):
        self.bg.draw()
    elif isinstance(self.bg, list) or isinstance(self.bg, tuple):
        self.bg_vlist.draw(GL_QUADS)
    elif callable(self.bg):
        self.bg()
    elif isinstance(self.bg, Background):
        if not self.bg.initialized:
            self.bg.init_bg()
            self.bg.redraw_bg()
            self.bg.initialized = True
    elif self.bg == 'blank':
        pass
    else:
        raise TypeError('Unknown background type')
    self.window.set2d()
    for widget in self.widgets.values():
        if widget.do_redraw:
            widget.on_redraw()
            widget.do_redraw = False
    self.batch2d.draw()
    for widget in self.widgets.values():
        widget.draw()
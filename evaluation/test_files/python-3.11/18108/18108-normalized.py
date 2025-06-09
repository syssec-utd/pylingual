def set_font_size(self, size):
    """Convenience method for just changing font size."""
    if self.font.font_size == size:
        pass
    else:
        self.font._set_size(size)
def text_width(self, text: str) -> float:
    """Returns the width, in pixels, of a string in DejaVu Sans 110pt."""
    (width, _) = self._font.getsize(text)
    return width
from __future__ import annotations
from prettyqt import gui
FORMAT_1 = gui.TextCharFormat()
FORMAT_1.set_background_color('lightgreen')
FORMAT_2 = gui.TextCharFormat()
FORMAT_2.set_background_color('lightblue')

class RegexMatchHighlighter(gui.SyntaxHighlighter):

    def __init__(self, document=None):
        super().__init__(document)
        self.spans: list[tuple[int, int]] | None = []

    def set_spans(self, spans: list[tuple[int, int]] | None):
        self.spans = spans
        self.rehighlight()

    def _colorize(self, line_pos: int, match_len: int, match_num: int):
        fmt = FORMAT_1 if match_num % 2 == 0 else FORMAT_2
        self.setFormat(line_pos, match_len, fmt)

    def highlightBlock(self, text: str):
        block = self.currentBlock()
        start_char = block.position()
        end_char = start_char + block.length()
        if not self.spans or not text:
            return None
        for (i, (start, end)) in enumerate(self.spans):
            if end < start_char:
                continue
            if start > end_char:
                break
            starts_in_line = start_char <= start <= end_char
            ends_in_line = start_char <= end <= end_char
            if starts_in_line and ends_in_line or (not ends_in_line and starts_in_line):
                self._colorize(start - start_char, end - start, i)
            elif ends_in_line:
                self._colorize(0, end - start, i)
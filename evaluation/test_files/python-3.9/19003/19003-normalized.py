def _sentences(self, clean_visible):
    """generate strings identified as sentences"""
    previous_end = 0
    clean_visible = clean_visible.decode('utf8')
    for (start, end) in self.sentence_tokenizer.span_tokenize(clean_visible):
        if start < previous_end:
            start = previous_end
            if start > end:
                continue
        try:
            label = self.label_index.find_le(end)
        except ValueError:
            label = None
        if label:
            off = label.offsets[OffsetType.CHARS]
            end = max(off.first + off.length, end)
        previous_end = end
        sent_str = clean_visible[start:end]
        yield (start, end, sent_str)
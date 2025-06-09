def draw_x_labels(self):
    """Draw the X axis labels"""
    if self.show_x_labels:
        labels = self.get_x_labels()
        count = len(labels)
        labels = enumerate(iter(labels))
        start = int(not self.step_include_first_x_label)
        labels = itertools.islice(labels, start, None, self.step_x_labels)
        list(map(self.draw_x_label, labels))
        self.draw_x_guidelines(self.field_width(), count)
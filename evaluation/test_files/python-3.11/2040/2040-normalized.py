def _compute_widget_sizes(self):
    """Initial rendering stage, done in order to compute widths of all widgets."""
    wl = [0] * len(self._widgets)
    flex_count = 0
    for i, widget in enumerate(self._widgets):
        if isinstance(widget, ProgressBarFlexibleWidget):
            flex_count += 1
        else:
            wl[i] = widget.render(1).length
    remaining_width = self._width - sum(wl)
    remaining_width -= len(self._widgets) - 1
    if remaining_width < 10 * flex_count:
        if self._file_mode:
            remaining_width = 10 * flex_count
        else:
            widget0 = self._widgets[0]
            if isinstance(widget0, PBWString) and remaining_width + widget0.render(0).length >= 10 * flex_count:
                remaining_width += widget0.render(0).length + 1
                self._to_render = widget0.render(0).rendered + '\n'
                self._widgets = self._widgets[1:]
            if remaining_width < 10 * flex_count:
                self._file_mode = True
                remaining_width = 10 * flex_count
    remaining_width = max(remaining_width, 10 * flex_count)
    for i, widget in enumerate(self._widgets):
        if isinstance(widget, ProgressBarFlexibleWidget):
            target_length = int(remaining_width / flex_count)
            result = widget.render(1, target_length)
            wl[i] = result.length
            remaining_width -= result.length
            flex_count -= 1
    return wl
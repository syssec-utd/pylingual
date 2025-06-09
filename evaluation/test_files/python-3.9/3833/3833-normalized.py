def _hide_tick_lines_and_labels(axis):
    """
    Set visible property of ticklines and ticklabels of an axis to False
    """
    for item in axis.get_ticklines() + axis.get_ticklabels():
        item.set_visible(False)
def display_html(*objs, **kwargs):
    """Display the HTML representation of an object.

    Parameters
    ----------
    objs : tuple of objects
        The Python objects to display, or if raw=True raw HTML data to
        display.
    raw : bool
        Are the data objects raw data or Python objects that need to be
        formatted before display? [default: False]
    """
    raw = kwargs.pop('raw', False)
    if raw:
        for obj in objs:
            publish_html(obj)
    else:
        display(*objs, include=['text/plain', 'text/html'])
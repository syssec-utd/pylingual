def page(strng, start=0, screen_lines=0, pager_cmd=None, html=None, auto_html=False):
    """Print a string, piping through a pager.

    This version ignores the screen_lines and pager_cmd arguments and uses
    IPython's payload system instead.

    Parameters
    ----------
    strng : str
      Text to page.

    start : int
      Starting line at which to place the display.
    
    html : str, optional
      If given, an html string to send as well.

    auto_html : bool, optional
      If true, the input string is assumed to be valid reStructuredText and is
      converted to HTML with docutils.  Note that if docutils is not found,
      this option is silently ignored.

    Note
    ----

    Only one of the ``html`` and ``auto_html`` options can be given, not
    both.
    """
    start = max(0, start)
    shell = InteractiveShell.instance()
    if auto_html:
        try:
            defaults = {'file_insertion_enabled': 0, 'raw_enabled': 0, '_disable_config': 1}
            html = publish_string(strng, writer_name='html', settings_overrides=defaults)
        except:
            pass
    payload = dict(source='IPython.zmq.page.page', text=strng, html=html, start_line_number=start)
    shell.payload_manager.write_payload(payload)
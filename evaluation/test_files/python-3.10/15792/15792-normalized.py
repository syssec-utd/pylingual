def parse(filename_or_url, parser=None, base_url=None, **kw):
    """
    Parse a filename, URL, or file-like object into an HTML document
    tree.  Note: this returns a tree, not an element.  Use
    ``parse(...).getroot()`` to get the document root.

    You can override the base URL with the ``base_url`` keyword.  This
    is most useful when parsing from a file-like object.
    """
    if parser is None:
        parser = html_parser
    return etree.parse(filename_or_url, parser, base_url=base_url, **kw)
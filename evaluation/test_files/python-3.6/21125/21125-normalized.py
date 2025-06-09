def format_display_data(obj, include=None, exclude=None):
    """Return a format data dict for an object.

    By default all format types will be computed.

    The following MIME types are currently implemented:

    * text/plain
    * text/html
    * text/latex
    * application/json
    * application/javascript
    * image/png
    * image/jpeg
    * image/svg+xml

    Parameters
    ----------
    obj : object
        The Python object whose format data will be computed.

    Returns
    -------
    format_dict : dict
        A dictionary of key/value pairs, one or each format that was
        generated for the object. The keys are the format types, which
        will usually be MIME type strings and the values and JSON'able
        data structure containing the raw data for the representation in
        that format.
    include : list or tuple, optional
        A list of format type strings (MIME types) to include in the
        format data dict. If this is set *only* the format types included
        in this list will be computed.
    exclude : list or tuple, optional
        A list of format type string (MIME types) to exclue in the format
        data dict. If this is set all format types will be computed,
        except for those included in this argument.
    """
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.instance().display_formatter.format(obj, include, exclude)
def xhtml_to_html(xhtml):
    """Convert all tags in an XHTML tree to HTML by removing their
    XHTML namespace.
    """
    try:
        xhtml = xhtml.getroot()
    except AttributeError:
        pass
    prefix = '{%s}' % XHTML_NAMESPACE
    prefix_len = len(prefix)
    for el in xhtml.iter(prefix + '*'):
        el.tag = el.tag[prefix_len:]
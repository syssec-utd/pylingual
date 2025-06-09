def nbviewer_link(url):
    """Return the link to the Jupyter nbviewer for the given notebook url"""
    if six.PY2:
        from urlparse import urlparse as urlsplit
    else:
        from urllib.parse import urlsplit
    info = urlsplit(url)
    domain = info.netloc
    url_type = 'github' if domain == 'github.com' else 'url'
    return 'https://nbviewer.jupyter.org/%s%s' % (url_type, info.path)
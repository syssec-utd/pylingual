def resolve_base_href(self, handle_failures=None):
    """
        Find any ``<base href>`` tag in the document, and apply its
        values to all links found in the document.  Also remove the
        tag once it has been applied.

        If ``handle_failures`` is None (default), a failure to process
        a URL will abort the processing.  If set to 'ignore', errors
        are ignored.  If set to 'discard', failing URLs will be removed.
        """
    base_href = None
    basetags = self.xpath('//base[@href]|//x:base[@href]', namespaces={'x': XHTML_NAMESPACE})
    for b in basetags:
        base_href = b.get('href')
        b.drop_tree()
    if not base_href:
        return
    self.make_links_absolute(base_href, resolve_base_href=False, handle_failures=handle_failures)
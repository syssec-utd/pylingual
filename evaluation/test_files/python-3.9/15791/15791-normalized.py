def fromstring(html, base_url=None, parser=None, **kw):
    """
    Parse the html, returning a single element/document.

    This tries to minimally parse the chunk of text, without knowing if it
    is a fragment or a document.

    base_url will set the document's base_url attribute (and the tree's docinfo.URL)
    """
    if parser is None:
        parser = html_parser
    if isinstance(html, bytes):
        is_full_html = _looks_like_full_html_bytes(html)
    else:
        is_full_html = _looks_like_full_html_unicode(html)
    doc = document_fromstring(html, parser=parser, base_url=base_url, **kw)
    if is_full_html:
        return doc
    bodies = doc.findall('body')
    if not bodies:
        bodies = doc.findall('{%s}body' % XHTML_NAMESPACE)
    if bodies:
        body = bodies[0]
        if len(bodies) > 1:
            for other_body in bodies[1:]:
                if other_body.text:
                    if len(body):
                        body[-1].tail = (body[-1].tail or '') + other_body.text
                    else:
                        body.text = (body.text or '') + other_body.text
                body.extend(other_body)
                other_body.drop_tree()
    else:
        body = None
    heads = doc.findall('head')
    if not heads:
        heads = doc.findall('{%s}head' % XHTML_NAMESPACE)
    if heads:
        head = heads[0]
        if len(heads) > 1:
            for other_head in heads[1:]:
                head.extend(other_head)
                other_head.drop_tree()
        return doc
    if body is None:
        return doc
    if len(body) == 1 and (not body.text or not body.text.strip()) and (not body[-1].tail or not body[-1].tail.strip()):
        return body[0]
    if _contains_block_level_tag(body):
        body.tag = 'div'
    else:
        body.tag = 'span'
    return body
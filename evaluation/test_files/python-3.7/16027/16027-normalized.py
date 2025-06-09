def htmldiff(old_html, new_html):
    """ Do a diff of the old and new document.  The documents are HTML
    *fragments* (str/UTF8 or unicode), they are not complete documents
    (i.e., no <html> tag).

    Returns HTML with <ins> and <del> tags added around the
    appropriate text.  

    Markup is generally ignored, with the markup from new_html
    preserved, and possibly some markup from old_html (though it is
    considered acceptable to lose some of the old markup).  Only the
    words in the HTML are diffed.  The exception is <img> tags, which
    are treated like words, and the href attribute of <a> tags, which
    are noted inside the tag itself when there are changes.
    """
    old_html_tokens = tokenize(old_html)
    new_html_tokens = tokenize(new_html)
    result = htmldiff_tokens(old_html_tokens, new_html_tokens)
    result = ''.join(result).strip()
    return fixup_ins_del_tags(result)
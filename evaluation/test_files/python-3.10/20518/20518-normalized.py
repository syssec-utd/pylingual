def highlight(string, keywords, cls_name='highlighted'):
    """ Given an list of words, this function highlights the matched text in the given string. """
    if not keywords:
        return string
    if not string:
        return ''
    (include, exclude) = get_text_tokenizer(keywords)
    highlighted = highlight_text(include, string, cls_name)
    return highlighted
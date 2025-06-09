def get_element_content(p, meta_data, is_td=False, remove_italics=False, remove_bold=False):
    """
    P tags are made up of several runs (r tags) of text. This function takes a
    p tag and constructs the text that should be part of the p tag.

    image_handler should be a callable that returns the desired ``src``
    attribute for a given image.
    """
    if not is_td and is_header(p, meta_data):
        (remove_bold, remove_italics) = whole_line_styled(p)
    p_text = ''
    w_namespace = get_namespace(p, 'w')
    if len(p) == 0:
        return ''
    content_tags = ('%sr' % w_namespace, '%shyperlink' % w_namespace, '%sins' % w_namespace, '%ssmartTag' % w_namespace)
    elements_with_content = []
    for child in p:
        if child is None:
            break
        if child.tag in content_tags:
            elements_with_content.append(child)
    for el in elements_with_content:
        if el.tag in ('%sins' % w_namespace, '%ssmartTag' % w_namespace):
            p_text += get_element_content(el, meta_data, remove_bold=remove_bold, remove_italics=remove_italics)
        elif el.tag == '%shyperlink' % w_namespace:
            p_text += build_hyperlink(el, meta_data)
        elif el.tag == '%sr' % w_namespace:
            p_text += get_text_run_content(el, meta_data, remove_bold=remove_bold, remove_italics=remove_italics)
        else:
            raise SyntaxNotSupported('Content element "%s" not handled.' % el.tag)
    return p_text
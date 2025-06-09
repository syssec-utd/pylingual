def replace_chars_for_svg_code(svg_content):
    """ Replace known special characters to SVG code.

    Parameters
    ----------
    svg_content: str

    Returns
    -------
    corrected_svg: str
        Corrected SVG content
    """
    result = svg_content
    svg_char = [('&', '&amp;'), ('>', '&gt;'), ('<', '&lt;'), ('"', '&quot;')]
    for (c, entity) in svg_char:
        result = result.replace(c, entity)
    return result
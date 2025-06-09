def blend_html_colour_to_white(html_colour, alpha):
    """
    :param html_colour: Colour string like FF552B or #334455
    :param alpha: Alpha value
    :return: Html colour alpha blended onto white
    """
    html_colour = html_colour.upper()
    has_hash = False
    if html_colour[0] == '#':
        has_hash = True
        html_colour = html_colour[1:]
    r_str = html_colour[0:2]
    g_str = html_colour[2:4]
    b_str = html_colour[4:6]
    r = int(r_str, 16)
    g = int(g_str, 16)
    b = int(b_str, 16)
    r = int(alpha * r + (1 - alpha) * 255)
    g = int(alpha * g + (1 - alpha) * 255)
    b = int(alpha * b + (1 - alpha) * 255)
    out = '{:02X}{:02X}{:02X}'.format(r, g, b)
    if has_hash:
        out = '#' + out
    return out
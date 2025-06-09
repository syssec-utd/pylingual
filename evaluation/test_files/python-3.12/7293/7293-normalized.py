def lookup_color(c):
    """Return RGBA values of color c

    c should be either an X11 color or a brewer color set and index
    e.g. "navajowhite", "greens3/2"

    """
    import sys
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('PangoCairo', '1.0')
    from gi.repository import Gdk
    try:
        color = Gdk.color_parse(c)
    except ValueError:
        pass
    else:
        s = 1.0 / 65535.0
        r = color.red * s
        g = color.green * s
        b = color.blue * s
        a = 1.0
        return (r, g, b, a)
    try:
        dummy, scheme, index = c.split('/')
        r, g, b = brewer_colors[scheme][int(index)]
    except (ValueError, KeyError):
        pass
    else:
        s = 1.0 / 255.0
        r = r * s
        g = g * s
        b = b * s
        a = 1.0
        return (r, g, b, a)
    sys.stderr.write("warning: unknown color '%s'\n" % c)
    return None
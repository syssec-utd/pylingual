def sheet_from_template(name, colors='lightbg'):
    """Use one of the base templates, and set bg/fg/select colors."""
    colors = colors.lower()
    if colors == 'lightbg':
        return default_light_style_template % get_colors(name)
    elif colors == 'linux':
        return default_dark_style_template % get_colors(name)
    elif colors == 'nocolor':
        return default_bw_style_sheet
    else:
        raise KeyError('No such color scheme: %s' % colors)
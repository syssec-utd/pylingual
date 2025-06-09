def build_component(res, parent=None):
    """Create a gui2py control based on the python resource"""
    kwargs = dict(res.items())
    comtype = kwargs.pop('type')
    if 'components' in res:
        components = kwargs.pop('components')
    elif comtype == 'Menu' and 'items' in res:
        components = kwargs.pop('items')
    else:
        components = []
    from gui import registry
    if comtype in registry.CONTROLS:
        comclass = registry.CONTROLS[comtype]
    elif comtype in registry.MENU:
        comclass = registry.MENU[comtype]
    elif comtype in registry.MISC:
        comclass = registry.MISC[comtype]
    else:
        raise RuntimeError('%s not in registry' % comtype)
    com = comclass(parent=parent, **kwargs)
    for comp in components:
        build_component(comp, parent=com)
    return com
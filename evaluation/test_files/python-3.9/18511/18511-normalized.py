def set_one(chainmap, thing_name, callobject):
    """ Add a mapping with key thing_name for callobject in chainmap with
        namespace handling.
    """
    namespaces = reversed(thing_name.split('.'))
    lstname = []
    for name in namespaces:
        lstname.insert(0, name)
        strname = '.'.join(lstname)
        chainmap[strname] = callobject
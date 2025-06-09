def create_typestr2type_dicts(dont_include_in_type2typestr=['lambda']):
    """Return dictionaries mapping lower case typename (e.g. 'tuple') to type
    objects from the types package, and vice versa."""
    typenamelist = [tname for tname in dir(types) if tname.endswith('Type')]
    typestr2type, type2typestr = ({}, {})
    for tname in typenamelist:
        name = tname[:-4].lower()
        obj = getattr(types, tname)
        typestr2type[name] = obj
        if name not in dont_include_in_type2typestr:
            type2typestr[obj] = name
    return (typestr2type, type2typestr)
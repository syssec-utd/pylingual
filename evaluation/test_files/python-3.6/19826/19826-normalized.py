def mk_enum(s_edt):
    """
    Create a named tuple from a BridgePoint enumeration.
    """
    s_dt = one(s_edt).S_DT[17]()
    enums = list()
    kwlist = ['False', 'None', 'True'] + keyword.kwlist
    for enum in many(s_edt).S_ENUM[27]():
        if enum.Name in kwlist:
            enums.append(enum.Name + '_')
        else:
            enums.append(enum.Name)
    Enum = collections.namedtuple(s_dt.Name, enums)
    return Enum(*range(len(enums)))
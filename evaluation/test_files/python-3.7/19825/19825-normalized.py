def _get_related_attributes(r_rgo, r_rto):
    """
    The two lists of attributes which relates two classes in an association.
    """
    l1 = list()
    l2 = list()
    ref_filter = lambda ref: ref.OIR_ID == r_rgo.OIR_ID
    for o_ref in many(r_rto).O_RTIDA[110].O_REF[111](ref_filter):
        o_attr = one(o_ref).O_RATTR[108].O_ATTR[106]()
        l1.append(o_attr.Name)
        o_attr = one(o_ref).O_RTIDA[111].O_OIDA[110].O_ATTR[105]()
        l2.append(o_attr.Name)
    return (l1, l2)
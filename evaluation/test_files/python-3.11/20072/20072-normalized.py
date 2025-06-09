def unrelate(from_instance, to_instance, rel_id, phrase=''):
    """
    Unrelate *from_instance* from *to_instance* across *rel_id*. For reflexive
    associations, a *phrase* indicating the direction must also be provided.
    
    The two instances are unrelated from each other by reseting the identifying
    attributes on the FROM side of the association. Updated values which affect
    existing associations are propagated. A set of all affected instances will
    be returned.
    """
    if None in [from_instance, to_instance]:
        return False
    inst1, inst2, ass = _find_link(from_instance, to_instance, rel_id, phrase)
    if not ass.source_link.disconnect(inst1, inst2):
        raise UnrelateException(from_instance, to_instance, rel_id, phrase)
    if not ass.target_link.disconnect(inst2, inst1):
        raise UnrelateException(from_instance, to_instance, rel_id, phrase)
    return True
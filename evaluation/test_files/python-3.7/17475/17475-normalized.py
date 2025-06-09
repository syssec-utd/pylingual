def get_change_values(change):
    """
    In the case of deletions, we pull the change values for the XML request
    from the ResourceRecordSet._initial_vals dict, since we want the original
    values. For creations, we pull from the attributes on ResourceRecordSet.

    Since we're dealing with attributes vs. dict key/vals, we'll abstract
    this part away here and just always pass a dict to write_change.

    :rtype: dict
    :returns: A dict of change data, used by :py:func:`write_change` to
        write the change request XML.
    """
    (action, rrset) = change
    if action == 'CREATE':
        values = dict()
        for (key, val) in rrset._initial_vals.items():
            values[key] = getattr(rrset, key)
        return values
    else:
        return rrset._initial_vals
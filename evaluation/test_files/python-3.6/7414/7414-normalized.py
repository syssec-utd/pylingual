def mBank_set_tnr(transactions, tag, tag_dict, *args):
    """
    mBank Collect states TNR in transaction details as unique id for
    transactions, that may be used to identify the same transactions in
    different statement files eg. partial mt942 and full mt940
    Information about tnr uniqueness has been obtained from mBank support,
    it lacks in mt940 mBank specification.
    """
    matches = tnr_re.search(tag_dict[tag.slug])
    if matches:
        tag_dict['tnr'] = matches.groupdict()['tnr']
    return tag_dict
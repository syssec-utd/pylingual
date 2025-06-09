def metadata_id(item):
    """Extracts the identifier from a Confluence item.

        This identifier will be the mix of two fields because a
        historical content does not have any unique identifier.
        In this case, 'id' and 'version' values are combined because
        it should not be possible to have two equal version numbers
        for the same content. The value to return will follow the
        pattern: <content>#v<version> (i.e 28979#v10).
        """
    cid = item['id']
    cversion = item['version']['number']
    return str(cid) + '#v' + str(cversion)
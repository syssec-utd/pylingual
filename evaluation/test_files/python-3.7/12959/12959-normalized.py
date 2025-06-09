def get_agency_id(relation):
    """Construct an id for agency using its tags."""
    op = relation.tags.get('operator')
    if op:
        return int(hashlib.sha256(op.encode('utf-8')).hexdigest(), 16) % 10 ** 8
    return -1
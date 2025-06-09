def is_embargoed(record):
    """Template filter to check if a record is embargoed."""
    return record.get('access_right') == 'embargoed' and record.get('embargo_date') and (record.get('embargo_date') > datetime.utcnow().date())
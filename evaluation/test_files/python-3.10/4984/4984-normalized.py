def __build_payload(self, size, operation=False, startdate=None):
    """Build payload"""
    payload = {'ws.size': size, 'order_by': 'date_last_updated', 'omit_duplicates': 'false', 'status': ['New', 'Incomplete', 'Opinion', 'Invalid', "Won't Fix", 'Expired', 'Confirmed', 'Triaged', 'In Progress', 'Fix Committed', 'Fix Released', 'Incomplete (with response)', 'Incomplete (without response)']}
    if operation:
        payload['ws.op'] = 'searchTasks'
    if startdate:
        startdate = startdate.isoformat()
        payload['modified_since'] = startdate
    return payload
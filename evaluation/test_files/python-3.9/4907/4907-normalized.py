def notes(self, item_type, item_id):
    """Get the notes from pagination"""
    payload = {'order_by': 'updated_at', 'sort': 'asc', 'per_page': PER_PAGE}
    path = urijoin(item_type, str(item_id), GitLabClient.NOTES)
    return self.fetch_items(path, payload)
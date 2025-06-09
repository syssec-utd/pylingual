def json_data(self, data=None):
    """Adds the default_data to data and dumps it to a json."""
    if data is None:
        data = {}
    data.update(self.default_data)
    return json.dumps(data)
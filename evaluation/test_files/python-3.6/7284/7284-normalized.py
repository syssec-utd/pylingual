def get_dataset(self, workspace_id, dataset_id):
    """Runs HTTP GET request to retrieve a single dataset."""
    api_path = self.DATASOURCE_URI_FMT.format(workspace_id, dataset_id)
    return self._send_get_req(api_path)
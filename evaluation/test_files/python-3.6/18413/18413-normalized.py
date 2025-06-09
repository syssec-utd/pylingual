def _handle_results(self):
    """
        Call back function to be implemented by the CLI.
        """
    if self._api_result.status_code == requests.codes.ok:
        if self.format == 'json':
            self.output_json(self._api_result.text)
        elif self.format == 'csv':
            self.output_csv(self._api_result.text)
        elif self.format == 'raw':
            self.output_raw(self._api_result.text)
        elif self.format == 'xml':
            self.output_xml(self._api_result.text)
    else:
        pass
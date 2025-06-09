def import_image(self, image_data):
    """**Description**
            Import an image from the scanner export

        **Arguments**
            - image_data: A JSON with the image information.

        **Success Return Value**
            A JSON object representing the image that was imported.
        """
    url = self.url + '/api/scanning/v1/anchore/imageimport'
    res = requests.post(url, data=json.dumps(image_data), headers=self.hdrs, verify=self.ssl_verify)
    if not self._checkResponse(res):
        return [False, self.lasterr]
    return [True, res.json()]
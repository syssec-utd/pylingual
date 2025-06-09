def add_device(self, device_id):
    """ Method for `Add device to collection <https://m2x.att.com/developer/documentation/v2/collections#Add-device-to-collection>`_ endpoint.

        :param device_id: ID of the Device being added to Collection
        :type device_id: str

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
    path = self.subpath('/devices/{device_id}'.format(device_id=device_id))
    return self.api.put(path)
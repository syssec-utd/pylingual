def create(self, deviceType):
    """
        Register one or more new device types, each request can contain a maximum of 512KB.
        """
    r = self._apiClient.post('api/v0002/device/types', deviceType)
    if r.status_code == 201:
        return DeviceType(apiClient=self._apiClient, **r.json())
    else:
        raise ApiException(r)
def getStatus(self, requestId, typeId=None, deviceId=None):
    """
        Get a list of device management request device statuses.
        Get an individual device mangaement request device status.
        """
    if typeId is None or deviceId is None:
        url = MgmtRequests.mgmtRequestStatus % requestId
        r = self._apiClient.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            raise ApiException(r)
    else:
        url = MgmtRequests.mgmtRequestSingleDeviceStatus % (requestId, typeId, deviceId)
        r = self._apiClient.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            raise ApiException(r)
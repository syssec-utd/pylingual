def get(self, requestId):
    """
        Gets details of a device management request.
        It accepts requestId (string) as parameters
        In case of failure it throws APIException
        """
    url = MgmtRequests.mgmtSingleRequest % requestId
    r = self._apiClient.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        raise ApiException(r)
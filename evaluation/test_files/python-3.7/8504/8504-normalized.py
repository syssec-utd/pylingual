def delete(self, requestId):
    """
        Clears the status of a device management request.
        You can use this operation to clear the status for a completed request, or for an in-progress request which may never complete due to a problem.
        It accepts requestId (string) as parameters
        In case of failure it throws APIException
        """
    url = MgmtRequests.mgmtSingleRequest % requestId
    r = self._apiClient.delete(url)
    if r.status_code == 204:
        return True
    else:
        raise ApiException(r)
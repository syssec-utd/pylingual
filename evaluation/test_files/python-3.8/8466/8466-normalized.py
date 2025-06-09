def getLogicalInterfacesOnDeviceType(self, typeId, draft=False):
    """
        Get all logical interfaces for a device type.
        Parameters:
          - typeId (string)
          - draft (boolean)
        Returns:
            - list of logical interface ids
            - HTTP response object
        Throws APIException on failure.
        """
    if draft:
        req = ApiClient.allDeviceTypeLogicalInterfacesUrl % (self.host, '/draft', typeId)
    else:
        req = ApiClient.allDeviceTypeLogicalInterfacesUrl % (self.host, '', typeId)
    resp = requests.get(req, auth=self.credentials, verify=self.verify)
    if resp.status_code == 200:
        self.logger.debug('All device type logical interfaces retrieved')
    else:
        raise ibmiotf.APIException(resp.status_code, 'HTTP error getting all device type logical interfaces', resp)
    return ([appintf['id'] for appintf in resp.json()], resp.json())
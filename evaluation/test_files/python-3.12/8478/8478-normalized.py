def removeLogicalInterfaceFromThingType(self, thingTypeId, logicalInterfaceId):
    """
        Removes a logical interface from a thing type.
        Parameters:
            - thingTypeId (string) - the thing type
            - logicalInterfaceId (string) - the id returned by the platform on creation of the logical interface
        Throws APIException on failure.
        """
    req = ApiClient.oneThingTypeLogicalInterfaceUrl % (self.host, thingTypeId, logicalInterfaceId)
    resp = requests.delete(req, auth=self.credentials, verify=self.verify)
    if resp.status_code == 204:
        self.logger.debug('Logical interface removed from a thing type')
    else:
        raise ibmiotf.APIException(resp.status_code, 'HTTP error removing logical interface from a thing type', resp)
    return resp
def addLogicalInterfaceToThingType(self, thingTypeId, logicalInterfaceId, schemaId=None, name=None):
    """
        Adds a logical interface to a thing type.
        Parameters:
            - thingTypeId (string) - the thing type
            - logicalInterfaceId (string) - the id returned by the platform on creation of the logical interface
        Throws APIException on failure.
        """
    req = ApiClient.allThingTypeLogicalInterfacesUrl % (self.host, '/draft', thingTypeId)
    body = {'id': logicalInterfaceId}
    resp = requests.post(req, auth=self.credentials, headers={'Content-Type': 'application/json'}, data=json.dumps(body), verify=self.verify)
    if resp.status_code == 201:
        self.logger.debug('The draft logical interface was successfully associated with the thing type.')
    else:
        raise ibmiotf.APIException(resp.status_code, 'HTTP error adding logical interface to a thing type', resp)
    return resp.json()
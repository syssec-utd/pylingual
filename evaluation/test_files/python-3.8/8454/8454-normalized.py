def createEvent(self, physicalInterfaceId, eventTypeId, eventId):
    """
        Create an event mapping for a physical interface.
        Parameters:
          physicalInterfaceId (string) - value returned by the platform when creating the physical interface
          eventTypeId (string) - value returned by the platform when creating the event type
          eventId (string) - matches the event id used by the device in the MQTT topic
        Throws APIException on failure.
        """
    req = ApiClient.allEventsUrl % (self.host, '/draft', physicalInterfaceId)
    body = {'eventId': eventId, 'eventTypeId': eventTypeId}
    resp = requests.post(req, auth=self.credentials, headers={'Content-Type': 'application/json'}, data=json.dumps(body), verify=self.verify)
    if resp.status_code == 201:
        self.logger.debug('Event mapping created')
    else:
        raise ibmiotf.APIException(resp.status_code, 'HTTP error creating event mapping', resp)
    return resp.json()
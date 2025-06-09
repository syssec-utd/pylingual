def addRuleToLogicalInterface(self, logicalInterfaceId, name, condition, description=None, alias=None):
    """
        Adds a rule to a logical interface.
        Parameters:
          - logicalInterfaceId (string)
          - name (string)
          - condition (string)
          - (description (string, optional)
        Returns: rule id (string), response (object).
        Throws APIException on failure.
        """
    req = ApiClient.allRulesForLogicalInterfaceUrl % (self.host, '/draft', logicalInterfaceId)
    body = {'name': name, 'condition': condition}
    if description:
        body['description'] = description
    resp = requests.post(req, auth=self.credentials, headers={'Content-Type': 'application/json'}, data=json.dumps(body), verify=self.verify)
    if resp.status_code == 201:
        self.logger.debug('Logical interface rule created')
    else:
        raise ibmiotf.APIException(resp.status_code, 'HTTP error creating logical interface rule', resp)
    return (resp.json()['id'], resp.json())
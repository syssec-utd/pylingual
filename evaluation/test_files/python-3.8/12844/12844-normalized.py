def request_pin(self):
    """ Method to request a PIN from ecobee for authorization """
    url = 'https://api.ecobee.com/authorize'
    params = {'response_type': 'ecobeePin', 'client_id': self.api_key, 'scope': 'smartWrite'}
    try:
        request = requests.get(url, params=params)
    except RequestException:
        logger.warn('Error connecting to Ecobee.  Possible connectivity outage.Could not request pin.')
        return
    self.authorization_code = request.json()['code']
    self.pin = request.json()['ecobeePin']
    logger.error('Please authorize your ecobee developer app with PIN code ' + self.pin + '\nGoto https://www.ecobee.com/consumerportal/index.html, click\nMy Apps, Add application, Enter Pin and click Authorize.\nAfter authorizing, call request_tokens() method.')
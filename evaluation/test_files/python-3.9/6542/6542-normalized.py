def get_url(self):
    """IFTTT Webhook url

        :return: url
        :rtype: str
        """
    if not self.data[self.execute_name]:
        raise InvalidConfig(extra_body='Value for IFTTT is required on {} device. Get your key here: https://ifttt.com/services/maker_webhooks/settings'.format(self.name))
    if not self.data.get('event'):
        raise InvalidConfig(extra_body='Event option is required for IFTTT on {} device. You define the event name when creating a Webhook applet'.format(self.name))
    url = self.url_pattern.format(event=self.data['event'], key=self.data[self.execute_name])
    return url
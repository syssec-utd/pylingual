def nameservers(self):
    """
        :rtype: list
        :returns: A list of nameserver strings for this hosted zone.
        """
    if not self._nameservers:
        hosted_zone = self.connection.get_hosted_zone_by_id(self.id)
        self._nameservers = hosted_zone._nameservers
    return self._nameservers
def devices(self, **params):
    """ Method for `List Devices from an existing Distribution <https://m2x.att.com/developer/documentation/v2/distribution#List-Devices-from-an-existing-Distribution>`_ endpoint.

        :param params: Query parameters passed as keyword arguments. View M2X API Docs for listing of available parameters.

        :return: List of Devices associated with this Distribution as :class:`.DistributionDevice` objects
        :rtype: `list <https://docs.python.org/2/library/functions.html#list>`_

        :raises: :class:`~requests.exceptions.HTTPError` if an error occurs when sending the HTTP request
        """
    return DistributionDevice.list(self.api, distribution_id=self.id, **params)
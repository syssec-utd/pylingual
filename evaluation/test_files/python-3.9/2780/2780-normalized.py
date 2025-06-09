def get_properties(self):
    """Perform an operation to update the properties of the entity.

        :returns: The properties of the entity as a dictionary.
        :rtype: dict[str, Any]
        :raises: ~azure.servicebus.common.errors.ServiceBusResourceNotFound if the entity does not exist.
        :raises: ~azure.servicebus.common.errors.ServiceBusConnectionError if the endpoint cannot be reached.
        :raises: ~azure.common.AzureHTTPError if the credentials are invalid.
        """
    try:
        self.entity = self._get_entity()
        self.properties = dict(self.entity)
        if hasattr(self.entity, 'requires_session'):
            self.requires_session = self.entity.requires_session
        return self.properties
    except AzureServiceBusResourceNotFound:
        raise ServiceBusResourceNotFound('Specificed queue does not exist.')
    except azure.common.AzureHttpError:
        self.entity = None
        self.properties = {}
        self.requires_session = False
    except requests.exceptions.ConnectionError as e:
        raise ServiceBusConnectionError('Namespace not found', e)
def get_namespace(self, name):
    """
        Get details about a specific namespace.

        name:
            Name of the service bus namespace.
        """
    response = self._perform_get(self._get_path('services/serviceBus/Namespaces', name), None)
    return _ServiceBusManagementXmlSerializer.xml_to_namespace(response.body)
def create_hosted_service(self, service_name, label, description=None, location=None, affinity_group=None, extended_properties=None):
    """
        Creates a new hosted service in Windows Azure.

        service_name:
            A name for the hosted service that is unique within Windows Azure.
            This name is the DNS prefix name and can be used to access the
            hosted service.
        label:
            A name for the hosted service. The name can be up to 100 characters
            in length. The name can be used to identify the storage account for
            your tracking purposes.
        description:
            A description for the hosted service. The description can be up to
            1024 characters in length.
        location:
            The location where the hosted service will be created. You can
            specify either a location or affinity_group, but not both.
        affinity_group:
            The name of an existing affinity group associated with this
            subscription. This name is a GUID and can be retrieved by examining
            the name element of the response body returned by
            list_affinity_groups. You can specify either a location or
            affinity_group, but not both.
        extended_properties:
            Dictionary containing name/value pairs of storage account
            properties. You can have a maximum of 50 extended property
            name/value pairs. The maximum length of the Name element is 64
            characters, only alphanumeric characters and underscores are valid
            in the Name, and the name must start with a letter. The value has
            a maximum length of 255 characters.
        """
    _validate_not_none('service_name', service_name)
    _validate_not_none('label', label)
    if affinity_group is None and location is None:
        raise ValueError('location or affinity_group must be specified')
    if affinity_group is not None and location is not None:
        raise ValueError('Only one of location or affinity_group needs to be specified')
    return self._perform_post(self._get_hosted_service_path(), _XmlSerializer.create_hosted_service_to_xml(service_name, label, description, location, affinity_group, extended_properties), as_async=True)
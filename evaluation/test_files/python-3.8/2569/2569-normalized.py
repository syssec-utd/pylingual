def create_reserved_ip_address(self, name, label=None, location=None):
    """
        Reserves an IPv4 address for the specified subscription.

        name:
            Required. Specifies the name for the reserved IP address.
        label:
            Optional. Specifies a label for the reserved IP address. The label
            can be up to 100 characters long and can be used for your tracking
            purposes.
        location:
            Required. Specifies the location of the reserved IP address. This
            should be the same location that is assigned to the cloud service
            containing the deployment that will use the reserved IP address.
            To see the available locations, you can use list_locations.
        """
    _validate_not_none('name', name)
    return self._perform_post(self._get_reserved_ip_path(), _XmlSerializer.create_reserved_ip_to_xml(name, label, location), as_async=True)
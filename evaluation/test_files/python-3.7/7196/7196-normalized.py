def validate(self):
    """
        Error check the attributes of the ActivateRequestPayload object.
        """
    if self.unique_identifier is not None:
        if not isinstance(self.unique_identifier, attributes.UniqueIdentifier):
            msg = 'invalid unique identifier'
            raise TypeError(msg)
def get(self, personId):
    """Get a person's details, by ID.

        Args:
            personId(basestring): The ID of the person to be retrieved.

        Returns:
            Person: A Person object with the details of the requested person.

        Raises:
            TypeError: If the parameter types are incorrect.
            ApiError: If the Webex Teams cloud returns an error.

        """
    check_type(personId, basestring, may_be_none=False)
    json_data = self._session.get(API_ENDPOINT + '/' + personId)
    return self._object_factory(OBJECT_TYPE, json_data)
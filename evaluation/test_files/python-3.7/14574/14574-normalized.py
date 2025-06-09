def create_organisation(self, organisation_json):
    """
        Create an Organisation object from a JSON object

        Returns:
            Organisation: The organisation from the given `organisation_json`.
        """
    return trolly.organisation.Organisation(trello_client=self, organisation_id=organisation_json['id'], name=organisation_json['name'], data=organisation_json)
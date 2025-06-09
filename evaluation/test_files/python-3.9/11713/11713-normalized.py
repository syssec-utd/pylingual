def disease_term(self, disease_identifier):
    """Return a disease term

        Checks if the identifier is a disease number or a id

        Args:
            disease_identifier(str)

        Returns:
            disease_obj(dict)
        """
    query = {}
    try:
        disease_identifier = int(disease_identifier)
        query['disease_nr'] = disease_identifier
    except ValueError:
        query['_id'] = disease_identifier
    return self.disease_term_collection.find_one(query)
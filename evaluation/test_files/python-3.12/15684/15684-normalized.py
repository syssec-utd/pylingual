def get_metadata(ontology, ols_base=None):
    """Gets the metadata for a given ontology

    :param str ontology: The name of the ontology
    :param str ols_base: An optional, custom OLS base url
    :return: The dictionary representing the JSON from the OLS
    :rtype: dict
    """
    client = OlsClient(ols_base=ols_base)
    return client.get_ontology(ontology)
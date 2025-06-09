def extract_params_from_query(query, user_ns):
    """Generates a dictionary with safe keys and values to pass onto Neo4j

    :param query: string with the Cypher query to execute
    :param user_ns: dictionary with the IPython user space
    """
    params = {}
    for k, v in user_ns.items():
        try:
            json.dumps(v)
            params[k] = v
        except:
            pass
    return params
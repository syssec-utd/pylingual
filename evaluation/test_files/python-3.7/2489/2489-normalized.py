def parse_response(response, return_type):
    """
        Parse the HTTPResponse's body and fill all the data into a class of
        return_type.
        """
    doc = minidom.parseString(response.body)
    return_obj = return_type()
    xml_name = return_type._xml_name if hasattr(return_type, '_xml_name') else return_type.__name__
    for node in _MinidomXmlToObject.get_child_nodes(doc, xml_name):
        _MinidomXmlToObject._fill_data_to_return_object(node, return_obj)
    return return_obj
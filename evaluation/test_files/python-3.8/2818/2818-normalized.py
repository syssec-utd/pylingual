def parse_enum_results_list(response, return_type, resp_type, item_type):
    """resp_body is the XML we received
        resp_type is a string, such as Containers,
        return_type is the type we're constructing, such as ContainerEnumResults
        item_type is the type object of the item to be created, such as Container

        This function then returns a ContainerEnumResults object with the
        containers member populated with the results.
        """
    return_obj = return_type()
    root = ETree.fromstring(response.body)
    items = []
    for container_element in root.findall(resp_type):
        for item_element in container_element.findall(resp_type[:-1]):
            items.append(_ETreeXmlToObject.fill_instance_element(item_element, item_type))
    for (name, value) in vars(return_obj).items():
        if name == resp_type.lower():
            continue
        value = _ETreeXmlToObject.fill_data_member(root, name, value)
        if value is not None:
            setattr(return_obj, name, value)
    setattr(return_obj, resp_type.lower(), items)
    return return_obj
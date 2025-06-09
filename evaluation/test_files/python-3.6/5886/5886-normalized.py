def class_names(self, nodes):
    """return class names if needed in diagram"""
    names = []
    for node in nodes:
        if isinstance(node, astroid.Instance):
            node = node._proxied
        if isinstance(node, astroid.ClassDef) and hasattr(node, 'name') and (not self.has_node(node)):
            if node.name not in names:
                node_name = node.name
                names.append(node_name)
    return names
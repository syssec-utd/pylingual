def extract_relationships(self):
    """extract relation ships between nodes in the diagram
        """
    for obj in self.classes():
        node = obj.node
        obj.attrs = self.get_attrs(node)
        obj.methods = self.get_methods(node)
        if is_interface(node):
            obj.shape = 'interface'
        else:
            obj.shape = 'class'
        for par_node in node.ancestors(recurs=False):
            try:
                par_obj = self.object_from_node(par_node)
                self.add_relationship(obj, par_obj, 'specialization')
            except KeyError:
                continue
        for impl_node in node.implements:
            try:
                impl_obj = self.object_from_node(impl_node)
                self.add_relationship(obj, impl_obj, 'implements')
            except KeyError:
                continue
        for (name, values) in list(node.instance_attrs_type.items()) + list(node.locals_type.items()):
            for value in values:
                if value is astroid.Uninferable:
                    continue
                if isinstance(value, astroid.Instance):
                    value = value._proxied
                try:
                    associated_obj = self.object_from_node(value)
                    self.add_relationship(associated_obj, obj, 'association', name)
                except KeyError:
                    continue
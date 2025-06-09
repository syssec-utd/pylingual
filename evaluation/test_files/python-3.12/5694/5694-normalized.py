def leave_classdef(self, cnode):
    """close a class node:
        check that instance attributes are defined in __init__ and check
        access to existent members
        """
    if self._ignore_mixin and cnode.name[-5:].lower() == 'mixin':
        return
    accessed = self._accessed.accessed(cnode)
    if cnode.type != 'metaclass':
        self._check_accessed_members(cnode, accessed)
    if not self.linter.is_message_enabled('attribute-defined-outside-init'):
        return
    defining_methods = self.config.defining_attr_methods
    current_module = cnode.root()
    for attr, nodes in cnode.instance_attrs.items():
        nodes = [n for n in nodes if not isinstance(n.statement(), (astroid.Delete, astroid.AugAssign)) and n.root() is current_module]
        if not nodes:
            continue
        if any((node.frame().name in defining_methods for node in nodes)):
            continue
        for parent in cnode.instance_attr_ancestors(attr):
            attr_defined = False
            for node in parent.instance_attrs[attr]:
                if node.frame().name in defining_methods:
                    attr_defined = True
            if attr_defined:
                break
        else:
            try:
                cnode.local_attr(attr)
            except astroid.NotFoundError:
                for node in nodes:
                    if node.frame().name not in defining_methods:
                        if _called_in_methods(node.frame(), cnode, defining_methods):
                            continue
                        self.add_message('attribute-defined-outside-init', args=attr, node=node)
def extract_classes(self, klass_node, anc_level, association_level):
    """extract recursively classes related to klass_node"""
    if self.classdiagram.has_node(klass_node) or not self.show_node(klass_node):
        return
    self.add_class(klass_node)
    for ancestor in self.get_ancestors(klass_node, anc_level):
        self.extract_classes(ancestor, anc_level - 1, association_level)
    for node in self.get_associated(klass_node, association_level):
        self.extract_classes(node, anc_level, association_level - 1)
def visit_classdef(self, node):
    """visit an astroid.Class node

        add this class to the class diagram definition
        """
    (anc_level, association_level) = self._get_levels()
    self.extract_classes(node, anc_level, association_level)
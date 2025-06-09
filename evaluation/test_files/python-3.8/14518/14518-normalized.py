def _nodelistcontents_to_text(self, nodelist):
    """
        Turn the node list to text representations of each node.  Basically apply
        `node_to_text()` to each node.  (But not quite actually, since we take
        some care as to where we add whitespace.)
        """
    s = ''
    prev_node = None
    for node in nodelist:
        if self._is_bare_macro_node(prev_node) and node.isNodeType(latexwalker.LatexCharsNode):
            if not self.strict_latex_spaces['between-macro-and-chars']:
                s += prev_node.macro_post_space
        s += self.node_to_text(node)
        prev_node = node
    return s
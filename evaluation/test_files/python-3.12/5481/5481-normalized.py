def walk(self, node, _done=None):
    """walk on the tree from <node>, getting callbacks from handler"""
    if _done is None:
        _done = set()
    if node in _done:
        raise AssertionError((id(node), node, node.parent))
    _done.add(node)
    self.visit(node)
    for child_node in node.get_children():
        assert child_node is not node
        self.walk(child_node, _done)
    self.leave(node)
    assert node.parent is not node
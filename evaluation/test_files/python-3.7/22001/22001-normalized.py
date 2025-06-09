def depth(n, tree):
    """get depth of an element in the tree"""
    d = 0
    parent = tree[n]
    while parent is not None:
        d += 1
        parent = tree[parent]
    return d
def _search(self, node, key, max_depth=float('inf'), with_links=True, crun=None):
    """ Searches for an item in the tree below `node`

        :param node:

            The parent node below which the search is performed

        :param key:

            Name to search for. Can be the short name, the full name or parts of it

        :param max_depth:

            maximum search depth.

        :param with_links:

            If links should be considered

        :param crun:

            Used for very fast search if we know we operate in a single run branch

        :return: The found node and the depth it was found for

        """
    if key in node._children and (with_links or key not in node._links):
        return (node._children[key], 1)
    try:
        result = self._very_fast_search(node, key, max_depth, with_links, crun)
        if result:
            return result
    except pex.TooManyGroupsError:
        pass
    except pex.NotUniqueNodeError:
        pass
    nodes_iterator = self._iter_nodes(node, recursive=True, max_depth=max_depth, in_search=True, with_links=with_links)
    result_node = None
    result_depth = float('inf')
    for (depth, name, child) in nodes_iterator:
        if depth > result_depth:
            break
        if key == name:
            if result_node is not None:
                raise pex.NotUniqueNodeError('Node `%s` has been found more than once within the same depth %d. Full name of first occurrence is `%s` and of second `%s`' % (key, child.v_depth, result_node.v_full_name, child.v_full_name))
            result_node = child
            result_depth = depth
    return (result_node, result_depth)
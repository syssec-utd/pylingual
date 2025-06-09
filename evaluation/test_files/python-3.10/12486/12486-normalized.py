def _remove_subtree(self, start_node, name, predicate=None):
    """Removes a subtree from the trajectory tree.

        Does not delete stuff from disk only from RAM.

        :param start_node: The parent node from where to start
        :param name: Name of child which will be deleted and recursively all nodes below the child
        :param predicate:

            Predicate that can be used to compute for individual nodes if they should be removed
            ``True`` or kept ``False``.

        """

    def _delete_from_children(node, child_name):
        del node._children[child_name]
        if child_name in node._groups:
            del node._groups[child_name]
        elif child_name in node._leaves:
            del node._leaves[child_name]
        else:
            raise RuntimeError('You shall not pass!')

    def _remove_subtree_inner(node, predicate):
        if not predicate(node):
            return False
        elif node.v_is_group:
            for name_ in itools.chain(list(node._leaves.keys()), list(node._groups.keys())):
                child_ = node._children[name_]
                child_deleted = _remove_subtree_inner(child_, predicate)
                if child_deleted:
                    _delete_from_children(node, name_)
                    del child_
            for link_ in list(node._links.keys()):
                node.f_remove_link(link_)
            if len(node._children) == 0:
                self._delete_node(node)
                return True
            else:
                return False
        else:
            self._delete_node(node)
            return True
    if name in start_node._links:
        start_node.f_remove_link(name)
    else:
        child = start_node._children[name]
        if predicate is None:
            predicate = lambda x: True
        if _remove_subtree_inner(child, predicate):
            _delete_from_children(start_node, name)
            del child
            return True
        else:
            return False
def _remove_along_branch(self, actual_node, split_name, recursive=False):
    """Removes a given node from the tree.

        Starts from a given node and walks recursively down the tree to the location of the node
        we want to remove.

        We need to walk from a start node in case we want to check on the way back whether we got
        empty group nodes due to deletion.

        :param actual_node: Current node

        :param split_name: DEQUE of names to get the next nodes.

        :param recursive:

            To also delete all children of a group node

        :return: True if node was deleted, otherwise False

        """
    if len(split_name) == 0:
        if actual_node.v_is_group and actual_node.f_has_children():
            if recursive:
                for child in list(actual_node._children.keys()):
                    actual_node.f_remove_child(child, recursive=True)
            else:
                raise TypeError('Cannot remove group `%s` it contains children. Please remove with `recursive=True`.' % actual_node.v_full_name)
        self._delete_node(actual_node)
        return True
    name = split_name.popleft()
    if name in actual_node._links:
        if len(split_name) > 0:
            raise RuntimeError('You cannot remove nodes while hopping over links!')
        actual_node.f_remove_link(name)
    else:
        child = actual_node._children[name]
        if self._remove_along_branch(child, split_name, recursive=recursive):
            del actual_node._children[name]
            if name in actual_node._groups:
                del actual_node._groups[name]
            elif name in actual_node._leaves:
                del actual_node._leaves[name]
            else:
                raise RuntimeError('You shall not pass!')
            del child
            return False
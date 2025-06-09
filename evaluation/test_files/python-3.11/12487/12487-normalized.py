def _delete_node(self, node):
    """Deletes a single node from the tree.

        Removes all references to the node.

        Note that the 'parameters', 'results', 'derived_parameters', and 'config' groups
        hanging directly below root cannot be deleted. Also the root node itself cannot be
        deleted. (This would cause a tremendous wave of uncontrollable self destruction, which
        would finally lead to the Apocalypse!)

        """
    full_name = node.v_full_name
    root = self._root_instance
    if full_name == '':
        return
    if node.v_is_leaf:
        if full_name in root._parameters:
            del root._parameters[full_name]
        elif full_name in root._config:
            del root._config[full_name]
        elif full_name in root._derived_parameters:
            del root._derived_parameters[full_name]
        elif full_name in root._results:
            del root._results[full_name]
        elif full_name in root._other_leaves:
            del root._other_leaves[full_name]
        if full_name in root._explored_parameters:
            if root._stored:
                root._explored_parameters[full_name] = None
            else:
                del root._explored_parameters[full_name]
            if len(root._explored_parameters) == 0:
                root.f_shrink()
        del self._flat_leaf_storage_dict[full_name]
    else:
        del root._all_groups[full_name]
        if full_name in root._run_parent_groups:
            del root._run_parent_groups[full_name]
    if full_name in root._linked_by:
        linking = root._linked_by[full_name]
        for linking_name in list(linking.keys()):
            linking_group, link_set = linking[linking_name]
            for link in list(link_set):
                linking_group.f_remove_link(link)
    if (node.v_location, node.v_name) in self._root_instance._new_nodes:
        del self._root_instance._new_nodes[node.v_location, node.v_name]
    self._remove_from_nodes_and_leaves(node)
    node._vars = None
    node._func = None
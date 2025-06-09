def _get(self, node, name, fast_access, shortcuts, max_depth, auto_load, with_links):
    """Searches for an item (parameter/result/group node) with the given `name`.

        :param node: The node below which the search is performed

        :param name: Name of the item (full name or parts of the full name)

        :param fast_access: If the result is a parameter, whether fast access should be applied.

        :param max_depth:

            Maximum search depth relative to start node.

        :param auto_load:

            If data should be automatically loaded

        :param with_links

            If links should be considered

        :return:

            The found instance (result/parameter/group node) or if fast access is True and you
            found a parameter or result that supports fast access, the contained value is returned.

        :raises:

            AttributeError if no node with the given name can be found.
            Raises errors that are raised by the storage service if `auto_load=True` and
            item cannot be found.

        """
    if auto_load and (not with_links):
        raise ValueError('If you allow auto-loading you mus allow links.')
    if isinstance(name, list):
        split_name = name
    elif isinstance(name, tuple):
        split_name = list(name)
    elif isinstance(name, int):
        split_name = [name]
    else:
        split_name = name.split('.')
    if node.v_is_root:
        if len(split_name) == 1 and split_name[0] == '':
            return node
        key = split_name[0]
        (_, key) = self._translate_shortcut(key)
        if key in SUBTREE_MAPPING and key not in node._children:
            node.f_add_group(key)
    if max_depth is None:
        max_depth = float('inf')
    if len(split_name) > max_depth and shortcuts:
        raise ValueError('Name of node to search for (%s) is longer thant the maximum depth %d' % (str(name), max_depth))
    try_auto_load_directly1 = False
    try_auto_load_directly2 = False
    wildcard_positions = []
    root = self._root_instance
    for (idx, key) in enumerate(split_name):
        (translated_shortcut, key) = self._translate_shortcut(key)
        if translated_shortcut:
            split_name[idx] = key
        if key[0] == '_':
            raise AttributeError('Leading underscores are not allowed for group or parameter names. Cannot return %s.' % key)
        is_wildcard = self._root_instance.f_is_wildcard(key)
        if not is_wildcard and key not in self._nodes_and_leaves and (key not in self._links_count):
            try_auto_load_directly1 = True
            try_auto_load_directly2 = True
        if is_wildcard:
            wildcard_positions.append((idx, key))
            if root.f_wildcard(key) not in self._nodes_and_leaves:
                try_auto_load_directly1 = True
            if root.f_wildcard(key, -1) not in self._nodes_and_leaves:
                try_auto_load_directly2 = True
    run_idx = root.v_idx
    wildcard_exception = None
    if try_auto_load_directly1 and try_auto_load_directly2 and (not auto_load):
        for (wildcard_pos, wildcard) in wildcard_positions:
            split_name[wildcard_pos] = root.f_wildcard(wildcard, run_idx)
        raise AttributeError("%s is not part of your trajectory or it's tree. " % str('.'.join(split_name)))
    if run_idx > -1:
        with self._disable_logging:
            try:
                for (wildcard_pos, wildcard) in wildcard_positions:
                    split_name[wildcard_pos] = root.f_wildcard(wildcard, run_idx)
                result = self._perform_get(node, split_name, fast_access, shortcuts, max_depth, auto_load, with_links, try_auto_load_directly1)
                return result
            except (pex.DataNotInStorageError, AttributeError) as exc:
                wildcard_exception = exc
    if wildcard_positions:
        for (wildcard_pos, wildcard) in wildcard_positions:
            split_name[wildcard_pos] = root.f_wildcard(wildcard, -1)
    try:
        return self._perform_get(node, split_name, fast_access, shortcuts, max_depth, auto_load, with_links, try_auto_load_directly2)
    except (pex.DataNotInStorageError, AttributeError):
        if wildcard_exception is not None:
            raise wildcard_exception
        else:
            raise
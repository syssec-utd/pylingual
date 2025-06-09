def _add_to_tree(self, start_node, split_names, type_name, group_type_name, instance, constructor, args, kwargs):
    """Adds a new item to the tree.

        The item can be an already given instance or it is created new.

        :param start_node:

            Parental node the adding of the item was initiated from.

        :param split_names:

            List of names of the new item

        :param type_name:

            Type of item 'RESULT', 'RESULT_GROUP', 'PARAMETER', etc. See name of constants
            at beginning of the python module.

        :param group_type_name:

            Name of the subbranch the item is added to 'RESULT_GROUP', 'PARAMETER_GROUP' etc.
            See name of constants at beginning of this python module.

        :param instance:

            Here an already given instance can be passed. If instance should be created new
            pass None.

        :param constructor:

            If instance should be created new pass a constructor class. If None is passed
            the standard constructor for the instance is chosen.

        :param args:

            Additional arguments passed to instance construction

        :param kwargs:

            Additional keyword arguments passed to instance construction

        :return: The new added instance

        :raises: ValueError if naming of the new item is invalid

        """
    try:
        act_node = start_node
        last_idx = len(split_names) - 1
        add_link = type_name == LINK
        link_added = False
        for (idx, name) in enumerate(split_names):
            if name not in act_node._children:
                if idx == last_idx:
                    if add_link:
                        new_node = self._create_link(act_node, name, instance)
                        link_added = True
                    elif group_type_name != type_name:
                        new_node = self._create_any_param_or_result(act_node, name, type_name, instance, constructor, args, kwargs)
                        self._flat_leaf_storage_dict[new_node.v_full_name] = new_node
                    else:
                        new_node = self._create_any_group(act_node, name, group_type_name, instance, constructor, args, kwargs)
                else:
                    new_node = self._create_any_group(act_node, name, group_type_name)
                if name in self._root_instance._run_information:
                    self._root_instance._run_parent_groups[act_node.v_full_name] = act_node
                if self._root_instance._is_run:
                    if link_added:
                        self._root_instance._new_links[act_node.v_full_name, name] = (act_node, new_node)
                    else:
                        self._root_instance._new_nodes[act_node.v_full_name, name] = (act_node, new_node)
            else:
                if name in act_node._links:
                    raise AttributeError('You cannot hop over links when adding data to the tree. There is a link called `%s` under `%s`.' % (name, act_node.v_full_name))
                if idx == last_idx:
                    if self._root_instance._no_clobber:
                        self._logger.warning('You already have a group/instance/link `%s` under `%s`. However, you set `v_no_clobber=True`, so I will ignore your addition of data.' % (name, act_node.v_full_name))
                    else:
                        raise AttributeError('You already have a group/instance/link `%s` under `%s`' % (name, act_node.v_full_name))
            act_node = act_node._children[name]
        return act_node
    except:
        self._logger.error('Failed adding `%s` under `%s`.' % (name, start_node.v_full_name))
        raise
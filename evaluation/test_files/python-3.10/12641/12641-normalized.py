def _tree_load_link(self, new_traj_node, load_data, traj, as_new, hdf5_soft_link):
    """ Loads a link
        
        :param new_traj_node: Node in traj containing link 
        :param load_data: How to load data in the linked node
        :param traj: The trajectory
        :param as_new: If data in linked node should be loaded as new
        :param hdf5_soft_link: The hdf5 soft link

        """
    try:
        linked_group = hdf5_soft_link()
        link_name = hdf5_soft_link._v_name
        if not link_name in new_traj_node._links or load_data == pypetconstants.OVERWRITE_DATA:
            link_location = linked_group._v_pathname
            full_name = '.'.join(link_location.split('/')[2:])
            if not full_name in traj:
                self._tree_load_sub_branch(traj, full_name, load_data=pypetconstants.LOAD_SKELETON, with_links=False, recursive=False, _trajectory=traj, _as_new=as_new, _hdf5_group=self._trajectory_group)
            if load_data == pypetconstants.OVERWRITE_DATA and link_name in new_traj_node._links:
                new_traj_node.f_remove_link(link_name)
            if not link_name in new_traj_node._links:
                new_traj_node._nn_interface._add_generic(new_traj_node, type_name=nn.LINK, group_type_name=nn.GROUP, args=(link_name, traj.f_get(full_name)), kwargs={}, add_prefix=False, check_naming=False)
            else:
                raise RuntimeError('You shall not pass!')
    except pt.NoSuchNodeError:
        self._logger.error('Link `%s` under `%s` is broken, cannot load it, I will ignore it, you have to manually delete it!' % (hdf5_soft_link._v_name, new_traj_node.v_full_name))
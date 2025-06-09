def _grp_load_group(self, traj_group, load_data=pypetconstants.LOAD_DATA, with_links=True, recursive=False, max_depth=None, _traj=None, _as_new=False, _hdf5_group=None):
    """Loads a group node and potentially everything recursively below"""
    if _hdf5_group is None:
        _hdf5_group = self._all_get_node_by_name(traj_group.v_full_name)
        _traj = traj_group.v_root
    if recursive:
        parent_traj_node = traj_group.f_get_parent()
        self._tree_load_nodes_dfs(parent_traj_node, load_data=load_data, with_links=with_links, recursive=recursive, max_depth=max_depth, current_depth=0, trajectory=_traj, as_new=_as_new, hdf5_group=_hdf5_group)
    else:
        if load_data == pypetconstants.LOAD_NOTHING:
            return
        elif load_data == pypetconstants.OVERWRITE_DATA:
            traj_group.v_annotations.f_empty()
            traj_group.v_comment = ''
        self._all_load_skeleton(traj_group, _hdf5_group)
        traj_group._stored = not _as_new
        self._node_processing_timer.signal_update()
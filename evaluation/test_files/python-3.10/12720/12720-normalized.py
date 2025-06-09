def _merge_single_runs(self, other_trajectory, used_runs):
    """  Updates the `run_information` of the current trajectory."""
    count = len(self)
    run_indices = range(len(other_trajectory))
    run_name_dict = OrderedDict()
    to_store_groups_with_annotations = []
    for idx in run_indices:
        if idx in used_runs:
            other_info_dict = other_trajectory.f_get_run_information(idx)
            time_ = other_info_dict['time']
            timestamp = other_info_dict['timestamp']
            completed = other_info_dict['completed']
            short_environment_hexsha = other_info_dict['short_environment_hexsha']
            finish_timestamp = other_info_dict['finish_timestamp']
            runtime = other_info_dict['runtime']
            new_idx = used_runs[idx]
            new_runname = self.f_wildcard('$', new_idx)
            run_name_dict[idx] = new_runname
            info_dict = dict(idx=new_idx, time=time_, timestamp=timestamp, completed=completed, short_environment_hexsha=short_environment_hexsha, finish_timestamp=finish_timestamp, runtime=runtime)
            self._add_run_info(**info_dict)
def _srn_summarize_explored_parameters(self, paramlist):
    """Summarizes the parameter settings.

        :param run_name: Name of the single run

        :param paramlist: List of explored parameters

        :param add_table: Whether to add the overview table

        :param create_run_group:

            If a group with the particular name should be created if it does not exist.
            Might be necessary when trajectories are merged.

        """
    runsummary = ''
    paramlist = sorted(paramlist, key=lambda name: name.v_name + name.v_location)
    for idx, expparam in enumerate(paramlist):
        if idx > 0:
            runsummary += ',   '
        valstr = expparam.f_val_to_str()
        if len(valstr) >= pypetconstants.HDF5_STRCOL_MAX_COMMENT_LENGTH:
            valstr = valstr[0:pypetconstants.HDF5_STRCOL_MAX_COMMENT_LENGTH - 3]
            valstr += '...'
        if expparam.v_name in runsummary:
            param_name = expparam.v_full_name
        else:
            param_name = expparam.v_name
        runsummary = runsummary + param_name + ': ' + valstr
    return runsummary
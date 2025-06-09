def reproduce(past_analysis, plotting=False, data_folder=None, srm_table=None, custom_stat_functions=None):
    """
    Reproduce a previous analysis exported with :func:`latools.analyse.minimal_export`

    For normal use, supplying `log_file` and specifying a plotting option should be
    enough to reproduce an analysis. All requisites (raw data, SRM table and any
    custom stat functions) will then be imported from the minimal_export folder.

    You may also specify your own raw_data, srm_table and custom_stat_functions,
    if you wish.

    Parameters
    ----------
    log_file : str
        The path to the log file produced by :func:`~latools.analyse.minimal_export`.
    plotting : bool
        Whether or not to output plots.
    data_folder : str
        Optional. Specify a different data folder. Data folder
        should normally be in the same folder as the log file.
    srm_table : str
        Optional. Specify a different SRM table. SRM table
        should normally be in the same folder as the log file.
    custom_stat_functions : str
        Optional. Specify a python file containing custom
        stat functions for use by reproduce. Any custom
        stat functions should normally be included in the
        same folder as the log file.
    """
    if '.zip' in past_analysis:
        dirpath = utils.extract_zipdir(past_analysis)
        logpath = os.path.join(dirpath, 'analysis.lalog')
    elif os.path.isdir(past_analysis):
        if os.path.exists(os.path.join(past_analysis, 'analysis.lalog')):
            logpath = os.path.join(past_analysis, 'analysis.lalog')
    elif 'analysis.lalog' in past_analysis:
        logpath = past_analysis
    else:
        raise ValueError('\n\n{} is not a valid input.\n\n' + 'Must be one of:\n' + '  - A .zip file exported by latools\n' + '  - An analysis.lalog file\n' + '  - A directory containing an analysis.lalog files\n')
    runargs, paths = logging.read_logfile(logpath)
    csfs = Bunch()
    if custom_stat_functions is None and 'custom_stat_functions' in paths.keys():
        with open(paths['custom_stat_functions'], 'r') as f:
            csf = f.read()
        fname = re.compile('def (.*)\\(.*')
        for c in csf.split('\n\n\n\n'):
            if fname.match(c):
                csfs[fname.match(c).groups()[0]] = c
    rep = analyse(*runargs[0][-1]['args'], **runargs[0][-1]['kwargs'])
    for fname, arg in runargs:
        if fname != '__init__':
            if 'plot' in fname.lower() and plotting:
                getattr(rep, fname)(*arg['args'], **arg['kwargs'])
            elif 'sample_stats' in fname.lower():
                rep.sample_stats(*arg['args'], csf_dict=csfs, **arg['kwargs'])
            else:
                getattr(rep, fname)(*arg['args'], **arg['kwargs'])
    return rep
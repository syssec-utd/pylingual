def create(config_name, srmfile=None, dataformat=None, base_on='DEFAULT', make_default=False):
    """
    Adds a new configuration to latools.cfg.

    Parameters
    ----------
    config_name : str
        The name of the new configuration. This should be descriptive
        (e.g. UC Davis Foram Group)
    srmfile : str (optional)
        The location of the srm file used for calibration.
    dataformat : str (optional)
        The location of the dataformat definition to use.
    base_on : str
        The name of the existing configuration to base the new one on.
        If either srm_file or dataformat are not specified, the new
        config will copy this information from the base_on config.
    make_default : bool
        Whether or not to make the new configuration the default
        for future analyses. Default = False.

    Returns
    -------
    None
    """
    base_config = read_configuration(base_on)
    config_file, cf = read_latoolscfg()
    if config_name not in cf.sections():
        cf.add_section(config_name)
    if dataformat is None:
        dataformat = base_config['dataformat']
    cf.set(config_name, 'dataformat', dataformat)
    if srmfile is None:
        srmfile = base_config['srmfile']
    cf.set(config_name, 'srmfile', srmfile)
    if make_default:
        cf.set('DEFAULT', 'config', config_name)
    with open(config_file, 'w') as f:
        cf.write(f)
    return
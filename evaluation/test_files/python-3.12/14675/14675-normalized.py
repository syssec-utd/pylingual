def copy_SRM_file(destination=None, config='DEFAULT'):
    """
    Creates a copy of the default SRM table at the specified location.

    Parameters
    ----------
    destination : str
        The save location for the SRM file. If no location specified, 
        saves it as 'LAtools_[config]_SRMTable.csv' in the current working 
        directory.
    config : str
        It's possible to set up different configurations with different
        SRM files. This specifies the name of the configuration that you 
        want to copy the SRM file from. If not specified, the 'DEFAULT'
        configuration is used.
    """
    conf = read_configuration()
    src = pkgrs.resource_filename('latools', conf['srmfile'])
    if destination is None:
        destination = './LAtools_' + conf['config'] + '_SRMTable.csv'
    if os.path.isdir(destination):
        destination += 'LAtools_' + conf['config'] + '_SRMTable.csv'
    copyfile(src, destination)
    print(src + ' \n    copied to:\n      ' + destination)
    return
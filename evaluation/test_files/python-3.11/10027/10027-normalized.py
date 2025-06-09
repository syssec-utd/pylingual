def get_endpoint_path(self, endpoint_id):
    """return the first fullpath to a folder in the endpoint based on
       expanding the user's home from the globus config file. This
       function is fragile but I don't see any other way to do it.
    
       Parameters
       ==========
       endpoint_id: the endpoint id to look up the path for

    """
    config = os.path.expanduser('~/.globusonline/lta/config-paths')
    if not os.path.exists(config):
        bot.error('%s not found for a local Globus endpoint.')
        sys.exit(1)
    path = None
    config = [x.split(',')[0] for x in read_file(config)]
    for path in config:
        if os.path.exists(path):
            break
    if path is None:
        bot.error('No path was found for a local Globus endpoint.')
        sys.exit(1)
    return path
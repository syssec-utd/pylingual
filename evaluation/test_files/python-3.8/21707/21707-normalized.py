def locate_profile(profile='default'):
    """Find the path to the folder associated with a given profile.
    
    I.e. find $IPYTHONDIR/profile_whatever.
    """
    from IPython.core.profiledir import ProfileDir, ProfileDirError
    try:
        pd = ProfileDir.find_profile_dir_by_name(get_ipython_dir(), profile)
    except ProfileDirError:
        raise IOError("Couldn't find profile %r" % profile)
    return pd.location
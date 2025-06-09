def get_thumbnail():
    """return the robot.png thumbnail from the database folder.
       if the user has exported a different image, use that instead.
    """
    from sregistry.defaults import SREGISTRY_THUMBNAIL
    if SREGISTRY_THUMBNAIL is not None:
        if os.path.exists(SREGISTRY_THUMBNAIL):
            return SREGISTRY_THUMBNAIL
    return '%s/database/robot.png' % get_installdir()
def format_container_name(name, special_characters=None):
    """format_container_name will take a name supplied by the user,
    remove all special characters (except for those defined by "special-characters"
    and return the new image name.
    """
    if special_characters is None:
        special_characters = []
    return ''.join((e.lower() for e in name if e.isalnum() or e in special_characters))
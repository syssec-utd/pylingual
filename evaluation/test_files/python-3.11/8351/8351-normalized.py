def lookup_by_number(errno):
    """ Used for development only """
    for key, val in globals().items():
        if errno == val:
            print(key)
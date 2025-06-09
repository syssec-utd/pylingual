def string_input(prompt=''):
    """Python 3 input()/Python 2 raw_input()"""
    v = sys.version[0]
    if v == '3':
        return input(prompt)
    else:
        return raw_input(prompt)
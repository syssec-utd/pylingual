def get_filename_safe_string(string):
    """
    Converts a string to a string that is safe for a filename
    Args:
        string (str): A string to make safe for a filename

    Returns:
        str: A string safe for a filename
    """
    invalid_filename_chars = ['\\', '/', ':', '"', '*', '?', '|', '\n', '\r']
    if string is None:
        string = 'None'
    for char in invalid_filename_chars:
        string = string.replace(char, '')
    string = string.rstrip('.')
    return string
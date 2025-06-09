def check(path, start, now):
    """check which processes need to be restarted

    :params path: a twisted.python.filepath.FilePath with configurations
    :params start: when the checker started running
    :params now: current time
    :returns: list of strings
    """
    return [child.basename() for child in path.children() if _isbad(child, start, now)]
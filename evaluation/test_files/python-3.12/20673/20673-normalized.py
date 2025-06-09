def taskinfo_with_label(label):
    """Return task info dictionary from task label.  Internal function,
    pretty much only used in migrations since the model methods aren't there."""
    task = Task.objects.get(label=label)
    info = json.loads(task._func_info)
    return info
def _mkdir(p):
    """The equivalent of 'mkdir -p' in shell."""
    isdir = os.path.isdir
    stack = [os.path.abspath(p)]
    while not isdir(stack[-1]):
        parent_dir = os.path.dirname(stack[-1])
        stack.append(parent_dir)
    while stack:
        p = stack.pop()
        if not isdir(p):
            os.mkdir(p)
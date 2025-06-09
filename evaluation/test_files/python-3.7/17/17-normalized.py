def print_log(text, *colors):
    """Print a log message to standard error."""
    sys.stderr.write(sprint('{}: {}'.format(script_name, text), *colors) + '\n')
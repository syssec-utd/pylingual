def get_environ_vars(self):
    """Returns a generator with all environmental vars with prefix PIP_"""
    for key, val in os.environ.items():
        if _environ_prefix_re.search(key):
            yield (_environ_prefix_re.sub('', key).lower(), val)
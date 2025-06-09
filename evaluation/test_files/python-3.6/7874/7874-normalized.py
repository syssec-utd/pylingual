def load(self, fm, **kwargs):
    """
        Parse YAML front matter. This uses yaml.SafeLoader by default. 
        """
    kwargs.setdefault('Loader', SafeLoader)
    return yaml.load(fm, **kwargs)
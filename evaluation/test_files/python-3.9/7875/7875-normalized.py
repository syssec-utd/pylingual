def export(self, metadata, **kwargs):
    """
        Export metadata as YAML. This uses yaml.SafeDumper by default.
        """
    kwargs.setdefault('Dumper', SafeDumper)
    kwargs.setdefault('default_flow_style', False)
    kwargs.setdefault('allow_unicode', True)
    metadata = yaml.dump(metadata, **kwargs).strip()
    return u(metadata)
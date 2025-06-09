def default(cls) -> 'PrecalculatedTextMeasurer':
    """Returns a reasonable default PrecalculatedTextMeasurer."""
    if cls._default_cache is not None:
        return cls._default_cache
    if pkg_resources.resource_exists(__name__, 'default-widths.json.xz'):
        import lzma
        with pkg_resources.resource_stream(__name__, 'default-widths.json.xz') as f:
            with lzma.open(f, 'rt') as g:
                cls._default_cache = PrecalculatedTextMeasurer.from_json(cast(TextIO, g))
                return cls._default_cache
    elif pkg_resources.resource_exists(__name__, 'default-widths.json'):
        with pkg_resources.resource_stream(__name__, 'default-widths.json') as f:
            cls._default_cache = PrecalculatedTextMeasurer.from_json(io.TextIOWrapper(f, encoding='utf-8'))
            return cls._default_cache
    else:
        raise ValueError('could not load default-widths.json')
def adapter(data, headers, **kwargs):
    """Wrap the formatting inside a function for TabularOutputFormatter."""
    for row in chain((headers,), data):
        yield '\t'.join((replace(r, (('\n', '\\n'), ('\t', '\\t'))) for r in row))
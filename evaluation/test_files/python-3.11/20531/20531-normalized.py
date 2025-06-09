def dedent(text):
    """Equivalent of textwrap.dedent that ignores unindented first line.

    This means it will still dedent strings like:
    '''foo
    is a bar
    '''

    For use in wrap_paragraphs.
    """
    if text.startswith('\n'):
        return textwrap.dedent(text)
    splits = text.split('\n', 1)
    if len(splits) == 1:
        return textwrap.dedent(text)
    first, rest = splits
    rest = textwrap.dedent(rest)
    return '\n'.join([first, rest])
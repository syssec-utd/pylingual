def _collapse_leading_ws(header, txt):
    """
    ``Description`` header must preserve newlines; all others need not
    """
    if header.lower() == 'description':
        return '\n'.join([x[8:] if x.startswith(' ' * 8) else x for x in txt.strip().splitlines()])
    else:
        return ' '.join([x.strip() for x in txt.splitlines()])
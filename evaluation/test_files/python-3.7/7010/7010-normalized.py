def dict_entry_has_key(line, key):
    """Return True if `line` is a dict entry that uses `key`.

    Return False for multiline cases where the line should not be removed by
    itself.

    """
    if '#' in line:
        return False
    result = re.match('\\s*(.*)\\s*:\\s*(.*),\\s*$', line)
    if not result:
        return False
    try:
        candidate_key = ast.literal_eval(result.group(1))
    except (SyntaxError, ValueError):
        return False
    if multiline_statement(result.group(2)):
        return False
    return candidate_key == key
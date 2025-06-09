def filter_unused_variable(line, previous_line=''):
    """Return line if used, otherwise return None."""
    if re.match(EXCEPT_REGEX, line):
        return re.sub(' as \\w+:$', ':', line, count=1)
    elif multiline_statement(line, previous_line):
        return line
    elif line.count('=') == 1:
        split_line = line.split('=')
        assert len(split_line) == 2
        value = split_line[1].lstrip()
        if ',' in split_line[0]:
            return line
        if is_literal_or_name(value):
            value = 'pass' + get_line_ending(line)
        return get_indentation(line) + value
    else:
        return line
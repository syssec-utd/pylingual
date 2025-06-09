def render_entries(cls, entries, additional_columns=None, only_show=None, numbers=False):
    """
        Pretty-prints a list of entries. If the window is wide enough to
        support printing as a table, runs the `print_table.render_table`
        function on the table. Otherwise, constructs a line-by-line
        representation..

        :param entries: A list of entries.
        :type entries: [:py:class:`HostEntry`]
        :param additional_columns: Columns to show in addition to defaults.
        :type additional_columns: ``list`` of ``str``
        :param only_show: A specific list of columns to show.
        :type only_show: ``NoneType`` or ``list`` of ``str``
        :param numbers: Whether to include a number column.
        :type numbers: ``bool``

        :return: A pretty-printed string.
        :rtype: ``str``
        """
    additional_columns = additional_columns or []
    if only_show is not None:
        columns = _uniquify(only_show)
    else:
        columns = _uniquify(cls.DEFAULT_COLUMNS + additional_columns)
    top_row = [cls.prettyname(col) for col in columns]
    table = [top_row] if numbers is False else [[''] + top_row]
    for (i, entry) in enumerate(entries):
        row = [entry._get_attrib(c, convert_to_str=True) for c in columns]
        table.append(row if numbers is False else [i] + row)
    cur_width = get_current_terminal_width()
    colors = [get_color_hash(c, MIN_COLOR_BRIGHT, MAX_COLOR_BRIGHT) for c in columns]
    if cur_width >= get_table_width(table):
        return render_table(table, column_colors=colors if numbers is False else [green] + colors)
    else:
        result = []
        first_index = 1 if numbers is True else 0
        for row in table[1:]:
            rep = [green('%s:' % row[0] if numbers is True else '-----')]
            for (i, val) in enumerate(row[first_index:]):
                color = colors[i - 1 if numbers is True else i]
                name = columns[i]
                rep.append('  %s: %s' % (name, color(val)))
            result.append('\n'.join(rep))
        return '\n'.join(result)
import datetime

def last_modified_from(days_back):
    """Check if input is a number and return a string to search for items last
    modified from n days ago. Also returns a message with the resulting number.
    """
    try:
        days_back = float(days_back)
    except (ValueError, TypeError):
        from_date_query = ''
        from_text = ''
    else:
        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_diff = datetime.timedelta(days=days_back)
        from_date = datetime.datetime.strftime(date_now - date_diff, '%Y-%m-%d %H:%M')
        from_date_query = '&last_modified.date_modified.from=' + from_date
        from_text = 'modified from %s ' % from_date
    return (from_date_query, from_text)

def md_cell_maker(item):
    """Builds a markdown cell"""
    outstr = ''
    if isinstance(item, str):
        outstr = item
    if isinstance(item, set):
        outstr = ',<br>'.join(item)
    if isinstance(item, list):
        outstr = '<br>'.join([md_cell_maker(i) for i in item])
    if isinstance(item, dict):
        if item.get('link') is None:
            print('Dictionaries in the table should have link fields!\n{}'.format(item))
        outstr = '[{}]({})'.format(item.get('text'), item.get('link').replace(')', '%29'))
    if not isinstance(outstr, str):
        print('type(outstr) = ' + str(type(outstr)))
    return outstr.replace("'", "\\'")

def md_table_maker(rows, keys, jsx_key, col_widths='[]'):
    """Builds markdown table"""
    part1 = "\n    <MdSortableTable\n        key='{}'\n        defaultColWidths={{{}}}\n    >{{' \\\n    ".format(jsx_key, col_widths)
    part2 = ''
    for key in keys:
        part2 += '|' + key
    part2 += '|\\\n' + '|---' * len(keys) + '|\\\n'
    part3 = ''
    for row in rows.values():
        row_str = ''
        for key in keys:
            row_str += '|' + md_cell_maker(row.get(key))
        row_str += '|\\\n'
        part3 += row_str
    part4 = "'}</MdSortableTable>"
    return part1 + part2 + part3 + part4
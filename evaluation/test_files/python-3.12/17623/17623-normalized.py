def parse_info_table(table):
    """Parses an info table, like the "Game Info" table or the "Officials"
    table on the PFR Boxscore page. Keys are lower case and have spaces/special
    characters converted to underscores.

    :table: PyQuery object representing the HTML table.
    :returns: A dictionary representing the information.
    """
    ret = {}
    for tr in list(table('tr').not_('.thead').items()):
        th, td = list(tr('th, td').items())
        key = th.text().lower()
        key = re.sub('\\W', '_', key)
        val = sportsref.utils.flatten_links(td)
        ret[key] = val
    return ret
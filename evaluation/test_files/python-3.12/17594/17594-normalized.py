def _get_player_stats_table(self, subpage, table_id):
    """Helper function for player season stats.

        :identifier: string identifying the type of stat, e.g. 'passing'.
        :returns: A DataFrame of stats.
        """
    doc = self.get_sub_doc(subpage)
    table = doc('table#{}'.format(table_id))
    df = sportsref.utils.parse_table(table)
    return df
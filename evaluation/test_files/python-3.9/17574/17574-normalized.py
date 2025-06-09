def stats_shooting(self, kind='R', summary=False):
    """Returns a DataFrame of shooting stats."""
    return self._get_stats_table('shooting', kind=kind, summary=summary)
def away_score(self):
    """Returns score of the away team.
        :returns: int of the away score.
        """
    doc = self.get_doc()
    table = doc('table.linescore')
    away_score = table('tr').eq(1)('td')[-1].text_content()
    return int(away_score)
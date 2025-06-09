def home_score(self):
    """Returns score of the home team.
        :returns: int of the home score.
        """
    doc = self.get_doc()
    table = doc('table.linescore')
    home_score = table('tr').eq(2)('td')[-1].text_content()
    return int(home_score)
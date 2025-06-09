def date(self):
    """ Returns the creation date stored in the las file

        Returns
        -------
        datetime.date

        """
    try:
        return datetime.date(self.creation_year, 1, 1) + datetime.timedelta(self.creation_day_of_year - 1)
    except ValueError:
        return None
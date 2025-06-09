def date(self, date):
    """ Returns the date of file creation as a python date object
        """
    self.creation_year = date.year
    self.creation_day_of_year = date.timetuple().tm_yday
def fetchall(self):
    """Fetchs all available rows from the cursor."""
    self._check_executed()
    r = self._fetch_row(0)
    self.rownumber = self.rownumber + len(r)
    self._warning_check()
    return r
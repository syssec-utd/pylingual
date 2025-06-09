def _backup(self):
    """
        Backup the database into its file.
        """
    if self._authorization():
        Dict(PyFunceble.INTERN['whois_db']).to_json(self.whois_db_path)
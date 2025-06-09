def rename(self, from_name, to_name):
    """
        Rename a file.

        :param from_name: rename file from name
        :param to_name: rename file to name
        """
    conn = self.get_conn()
    return conn.rename(from_name, to_name)
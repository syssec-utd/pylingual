def get_mod_time(self, path):
    """
        Returns a datetime object representing the last time the file was modified

        :param path: remote file path
        :type path: string
        """
    conn = self.get_conn()
    ftp_mdtm = conn.sendcmd('MDTM ' + path)
    time_val = ftp_mdtm[4:]
    try:
        return datetime.datetime.strptime(time_val, '%Y%m%d%H%M%S.%f')
    except ValueError:
        return datetime.datetime.strptime(time_val, '%Y%m%d%H%M%S')
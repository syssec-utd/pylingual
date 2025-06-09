def dbExec(self, query_str):
    """ Required override of dbExec() from MeterDB(), run query.
        Args:
            query_str (str): query to run
        """
    try:
        connection = sqlite3.connect(self.m_connection_string)
        cursor = connection.cursor()
        cursor.execute(query_str)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except:
        ekm_log(traceback.format_exc(sys.exc_info()))
        return False
    pass
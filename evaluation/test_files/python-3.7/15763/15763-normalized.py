def check(self):
    """
        Checks to see if Spark worker and HDFS datanode are still running.
        """
    status = _checkContainerStatus(self.sparkContainerID, self.hdfsContainerID, sparkNoun='worker', hdfsNoun='datanode')
    return status
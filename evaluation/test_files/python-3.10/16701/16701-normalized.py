def finish(self):
    """
        Finishes the load job. Called automatically when the connection closes.

        :return: The exit code returned when applying rows to the table
        """
    if self.finished:
        return self.exit_code
    checkpoint_status = self.checkpoint()
    self.exit_code = self._exit_code()
    if self.exit_code != 0:
        raise TeradataPTError("BulkLoad job finished with return code '{}'".format(self.exit_code))
    if self.applied_count > 0:
        self._end_acquisition()
        self._apply_rows()
    self.exit_code = self._exit_code()
    if self.exit_code != 0:
        raise TeradataPTError("BulkLoad job finished with return code '{}'".format(self.exit_code))
    self.finished = True
    return self.exit_code
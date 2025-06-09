def try_number(self):
    """
        Return the try number that this task number will be when it is actually
        run.

        If the TI is currently running, this will match the column in the
        databse, in all othercases this will be incremenetd
        """
    if self.state == State.RUNNING:
        return self._try_number
    return self._try_number + 1
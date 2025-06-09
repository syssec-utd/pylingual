def log(self, line_mod, line_ori):
    """Write the sources to a log.

        Inputs:

        - line_mod: possibly modified input, such as the transformations made
        by input prefilters or input handlers of various kinds.  This should
        always be valid Python.

        - line_ori: unmodified input line from the user.  This is not
        necessarily valid Python.
        """
    if self.log_raw_input:
        self.log_write(line_ori)
    else:
        self.log_write(line_mod)
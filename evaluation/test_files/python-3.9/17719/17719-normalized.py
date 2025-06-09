def get_process(self):
    """Returns :class:`subprocess.Popen` instance with args from
        :meth:`get_args` result and piped stdin, stdout and stderr.
        """
    return Popen(self.get_args(), stdin=PIPE, stdout=PIPE, stderr=PIPE)
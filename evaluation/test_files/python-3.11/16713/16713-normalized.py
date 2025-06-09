def execute(self, command, coerce_floats=True, parse_dates=False, header=False, sanitize=True, silent=False, panic=None, multi_statement=False, prepare_only=False):
    """
        Execute commands using CLIv2.

        :param str command: The SQL command to be executed
        :param bool coerce_floats: Coerce Teradata decimal types into Python floats
        :param bool parse_dates: Parses Teradata datetime types into Python datetimes
        :param bool header: Include row header
        :param bool sanitize: Whether or not to call :func:`~giraffez.sql.prepare_statement`
            on the command
        :param bool silent: Silence console logging (within this function only)
        :param bool panic: If :code:`True`, when an error is encountered it will be
            raised.
        :param bool multi_statement: Execute in multi-statement mode
        :param bool prepare_only: Only prepare the command (no results)
        :return: a cursor over the results of each statement in the command
        :rtype: :class:`~giraffez.cmd.Cursor`
        :raises `giraffez.TeradataError`: if the query is invalid
        :raises `giraffez.errors.GiraffeError`: if the return data could not be decoded
        """
    if panic is None:
        panic = self.panic
    self.options('panic', panic)
    self.options('multi-statement mode', multi_statement, 3)
    if isfile(command):
        self.options('file', command, 2)
        with open(command, 'r') as f:
            command = f.read()
    elif log.level >= VERBOSE:
        self.options('query', command, 2)
    else:
        self.options('query', truncate(command), 2)
    if not silent and (not self.silent):
        log.info('Command', 'Executing ...')
        log.info(self.options)
    if sanitize:
        command = prepare_statement(command)
        log.debug('Debug[2]', 'Command (sanitized): {!r}'.format(command))
    self.cmd.set_encoding(ENCODER_SETTINGS_DEFAULT)
    return Cursor(self.cmd, command, multi_statement=multi_statement, header=header, prepare_only=prepare_only, coerce_floats=coerce_floats, parse_dates=parse_dates, panic=panic)
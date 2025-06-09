import subprocess

class SubprocessWrapper(object):
    VERBOSE = False

    def __init__(self, arguments, working_directory=None, require_out=False, require_log=False):
        assert isinstance(arguments, list) or isinstance(arguments, str)
        assert require_out != require_log or require_out is False
        if isinstance(arguments, str):
            arguments = arguments.split(' ')
        assert len(arguments) > 0
        self.arguments = arguments
        self.require_out = require_out
        log = require_log or SubprocessWrapper.VERBOSE
        stdout = None if log and (not require_out) else subprocess.PIPE
        stderr = None if log and (not require_out) else subprocess.PIPE
        self.process = subprocess.Popen(arguments, stdout=stdout, stderr=stderr, cwd=working_directory)
        self.code = 0

    def call(self):
        (out, err) = self.process.communicate()
        self.code = self.process.returncode
        if self.require_out:
            return (self.code, out.decode(), err.decode())
        return self.code
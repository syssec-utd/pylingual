import threading
import types
from .. import protocol
from ..channel.Command import Command

class DispatchWrapper(object):
    """Simple wrapper for attribute access and invocation on TCF dispatch thread"""

    def __init__(self, inner):
        self.inner = inner

    def __getattr__(self, attr):
        val = protocol.invokeAndWait(getattr, self.inner, attr)
        if type(val) in (types.FunctionType, types.MethodType):
            return DispatchWrapper(val)
        return val

    def __call__(self, *args, **kwargs):
        return protocol.invokeAndWait(self.inner, *args, **kwargs)

class CommandControl(object):
    """Provides a simple interface to send commands to remote services
    and receive results.

    Usage:
    > cmd = CommandControl(channel)
    > cmd.<service>.<command>(<args>)

    Examples:
    # send command, but don't wait for result:
    > cmd.RunControl.suspend("system")
    # getE() returns the result and raises an exception in case of error:
    > result = cmd.RunControl.getChildren(None).getE()
    # to get error and result at the same time, use this form:
    > error, result = cmd.Breakpoints.getIDs()
    """

    def __init__(self, channel, onDone=None, interactive=False):
        self._lock = threading.Condition()
        self._channel = channel
        self._onDone = onDone
        self._interactive = interactive
        self._queue = []
        self._pending = {}
        self._complete = []

    def __getattr__(self, attr):
        val = getattr(self._channel, attr, None)
        if val:
            if self._interactive and type(val) in (types.FunctionType, types.MethodType):
                val = DispatchWrapper(val)
            return val
        services = protocol.invokeAndWait(self._channel.getRemoteServices)
        if attr == 'services':
            return services
        if attr in services:
            return ServiceWrapper(self, attr)
        raise AttributeError('Unknown service: %s. Use one of %s' % (attr, services))

    def invoke(self, service, command, *args, **kwargs):
        cmd = None
        if not protocol.isDispatchThread():
            if not kwargs.get('async'):
                cmd = protocol.invokeAndWait(self._invoke, service, command, *args, **kwargs)
                if cmd and self._interactive:
                    return cmd.getE()
            else:
                with self._lock:
                    self._queue.append((service, command, args, kwargs))
                    if len(self._queue) == 1:
                        protocol.invokeLater(self._processQueue)
                return
        return cmd

    def _invoke(self, service, command, *args, **kwargs):
        cmdCtrl = self

        class GenericCommand(Command):
            _result = None

            def done(self, error, args):
                resultArgs = None
                rcmds = ('read', 'readdir', 'roots')
                if not error and args:
                    if service == 'StackTrace' and command == 'getContext':
                        error = self.toError(args[1])
                        resultArgs = (args[0],)
                    elif service == 'Expressions' and command == 'evaluate':
                        error = self.toError(args[1])
                        resultArgs = (args[0], args[2])
                    elif service == 'FileSystem' and command in rcmds:
                        error = self.toError(args[1])
                        resultArgs = (args[0],) + tuple(args[2:])
                    elif service == 'Streams' and command == 'read':
                        error = self.toError(args[1])
                        resultArgs = (args[0],) + tuple(args[2:])
                    elif service == 'Diagnostics':
                        if command.startswith('echo'):
                            resultArgs = (args[0],)
                    else:
                        error = self.toError(args[0])
                        resultArgs = args[1:]
                cmdCtrl._doneCommand(self.token, error, resultArgs)

            def wait(self, timeout=None):
                cmdCtrl._waitForCommand(self.token, timeout)

            def cancel(self):
                return protocol.invokeAndWait(self.token.cancel)

            def getResult(self, wait=None):
                if wait:
                    cmdCtrl._waitForCommand(self.token)
                return self._result

            def getE(self):
                r = self.getResult(True)
                if r.error:
                    raise r.error
                return r.args

            def get(self):
                r = self.getResult(True)
                return r.args

            def getError(self):
                r = self.getResult(True)
                return r.error

            def __str__(self):
                if self._async:
                    return self.getCommandString()
                return str(self.get())

            def __iter__(self):
                return iter(self.getResult(True))
        cmd = GenericCommand(self._channel, service, command, args)
        cmd._async = kwargs.get('async')
        cmd._onDone = kwargs.get('onDone')
        self._addPending(cmd)
        return cmd

    def _processQueue(self):
        assert protocol.isDispatchThread()
        with self._lock:
            for cmd in self._queue:
                service, command, args, kwargs = cmd
                self._invoke(service, command, *args, **kwargs)
            del self._queue[:]

    def _addPending(self, cmd):
        with self._lock:
            self._pending[cmd.token.id] = cmd
            self._lock.notifyAll()

    def _doneCommand(self, token, error, args):
        with self._lock:
            cmd = self._pending.get(token.id)
            assert cmd
            del self._pending[token.id]
            cmd._result = CommandResult(token, error, args)
            if cmd._async:
                self._complete.append(cmd)
            isDone = self.isDone()
            if isDone:
                self._lock.notifyAll()
        if cmd._onDone:
            if args is None:
                args = (None,)
            cmd._onDone(error, *args)
        if isDone and self._onDone:
            self._onDone()

    def isDone(self):
        with self._lock:
            return not self._pending and (not self._queue)

    def wait(self, timeout=None):
        assert not protocol.isDispatchThread()
        with self._lock:
            while self._pending or self._queue:
                self._lock.wait(timeout)
                if timeout:
                    break

    def _waitForCommand(self, token, timeout=None):
        assert not protocol.isDispatchThread()
        with self._lock:
            while token.id in self._pending:
                self._lock.wait(timeout)
                if timeout:
                    break
            else:
                if self._queue:
                    self._lock.wait(timeout)
                    while token.id in self._pending:
                        self._lock.wait(timeout)
                        if timeout:
                            break

    def cancel(self):
        if not protocol.isDispatchThread():
            protocol.invokeLater(self.cancel)
            return
        with self._lock:
            for cmd in list(self._pending.values()):
                cmd.token.cancel()
            del self._queue[:]

    def getResult(self, wait=True):
        if wait:
            self.wait()
        with self._lock:
            result = [c.getResult() for c in self._complete]
            del self._complete[:]
        return result

class CommandResult(object):

    def __init__(self, token, error, args):
        self.token = token
        self.error = error
        if args and len(args) == 1:
            args = args[0]
        self.args = args

    def __str__(self):
        if self.error:
            return '[%s] error: %s' % (self.token.id, self.error)
        return '[%s] result: %s' % (self.token.id, self.args)
    __repr__ = __str__

    def __iter__(self):
        yield self.error
        yield self.args

class ServiceWrapper(object):

    def __init__(self, control, service):
        self._control = control
        self._service = service

    def __getattr__(self, attr):
        return CommandWrapper(self._control, self._service, attr)

class CommandWrapper(object):

    def __init__(self, control, service, command):
        self._control = control
        self._service = service
        self._command = command

    def __call__(self, *args, **kwargs):
        return self._control.invoke(self._service, self._command, *args, **kwargs)
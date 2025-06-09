"""
Enable wxPython to be used interacive by setting PyOS_InputHook.

Authors:  Robin Dunn, Brian Granger, Ondrej Certik
"""
import sys
import signal
from _pydev_bundle._pydev_saved_modules import time
from timeit import default_timer as clock
import wx
from pydev_ipython.inputhook import stdin_ready

def inputhook_wx1():
    """Run the wx event loop by processing pending events only.

    This approach seems to work, but its performance is not great as it
    relies on having PyOS_InputHook called regularly.
    """
    try:
        app = wx.GetApp()
        if app is not None:
            assert wx.Thread_IsMain()
            evtloop = wx.EventLoop()
            ea = wx.EventLoopActivator(evtloop)
            while evtloop.Pending():
                evtloop.Dispatch()
            app.ProcessIdle()
            del ea
    except KeyboardInterrupt:
        pass
    return 0

class EventLoopTimer(wx.Timer):

    def __init__(self, func):
        self.func = func
        wx.Timer.__init__(self)

    def Notify(self):
        self.func()

class EventLoopRunner(object):

    def Run(self, time):
        self.evtloop = wx.EventLoop()
        self.timer = EventLoopTimer(self.check_stdin)
        self.timer.Start(time)
        self.evtloop.Run()

    def check_stdin(self):
        if stdin_ready():
            self.timer.Stop()
            self.evtloop.Exit()

def inputhook_wx2():
    """Run the wx event loop, polling for stdin.

    This version runs the wx eventloop for an undetermined amount of time,
    during which it periodically checks to see if anything is ready on
    stdin.  If anything is ready on stdin, the event loop exits.

    The argument to elr.Run controls how often the event loop looks at stdin.
    This determines the responsiveness at the keyboard.  A setting of 1000
    enables a user to type at most 1 char per second.  I have found that a
    setting of 10 gives good keyboard response.  We can shorten it further,
    but eventually performance would suffer from calling select/kbhit too
    often.
    """
    try:
        app = wx.GetApp()
        if app is not None:
            assert wx.Thread_IsMain()
            elr = EventLoopRunner()
            elr.Run(time=10)
    except KeyboardInterrupt:
        pass
    return 0

def inputhook_wx3():
    """Run the wx event loop by processing pending events only.

    This is like inputhook_wx1, but it keeps processing pending events
    until stdin is ready.  After processing all pending events, a call to
    time.sleep is inserted.  This is needed, otherwise, CPU usage is at 100%.
    This sleep time should be tuned though for best performance.
    """
    try:
        app = wx.GetApp()
        if app is not None:
            if hasattr(wx, 'IsMainThread'):
                assert wx.IsMainThread()
            else:
                assert wx.Thread_IsMain()
            if not callable(signal.getsignal(signal.SIGINT)):
                signal.signal(signal.SIGINT, signal.default_int_handler)
            evtloop = wx.EventLoop()
            ea = wx.EventLoopActivator(evtloop)
            t = clock()
            while not stdin_ready():
                while evtloop.Pending():
                    t = clock()
                    evtloop.Dispatch()
                app.ProcessIdle()
                used_time = clock() - t
                if used_time > 10.0:
                    time.sleep(1.0)
                elif used_time > 0.1:
                    time.sleep(0.05)
                else:
                    time.sleep(0.001)
            del ea
    except KeyboardInterrupt:
        pass
    return 0
if sys.platform == 'darwin':
    inputhook_wx = inputhook_wx2
else:
    inputhook_wx = inputhook_wx3
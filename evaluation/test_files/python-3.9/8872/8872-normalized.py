def debug(dbg_opts=None, start_opts=None, post_mortem=True, step_ignore=1, level=0):
    """
Enter the debugger.

Parameters
----------

level : how many stack frames go back. Usually it will be
the default 0. But sometimes though there may be calls in setup to the debugger
that you may want to skip.

step_ignore : how many line events to ignore after the
debug() call. 0 means don't even wait for the debug() call to finish.

param dbg_opts : is an optional "options" dictionary that gets fed
trepan.Debugger(); `start_opts' are the optional "options"
dictionary that gets fed to trepan.Debugger.core.start().

Use like this:

.. code-block:: python

    ... # Possibly some Python code
    import trepan.api # Needed only once
    ... # Possibly some more Python code
    trepan.api.debug() # You can wrap inside conditional logic too
    pass  # Stop will be here.
    # Below is code you want to use the debugger to do things.
    ....  # more Python code
    # If you get to a place in the program where you aren't going
    # want to debug any more, but want to remove debugger trace overhead:
    trepan.api.stop()

Parameter "level" specifies how many stack frames go back. Usually it will be
the default 0. But sometimes though there may be calls in setup to the debugger
that you may want to skip.

Parameter "step_ignore" specifies how many line events to ignore after the
debug() call. 0 means don't even wait for the debug() call to finish.

In situations where you want an immediate stop in the "debug" call
rather than the statement following it ("pass" above), add parameter
step_ignore=0 to debug() like this::

    import trepan.api  # Needed only once
    # ... as before
    trepan.api.debug(step_ignore=0)
    # ... as before

Module variable _debugger_obj_ from module trepan.debugger is used as
the debugger instance variable; it can be subsequently used to change
settings or alter behavior. It should be of type Debugger (found in
module trepan). If not, it will get changed to that type::

   $ python
   >>> from trepan.debugger import debugger_obj
   >>> type(debugger_obj)
   <type 'NoneType'>
   >>> import trepan.api
   >>> trepan.api.debug()
   ...
   (Trepan) c
   >>> from trepan.debugger import debugger_obj
   >>> debugger_obj
   <trepan.debugger.Debugger instance at 0x7fbcacd514d0>
   >>>

If however you want your own separate debugger instance, you can
create it from the debugger _class Debugger()_ from module
trepan.debugger::

  $ python
  >>> from trepan.debugger import Debugger
  >>> dbgr = Debugger()  # Add options as desired
  >>> dbgr
  <trepan.debugger.Debugger instance at 0x2e25320>

`dbg_opts' is an optional "options" dictionary that gets fed
trepan.Debugger(); `start_opts' are the optional "options"
dictionary that gets fed to trepan.Debugger.core.start().
"""
    if not isinstance(Mdebugger.debugger_obj, Mdebugger.Trepan):
        Mdebugger.debugger_obj = Mdebugger.Trepan(dbg_opts)
        Mdebugger.debugger_obj.core.add_ignore(debug, stop)
        pass
    core = Mdebugger.debugger_obj.core
    frame = sys._getframe(0 + level)
    core.set_next(frame)
    if start_opts and 'startup-profile' in start_opts and start_opts['startup-profile']:
        dbg_initfiles = start_opts['startup-profile']
        from trepan import options
        options.add_startup_file(dbg_initfiles)
        for init_cmdfile in dbg_initfiles:
            core.processor.queue_startfile(init_cmdfile)
    if not core.is_started():
        core.start(start_opts)
        pass
    if post_mortem:
        debugger_on_post_mortem()
        pass
    if 0 == step_ignore:
        frame = sys._getframe(1 + level)
        core.stop_reason = 'at a debug() call'
        old_trace_hook_suspend = core.trace_hook_suspend
        core.trace_hook_suspend = True
        core.processor.event_processor(frame, 'line', None)
        core.trace_hook_suspend = old_trace_hook_suspend
    else:
        core.step_ignore = step_ignore - 1
        pass
    return
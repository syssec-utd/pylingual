from __future__ import annotations
import asyncio
import functools
import inspect
from prettyqt.qt import QtCore

def Slot(*args):

    def outer_decorator(fn):
        if inspect.iscoroutinefunction(fn):

            @QtCore.Slot(*args)
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                return asyncio.create_task(fn(*args, **kwargs))
            return wrapper
        else:
            return fn
    return outer_decorator
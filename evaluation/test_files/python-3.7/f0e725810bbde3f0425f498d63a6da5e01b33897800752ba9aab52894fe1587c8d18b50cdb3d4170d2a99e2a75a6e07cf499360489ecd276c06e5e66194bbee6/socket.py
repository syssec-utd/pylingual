"""
Module SOCKET -- UI Socket Handler Classes
Sub-Package UI.SOCKET of Package PLIB3 -- Python UI Framework
Copyright (C) 2008-2022 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

class PSocketNotifierBase(object):

    def __init__(self, obj, notify_type, select_fn, notify_fn):
        self._obj = obj
        self._notify_type = notify_type
        self.select_fn = select_fn
        self.notify_fn = notify_fn

    def set_enabled(self, enable):
        """Enable or disable this specific notifier.
        """
        raise NotImplementedError

    @classmethod
    def start(cls):
        """Tell the notifier event loop to start processing socket events.
        """
        pass

    @classmethod
    def done(cls):
        """Tell the notifier event loop to stop processing socket events.
        """
        pass
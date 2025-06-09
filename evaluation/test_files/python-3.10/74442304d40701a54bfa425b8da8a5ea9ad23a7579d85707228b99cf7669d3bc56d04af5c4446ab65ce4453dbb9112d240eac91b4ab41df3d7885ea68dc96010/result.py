from datetime import datetime, timedelta, time
from enum import Enum

class Status(Enum):
    UNSET = -1
    IGNORE = 256
    ERROR = 512
    CANCELED = 0
    SELECTED = 199
    SELECTED_SECOND = 193
    SELECTED_MINUTE = 194
    SELECTED_HOUR = 196
    CHANGED = 135
    CHANGED_SECOND = 129
    CHANGED_MINUTE = 130
    CHANGED_HOUR = 132
    CHANGE_SECOND = 65
    CHANGE_MINUTE = 66
    CHANGE_HOUR = 68
    SELECT_GROUP_SECOND = 257
    SELECT_GROUP_MINUTE = 258
    SELECT_GROUP_HOUR = 260
    BACK_TO_GROUP = 16384

class Result:
    selected: bool
    status: Status

    def __init__(self, status: Status=Status.UNSET, **kwargs):
        self.status = status
        self.selected = kwargs.get('selected', self.status == Status.SELECTED) is True
        self._hours = kwargs.get('hours', 0)
        self._minutes = kwargs.get('minutes', 0)
        self._seconds = kwargs.get('seconds', 0)
        self._editable = kwargs.get('editable', False) is True
        self._datetime = None
        self._timedelta = None
        self._time = None

    def _clear(self):
        self._datetime = None
        self._timedelta = None
        self._time = None

    def __str__(self):
        if self._time:
            return 'Result<{status} {time}>'.format(status=self.status, time=self._time.strftime('%H:%M:%S'))
        return 'Result({status})'.format(status=self.status)

    def __repr__(self):
        return 'aiogram_timepicker.result.Result({status}, hours={hours}, minutes={minutes}, seconds={seconds})'.format(status=self.status, hours=self._hours, minutes=self._minutes, seconds=self._seconds)

    @property
    def editable(self):
        return self._editable

    @editable.setter
    def editable(self, value: bool):
        if not self._editable:
            AttributeError()
        self._editable = value is True

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value: int):
        if not self._editable:
            AttributeError()
        self._hours = value
        self._clear()

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value: int):
        if not self._editable:
            AttributeError()
        self._minutes = value
        self._clear()

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value: int):
        if not self._editable:
            AttributeError()
        self._seconds = value
        self._clear()

    @property
    def datetime(self):
        if not self._datetime:
            self._datetime = datetime(1970, 1, 1) + self.timedelta
        return self._datetime

    @property
    def time(self):
        if not self._time:
            self._time = time(self._hours, self._minutes, self._seconds)
        return self._time

    @property
    def timedelta(self):
        if not self._timedelta:
            self._timedelta = timedelta(hours=self._hours, minutes=self._minutes, seconds=self._seconds)
        return self._timedelta
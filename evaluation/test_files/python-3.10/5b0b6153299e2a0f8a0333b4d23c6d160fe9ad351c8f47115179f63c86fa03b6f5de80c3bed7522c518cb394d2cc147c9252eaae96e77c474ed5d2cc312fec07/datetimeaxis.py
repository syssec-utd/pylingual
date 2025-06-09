from __future__ import annotations
import datetime
from prettyqt import charts
from prettyqt.qt import QtCharts

class DateTimeAxis(charts.AbstractAxisMixin, QtCharts.QDateTimeAxis):

    def get_min(self) -> datetime.datetime:
        return self.min().toPython()

    def get_max(self) -> datetime.datetime:
        return self.max().toPython()
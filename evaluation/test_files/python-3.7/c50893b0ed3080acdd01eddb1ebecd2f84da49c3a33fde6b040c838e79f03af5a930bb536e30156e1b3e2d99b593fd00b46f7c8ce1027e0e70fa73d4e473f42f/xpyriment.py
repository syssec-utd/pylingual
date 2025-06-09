"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""
from libopensesame.py3compat import *
from openexp._canvas._line.line import Line
from openexp._canvas._element.xpyriment import XpyrimentElement
from expyriment.stimuli import Line as ExpyrimentLine

class Xpyriment(XpyrimentElement, Line):

    def prepare(self):
        self._stim = ExpyrimentLine(start_point=self.to_xy(self.sx, self.sy), end_point=self.to_xy(self.ex, self.ey), line_width=self.penwidth, colour=self.color.backend_color, anti_aliasing=self.ANTI_ALIAS)
        self._stim.preload()
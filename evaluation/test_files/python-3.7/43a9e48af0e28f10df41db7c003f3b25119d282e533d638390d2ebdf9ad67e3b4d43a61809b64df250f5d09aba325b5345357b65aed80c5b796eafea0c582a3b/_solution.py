import numpy as np
from scipy.interpolate import interp1d

class Solution(np.ndarray):
    """Brief description of 'Solution'"""
    pass

class SolutionContainer(dict):
    """Brief description of 'SolutionContainer'"""
    pass

class SteadyStateSolution(np.ndarray):
    """Brief description of 'SteadyStateSolution'"""

    def __new__(cls, x):
        obj = np.asarray(x).view(cls)
        return obj

class UnsteadySolution(Solution):
    """Brief description of 'UnsteadySolution'"""

    def __new__(cls, x, y):
        obj = np.asarray(y).view(cls)
        obj._x = np.asarray(x).view(cls)
        return obj

    def _create_interpolant(self):
        self._interpolant = interp1d(self._x, self, bounds_error=True)

    def interpolate(self, x):
        """
        Interpolates solution at point 'x'.

        Parameters
        ----------
        x : float
            Point at which the solution is to be interpolated

        Returns
        -------
        ndarray
            Solution interpolated at the given point 'x'

        """
        if not hasattr(self, '_interpolant'):
            self._create_interpolant()
        return self._interpolant(x)
    __call__ = interpolate

class TransientSolution(UnsteadySolution):

    def interpolate(self, t):
        """
        Interpolates solution at time 't'.

        Parameters
        ----------
        t : float
            Time at which the solution is to be interpolated

        Returns
        -------
        ndarray
            Transient solution interpolated at the given time 't'

        Notes
        -----
        't' must reside inside the 'tspan' used during integration.

        """
        return super().interpolate(x=t)

    @property
    def t(self):
        """
        Wrapper to access the generic _x attribute on the super class
        """
        return self._x

class PressureScan(UnsteadySolution):

    def interpolate(self, p):
        s = super().interpolate(x=p).astype(self.dtype)
        return s

    @property
    def p(self):
        """
        Wrapper to access the generic _x attribute on the super class
        """
        return self._x
    __call__ = interpolate
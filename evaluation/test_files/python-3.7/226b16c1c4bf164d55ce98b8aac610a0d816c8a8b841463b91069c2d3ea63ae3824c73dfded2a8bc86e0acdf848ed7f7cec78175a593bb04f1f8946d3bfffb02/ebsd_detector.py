from __future__ import annotations
from copy import deepcopy
from datetime import datetime
import logging
from pathlib import Path
import re
from typing import List, Optional, Tuple, Union
from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from orix.crystal_map import PhaseList
from orix.quaternion import Rotation
from orix.vector import Vector3d
import scipy.stats as scs
from skimage.transform import ProjectiveTransform
from sklearn.linear_model import LinearRegression, RANSACRegressor
from kikuchipy import __version__
from kikuchipy.indexing._hough_indexing import _get_indexer_from_detector
_logger = logging.getLogger(__name__)
CONVENTION_ALIAS = {'bruker': ['bruker'], 'tsl': ['edax', 'tsl', 'amatek'], 'oxford': ['oxford', 'aztec'], 'emsoft': ['emsoft', 'emsoft4', 'emsoft5']}
CONVENTION_ALIAS_ALL = list(np.concatenate(list(CONVENTION_ALIAS.values())))

class EBSDDetector:
    """An EBSD detector class storing its shape, pixel size, binning
    factor, detector tilt, sample tilt and projection center (PC) per
    pattern. Given one or multiple PCs, the detector's gnomonic
    coordinates are calculated. Uses of these include projecting Kikuchi
    bands, given a unit cell, unit cell orientation and family of
    planes, onto the detector.

    Calculation of gnomonic coordinates is based on the work by Aimo
    Winkelmann in the supplementary material to
    :cite:`britton2016tutorial`.

    Parameters
    ----------
    shape
        Number of detector rows and columns in pixels. Default is
        (1, 1).
    px_size
        Size of unbinned detector pixel in um, assuming a square
        pixel shape. Default is 1.
    binning
        Detector binning, i.e. how many pixels are binned into one.
        Default is 1, i.e. no binning.
    tilt
        Detector tilt from horizontal in degrees. Default is 0.
    azimuthal
        Sample tilt about the sample RD (downwards) axis. A positive
        angle means the sample normal moves towards the right
        looking from the sample to the detector. Default is 0.
    sample_tilt
        Sample tilt from horizontal in degrees. Default is 70.
    pc
        X, Y and Z coordinates of the projection/pattern centers
        (PCs), describing the location of the beam on the sample
        measured relative to the detection screen. See *Notes* for
        the definition and conversions between conventions. If
        multiple PCs are passed, they are assumed to be on the form
        [[x0, y0, z0], [x1, y1, z1], ...]. Default is [0.5, 0.5, 0.5].
    convention
        PC convention. If not given, Bruker's convention is assumed.
        Options are "tsl"/"edax"/"amatek", "oxford"/"aztec", "bruker",
        "emsoft", "emsoft4", and "emsoft5". "emsoft" and "emsoft5" is
        the same convention. See *Notes* for conversions between
        conventions.

    Notes
    -----
    The pattern on the detector is always viewed *from* the detector
    *towards*  the sample. Pattern width and height is here given as
    :math:`N_x` and :math:`N_y` (possibly binned).

    The Bruker PC coordinates :math:`(x_B^*, y_B^*, z_B^*)` are defined
    in fractions of :math:`N_x`, :math:`N_y`, and :math:`N_y`,
    respectively, with :math:`x_B^*` and :math:`y_B^*` defined with
    respect to the upper left corner of the detector. These coordinates
    are used internally, called :math:`(PC_x, PC_y, PC_z)` in the rest
    of the documentation when there is no reference to Bruker
    specifically.

    The EDAX TSL PC coordinates :math:`(x_T^*, y_T^*, z_T^*)` and Oxford
    Instruments PC coordinates :math:`(x_O^*, y_O^*, z_O^*)` are
    identical and defined in fractions of :math:`N_x` with respect to
    the lower left corner of the detector.

    The EMsoft PC coordinates :math:`(x_{pc}, y_{pc})` are defined as
    number of pixels (subpixel accuracy) with respect to the center of
    the detector, with :math:`x_{pc}` towards the right and
    :math:`y_{pc}` upwards. The final PC coordinate :math:`L` is the
    detector distance in microns. Note that prior to EMsoft v5.0,
    :math:`x_{pc}` was defined towards the left.

    Given these definitions, the following is the conversion from
    TSL/Oxford to Bruker

    .. math::

        x_B^* &= x_T^*,\\\\
        y_B^* &= 1 - \\frac{N_x}{N_y} y_T^*,\\\\
        z_B^* &= \\frac{N_x}{N_y} z_T^*.

    The conversion from EMsoft to Bruker is given as

    .. math::

        x_B^* &= \\frac{1}{2} - \\frac{x_{pc}}{N_x b},\\\\
        y_B^* &= \\frac{1}{2} - \\frac{y_{pc}}{N_y b},\\\\
        z_B^* &= \\frac{L}{N_y b \\delta},

    where :math:`\\delta` is the unbinned detector pixel size in
    microns, and :math:`b` is the binning factor.

    Examples
    --------
    Create an EBSD detector and plot the PC on top of a pattern

    >>> import numpy as np
    >>> import kikuchipy as kp
    >>> det = kp.detectors.EBSDDetector(
    ...     shape=(60, 60),
    ...     pc=np.ones((10, 20, 3)) * (0.421, 0.779, 0.505),
    ...     convention="edax",
    ...     px_size=70,
    ...     binning=8,
    ...     tilt=5,
    ...     sample_tilt=70,
    ... )
    >>> det
    EBSDDetector (60, 60), px_size 70 um, binning 8, tilt 5, azimuthal 0, pc (0.421, 0.221, 0.505)
    >>> det.navigation_shape
    (10, 20)
    >>> det.bounds
    array([ 0, 59,  0, 59])
    >>> det.gnomonic_bounds[0, 0]
    array([-0.83366337,  1.14653465, -1.54257426,  0.43762376])
    >>> s = kp.data.nickel_ebsd_small()
    >>> det.plot(
    ...     pattern=s.inav[0, 0].data,
    ...     coordinates="gnomonic",
    ...     draw_gnomonic_circles=True
    ... )
    """

    def __init__(self, shape: Tuple[int, int]=(1, 1), px_size: float=1, binning: int=1, tilt: float=0, azimuthal: float=0, sample_tilt: float=70, pc: Union[np.ndarray, list, tuple]=(0.5, 0.5, 0.5), convention: Optional[str]=None) -> None:
        """Create an EBSD detector with a shape, pixel size, binning
        factor, sample and detector tilt about the detector X axis,
        azimuthal tilt about the detector Y axis and one or more
        projection/pattern centers (PCs).
        """
        self.shape = shape
        self.px_size = px_size
        self.binning = binning
        self.tilt = tilt
        self.azimuthal = azimuthal
        self.sample_tilt = sample_tilt
        self.pc = pc
        if convention is None:
            convention = 'bruker'
        self._set_pc_in_bruker_convention(convention)

    def __repr__(self) -> str:
        pc_average = tuple(self.pc_average.round(3))
        return f'{type(self).__name__} {self.shape}, px_size {self.px_size} um, binning {self.binning}, tilt {self.tilt}, azimuthal {self.azimuthal}, pc {pc_average}'

    @property
    def specimen_scintillator_distance(self) -> float:
        """Return the specimen to scintillator distance, known in EMsoft
        as :math:`L`.
        """
        return self.pcz * self.height

    @property
    def nrows(self) -> int:
        """Return the number of detector pixel rows."""
        return self.shape[0]

    @property
    def ncols(self) -> int:
        """Return the number of detector pixel columns."""
        return self.shape[1]

    @property
    def size(self) -> int:
        """Return the number of detector pixels."""
        return self.nrows * self.ncols

    @property
    def height(self) -> float:
        """Return the detector height in microns."""
        return self.nrows * self.px_size * self.binning

    @property
    def width(self) -> float:
        """Return the detector width in microns."""
        return self.ncols * self.px_size * self.binning

    @property
    def aspect_ratio(self) -> float:
        """Return the number of detector columns divided by rows."""
        return self.ncols / self.nrows

    @property
    def unbinned_shape(self) -> Tuple[int, int]:
        """Return the unbinned detector shape in pixels."""
        return tuple(np.array(self.shape) * self.binning)

    @property
    def px_size_binned(self) -> float:
        """Return the binned pixel size in microns."""
        return self.px_size * self.binning

    @property
    def pc(self) -> np.ndarray:
        """Return or set all projection center coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list or tuple
            Projection center coordinates. If multiple PCs are passed,
            they are assumed to be on the form ``[[x0, y0, z0],
            [x1, y1, z1], ...]``. Default is ``[[0.5, 0.5, 0.5]]``.
        """
        return self._pc

    @pc.setter
    def pc(self, value: Union[np.ndarray, List, Tuple]):
        """Set all projection center coordinates."""
        self._pc = np.atleast_2d(value)

    @property
    def pc_flattened(self) -> np.ndarray:
        """Return flattened array of projection center coordinates of
        shape (:attr:`navigation_size`, 3).
        """
        return self.pc.reshape((-1, 3))

    @property
    def pcx(self) -> np.ndarray:
        """Return or set the projection center x coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center x coordinates. If multiple x coordinates
            are passed, they are assumed to be on the form
            ``[x0, x1,...]``.
        """
        return self.pc[..., 0]

    @pcx.setter
    def pcx(self, value: Union[np.ndarray, list, tuple, float]):
        """Set the x projection center coordinates."""
        self._pc[..., 0] = np.atleast_2d(value)

    @property
    def pcy(self) -> np.ndarray:
        """Return or set the projection center y coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center y coordinates. If multiple y coordinates
            are passed, they are assumed to be on the form
            ``[y0, y1,...]``.
        """
        return self.pc[..., 1]

    @pcy.setter
    def pcy(self, value: Union[np.ndarray, list, tuple, float]):
        """Set y projection center coordinates."""
        self._pc[..., 1] = np.atleast_2d(value)

    @property
    def pcz(self) -> np.ndarray:
        """Return or set the projection center z coordinates.

        Parameters
        ----------
        value : numpy.ndarray, list, tuple or float
            Projection center z coordinates. If multiple z coordinates
            are passed, they are assumed to be on the form
            ``[z0, z1,...]``.
        """
        return self.pc[..., 2]

    @pcz.setter
    def pcz(self, value: Union[np.ndarray, list, tuple, float]):
        """Set z projection center coordinates."""
        self._pc[..., 2] = np.atleast_2d(value)

    @property
    def pc_average(self) -> np.ndarray:
        """Return the overall average projection center."""
        ndim = self.pc.ndim
        axis = ()
        if ndim == 2:
            axis += (0,)
        elif ndim == 3:
            axis += (0, 1)
        return np.nanmean(self.pc, axis=axis)

    @property
    def navigation_shape(self) -> tuple:
        """Return or set the navigation shape of the projection center
        array.

        Parameters
        ----------
        value : tuple
            Navigation shape, with a maximum dimension of 2.
        """
        return self.pc.shape[:self.pc.ndim - 1]

    @navigation_shape.setter
    def navigation_shape(self, value: tuple):
        """Set the navigation shape of the projection center array."""
        ndim = len(value)
        if ndim > 2:
            raise ValueError(f'A maximum dimension of 2 is allowed, 2 < {ndim}')
        else:
            self.pc = self.pc.reshape(value + (3,))

    @property
    def navigation_dimension(self) -> int:
        """Return the number of navigation dimensions of the projection
        center array (a maximum of 2).
        """
        return len(self.navigation_shape)

    @property
    def navigation_size(self) -> int:
        """Return the number of projection centers."""
        return int(np.prod(self.navigation_shape))

    @property
    def bounds(self) -> np.ndarray:
        """Return the detector bounds ``[x0, x1, y0, y1]`` in pixel
        coordinates.
        """
        return np.array([0, self.ncols - 1, 0, self.nrows - 1])

    @property
    def x_min(self) -> Union[np.ndarray, float]:
        """Return the left bound of detector in gnomonic coordinates."""
        return -self.aspect_ratio * (self.pcx / self.pcz)

    @property
    def x_max(self) -> Union[np.ndarray, float]:
        """Return the right bound of detector in gnomonic coordinates."""
        return self.aspect_ratio * (1 - self.pcx) / self.pcz

    @property
    def x_range(self) -> np.ndarray:
        """Return the x detector limits in gnomonic coordinates."""
        return np.dstack((self.x_min, self.x_max)).reshape(self.navigation_shape + (2,))

    @property
    def y_min(self) -> Union[np.ndarray, float]:
        """Return the top bound of detector in gnomonic coordinates."""
        return -(1 - self.pcy) / self.pcz

    @property
    def y_max(self) -> Union[np.ndarray, float]:
        """Return the bottom bound of detector in gnomonic coordinates."""
        return self.pcy / self.pcz

    @property
    def y_range(self) -> np.ndarray:
        """Return the y detector limits in gnomonic coordinates."""
        return np.dstack((self.y_min, self.y_max)).reshape(self.navigation_shape + (2,))

    @property
    def gnomonic_bounds(self) -> np.ndarray:
        """Return the detector bounds ``[x0, x1, y0, y1]`` in gnomonic
        coordinates.
        """
        return np.concatenate((self.x_range, self.y_range), axis=-1)

    @property
    def _average_gnomonic_bounds(self) -> np.ndarray:
        return np.nanmean(self.gnomonic_bounds, axis=(0, 1, 2)[:self.navigation_dimension])

    @property
    def x_scale(self) -> np.ndarray:
        """Return the width of a pixel in gnomonic coordinates."""
        if self.ncols == 1:
            x_scale = np.diff(self.x_range)
        else:
            x_scale = np.diff(self.x_range) / (self.ncols - 1)
        return x_scale.reshape(self.navigation_shape)

    @property
    def y_scale(self) -> np.ndarray:
        """Return the height of a pixel in gnomonic coordinates."""
        if self.nrows == 1:
            y_scale = np.diff(self.y_range)
        else:
            y_scale = np.diff(self.y_range) / (self.nrows - 1)
        return y_scale.reshape(self.navigation_shape)

    @property
    def r_max(self) -> np.ndarray:
        """Return the maximum distance from PC to detector edge in
        gnomonic coordinates.
        """
        corners = np.zeros(self.navigation_shape + (4,))
        corners[..., 0] = self.x_min ** 2 + self.y_min ** 2
        corners[..., 1] = self.x_max ** 2 + self.y_min ** 2
        corners[..., 2] = self.x_max ** 2 + self.y_max ** 2
        corners[..., 3] = self.x_min ** 2 + self.y_min ** 2
        return np.atleast_2d(np.sqrt(np.max(corners, axis=-1)))

    @classmethod
    def load(cls, fname: Union[Path, str]) -> EBSDDetector:
        """Return an EBSD detector loaded from a text file saved with
        :meth:`save`.

        Parameters
        ----------
        fname
            Full path to file.

        Returns
        -------
        detector
            Loaded EBSD detector.
        """
        pc = np.loadtxt(fname)
        keys = ['shape', 'px_size', 'binning', 'tilt', 'azimuthal', 'sample_tilt', 'convention', 'navigation_shape']
        detector_kw = dict(zip(keys, [None] * len(keys)))
        with open(fname, mode='r') as f:
            header = []
            for line in f.readlines():
                if line[0] == '#':
                    line = line[2:-1].lstrip(' ')
                    if len(line) > 0:
                        header.append(line)
                        match = re.match('^(\\w+|\\w+\\s\\w+): (.*)', line)
                        if match:
                            groups = match.groups()
                            if groups[0] in detector_kw and len(groups) > 1:
                                detector_kw[groups[0]] = groups[1]
                else:
                    break
        for k in ['shape', 'navigation_shape']:
            shape = detector_kw[k]
            try:
                detector_kw[k] = tuple((int(i) for i in shape[1:-1].split(',')))
            except ValueError:
                detector_kw[k] = None
        for (k, dtype) in zip(['px_size', 'binning', 'tilt', 'azimuthal', 'sample_tilt'], [float, int, float, float, float]):
            value = detector_kw[k].rstrip(' deg')
            try:
                detector_kw[k] = dtype(value)
            except ():
                detector_kw[k] = None
        nav_shape = detector_kw.pop('navigation_shape')
        if isinstance(nav_shape, tuple):
            pc = pc.reshape(nav_shape + (3,))
        return cls(pc=pc, **detector_kw)

    def crop(self, extent: Union[Tuple[int, int, int, int], List[int]]) -> EBSDDetector:
        """Return a new detector with its :attr:`shape` cropped and
        :attr:`pc` values updated accordingly.

        Parameters
        ----------
        extent
            Tuple with four integers: (top, bottom, left, right).

        Returns
        -------
        new_detector
            A new detector with a new shape and PC values.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector((6, 6), pc=[3 / 6, 2 / 6, 0.5])
        >>> det
        EBSDDetector (6, 6), px_size 1 um, binning 1, tilt 0, azimuthal 0, pc (0.5, 0.333, 0.5)
        >>> det.crop((1, 5, 2, 6))
        EBSDDetector (4, 4), px_size 1 um, binning 1, tilt 0, azimuthal 0, pc (0.25, 0.25, 0.75)

        Plot a cropped detector with the PC on a cropped pattern

        >>> s = kp.data.nickel_ebsd_small()
        >>> s.remove_static_background(show_progressbar=False)
        >>> det2 = s.detector
        >>> det2.plot(pattern=s.inav[0, 0].data)
        >>> det3 = det2.crop((10, 50, 20, 60))
        >>> det3.plot(pattern=s.inav[0, 0].data[10:50, 20:60])
        """
        (ny, nx) = self.shape
        (top, bottom, left, right) = extent
        top = max(top, 0)
        bottom = min(bottom, ny)
        left = max(left, 0)
        right = min(right, nx)
        (ny_new, nx_new) = (bottom - top, right - left)
        if any([ny_new <= 0, nx_new <= 0]) or any([not isinstance(e, int) for e in extent]):
            raise ValueError('`extent` (top, bottom, left, right) must be integers and given so that bottom > top and right > left')
        pcx_new = (self.pcx * nx - left) / nx_new
        pcy_new = (self.pcy * ny - top) / ny_new
        pcz_new = self.pcz * ny / ny_new
        return EBSDDetector(shape=(ny_new, nx_new), pc=np.dstack((pcx_new, pcy_new, pcz_new)), tilt=self.tilt, sample_tilt=self.sample_tilt, binning=self.binning, px_size=self.px_size, azimuthal=self.azimuthal)

    def deepcopy(self) -> EBSDDetector:
        """Return a deep copy using :func:`copy.deepcopy`.

        Returns
        -------
        detector
            Identical detector without shared memory.
        """
        return deepcopy(self)

    def estimate_xtilt(self, detect_outliers: bool=False, plot: bool=True, degrees: bool=False, return_figure: bool=False, return_outliers: bool=False, figure_kwargs: Optional[dict]=None) -> Union[float, Tuple[float, np.ndarray], Tuple[float, plt.Figure], Tuple[float, np.ndarray, plt.Figure]]:
        """Estimate the tilt about the detector :math:`X_d` axis.

        This tilt is assumed to bring the sample plane normal into
        coincidence with the detector plane normal (but in the opposite
        direction) :cite:`winkelmann2020refined`.

        See the `reference frame tutorial
        </doc/tutorials/reference_frames.ipynb>`_ for details on the
        detector sample geometry.

        An estimate is found by linear regression of :attr:`pcz` vs.
        :attr:`pcy`.

        Parameters
        ----------
        detect_outliers
            Whether to attempt to detect outliers. If ``False``
            (default), a linear fit to all points is performed. If
            ``True``, a robust fit using the RANSAC algorithm is
            performed instead, which also detects outliers.
        plot
            Whether to plot data points and the estimated line. Default
            is ``True``.
        degrees
            Whether to return the estimated tilt in radians (``False``,
            default) or degrees (``True``).
        return_figure
            Whether to return the plotted figure. Default is ``False``.
        return_outliers
            Whether to return a mask with ``True`` for PC values
            considered outliers. Default is ``False``. If ``True``,
            ``detect_outliers`` is assumed to be ``True`` and the value
            passed is not considered.
        figure_kwargs
            Keyword arguments passed to
            :func:`matplotlib.pyplot.Figure` if ``plot=True``.

        Returns
        -------
        x_tilt
            Estimated tilt about detector :math:`X_d` in radians
            (``degrees=False``) or degrees (``degrees=True``).
        outliers
            Returned if ``return_outliers=True``, in the shape of
            :attr:`navigation_shape`.
        fig
            Returned if ``plot=True`` and ``return_figure=True``.

        Notes
        -----
        This method is adapted from Aimo Winkelmann's function
        ``fit_xtilt()`` in the *xcdskd* Python package. See
        :cite:`winkelmann2020refined` for their use of related
        functions.

        See Also
        --------
        sklearn.linear_model.LinearRegression,
        sklearn.linear_model.RANSACRegressor, estimate_xtilt_ztilt,
        fit_pc
        """
        if self.navigation_size == 1:
            raise ValueError('Estimation requires more than one projection center')
        if return_outliers:
            detect_outliers = True
        if detect_outliers:
            regressor = RANSACRegressor()
        else:
            regressor = LinearRegression()
        pcy = self.pcy.reshape((-1, 1))
        pcz = self.pcz.reshape((-1, 1))
        regressor.fit(pcz, pcy)
        if detect_outliers:
            slope = regressor.estimator_.coef_
        else:
            slope = regressor.coef_
        slope = slope.squeeze()
        x_tilt = np.pi / 2 + np.arctan(slope)
        if detect_outliers:
            is_outlier = ~regressor.inlier_mask_
        else:
            is_outlier = np.zeros(self.navigation_size)
        pcz_fit = np.linspace(np.min(pcz), np.max(pcz), 2)
        pcy_fit = regressor.predict(pcz_fit[:, np.newaxis])
        x_tilt_deg = np.rad2deg(x_tilt)
        if degrees:
            out = (x_tilt_deg,)
        else:
            out = (x_tilt,)
        if return_outliers:
            is_outlier2d = is_outlier.reshape(self.navigation_shape)
            out += (is_outlier2d,)
        if plot:
            if figure_kwargs is None:
                figure_kwargs = {}
            figure_kwargs.setdefault('layout', 'tight')
            fig = plt.figure(**figure_kwargs)
            ax = fig.add_subplot()
            ax.scatter(pcz, pcy, c='yellowgreen', ec='k', label='Data')
            if detect_outliers:
                ax.scatter(pcz[is_outlier], pcy[is_outlier], c='gold', label='Outliers')
            fit_label = 'Fit, tilt = ' + f'{x_tilt_deg:.2f}' + '$^{\\circ}$'
            ax.plot(pcz_fit, pcy_fit, label=fit_label, c='C1')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.0)
            ax.set(aspect='equal', xlabel='PCz', ylabel='PCy')
            if return_figure:
                out += (fig,)
        if len(out) == 1:
            out = out[0]
        return out

    def estimate_xtilt_ztilt(self, degrees: bool=False, is_outlier: Optional[Union[list, tuple, np.ndarray]]=None) -> Union[float, Tuple[float, float]]:
        """Estimate the tilts about the detector :math:`X_d` and
        :math:`Z_d` axes.

        These tilts bring the sample plane normal into coincidence with
        the detector plane normal (but in the opposite direction)
        :cite:`winkelmann2020refined`.

        See the `reference frame tutorial
        </doc/tutorials/reference_frames.ipynb>`_ for details on the
        detector sample geometry.

        Estimates are found by fitting a hyperplane to :attr:`pc` using
        singular value decomposition.

        Parameters
        ----------
        degrees
            Whether to return the estimated tilts in radians (``False``,
            default) or degrees (``True``).
        is_outlier
            Boolean array with ``True`` for PCs to not include in the
            fit. If not given, all PCs are used. Must be of
            :attr:`navigation_shape`.

        Returns
        -------
        x_tilt
            Estimated tilt about detector :math:`X_d` in radians
            (``degrees=False``) or degrees (``degrees=True``).
        z_tilt
            Estimated tilt about detector :math:`Z_d` in radians
            (``degrees=False``) or degrees (``degrees=True``).

        Notes
        -----
        This method is adapted from Aimo Winkelmann's function
        ``fit_plane()`` in the *xcdskd* Python package. Its use is
        described in :cite:`winkelmann2020refined`.

        Winkelmann refers to Gander & Hrebicek, "Solving Problems in
        Scientific Computing", 3rd Ed., Chapter 6, p. 97 for the
        implementation of the hyperplane fitting.

        See Also
        --------
        estimate_xtilt, fit_pc
        """
        if self.navigation_size == 1:
            raise ValueError('Estimation requires more than one projection center')
        pc = self.pc
        if isinstance(is_outlier, np.ndarray):
            pc = pc[~is_outlier]
        pc = pc.reshape((-1, 3))
        pc_centered = pc - pc.mean(axis=0)
        (x_tilt, z_tilt, *_) = _fit_hyperplane(pc_centered)
        if degrees:
            x_tilt = np.rad2deg(x_tilt)
            z_tilt = np.rad2deg(z_tilt)
        return (x_tilt, z_tilt)

    def extrapolate_pc(self, pc_indices: Union[tuple, list, np.ndarray], navigation_shape: tuple, step_sizes: tuple, shape: Optional[tuple]=None, px_size: float=None, binning: int=None, is_outlier: Optional[Union[tuple, list, np.ndarray]]=None):
        """Return a new detector with projection centers (PCs) in a 2D
        map extrapolated from an average PC.

        The average PC :math:`\\bar{PC}` is calculated from :attr:`pc`,
        possibly excluding some PCs based on the ``is_outlier`` mask.
        The sample position having this PC, :math:`(\\bar{x}, \\bar{y})`,
        is assumed to be the one obtained by averaging ``pc_indices``.
        All other PCs :math:`(PC_x, PC_y, PC_z)` in positions
        :math:`(x, y)` are then extrapolated based on the following
        equations given in appendix A in :cite:`singh2017application`:

        .. math::
            PC_x &= \\bar{PC_x} + (\\bar{x} - x) \\cdot \\Delta x / (\\delta \\cdot N_x \\cdot b),\\\\
            PC_y &= \\bar{PC_y} + (\\bar{y} - y) \\cdot \\Delta y \\cdot \\cos{\\alpha} / (\\delta \\cdot N_y \\cdot b),\\\\
            PC_z &= \\bar{PC_z} - (\\bar{y} - y) \\cdot \\Delta y \\cdot \\sin{\\alpha} / (\\delta \\cdot N_y \\cdot b),\\\\

        where :math:`(\\Delta y, \\Delta x)` are the vertical and
        horizontal step sizes, respectively, :math:`(N_y, N_x)` are the
        number of binned detector rows and columns, respectively, the
        angle :math:`\\alpha = 90^{\\circ} - \\sigma + \\theta`, where
        :math:`\\sigma` is the sample tilt and :math:`\\theta` is the
        detector tilt, :math:`\\delta` is the unbinned detector pixel
        size and :math:`b` is the binning factor.

        Parameters
        ----------
        pc_indices
            2D map pixel coordinates (row, column) of each :attr:`pc`,
            possibly outside ``navigation_shape``. Must be a flattened
            array of shape (2,) + :attr:`navigation_size`.
        navigation_shape
            Shape of the output PC array (n rows, n columns).
        step_sizes
            Vertical and horizontal step sizes (dy, dx).
        shape
            Detector (signal) shape (n rows, n columns). If not given,
            (:attr:`nrows`, :attr:`ncols`) is used.
        px_size
            Unbinned detector pixel size. If not given, :attr:`px_size`
            is used.
        binning
            Detector binning factor. If not given, :attr:`binning` is
            used.
        is_outlier
            Boolean array with ``True`` for PCs to not include in the
            fit. If not given, all PCs are used. Must be of
            :attr:`navigation_shape`.

        Returns
        -------
        new_detector
            Detector with :attr:`navigation_shape` given by
            input ``navigation_shape``.
        """
        (dy, dx) = step_sizes
        pc_indices = np.atleast_2d(pc_indices).T
        (ny, nx) = navigation_shape
        if not shape:
            shape = self.shape
        (nrows, ncols) = shape
        if not px_size:
            px_size = self.px_size
        if not binning:
            binning = self.binning
        pc = self.pc_flattened
        if is_outlier is not None:
            is_inlier = ~np.asarray(is_outlier)
            pc = pc[is_inlier]
            pc_indices = pc_indices[is_inlier]
        pc_mean = pc.mean(axis=0)
        pc_indices_mean = pc_indices.mean(axis=1)
        pc_indices_mean = np.round(pc_indices_mean).astype(int)
        alpha = np.deg2rad(90 - self.sample_tilt + self.tilt)
        (y, x) = np.indices((ny, nx), dtype=float)
        factor = px_size * binning
        d_pcx = -(pc_indices_mean[1] - x) * dx / (factor * ncols)
        d_pcy = -(pc_indices_mean[0] - y) * dy * np.cos(alpha) / (factor * nrows)
        d_pcz = +(pc_indices_mean[0] - y) * dy * np.sin(alpha) / (factor * nrows)
        pcx = pc_mean[0] - d_pcx
        pcy = pc_mean[1] - d_pcy
        pcz = pc_mean[2] - d_pcz
        new_detector = self.deepcopy()
        new_detector.pc = np.stack((pcx, pcy, pcz), axis=2)
        new_detector.shape = shape
        new_detector.px_size = px_size
        new_detector.binning = binning
        return new_detector

    def fit_pc(self, pc_indices: Union[list, tuple, np.ndarray], map_indices: Union[list, tuple, np.ndarray], transformation: str='projective', is_outlier: Optional[np.ndarray]=None, plot: bool=True, return_figure: bool=False, figure_kwargs: Optional[dict]=None) -> Union[EBSDDetector, Tuple[EBSDDetector, plt.Figure]]:
        """Return a new detector with interpolated projection centers
        (PCs) for all points in a map by fitting a plane to :attr:`pc`
        :cite:`winkelmann2020refined`.

        Parameters
        ----------
        pc_indices
            2D coordinates (row, column) of each :attr:`pc` in
            ``map_coordinates``. Must be a flattened array of shape
            (2,) + :attr:`navigation_shape`.
        map_indices
            2D coordinates (row, column) of all map points in a regular
            grid to interpolate PCs for. Must be a flattened array of
            shape ``(2,) + map_shape``.
        transformation
            Which transformation function to use when fitting PCs,
            either ``"projective"`` (default) or ``"affine"``. Both
            transformations perserve co-planarity of map points, while
            the projective transformation allows parallel lines in the
            map point grid to become non-parallel within the sample
            plane.
        is_outlier
            Boolean array with ``True`` for PCs to not include in the
            fit. If not given, all PCs are used. Must be of
            :attr:`navigation_shape`.
        plot
            Whether to plot the experimental and estimated PCs (default
            is ``True``).
        return_figure
            Whether to return the figure if ``plot=True`` (default is
            ``False``).
        figure_kwargs
            Keyword arguments passed to
            :func:`matplotlib.pyplot.Figure` if ``plot=True``.

        Returns
        -------
        new_detector
            New detector with as many interpolated PCs as indices given
            in ``map_indices`` and an estimated sample tilt. The
            detector tilt is assumed to be constant.
        fig
            Figure of experimental and estimated PCs, returned if
            ``plot=True`` and ``return_figure=True``.

        Raises
        ------
        ValueError
            If :attr:`navigation_size` is 1 or if the ``pc_indices`` or
            ``map_indices`` arrays have the incorrect shape.

        See Also
        --------
        estimate_xtilt, estimate_xtilt_ztilt, extrapolate_pc

        Notes
        -----
        This method is adapted from Aimo Winkelmann's functions
        ``fit_affine()`` and ``fit_projective()`` in the *xcdskd* Python
        package. Their uses are described in
        :cite:`winkelmann2020refined`. Winkelmann refers to a code
        example from StackOverflow
        (https://stackoverflow.com/a/20555267/3228100) for the affine
        transformation.
        """
        n_pc = self.navigation_size
        if n_pc == 1:
            raise ValueError('Fitting requires multiple projection centers (PCs)')
        pc_indices = np.asarray(pc_indices)
        map_indices = np.asarray(map_indices)
        nav_shape = self.navigation_shape
        if pc_indices.shape != (2,) + nav_shape:
            raise ValueError(f'`pc_indices` array shape {pc_indices.shape} must be equal to {(2,) + nav_shape}')
        if map_indices.ndim not in [2, 3] or map_indices.shape[0] != 2:
            raise ValueError(f'`map_indices` array shape {map_indices.shape} must be (2, m columns) or (2, n rows, m columns)')
        if is_outlier is not None and (not isinstance(is_outlier, np.ndarray) or not np.issubdtype(is_outlier.dtype, np.bool_) or is_outlier.size != n_pc):
            raise ValueError('`is_outlier` must be a boolean array of a size equal to the number of PCs')
        pc_flat = self.pc_flattened
        pc_indices_flat = pc_indices.reshape((2, -1)).T
        pc_indices_flat = np.column_stack((pc_indices_flat, np.ones(n_pc)))
        map_indices_flat = map_indices.reshape((2, -1)).T
        map_indices_flat = np.column_stack((map_indices_flat, np.ones(map_indices_flat.shape[0])))
        if isinstance(is_outlier, np.ndarray):
            is_inlier = ~is_outlier.ravel()
            nav_shape = (np.sum(is_inlier),)
            pc_flat = pc_flat[is_inlier]
            pc_indices_flat = pc_indices_flat[is_inlier]
        if transformation == 'projective':
            pc_average = np.mean(pc_flat, axis=0)
            pc_flat_centered = pc_flat - pc_average
            (pc_fit, pc_fit_map) = _fit_pc_projective(pc_flat_centered, pc_indices_flat, map_indices_flat)
            pc_fit += pc_average
            pc_fit_map += pc_average
        else:
            (pc_fit, pc_fit_map) = _fit_pc_affine(pc_flat, pc_indices_flat, map_indices_flat)
        max_err = np.max(np.abs(pc_flat - pc_fit), axis=0)
        _logger.debug(f'Max. error for (PCx, PCy, PCz): {max_err}')
        (slope, intercept, _, _, _) = scs.linregress(pc_fit[..., 2], pc_fit[..., 1])
        x_tilt = np.pi / 2 + np.arctan(slope)
        x_tilt_deg = np.rad2deg(x_tilt)
        _logger.debug(f'Estimated detector X tilt: {x_tilt_deg:.5f} deg')
        pc_fit_map = pc_fit_map.reshape(map_indices.shape[1:] + (3,))
        new_detector = self.deepcopy()
        new_detector.pc = pc_fit_map
        new_detector.sample_tilt = 90 - x_tilt_deg - new_detector.tilt
        if plot:
            if figure_kwargs is None:
                figure_kwargs = {}
            pc_fit_2d = pc_fit.reshape(nav_shape + (3,))
            fig = _plot_pc_fit(pc_flat, pc_fit_2d, intercept, slope, return_figure=return_figure, figure_kwargs=figure_kwargs)
        else:
            fig = None
        if return_figure and fig:
            return (new_detector, fig)
        else:
            return new_detector

    def get_indexer(self, phase_list: PhaseList, **kwargs) -> 'EBSDIndexer':
        """Return a PyEBSDIndex EBSD indexer.

        Parameters
        ----------
        phase_list
            List of phases. :class:`~pyebsdindex.ebsd_index.EBSDIndexer`
            only supports a list containing one face-centered cubic
            (FCC) phase, one body-centered cubic (BCC) phase or both.
        **kwargs
            Keyword arguments passed to
            :class:`~pyebsdindex.ebsd_index.EBSDIndexer`, except for the
            following arguments which cannot be passed since they are
            determined from the detector or ``phase_list``:
            ``phaselist`` (not to be confused with ``phase_list``),
            ``vendor``, ``PC``, ``sampleTilt``, ``camElev`` and
            ``patDim``.

        Returns
        -------
        pyebsdindex.ebsd_index.EBSDIndexer
            Indexer instance for use with PyEBSDIndex or in
            :meth:`~kikuchipy.signals.EBSD.hough_indexing`.
            ``indexer.PC`` is set equal to :attr:`pc_flattened`.

        Notes
        -----
        Requires that PyEBSDIndex is installed, which is an optional
        dependency of kikuchipy. See :ref:`optional-dependencies` for
        details.
        """
        return _get_indexer_from_detector(phase_list=phase_list, shape=self.shape, pc=self.pc_flattened.squeeze(), sample_tilt=self.sample_tilt, tilt=self.tilt, **kwargs)

    def pc_emsoft(self, version: int=5) -> np.ndarray:
        """Return PC in the EMsoft convention.

        Parameters
        ----------
        version
            Which EMsoft PC convention to use. The direction of the x PC
            coordinate, :math:`x_{pc}`, flipped in version 5.

        Returns
        -------
        new_pc
            PC in the EMsoft convention.

        Notes
        -----
        The PC coordinate conventions of Bruker, EDAX TSL, Oxford
        Instruments and EMsoft are given in the class description. The
        PC is stored in the Bruker convention internally, so the
        conversion is

        .. math::

            x_{pc} &= N_x b \\left(\\frac{1}{2} - x_B^*\\right),\\\\
            y_{pc} &= N_y b \\left(\\frac{1}{2} - y_B^*\\right),\\\\
            L &= N_y b \\delta z_B^*,

        where :math:`N_x` and :math:`N_y` are number of detector columns
        and rows, :math:`b` is binning, :math:`\\delta` is the unbinned
        pixel size, :math:`(x_B^*, y_B^*, z_B^*)` are the Bruker PC
        coordinates, and :math:`(x_{pc}, y_{pc}, L)` are the returned
        EMsoft PC coordinates.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 80),
        ...     pc=(0.4, 0.2, 0.6),
        ...     convention="bruker",
        ...     px_size=59.2,
        ...     binning=8,
        ... )
        >>> det.pc_emsoft()
        array([[   64. ,   144. , 17049.6]])
        >>> det.pc_emsoft(4)
        array([[  -64. ,   144. , 17049.6]])
        """
        return self._pc_bruker2emsoft(version=version)

    def pc_bruker(self) -> np.ndarray:
        """Return PC in the Bruker convention, given in the class
        description.

        Returns
        -------
        new_pc
            PC in the Bruker convention.
        """
        return self.pc

    def pc_tsl(self) -> np.ndarray:
        """Return PC in the EDAX TSL convention.

        Returns
        -------
        new_pc
            PC in the EDAX TSL convention.

        Notes
        -----
        The PC coordinate conventions of Bruker, EDAX TSL, Oxford
        Instruments and EMsoft are given in the class description. The
        PC is stored in the Bruker convention internally, so the
        conversion is

        .. math::

            x_T^* &= x_B^*,\\\\
            y_T^* &= \\frac{N_y}{N_x} (1 - y_B^*),\\\\
            z_T^* &= \\frac{N_y}{N_x} z_B^*,

        where :math:`N_x` and :math:`N_y` are number of detector columns
        and rows, :math:`(x_B^*, y_B^*, z_B^*)` are the Bruker PC
        coordinates, and :math:`(x_T^*, y_T^*, z_T^*)` are the returned
        EDAX TSL PC coordinates.

        Examples
        --------
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 80),
        ...     pc=(0.4, 0.2, 0.6),
        ...     convention="bruker",
        ... )
        >>> det.pc_tsl()
        array([[0.4 , 0.6 , 0.45]])
        """
        return self._pc_bruker2tsl()

    def pc_oxford(self) -> np.ndarray:
        """Return PC in the Oxford convention.

        Returns
        -------
        new_pc
            PC in the Oxford convention.

        Notes
        -----
        The Oxford PC coordinates are identical to the TSL coordinates,
        see :meth:`pc_tsl`.
        """
        return self._pc_bruker2tsl()

    def plot(self, coordinates: str='detector', show_pc: bool=True, pc_kwargs: Optional[dict]=None, pattern: Optional[np.ndarray]=None, pattern_kwargs: Optional[dict]=None, draw_gnomonic_circles: bool=False, gnomonic_angles: Union[None, list, np.ndarray]=None, gnomonic_circles_kwargs: Optional[dict]=None, zoom: float=1, return_figure: bool=False) -> Union[None, Figure]:
        """Plot the detector screen.

        The plotting of gnomonic circles and general style is adapted
        from the supplementary material to :cite:`britton2016tutorial`
        by Aimo Winkelmann.

        Parameters
        ----------
        coordinates
            Which coordinates to use, ``"detector"`` (default) or
            ``"gnomonic"``.
        show_pc
            Show the average projection center in the Bruker convention.
            Default is ``True``.
        pc_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.axes.Axes.scatter`.
        pattern
            A pattern to put on the detector. If not given, no pattern
            is displayed. The pattern array must have the same shape as
            the detector.
        pattern_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.axes.Axes.imshow`.
        draw_gnomonic_circles
            Draw circles for angular distances from pattern. Default is
            ``False``. Circle positions are only correct when
            ``coordinates="gnomonic"``.
        gnomonic_angles
            Which angular distances to plot if
            ``draw_gnomonic_circles=True``. Default is from 10 to 80 in
            steps of 10.
        gnomonic_circles_kwargs
            A dictionary of keyword arguments passed to
            :meth:`matplotlib.patches.Circle`.
        zoom
            Whether to zoom in/out from the detector, e.g. to show the
            extent of the gnomonic projection circles. A zoom > 1 zooms
            out. Default is ``1``, i.e. no zoom.
        return_figure
            Whether to return the figure. Default is False.

        Returns
        -------
        fig
            Matplotlib figure instance, if `return_figure` is True.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> import kikuchipy as kp
        >>> det = kp.detectors.EBSDDetector(
        ...     shape=(60, 60),
        ...     pc=(0.4, 0.8, 0.5),
        ...     convention="tsl",
        ...     sample_tilt=70,
        ... )
        >>> det.plot()
        >>> plt.show()

        Plot with gnomonic coordinates and circles

        >>> det.plot(
        ...     coordinates="gnomonic",
        ...     draw_gnomonic_circles=True,
        ...     gnomonic_circles_kwargs={"edgecolor": "b", "alpha": 0.3}
        ... )
        >>> plt.show()

        Plot a pattern on the detector and return it for saving etc.

        >>> s = kp.data.nickel_ebsd_small()
        >>> fig = det.plot(pattern=s.inav[0, 0].data, return_figure=True)
        """
        (sy, sx) = self.shape
        (pcx, pcy) = self.pc_average[:2]
        if coordinates == 'detector':
            pcy *= sy - 1
            pcx *= sx - 1
            bounds = self.bounds
            bounds[2:] = bounds[2:][::-1]
            x_label = 'x detector'
            y_label = 'y detector'
        else:
            (pcy, pcx) = (0, 0)
            bounds = self._average_gnomonic_bounds
            x_label = 'x gnomonic'
            y_label = 'y gnomonic'
        (fig, ax) = plt.subplots()
        ax.axis(zoom * bounds)
        ax.set(xlabel=x_label, ylabel=y_label, aspect='equal')
        if isinstance(pattern, np.ndarray):
            if pattern.shape != (sy, sx):
                raise ValueError(f'Pattern shape {pattern.shape} must equal the detector shape {(sy, sx)}')
            if pattern_kwargs is None:
                pattern_kwargs = {}
            pattern_kwargs.setdefault('cmap', 'gray')
            ax.imshow(pattern, extent=bounds, **pattern_kwargs)
        else:
            origin = (bounds[0], bounds[2])
            width = np.diff(bounds[:2])[0]
            height = np.diff(bounds[2:])[0]
            ax.add_artist(mpatches.Rectangle(origin, width, height, fc=(0.5,) * 3, zorder=-1))
        if show_pc:
            if pc_kwargs is None:
                pc_kwargs = {}
            default_params_pc = dict(s=300, facecolor='gold', edgecolor='k', marker=MarkerStyle(marker='*', fillstyle='full'), zorder=10)
            _ = [pc_kwargs.setdefault(k, v) for (k, v) in default_params_pc.items()]
            ax.scatter(x=pcx, y=pcy, **pc_kwargs)
        if draw_gnomonic_circles:
            if gnomonic_circles_kwargs is None:
                gnomonic_circles_kwargs = {}
            default_params_gnomonic = {'alpha': 0.4, 'edgecolor': 'k', 'facecolor': 'None', 'linewidth': 3}
            [gnomonic_circles_kwargs.setdefault(k, v) for (k, v) in default_params_gnomonic.items()]
            if gnomonic_angles is None:
                gnomonic_angles = np.arange(1, 9) * 10
            for angle in gnomonic_angles:
                ax.add_patch(plt.Circle((pcx, pcy), np.tan(np.deg2rad(angle)), **gnomonic_circles_kwargs))
        if return_figure:
            return fig

    def plot_pc(self, mode: str='map', return_figure: bool=False, orientation: str='horizontal', annotate: bool=False, figure_kwargs: Optional[dict]=None, **kwargs) -> Union[None, plt.Figure]:
        """Plot all projection centers (PCs).

        Parameters
        ----------
        mode
            String describing how to plot PCs. Options are ``"map"``
            (default), ``"scatter"`` and ``"3d"``. If ``mode="map"``,
            :attr:`navigation_dimension` must be 2.
        return_figure
            Whether to return the figure (default is ``False``).
        orientation
            Whether to align the plots in a ``"horizontal"`` (default)
            or ``"vertical"`` orientation.
        annotate
            Whether to label each pattern with its 1D index into
            :attr:`pc_flattened` when ``mode="scatter"``. Default is
            ``False``.
        figure_kwargs
            Keyword arguments to pass to
            :func:`matplotlib.pyplot.figure` upon figure creation. Note
            that ``layout="tight"`` is used by default unless another
            layout is passed.
        **kwargs
            Keyword arguments passed to the plotting function, which is
            :meth:`~matplotlib.axes.Axes.imshow` if ``mode="map"``,
            :meth:`~matplotlib.axes.Axes.scatter` if ``mode="scatter"``
            and :meth:`~mpl_toolkits.mplot3d.axes3d.Axes3D.scatter`
            if ``mode="3d"``.

        Returns
        -------
        fig
            Figure is returned if ``return_figure=True``.

        Examples
        --------
        Create a detector with smoothly changing PC values, extrapolated
        from a single PC (assumed to be in the upper left corner of a
        map)

        >>> import matplotlib.pyplot as plt
        >>> import kikuchipy as kp
        >>> det0 = kp.detectors.EBSDDetector(
        ... shape=(480, 640), pc=(0.4, 0.3, 0.5), px_size=70, sample_tilt=70
        ... )
        >>> det0
        EBSDDetector (480, 640), px_size 70 um, binning 1, tilt 0, azimuthal 0, pc (0.4, 0.3, 0.5)
        >>> det = det0.extrapolate_pc(
        ... pc_indices=[0, 0], navigation_shape=(5, 10), step_sizes=(20, 20)
        ... )
        >>> det
        EBSDDetector (480, 640), px_size 70 um, binning 1, tilt 0, azimuthal 0, pc (0.398, 0.299, 0.5)

        Plot PC values in maps

        >>> det.plot_pc()
        >>> plt.show()

        Plot in scatter plots in vertical orientation

        >>> det.plot_pc("scatter", orientation="vertical", annotate=True)
        >>> plt.show()

        Plot in a 3D scatter plot, returning the figure for saving etc.

        >>> fig = det.plot_pc("3d", return_figure=True)
        """
        if self.navigation_size == 1:
            raise ValueError('Detector must have more than one projection center value to plot')
        if mode == 'map' and self.navigation_dimension != 2:
            raise ValueError("Detector's navigation dimension must be 2D when plotting PCs in a map")
        modes = ['map', 'scatter', '3d']
        if not isinstance(mode, str) or mode.lower() not in modes:
            raise ValueError(f"Plot mode '{mode}' must be one of the following strings {modes}")
        mode = mode.lower()
        if figure_kwargs is None:
            figure_kwargs = {}
        figure_kwargs.setdefault('layout', 'tight')
        if mode in ['map', 'scatter']:
            (w, h) = plt.rcParams['figure.figsize']
            k = max(w, h) / 3
            if orientation == 'horizontal':
                figure_kwargs.setdefault('figsize', (6 * k, 2 * k))
                subplots_kw = dict(ncols=3)
            else:
                figure_kwargs.setdefault('figsize', (2 * k, 6 * k))
                subplots_kw = dict(nrows=3)
        if mode in ['scatter', '3d']:
            kwargs.setdefault('c', np.arange(self.navigation_size))
            kwargs.setdefault('ec', 'k')
            kwargs.setdefault('clip_on', False)
        fig = plt.figure(**figure_kwargs)
        labels = ['PCx', 'PCy', 'PCz']
        if mode == 'map':
            axes = fig.subplots(**subplots_kw)
            for (i, ax) in enumerate(axes):
                ax.set(xlabel='Column', ylabel='Row', aspect='equal')
                im = ax.imshow(self.pc[..., i], **kwargs)
                divider = make_axes_locatable(ax)
                cax = divider.append_axes(position='right', size='5%', pad=0.1)
                fig.colorbar(im, cax=cax, label=labels[i])
        elif mode == 'scatter':
            pc_flat = self.pc_flattened
            axes = fig.subplots(**subplots_kw)
            for (i, (j, k)) in enumerate([[0, 1], [0, 2], [2, 1]]):
                x_coord = pc_flat[:, j]
                y_coord = pc_flat[:, k]
                axes[i].scatter(x_coord, y_coord, **kwargs)
                axes[i].set(xlabel=labels[j], ylabel=labels[k], aspect='equal')
                if annotate:
                    for (l, (x, y)) in enumerate(zip(x_coord, y_coord)):
                        axes[i].text(x, y, l, ha='left', va='bottom')
            axes[0].invert_xaxis()
            axes[1].invert_xaxis()
            axes[1].invert_yaxis()
        else:
            ax = fig.add_subplot(projection='3d')
            (pcx, pcy, pcz) = self.pc_flattened.T
            ax.scatter(pcx, pcz, pcy, **kwargs)
            nav_axes = tuple(np.arange(len(self.pc.shape))[:self.navigation_dimension])
            extent_min = np.min(self.pc, axis=nav_axes)
            extent_max = np.max(self.pc, axis=nav_axes)
            ax.set(xlabel=labels[0], ylabel=labels[2], zlabel=labels[1], xlim=[extent_min[0], extent_max[0]], ylim=[extent_min[2], extent_max[2]], zlim=[extent_min[1], extent_max[1]])
            ax.invert_zaxis()
            if annotate:
                for (i, (x, z, y)) in enumerate(zip(pcx, pcz, pcy)):
                    ax.text(x, z, y, i)
        if return_figure:
            return fig

    def save(self, filename: str, convention: str='Bruker', **kwargs) -> None:
        """Save detector in a text file with projection centers (PCs) in
        the given convention.

        Parameters
        ----------
        filename
            Name of text file to write to. See :func:`~numpy.savetxt`
            for supported file formats.
        convention
            PC convention. Default is Bruker's convention. Options are
            "tsl"/"edax", "oxford", "bruker", "emsoft", "emsoft4", and
            "emsoft5". "emsoft" and "emsoft5" is the same convention.
            See *Notes* in :class:`EBSDDetector` for conversions between
            conventions.
        **kwargs
            Keyword arguments passed to :func:`~numpy.savetxt`, e.g.
            ``fmt="%.4f"`` to reduce the number of PC decimals from the
            default 7 to 4.
        """
        pc = self._get_pc_in_convention(convention)
        pc = pc.reshape(-1, 3)
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        kwargs.setdefault('header', f'EBSDDetector\n  shape: {self.shape}\n  px_size: {self.px_size}\n  binning: {self.binning}\n  tilt: {self.tilt} deg\n  azimuthal: {self.azimuthal} deg\n  sample_tilt: {self.sample_tilt} deg\n  convention: {convention}\n  navigation_shape: {self.navigation_shape}\n\nkikuchipy version: {__version__}\nTime: {time_now}\n\nColumn names: PCx, PCy, PCz')
        kwargs.setdefault('fmt', '%.7f')
        np.savetxt(fname=filename, X=pc, **kwargs)

    def _get_pc_in_bruker_convention(self, convention: str='bruker') -> np.ndarray:
        """Convert current :attr:`pc` to Bruker's convention from
        another convention.

        Parameters
        ----------
        convention
            Convention of the current PCs. Default is "bruker".

        Returns
        -------
        pc
            PC array in Bruker's convention.
        """
        conv = convention.lower()
        if conv in CONVENTION_ALIAS['bruker']:
            return self.pc
        elif conv in CONVENTION_ALIAS['tsl'] + CONVENTION_ALIAS['oxford']:
            return self._pc_tsl2bruker()
        elif conv in CONVENTION_ALIAS['emsoft']:
            try:
                version = int(convention[-1])
            except ValueError:
                version = 5
            return self._pc_emsoft2bruker(version)
        else:
            raise ValueError(f"Projection center convention '{convention}' not among the recognised conventions {CONVENTION_ALIAS_ALL}")

    def _set_pc_in_bruker_convention(self, convention: str='bruker'):
        self.pc = self._get_pc_in_bruker_convention(convention)

    def _get_pc_in_convention(self, convention: str='bruker') -> np.ndarray:
        """Convert current :attr:`pc` from Bruker's convention to
        another convention.

        Parameters
        ----------
        convention
            Convention of the output PCs. Default is "bruker", which
            means the PCs are returned without conversion.

        Returns
        -------
        pc
            PC array in specified convention.
        """
        conv = convention.lower()
        if conv in CONVENTION_ALIAS['bruker']:
            return self.pc
        elif conv in CONVENTION_ALIAS['tsl'] + CONVENTION_ALIAS['oxford']:
            return self._pc_bruker2tsl()
        elif conv in CONVENTION_ALIAS['emsoft']:
            try:
                version = int(convention[-1])
            except ValueError:
                version = 5
            return self._pc_bruker2emsoft(version)
        else:
            raise ValueError(f"Projection center convention '{convention}' not among the recognised conventions {CONVENTION_ALIAS_ALL}")

    def _pc_emsoft2bruker(self, version: int=5) -> np.ndarray:
        new_pc = np.zeros_like(self.pc, dtype=float)
        pcx = self.pcx
        if version < 5:
            pcx = -pcx
        new_pc[..., 0] = 0.5 - pcx / (self.ncols * self.binning)
        new_pc[..., 1] = 0.5 - self.pcy / (self.nrows * self.binning)
        new_pc[..., 2] = self.pcz / (self.nrows * self.binning * self.px_size)
        return new_pc

    def _pc_tsl2bruker(self) -> np.ndarray:
        new_pc = deepcopy(self.pc)
        new_pc[..., 1] = 1 - self.pcy * self.aspect_ratio
        new_pc[..., 2] *= self.aspect_ratio
        return new_pc

    def _pc_bruker2emsoft(self, version: int=5) -> np.ndarray:
        new_pc = np.zeros_like(self.pc, dtype=float)
        new_pc[..., 0] = (0.5 - self.pcx) * self.ncols * self.binning
        if version < 5:
            new_pc[..., 0] = -new_pc[..., 0]
        new_pc[..., 1] = (0.5 - self.pcy) * self.nrows * self.binning
        new_pc[..., 2] = self.pcz * self.nrows * self.binning * self.px_size
        return new_pc

    def _pc_bruker2tsl(self) -> np.ndarray:
        new_pc = deepcopy(self.pc)
        new_pc[..., 1] = (1 - self.pcy) / self.aspect_ratio
        new_pc[..., 2] /= self.aspect_ratio
        return new_pc

def _fit_hyperplane(pc_centered: np.ndarray) -> Tuple[float, float, Rotation, Rotation, np.ndarray]:
    pc_trim_mean = scs.trim_mean(pc_centered, proportiontocut=0.1)
    pc_trim_centered = pc_centered - pc_trim_mean[np.newaxis, :]
    (u, s, vh) = np.linalg.svd(pc_trim_centered, full_matrices=False)
    determinant = np.linalg.det(vh)
    _logger.debug(f'Determinant of SVD: {determinant:.7f}')
    sample_normal = Vector3d(vh[2])
    sample_normal = sample_normal.unit
    if sample_normal.z < 0:
        sample_normal = -sample_normal
    _logger.debug(f'Sample plane normal from SVD: {sample_normal.data.squeeze()}')
    (vx, vy, vz) = sample_normal.data.squeeze()
    x_tilt = np.arccos(vz)
    z_tilt = np.pi / 2 - np.arctan2(vy, vx)
    rot_xtilt = Rotation.from_axes_angles([1, 0, 0], -x_tilt)
    rot_ztilt = Rotation.from_axes_angles([0, 0, 1], -z_tilt)
    sample_normal_tilts = rot_ztilt * rot_xtilt * Vector3d.zvector()
    _logger.debug(f'Sample plane normal from tilts: {sample_normal_tilts.data.squeeze()}')
    return (x_tilt, z_tilt, rot_xtilt, rot_ztilt, pc_trim_mean)

def _fit_pc_projective(pc_centered_flat: np.ndarray, pc_indices_flat: np.ndarray, map_indices_flat: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    (*_, rot_xtilt, rot_ztilt, pc_trim_mean) = _fit_hyperplane(pc_centered_flat)
    v_pc_centered = Vector3d(pc_centered_flat)
    v_pc_trim_mean = Vector3d(pc_trim_mean)
    v_pc_plane = ~(rot_ztilt * rot_xtilt) * (v_pc_centered - v_pc_trim_mean)
    tform = ProjectiveTransform()
    status = tform.estimate(pc_indices_flat[:, :2], v_pc_plane.data[:, :2])
    _logger.debug(f'Status of projective transformation: {status}')
    matrix = tform.params.T
    pc_fit = np.dot(pc_indices_flat, matrix)
    pc_fit /= pc_fit[:, 2, None]
    pc_fit[:, 2] = 0
    v_pc_fit = rot_ztilt * rot_xtilt * Vector3d(pc_fit)
    v_pc_fit += v_pc_trim_mean
    pc_fit_map = np.dot(map_indices_flat, matrix)
    pc_fit_map /= pc_fit_map[:, 2, None]
    pc_fit_map[:, 2] = 0
    v_pc_fit_map = rot_ztilt * rot_xtilt * Vector3d(pc_fit_map)
    v_pc_fit_map += v_pc_trim_mean
    return (v_pc_fit.data, v_pc_fit_map.data)

def _fit_pc_affine(pc_flat: np.ndarray, pc_indices_flat: np.ndarray, map_indices_flat: np.ndarray) -> Tuple[np.array, np.ndarray]:
    (matrix, res, *_) = np.linalg.lstsq(pc_indices_flat, pc_flat, rcond=None)
    _logger.debug(f'Residuals of least squares fit: {res}')
    pc_fit = np.dot(pc_indices_flat, matrix)
    pc_fit_map = np.dot(map_indices_flat, matrix)
    return (pc_fit, pc_fit_map)

def _plot_pc_fit(pc: np.ndarray, pc_fit: np.ndarray, fit_intercept: float, fit_slope: float, figure_kwargs: dict, return_figure: bool=False) -> Union[None, plt.Figure]:
    (pcx, pcy, pcz) = pc.T
    (pcx_fit_2d, pcy_fit_2d, pcz_fit_2d) = pc_fit.T
    pcx_fit = pcx_fit_2d.ravel()
    pcy_fit = pcy_fit_2d.ravel()
    pcz_fit = pcz_fit_2d.ravel()
    pcy_fit_line = fit_intercept + fit_slope * pcz_fit
    data_kw = dict(s=25, c='k')
    fit_kw = dict(s=50, fc='gray', alpha=0.5, ec='k')
    (w, h) = plt.rcParams['figure.figsize']
    figure_kwargs.setdefault('layout', 'compressed')
    figure_kwargs.setdefault('figsize', (w, h))
    fig = plt.figure()
    ax0 = fig.add_subplot(221)
    ax0.set(xlabel='PCx', ylabel='PCy', aspect='equal')
    ax0.scatter(pcx_fit, pcy_fit, **fit_kw)
    ax0.scatter(pcx, pcy, **data_kw)
    ax0.invert_xaxis()
    ax1 = fig.add_subplot(222)
    ax1.set(xlabel='PCx', ylabel='PCz', aspect='equal')
    ax1.scatter(pcx, pcz, **data_kw)
    ax1.scatter(pcx_fit, pcz_fit, **fit_kw)
    ax1.invert_xaxis()
    ax1.invert_yaxis()
    ax2 = fig.add_subplot(223)
    ax2.set(xlabel='PCz', ylabel='PCy', aspect='equal')
    ax2.scatter(pcz, pcy, label='Data', **data_kw)
    ax2.scatter(pcz_fit, pcy_fit, label='Fit', **fit_kw)
    ax2.plot(pcz_fit, pcy_fit_line, 'r-', label='Linear fit')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.0)
    ax3 = fig.add_subplot(224, projection='3d')
    ax3.scatter(pcx, pcz, pcy, **data_kw)
    ax3.scatter(pcx_fit, pcz_fit, pcy_fit, **fit_kw)
    ax3.set(xlabel='PCx', ylabel='PCz', zlabel='PCy', xlim=[np.min([pcx, pcx_fit]), np.max([pcx, pcx_fit])], ylim=[np.min([pcz, pcz_fit]), np.max([pcz, pcz_fit])], zlim=[np.min([pcy, pcy_fit]), np.max([pcy, pcy_fit])])
    ax3.invert_zaxis()
    if pcx_fit_2d.ndim == 2:
        ax3.plot_surface(pcx_fit_2d, pcz_fit_2d, pcy_fit_2d, color='r', alpha=0.5)
    fig.tight_layout()
    if return_figure:
        return fig
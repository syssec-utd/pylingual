"""
Module for assisting with aligning the input into the Zyla camera.
"""
import logging
from time import monotonic
import numpy as np
from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtUiTools import loadUiType
import pyqtgraph as pg
import andor3
import hardware as hw
import configuration as config
from utils import status_message
from signalstorage import signals

class ZylaAlign(*loadUiType(__file__.split('.py')[0] + '.ui')):
    """
    UI panel to view the Zyla image data to assist with alignment.

    :param parent: Parent of the QWidget.
    """
    _data_received = Signal(np.ndarray)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._log = logging.getLogger(__name__)
        pg.setConfigOptions(imageAxisOrder='row-major', antialias=True)
        self.imageplot = self.glw.addPlot(row=0, col=0, enableMenu=False)
        self.imageplot.setLabels(left='Y Pixel Number', bottom='Wavelength (nm)')
        self.image = pg.ImageItem()
        self.imageplot.addItem(self.image)
        self.midline1 = pg.InfiniteLine(angle=0, movable=False)
        self.midline2 = pg.InfiniteLine(angle=0, movable=False)
        self.imageplot.addItem(self.midline1, ignoreBounds=True, pen=(255, 255, 0, 128))
        self.imageplot.addItem(self.midline2, ignoreBounds=True, pen=(255, 255, 0, 128))
        self.fvbplot = self.glw.addPlot(row=1, col=0, enableMenu=False)
        self.fvbplot.setLabels(left='Intensity (a.u.)', bottom='Wavelength (nm)')
        self.fvbplot.setXLink(self.imageplot)
        self.spectrum = self.fvbplot.plot(pen=(255, 255, 0), name='Signal')
        self.glw.ci.layout.setRowStretchFactor(0, 2)
        self.glw.ci.layout.setRowStretchFactor(1, 1)
        self.imageplot.getAxis('left').setStyle(tickTextWidth=50, autoExpandTextSpace=False)
        self.fvbplot.getAxis('left').setStyle(tickTextWidth=50, autoExpandTextSpace=False)
        self._detector = None
        self._fsvr = None
        self._interface = None
        self._wl = np.array([400, 800])
        self._pixmax = 65535
        self._last_update_time = monotonic()
        self._update_interval = 0.033
        self._load_ui_config()
        self._data_received.connect(self._set_data)
        self.imageRadioButton.toggled.connect(self._viewarea_changed)

    def showEvent(self, event):
        """
        Handle the Qt event when widget is shown.

        :param event: ``QEvent`` describing the event.
        """
        self.start()
        signals.laser_reprate_changed.connect(self._reprate_changed)

    def hideEvent(self, event):
        """
        Handle the Qt event when widget is hidden.

        :param event: ``QEvent`` describing the event.
        """
        self.stop()
        self._save_ui_config()

    def _viewarea_changed(self):
        """
        Handle view area configuration changes.
        """
        self.stop()
        self.start()

    def _save_ui_config(self):
        """Save GUI control values out to configuration file."""
        config.data['zylaalign']['ui']['viewarea'] = 'full' if self.imageRadioButton.isChecked() else 'active'

    def _load_ui_config(self):
        """Load GUI control values from configuration file."""
        if config.data['zylaalign']['ui']['viewarea'] == 'full':
            self.imageRadioButton.setChecked(True)
        else:
            self.activeRadioButton.setChecked(True)

    def _reprate_changed(self):
        """
        Handle changes to laser reprate if currently acquiring.
        """
        self.stop()
        self.start()

    def start(self):
        """
        Start acquiring images.
        """
        if not ('interface' in hw.modules and (not hw.modules['interface'].devices[0] is None) and hw.modules['interface'].devices[0].is_initialised() and ('detector' in hw.modules) and (not hw.modules['detector'].devices[0] is None) and hw.modules['detector'].devices[0].is_initialised() and (type(hw.modules['detector'].devices[0]).__name__ == 'ZylaFixed')):
            msg = 'Unable to start Zyla alignment due to missing hardware (requires interface, detector=ZylaFixed).'
            self._log.info(msg)
            status_message(msg)
            return
        self._detector = hw.modules['detector'].devices[0]
        self._interface = hw.modules['interface'].devices[0]
        self._detector.cam.SensorCooling = True
        self._detector.cam.FanSpeed = 'On'
        self._detector.cam.CycleMode = 'Fixed'
        self._detector.cam.AccumulateCount = 1
        self._detector.cam.ElectronicShutteringMode = 'Rolling'
        self._detector.cam.SimplePreAmpGainControl = '16-bit (low noise & high well capacity)'
        self._detector.cam.PixelReadoutRate = '280 MHz'
        self._detector.cam.PixelEncoding = 'Mono16'
        self._detector.cam.SpuriousNoiseFilter = False
        self._detector.cam.StaticBlemishCorrection = False
        self._detector.cam.MetadataEnable = False
        if self.imageRadioButton.isChecked():
            self._detector.cam.ExposureTime = config.data['zylaalign']['image']['exposure']
            self._detector.cam.TriggerMode = 'Internal'
            self._detector.cam.AOIHeight = config.data['zylaalign']['image']['height']
            self._detector.cam.FrameRate = self._detector.cam.max('FrameRate')
            self.image.setColorMap(pg.colormap.ColorMap(pos=[0.0, 1.0], color=[(0, 0, 0, 255), (255, 255, 255, 255)]))
        else:
            self._detector.cam.ExposureTime = 5e-05
            self._detector.cam.TriggerMode = 'External'
            self._detector.cam.AOIHeight = 8
            self.image.setColorMap(pg.colormap.ColorMap(pos=[0.0, 0.99, 1.0], color=[(0, 0, 0, 255), (255, 255, 255, 255), (255, 0, 0, 255)]))
        self._detector.cam.AOILeft = 1
        self._detector.cam.AOIWidth = self._detector.cam.max('AOIWidth')
        self._detector.cam.VerticallyCentreAOI = True
        self._detector.cam.FastAOIFrameRateEnable = True
        self.midline1.setPos(0.5 * self._detector.cam.AOIHeight - 4)
        self.midline2.setPos(0.5 * self._detector.cam.AOIHeight + 4)
        self._wl = self._detector.get_pixel_wavelengths()
        self._pixmax = self._detector.get_max_value()
        msg = 'Starting Zyla alignment.'
        self._log.info(msg)
        status_message(msg)
        self.fvbplot.setLimits(xMin=self._wl[0], xMax=self._wl[-1], yMin=0, yMax=self._pixmax)
        self.spectrum.setData()
        self.fvbplot.setRange(xRange=(self._wl[0], self._wl[-1]), yRange=(0, self._pixmax))
        self.spectrum.setData()
        self.imageplot.setLimits(xMin=self._wl[0], xMax=self._wl[-1], yMin=0, yMax=self._detector.cam.AOIHeight)
        self.imageplot.setRange(xRange=(self._wl[0], self._wl[-1]), yRange=(0, self._detector.cam.AOIHeight))
        self.image.setImage(np.zeros((self._detector.cam.AOIHeight, self._detector.cam.AOIWidth)))
        self.image.setRect(self._wl[0], 0, self._wl[-1] - self._wl[0], self._detector.cam.AOIHeight)
        self._interface.stop()
        self._detector.stop()
        self._fsvr = andor3.FrameServer(self._detector.cam, frame_callback=self._frame_handler, fvb=False, frame_rate_max=30)
        self._fsvr.start()
        if not self.imageRadioButton.isChecked():
            self._interface.trigger()

    def stop(self):
        """
        Stop acquiring spectra.
        """
        msg = 'Stopping Zyla alignment.'
        self._log.info(msg)
        status_message(msg)
        try:
            self._interface.stop()
        except:
            self._log.debug('Error stopping interface.')
        try:
            self._fsvr.stop()
        except:
            self._log.debug('Error stopping Zyla frameserver.')
        try:
            self._detector.cam.AOIHeight = 8
            self._detector.cam.TriggerMode = 'External'
            self._detector.cam.ExposureTime = 5e-05
        except:
            pass
        self._detector = None
        self._fsvr = None
        self._interface = None

    def _frame_handler(self, n, data, timestamp):
        """
        Handle a frame received from the Zyla's FrameServer.
        """
        this_update_time = monotonic()
        if this_update_time > self._last_update_time + self._update_interval:
            self._data_received.emit(data.copy()[::-1])
            self._last_update_time = this_update_time

    def _set_data(self, data):
        """
        Update the plot with the provided image data.

        This should only be called from inside the Qt event loop. Emit the :data:`_data_received`
        signal or call :meth:`_frame_handler` if the plot needs to be updated from alternative
        background threads.

        :param data: Camera image data.
        """
        if data is None:
            self.image.setImage()
            self.spectrum.setData()
        else:
            try:
                rowstart = int(data.shape[1] / 2 - 4)
                rowend = rowstart + 8
                self.spectrum.setData(self._wl, np.mean(data[:, rowstart:rowend], axis=1))
            except (AttributeError, ValueError):
                self._log.exception('Error setting spectrum data.')
                self.spectrum.setData()
            try:
                if self.imageRadioButton.isChecked():
                    self.image.setImage(data.T, autoLevels=True)
                else:
                    self.image.setImage(data.T, levels=(0, self._pixmax))
            except:
                self._log.exception('Error setting image data.')
                self.image.setImage()
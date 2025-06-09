"""
contains gui relative to semi-automatic axis calculation
"""
__authors__ = ['H. Payno']
__license__ = 'MIT'
__date__ = '20/05/2021'
from silx.gui import qt
from tomwer.gui import icons
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import SADeltaBetaProcess
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams
from tomwer.gui.utils.buttons import TabBrowsersButtons
from tomwer.gui.reconstruction.nabu.slices import NabuWindow
from tomwer.gui.reconstruction.scores.scoreplot import ScorePlot as _ScorePlot
from tomwer.gui.reconstruction.scores.scoreplot import DelaBetaSelection
from tomwer.core.process.reconstruction.nabu.utils import _NabuMode
from tomwer.core.process.reconstruction.nabu.utils import ConfigurationLevel
from tomwer.core.process.reconstruction.nabu.utils import retrieve_lst_of_value_from_str
from tomwer.gui.reconstruction.scores.control import ControlWidget
from tomwer.gui.reconstruction.saaxis.sliceselector import SliceSelector
from tomwer.gui.reconstruction.nabu.nabuconfig.phase import _NabuPhaseConfig
from tomwer.core.scan.scanbase import TomwerScanBase
import typing
import numpy
import logging
_logger = logging.getLogger(__name__)

class ScorePlot(_ScorePlot, constructor=DelaBetaSelection):
    """Score plot dedicated to center delta / beta values."""

    def _updateScores(self):
        scan = self.__scan() if self.__scan else None
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            if scan.sa_delta_beta_params:
                scan.sa_delta_beta_params.score_method = self.getScoreMethod()
                SADeltaBetaProcess.autofocus(scan)
        self.setVarScores(scores=self._scores, score_method=self.getScoreMethod(), update_only_scores=True)

    def _applyAutofocus(self):
        scan = self.__scan() if self.__scan else None
        if scan is None:
            return
        if scan.sa_delta_beta_params:
            best_db = scan.sa_delta_beta_params.autofocus
            if best_db:
                self._varSlider.setVarValue(best_db)

class _SADeltaBetaTabWidget(qt.QTabWidget):
    sigConfigurationChanged = qt.Signal()
    'Signal emit when the configuration changes'

    def __init__(self, parent=None):
        qt.QTabWidget.__init__(self, parent=parent)
        self._deltaBetaSelectionWidget = DeltaBetaSelectionWidget(self)
        delta_beta_icon = icons.getQIcon('delta_beta')
        self.addTab(self._deltaBetaSelectionWidget, delta_beta_icon, 'delta beta values')
        self._nabuSettings = NabuWindow(self)
        self._nabuSettings.setConfigurationLevel(level='required')
        self._nabuSettings.hidePaganinInterface()
        self._nabuSettings.hideSlicesInterface()
        nabu_icon = icons.getQIcon('nabu')
        self.addTab(self._nabuSettings, nabu_icon, 'reconstruction settings')
        self._resultsViewer = ScorePlot(self, variable_name='db')
        results_icon = icons.getQIcon('results')
        self.addTab(self._resultsViewer, results_icon, 'reconstructed slices')
        self._nabuSettings.sigConfigChanged.connect(self._configurationChanged)
        self._deltaBetaSelectionWidget.sigConfigurationChanged.connect(self._configurationChanged)
        self._resultsViewer.sigConfigurationChanged.connect(self._configurationChanged)
        self.setNabuReconsParams = self._nabuSettings.setConfiguration
        self.getNabuReconsParams = self._nabuSettings.getConfiguration
        self.saveReconstructedSlicesTo = self._resultsViewer.saveReconstructedSlicesTo

    def setDeltaBetaScores(self, *args, **kwargs):
        self._resultsViewer.setVarScores(*args, **kwargs)

    def setCurrentVarValue(self, *args, **kwargs):
        self._resultsViewer.setCurrentVarValue(*args, **kwargs)

    def getCurrentVarValue(self):
        return self._resultsViewer.getCurrentVarValue()

    def showResults(self):
        self.setCurrentWidget(self._resultsViewer)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def lockAutoFocus(self, lock):
        self._resultsViewer.lockAutoFocus(lock=lock)

    def isAutoFocusLock(self):
        return self._resultsViewer.isAutoFocusLock()

    def hideAutoFocusButton(self):
        self._resultsViewer.hideAutoFocusButton()

    def getDeltaBetaValues(self):
        """Return db values to be computed"""
        return self._deltaBetaSelectionWidget.getDeltaBetaValues()

    def setDeltaBetaValues(self, values):
        """set db values to be computed"""
        self._deltaBetaSelectionWidget.setDeltaBetaValues(values)

    def loadPreprocessingParams(self):
        """load reconstruction nabu if tomwer has already process this
        dataset. Not done for now"""
        return False

    def setScan(self, scan):
        self._resultsViewer.setScan(scan)
        self._nabuSettings.setScan(scan)
        if self.loadPreprocessingParams() and scan.axis_params is not None:
            self._nabuSettings.setConfiguration(scan.axis_params)
        self._deltaBetaSelectionWidget.setScan(scan)

    def getConfiguration(self):
        nabu_config = self.getNabuReconsParams()
        enable_ht = int(self._nabuSettings.getMode() is _NabuMode.HALF_ACQ)
        nabu_config['reconstruction']['enable_halftomo'] = enable_ht
        return {'slice_index': self.getReconstructionSlice(), 'nabu_params': nabu_config, 'score_method': self.getScoreMethod().value, 'delta_beta_values': self.getDeltaBetaValues()}

    def getReconstructionSlice(self):
        return self._deltaBetaSelectionWidget.getSlice()

    def setReconstructionSlice(self, slice):
        return self._deltaBetaSelectionWidget.setSlice(slice=slice)

    def setConfiguration(self, config):
        if isinstance(config, QSADeltaBetaParams):
            config = config.to_dict()
        if not isinstance(config, dict):
            raise TypeError('config should be a dictionary or a SAAxisParams. Not {}'.format(type(config)))
        db_values = config.get('delta_beta_values', None)
        if db_values is not None:
            self.setDeltaBetaValues(db_values)
        slice_index = config.get('slice_index', None)
        if slice_index is not None:
            self.setReconstructionSlice(slice_index)
        if 'nabu_params' in config:
            self.setNabuReconsParams(config['nabu_params'])
        if 'score_method' in config:
            self.setScoreMethod(config['score_method'])

    def getScoreMethod(self):
        return self._resultsViewer.getScoreMethod()

    def setScoreMethod(self, method):
        self._resultsViewer.setScoreMethod(method)

    def close(self):
        self._stopAnimationThread()
        self._resultsViewer.close()
        self._resultsViewer = None
        self._deltaBetaSelectionWidget.close()
        self._deltaBetaSelectionWidget = None
        self._nabuSettings.close()
        self._nabuSettings = None
        super().close()

    def _stopAnimationThread(self):
        self._resultsViewer._stopAnimationThread()

    def setSliceRange(self, min_, max_):
        self._deltaBetaSelectionWidget.setSliceRange(min_, max_)

class SADeltaBetaWindow(qt.QMainWindow):
    """
    Widget used to determine half-automatically the better delta / beta value
    """

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self._db_values = []
        self._urls = []
        self._scan = None
        self._qdeltabeta_rp = QSADeltaBetaParams()
        self.setWindowFlags(qt.Qt.Widget)
        self._tabWidget = _SADeltaBetaTabWidget(self)
        self.setCentralWidget(self._tabWidget)
        self._browserButtons = TabBrowsersButtons(self)
        self._dockWidgetBrwButtons = qt.QDockWidget(self)
        self._dockWidgetBrwButtons.setWidget(self._browserButtons)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetBrwButtons)
        self._dockWidgetBrwButtons.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._sadbControl = ControlWidget(self)
        self._dockWidgetCtrl = qt.QDockWidget(self)
        self._dockWidgetCtrl.setWidget(self._sadbControl)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetCtrl)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.sigConfigurationChanged = self._tabWidget.sigConfigurationChanged
        self._browserButtons.sigNextReleased.connect(self._showNextPage)
        self._browserButtons.sigPreviousReleased.connect(self._showPreviousPage)
        self._sadbControl.sigComputationRequest.connect(self._launchReconstructions)
        self._sadbControl.sigValidateRequest.connect(self._validate)

    def showResults(self):
        self._tabWidget.showResults()

    def compute(self):
        """force compute of the current scan"""
        'force compute of the current scan'
        self._sadbControl.sigComputationRequest.emit()

    def getConfiguration(self) -> dict:
        return self._tabWidget.getConfiguration()

    def setConfiguration(self, config: dict):
        self._tabWidget.setConfiguration(config)

    def getQDeltaBetaRP(self):
        return self._qdeltabeta_rp

    def setScan(self, scan):
        self._scan = scan
        self._tabWidget.setScan(scan)

    def getScan(self):
        return self._scan

    def lockAutofocus(self, lock):
        self._tabWidget.lockAutoFocus(lock=lock)

    def isAutoFocusLock(self):
        return self._tabWidget.isAutoFocusLock()

    def hideAutoFocusButton(self):
        return self._tabWidget.hideAutoFocusButton()

    def _launchReconstructions(self):
        """callback when we want to launch the reconstruction of the
        slice for n delta/beta value"""
        raise NotImplementedError('Base class')

    def _validate(self):
        raise NotImplementedError('Base class')

    def _showNextPage(self, *args, **kwargs):
        idx = self._tabWidget.currentIndex()
        idx += 1
        if idx < self._tabWidget.count():
            self._tabWidget.setCurrentIndex(idx)

    def _showPreviousPage(self, *args, **kwargs):
        idx = self._tabWidget.currentIndex()
        idx -= 1
        if idx >= 0:
            self._tabWidget.setCurrentIndex(idx)

    def close(self):
        self._tabWidget.close()
        self._tabWidget = None
        super().close()

    def stop(self):
        self._stopAnimationThread()

    def _stopAnimationThread(self):
        self._tabWidget._stopAnimationThread()

    def setDBScores(self, scores: dict, score_method: typing.Union[str, ScoreMethod], img_width=None, update_only_scores=False):
        """

        :param dict scores: cor value (float) as key and
                            tuple(url: DataUrl, score: float) as value
        """
        self._tabWidget.setDeltaBetaScores(scores=scores, score_method=score_method, img_width=img_width, update_only_scores=update_only_scores)

    def getScoreMethod(self):
        return self._tabWidget.getScoreMethod()

    def setCurrentDeltaBetaValue(self, value):
        self._tabWidget.setCurrentVarValue(value)

    def getCurrentDeltaBetaValue(self):
        return self._tabWidget.getCurrentVarValue()

    def setSlicesRange(self, min_, max_):
        self._tabWidget.setSliceRange(min_, max_)

    def saveReconstructedSlicesTo(self, output_folder):
        self._tabWidget.saveReconstructedSlicesTo(output_folder=output_folder)

class DeltaBetaSelectionWidget(qt.QWidget):
    """Widget used to select the range of delta / beta to use"""
    sigConfigurationChanged = qt.Signal()
    _DEFAULT_VERTICAL_SLICE_MODE = ('middle', 'other')

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self.setLayout(qt.QVBoxLayout())
        self._sliceGB = qt.QGroupBox('slice', self)
        self.layout().addWidget(self._sliceGB)
        self._sliceGB.setLayout(qt.QGridLayout())
        self._label = qt.QLabel('slice', self)
        self._sliceGB.layout().addWidget(self._label, 0, 0, 1, 1)
        sl_spacer = qt.QWidget(self)
        sl_spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._sliceGB.layout().addWidget(sl_spacer, 0, 5, 1, 1)
        self._defaultSlicesCB = qt.QComboBox(self)
        for mode in self._DEFAULT_VERTICAL_SLICE_MODE:
            self._defaultSlicesCB.addItem(mode)
        self._sliceGB.layout().addWidget(self._defaultSlicesCB, 0, 1, 1, 1)
        self._sliceSelectionQSB = SliceSelector(self, insert=False, invert_y_axis=True)
        self._sliceSelectionQSB.addSlice(value=0, name='Slice', color='green')
        self._sliceSelectionQSB.setFixedSize(qt.QSize(250, 250))
        self._sliceGB.layout().addWidget(self._sliceSelectionQSB, 1, 0, 1, 5)
        self._paganinGB = qt.QGroupBox('paganin', self)
        self._paganinGB.setLayout(qt.QVBoxLayout())
        self._mainWindow = _NabuPhaseConfig(self, scrollArea=None)
        self._mainWindow.setConfigurationLevel(ConfigurationLevel.ADVANCED)
        self._paganinGB.layout().addWidget(self._mainWindow)
        self._mainWindow._methodCB.hide()
        self._mainWindow._methodLabel.hide()
        self.layout().addWidget(self._paganinGB)
        widget_spacer = qt.QWidget(self)
        widget_spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(widget_spacer)
        self._sliceSelectionQSB.sigSlicesChanged.connect(self._updated)
        self._mainWindow.sigConfChanged.connect(self._updated)
        self._defaultSlicesCB.currentIndexChanged.connect(self._updated)
        self._defaultSlicesCB.currentIndexChanged.connect(self._updateModeCB)
        self.setSlice('middle')

    def _updated(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def setSlice(self, slice: typing.Union['str', int]):
        if isinstance(slice, str):
            if slice != 'middle':
                raise ValueError("Slice should be 'middle' or an int. Not {}".format(slice))
            else:
                self.setMode('middle')
        elif isinstance(slice, int):
            self.setMode('other')
            self._sliceSelectionQSB.setSliceValue('Slice', slice)
        elif isinstance(slice, dict) and 'Slice' in slice:
            self.setMode('other')
            self._sliceSelectionQSB.setSliceValue('Slice', slice['Slice'])
        else:
            raise TypeError("slice should be an int or 'middle'. Not {}".format(type(slice)))

    def setSliceRange(self, min_, max_):
        self._sliceSelectionQSB.setSlicesRange(min_, max_)

    def getMode(self):
        return self._defaultSlicesCB.currentText()

    def setMode(self, mode):
        if mode not in self._DEFAULT_VERTICAL_SLICE_MODE:
            raise ValueError('mode should be in {}. Not {}.'.format(self._DEFAULT_VERTICAL_SLICE_MODE, mode))
        idx = self._defaultSlicesCB.findText(mode)
        self._defaultSlicesCB.setCurrentIndex(idx)
        self._updateModeCB()

    def _updateModeCB(self):
        self._sliceSelectionQSB.setVisible(self.getMode() == 'other')

    def getSlice(self):
        if self.getSliceMode() == 'middle':
            return 'middle'
        else:
            return self._sliceSelectionQSB.getSlicesValue()

    def getSliceMode(self):
        return self._defaultSlicesCB.currentText()

    def setScan(self, scan: TomwerScanBase):
        self._sliceSelectionQSB.setSlicesRange(0, scan.dim_2)

    def getDeltaBetaValues(self) -> numpy.array:
        db_values = self._mainWindow._paganinOpts.getDeltaBeta()
        return retrieve_lst_of_value_from_str(db_values, type_=float)

    def setDeltaBetaValues(self, values: typing.Union[numpy.array, typing.Iterable]):
        values = numpy.array(values)
        step = None
        if len(values) > 3:
            deltas = values[1:] - values[:-1]
            if deltas.min() == deltas.max():
                step = deltas.min()
        deltaBetaQLE = self._mainWindow._paganinOpts._deltaBetaQLE
        if step is None:
            deltaBetaQLE.setText(','.join([str(value) for value in values]))
        else:
            deltaBetaQLE.setText('{from_}:{to_}:{step_}'.format(from_=values.min(), to_=values.max(), step_=step))
__authors__ = ['H. Payno']
__license__ = 'MIT'
__date__ = '01/02/2021'
from ..utils import WidgetLongProcessing
from orangewidget import gui
from orangecontrib.tomwer.orange.managedprocess import SuperviseOW
from orangewidget.settings import Setting
from orangecontrib.tomwer.orange.settings import CallbackSettingsHandler
from orangewidget.widget import Input, Output
from tomwer.synctools.stacks.reconstruction.saaxis import SAAxisProcessStack
from tomwer.synctools.saaxis import QSAAxisParams
from tomwer.synctools.axis import QAxisRP
from tomwer.core.process.reconstruction.axis import AxisProcess
from tomwer.core.scan.scanbase import TomwerScanBase
from silx.gui import qt
from tomwer.gui.reconstruction.saaxis.saaxis import SAAxisWindow as _SAAxisWindow
from processview.core.manager import ProcessManager, DatasetState
from tomwer.core import settings
from tomwer.core import utils
from tomwer.core.process.reconstruction.saaxis.saaxis import SAAxisProcess
from tomwer.core.scan.scanbase import _TomwerBaseDock
import tomwer.core.process.reconstruction.saaxis.saaxis
from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from processview.core import helpers as pv_helpers
import functools
import logging
from typing import Union
_logger = logging.getLogger(__name__)

class SAAxisWindow(_SAAxisWindow):
    sigResultsToBeShow = qt.Signal()
    'signal emit when some results are ready to be display'

    def __init__(self, Outputs, parent=None, process_id=None):
        _SAAxisWindow.__init__(self, parent=parent)
        self.Outputs = Outputs
        self._saaxis_params = QSAAxisParams()
        self._processing_stack = SAAxisProcessStack(saaxis_params=self._saaxis_params, process_id=process_id)
        self.sigValidated.connect(self.validateCurrentScan)
        self._clusterConfig = None

    def setClusterConfig(self, cluster_config: dict):
        if not isinstance(cluster_config, (dict, type(None), SlurmClusterConfiguration)):
            raise TypeError(f'cluster config is expected to be None, dict, {SlurmClusterConfiguration} not {type(cluster_config)}')
        self._clusterConfig = cluster_config

    def _computeEstimatedCor(self) -> Union[float, None]:
        """callback when calculation of a estimated cor is requested"""
        scan = self.getScan()
        if scan is None:
            text = 'No scan is set on the widget currently. No automatic center of rotation to be computed'
            _logger.warning(text)
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            msg.setText(text)
            msg.show()
            return
        else:
            axis_params_info = self.getQAxisRP().get_simple_str()
            text = 'start automatic cor for {} with {}'.format(scan, axis_params_info)
            _logger.inform(text)
            cor_estimation_process = AxisProcess(inputs={'axis_params': self.getQAxisRP(), 'data': scan, 'wait': True}, process_id=-1)
            try:
                cor_estimation_process.run()
            except Exception as e:
                text = 'Unable to run automatic cor calculation. Reason is {}.'.format(e)
                _logger.error(text)
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Critical)
                msg.setText(text)
                msg.show()
                return None
            else:
                cor = scan.axis_params.relative_cor_value
                text = 'automatic cor computed for {}: {} ({})'.format(scan, cor, axis_params_info)
                _logger.inform(text)
                self.setEstimatedCorPosition(value=cor)
                self.getAutomaticCorWindow().hide()
                return cor

    def _launchReconstructions(self):
        """callback when we want to launch the reconstruction of the
        slice for n cor value"""
        scan = self.getScan()
        if scan is None:
            return
        callback = functools.partial(self._mightUpdateResult, scan, self.isAutoFocusLock())
        self._processing_stack.add(data=scan, configuration=self.getConfiguration(), callback=callback)

    def _validate(self):
        pass

    def _mightUpdateResult(self, scan: TomwerScanBase, validate: bool):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError('scan is expected to be an instance of TomwerScanBase')
        if not isinstance(validate, bool):
            raise TypeError('validate is expected to be a boolean')
        if scan == self.getScan():
            self.setCorScores(scan.saaxis_params.scores, score_method=scan.saaxis_params.score_method, img_width=scan.saaxis_params.image_width)
            if scan.saaxis_params.autofocus is not None:
                self.setCurrentCorValue(scan.saaxis_params.autofocus)
            pm = ProcessManager()
            details = pm.get_dataset_details(dataset_id=scan.get_identifier(), process=self._processing_stack)
            ProcessManager().notify_dataset_state(dataset=scan, process=self._processing_stack, details=details, state=DatasetState.WAIT_USER_VALIDATION)
            self.sigResultsToBeShow.emit()
        if validate:
            self.validateScan(scan)

    def wait_processing(self, wait_time):
        self._processing_stack._computationThread.wait(wait_time)

    def validateCurrentScan(self):
        return self.validateScan(self.getScan())

    def validateScan(self, scan):
        if scan is None:
            return
        assert isinstance(scan, TomwerScanBase)
        selected_cor_value = self.getCurrentCorValue()
        details = ProcessManager().get_dataset_details(dataset_id=scan.get_identifier(), process=self._processing_stack)
        if details is None:
            details = ''
        if selected_cor_value is None:
            infos = 'no selected cor value. {} skip SAAXIS'.format(scan)
            infos = '\n'.join((infos, details))
            _logger.warning(infos)
            scan.axis_params.set_relative_value(None)
            pv_helpers.notify_skip(process=self._processing_stack, dataset=scan, details=infos)
        else:
            scan.axis_params.set_relative_value(selected_cor_value)
            infos = 'cor selected for {}: relative: {}, absolute: {}'.format(scan, scan.axis_params.relative_cor_value, scan.axis_params.absolute_cor_value)
            infos = '\n'.join((infos, details))
            pv_helpers.notify_succeed(process=self._processing_stack, dataset=scan, details=infos)
        SAAxisProcess.process_to_tomwer_processes(scan=scan)
        self.Outputs.data.send(scan)

    def getConfiguration(self) -> dict:
        config = super().getConfiguration()
        config['cluster_config'] = self._clusterConfig
        return config

    def setConfiguration(self, config: dict):
        config.pop('cluster_config', None)
        return super().setConfiguration(config)

class SAAxisOW(SuperviseOW, WidgetLongProcessing):
    """
    Widget for semi-automatic center of rotation calculation

    behavior within a workflow:
    * when a scan arrived:
        * if he already has a center of rotation defined (if the axis widget
          has been defined for example) it will be used as
          'estimated center of rotation'
        * if no cor has been computed yet and if the .nx entry contains
          information regarding an "estimated_cor_from_motor" this value will
          be set.
    * if autofocus option is lock:
       * launch the series of reconstruction (with research width defined)
         and the estimated center of rotation if defined. Once the
         reconstruction is ended and if the autofocus button is still lock
         it will select the cor with the highest
         value and mode to workflow downstream.
    * hint: you can define a "multi-step" half-automatic center of rotation
       research by creating several "saaxis" widget and reducing the research
       width.

    Details about :ref:`saaxis score calculation`
    """
    name = 'semi-automated center of rotation'
    id = 'orange.widgets.tomwer.sa_axis'
    description = 'use to compute the center of rotation semi automatic way'
    icon = 'icons/saaxis.png'
    priority = 21
    keywords = ['tomography', 'semi automatic', 'half automatic', 'axis', 'tomwer', 'reconstruction', 'rotation', 'position', 'center of rotation', 'saaxis']
    ewokstaskclass = tomwer.core.process.reconstruction.saaxis.saaxis.SAAxisProcess
    want_main_area = True
    resizing_enabled = True
    allows_cycle = True
    compress_signal = False
    settingsHandler = CallbackSettingsHandler()
    sigScanReady = qt.Signal(TomwerScanBase)
    'Signal emitted when a scan is ready'
    _rpSetting = Setting(dict())
    'SAAxisRP store as dict'
    static_input = Setting({'data': None, 'sa_axis_params': None})

    class Inputs:
        data = Input(name='data', type=TomwerScanBase, doc='one scan to be process', default=True, multiple=False)
        data_recompute = Input(name='change recons params', type=_TomwerBaseDock)
        cluster_in = Input(name='cluster_config', type=SlurmClusterConfiguration, doc='slurm cluster to be used', multiple=False)

    class Outputs:
        data = Output(name='data', type=TomwerScanBase, doc='one scan to be process')
        future_out = Output(name='future_tomo_obj', type=FutureTomwerObject, doc='data with some remote processing')

    def __init__(self, parent=None):
        """

        :param parent: QWidget parent or None
        """
        SuperviseOW.__init__(self, parent)
        WidgetLongProcessing.__init__(self)
        self._layout = gui.vBox(self.mainArea, self.name).layout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._widget = SAAxisWindow(Outputs=self.Outputs, parent=self, process_id=self.process_id)
        self._layout.addWidget(self._widget)
        sa_axis_params = self.static_input.get('sa_axis_params', None)
        if sa_axis_params is None:
            sa_axis_params = self._rpSetting
        self.setConfiguration(sa_axis_params)
        self._widget.sigConfigurationChanged.connect(self._updateSettings)
        self.destroyed.connect(self._widget.stop)
        self._widget._processing_stack.sigComputationStarted.connect(self._startProcessing)
        self._widget._processing_stack.sigComputationEnded.connect(self._endProcessing)
        self._widget.sigValidated.connect(self.accept)
        self._widget.sigResultsToBeShow.connect(self._raiseResults)
        self.wait_processing = self._widget.wait_processing

    def setConfiguration(self, configuration):
        if 'workflow' in configuration:
            autofocus_lock = configuration['workflow'].get('autofocus_lock', None)
            if autofocus_lock is not None:
                self._widget.lockAutofocus(autofocus_lock)
            del configuration['workflow']
        self._widget.setConfiguration(configuration)

    def getCurrentCorValue(self):
        return self._widget.getCurrentCorValue()

    def load_sinogram(self):
        self._widget.loadSinogram()

    def compute(self):
        self._widget.compute()

    def lockAutofocus(self, lock):
        self._widget.lockAutofocus(lock=lock)

    def isAutoFocusLock(self):
        return self._widget.isAutoFocusLock()

    @Inputs.data
    def process(self, scan):
        if scan is None:
            return
        if scan.axis_params is None:
            scan.axis_params = QAxisRP()
        if scan.saaxis_params is None:
            scan.saaxis_params = QSAAxisParams()
        self._skipCurrentScan(new_scan=scan)
        if settings.isOnLbsram(scan) and utils.isLowOnMemory(settings.get_lbsram_path()):
            self.notify_skip(scan=scan, details='saaxis has been skiped for {} because of low space in lbsram'.format(scan))
            self.Outputs.data.send(scan)
        else:
            self._widget.setScan(scan=scan)
            self.notify_pending(scan)
            self.activateWindow()
            if self.isAutoFocusLock():
                self.compute()
            else:
                self.raise_()
                self.show()

    @Inputs.cluster_in
    def setCluster(self, cluster):
        self._widget.setClusterConfig(cluster_config=cluster)

    def _skipCurrentScan(self, new_scan):
        scan = self._widget.getScan()
        if scan is None or str(scan) == str(new_scan):
            return
        current_scan_state = ProcessManager().get_dataset_state(dataset_id=scan.get_identifier(), process=self)
        if current_scan_state in (DatasetState.PENDING, DatasetState.WAIT_USER_VALIDATION):
            details = 'Was pending and has been replaced by another scan.'
            self.notify_skip(scan=scan, details=details)
            self.Outputs.data.send(scan)

    @Inputs.data_recompute
    def reprocess(self, dataset):
        self.lockAutofocus(False)
        self.process(dataset)

    def validateCurrentScan(self):
        self._widget.validateCurrentScan()

    def _updateSettings(self):
        config = self._widget.getConfiguration()
        config.pop('cluster_config', None)
        self._rpSetting = config
        self._rpSetting['workflow'] = {'autofocus_lock': self._widget.isAutoFocusLock()}
        self.static_input = {'data': None, 'sa_axis_params': self._widget.getConfiguration()}
        self.static_input['sa_axis_params']['autofocus_lock'] = self._widget.isAutoFocusLock()

    def _raiseResults(self):
        if not self.isAutoFocusLock():
            self.raise_()
            self.show()
            self._widget.showResults()

    def stop(self):
        self._widget.stop()

    def close(self):
        self.stop()
        self._widget = None
        super().close()

    def getConfiguration(self):
        return self._widget.getConfiguration()
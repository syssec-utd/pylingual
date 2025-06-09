from dataclasses import dataclass
from qtpy.QtWidgets import QFormLayout, QLabel
from ert._c_wrappers.enkf import EnKFMain
from ert.gui.ertnotifier import ErtNotifier
from ert.gui.ertwidgets import AnalysisModuleEdit, addHelpToWidget
from ert.gui.ertwidgets.caseselector import CaseSelector
from ert.gui.ertwidgets.copyablelabel import CopyableLabel
from ert.gui.ertwidgets.models.activerealizationsmodel import ActiveRealizationsModel
from ert.gui.ertwidgets.models.ertmodel import get_runnable_realizations_mask
from ert.gui.ertwidgets.models.targetcasemodel import TargetCaseModel
from ert.gui.ertwidgets.stringbox import StringBox
from ert.libres_facade import LibresFacade
from ert.run_models import EnsembleSmoother
from ert.validation import ProperNameArgument, RangeStringArgument
from .simulation_config_panel import SimulationConfigPanel

@dataclass
class Arguments:
    mode: str
    target_case: str
    realizations: str
    current_case: str = 'default'

class EnsembleSmootherPanel(SimulationConfigPanel):

    def __init__(self, ert: EnKFMain, notifier: ErtNotifier):
        super().__init__(EnsembleSmoother)
        self.ert = ert
        self.notifier = notifier
        facade = LibresFacade(ert)
        layout = QFormLayout()
        self.setObjectName('ensemble_smoother_panel')
        self._case_selector = CaseSelector(notifier)
        layout.addRow('Current case:', self._case_selector)
        runpath_label = CopyableLabel(text=facade.run_path)
        layout.addRow('Runpath:', runpath_label)
        number_of_realizations_label = QLabel(f'<b>{facade.get_ensemble_size()}</b>')
        addHelpToWidget(number_of_realizations_label, 'config/ensemble/num_realizations')
        layout.addRow(QLabel('Number of realizations:'), number_of_realizations_label)
        self._target_case_model = TargetCaseModel(facade, notifier)
        self._target_case_field = StringBox(self._target_case_model, 'config/simulation/target_case')
        self._target_case_field.setValidator(ProperNameArgument())
        layout.addRow('Target case:', self._target_case_field)
        self._analysis_module_edit = AnalysisModuleEdit(facade, module_name='STD_ENKF', help_link='config/analysis/analysis_module')
        self._analysis_module_edit.setObjectName('ensemble_smoother_edit')
        layout.addRow('Analysis module:', self._analysis_module_edit)
        active_realizations_model = ActiveRealizationsModel(facade)
        self._active_realizations_field = StringBox(active_realizations_model, 'config/simulation/active_realizations')
        self._active_realizations_field.setValidator(RangeStringArgument(facade.get_ensemble_size()))
        layout.addRow('Active realizations', self._active_realizations_field)
        self.setLayout(layout)
        self._target_case_field.getValidationSupport().validationChanged.connect(self.simulationConfigurationChanged)
        self._active_realizations_field.getValidationSupport().validationChanged.connect(self.simulationConfigurationChanged)
        self._case_selector.currentIndexChanged.connect(self._realizations_from_fs)

    def isConfigurationValid(self):
        return self._target_case_field.isValid() and self._active_realizations_field.isValid()

    def getSimulationArguments(self):
        arguments = Arguments(mode='ensemble_smoother', current_case=f'{self.notifier.current_case_name}_prior', target_case=self._target_case_model.getValue(), realizations=self._active_realizations_field.text())
        return arguments

    def _realizations_from_fs(self):
        case = str(self._case_selector.currentText())
        mask = get_runnable_realizations_mask(self.notifier.storage, case)
        self._active_realizations_field.model.setValueFromMask(mask)
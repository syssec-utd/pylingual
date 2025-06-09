from abaqusConstants import *
from .AnalysisStep import AnalysisStep
from ..Adaptivity.AdaptiveMeshConstraintState import AdaptiveMeshConstraintState
from ..Adaptivity.AdaptiveMeshDomain import AdaptiveMeshDomain
from ..BoundaryCondition.BoundaryConditionState import BoundaryConditionState
from ..Load.LoadCase import LoadCase
from ..Load.LoadState import LoadState
from ..PredefinedField.PredefinedFieldState import PredefinedFieldState
from ..StepMiscellaneous.Control import Control
from ..StepMiscellaneous.SolverControl import SolverControl
from ..StepOutput.DiagnosticPrint import DiagnosticPrint
from ..StepOutput.FieldOutputRequestState import FieldOutputRequestState
from ..StepOutput.HistoryOutputRequestState import HistoryOutputRequestState
from ..StepOutput.Monitor import Monitor
from ..StepOutput.Restart import Restart

class CoupledThermalElectricalStructuralStep(AnalysisStep):
    """The CoupledThermalElectricalStructuralStep object is used to analyze problems where the
    simultaneous solution of the temperature, stress/displacement and electrical fields is
    necessary.
    The CoupledThermalElectricalStructuralStep object is derived from the AnalysisStep
    object.

    .. note:: 
        This object can be accessed by:

        .. code-block:: python

            import step
            mdb.models[name].steps[name]

        The corresponding analysis keywords are:

        - COUPLED TEMPERATURE-DISPLACEMENT
                - SOLUTION TECHNIQUE
                - STEP
    """
    name: str = ''
    response: SymbolicConstant = TRANSIENT
    timePeriod: float = 1
    nlgeom: Boolean = OFF
    stabilizationMethod: SymbolicConstant = NONE
    stabilizationMagnitude: float = None
    timeIncrementationMethod: SymbolicConstant = AUTOMATIC
    maxNumInc: int = 100
    initialInc: float = None
    minInc: float = None
    maxInc: float = None
    deltmx: float = 0
    cetol: float = 0
    creepIntegration: SymbolicConstant = IMPLICIT
    matrixStorage: SymbolicConstant = SOLVER_DEFAULT
    amplitude: SymbolicConstant = STEP
    extrapolation: SymbolicConstant = LINEAR
    convertSDI: SymbolicConstant = PROPAGATED
    adaptiveDampingRatio: float = 0
    continueDampingFactors: Boolean = OFF
    previous: str = ''
    description: str = ''
    explicit: SymbolicConstant = None
    perturbation: Boolean = OFF
    nonmechanical: Boolean = OFF
    procedureType: SymbolicConstant = None
    suppressed: Boolean = OFF
    fieldOutputRequestState: dict[str, FieldOutputRequestState] = dict[str, FieldOutputRequestState]()
    historyOutputRequestState: dict[str, HistoryOutputRequestState] = dict[str, HistoryOutputRequestState]()
    diagnosticPrint: DiagnosticPrint = DiagnosticPrint()
    monitor: Monitor = None
    restart: Restart = Restart()
    adaptiveMeshConstraintStates: dict[str, AdaptiveMeshConstraintState] = dict[str, AdaptiveMeshConstraintState]()
    adaptiveMeshDomains: dict[str, AdaptiveMeshDomain] = dict[str, AdaptiveMeshDomain]()
    control: Control = Control()
    solverControl: SolverControl = SolverControl()
    boundaryConditionStates: dict[str, BoundaryConditionState] = dict[str, BoundaryConditionState]()
    interactionStates: int = None
    loadStates: dict[str, LoadState] = dict[str, LoadState]()
    loadCases: dict[str, LoadCase] = dict[str, LoadCase]()
    predefinedFieldStates: dict[str, PredefinedFieldState] = dict[str, PredefinedFieldState]()

    def __init__(self, name: str, previous: str, description: str='', response: SymbolicConstant=TRANSIENT, timePeriod: float=1, nlgeom: Boolean=OFF, stabilizationMethod: SymbolicConstant=NONE, stabilizationMagnitude: float=None, timeIncrementationMethod: SymbolicConstant=AUTOMATIC, maxNumInc: int=100, initialInc: float=None, minInc: float=None, maxInc: float=None, deltmx: float=0, cetol: float=0, creepIntegration: SymbolicConstant=IMPLICIT, matrixStorage: SymbolicConstant=SOLVER_DEFAULT, amplitude: SymbolicConstant=STEP, extrapolation: SymbolicConstant=LINEAR, maintainAttributes: Boolean=False, convertSDI: SymbolicConstant=PROPAGATED, adaptiveDampingRatio: float=0, continueDampingFactors: Boolean=OFF):
        """This method creates a CoupledThermalElectricalStructuralStep object.

        .. note:: 
            This function can be accessed by:

            .. code-block:: python

                mdb.models[name].CoupledThermalElectricalStructuralStep

        Parameters
        ----------
        name
            A String specifying the repository key.
        previous
            A String specifying the name of the previous step. The new step appears after this step
            in the list of analysis steps.
        description
            A String specifying a description of the new step. The default value is an empty string.
        response
            A SymbolicConstant specifying the analysis type. Possible values are STEADY_STATE and
            TRANSIENT. The default value is TRANSIENT.
        timePeriod
            A Float specifying the total time period for the step. The default value is 1.0.
        nlgeom
            A Boolean specifying whether geometric nonlinearities should be accounted for during the
            step. The default value is OFF.
        stabilizationMethod
            A SymbolicConstant specifying the stabilization type. Possible values are NONE,
            DISSIPATED_ENERGY_FRACTION, and DAMPING_FACTOR. The default value is NONE.
        stabilizationMagnitude
            A Float specifying the damping intensity of the automatic damping algorithm if the
            problem is expected to be unstable and **stabilizationMethod**≠NONE. The default value is
            2×10-4.
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values
            are FIXED and AUTOMATIC. The default value is AUTOMATIC.
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100.
        initialInc
            A Float specifying the initial time increment. The default value is the total time
            period for the step.
        minInc
            A Float specifying the minimum time increment allowed. The default value is the smaller
            of the suggested initial time increment or 10−5 times the total time period.
        maxInc
            A Float specifying the maximum time increment allowed. The default value is the total
            time period for the step.
        deltmx
            A Float specifying the maximum temperature change to be allowed in an increment in a
            transient analysis. The default value is 0.0.
        cetol
            A Float specifying the maximum difference in the creep strain increment calculated from
            the creep strain rates at the beginning and end of the increment. The default value is
            0.0.
        creepIntegration
            A SymbolicConstant specifying the type of integration to be used for creep and swelling
            effects throughout the step. Possible values are IMPLICIT, EXPLICIT, and NONE. The
            default value is IMPLICIT.
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
        amplitude
            A SymbolicConstant specifying the amplitude variation for loading magnitudes during the
            step. The default value is STEP. Possible values are STEP and RAMP.
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and
            PARABOLIC. The default value is LINEAR.
        maintainAttributes
            A Boolean specifying whether to retain attributes from an existing step with the same
            name. The default value is False.
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and
            CONVERT_SDI_ON. The default value is PROPAGATED.
        adaptiveDampingRatio
            A Float specifying the maximum allowable ratio of the stabilization energy to the total
            strain energy and can be used only if **stabilizationMethod** is not NONE. The default
            value is 0.05.
        continueDampingFactors
            A Boolean specifying whether this step will carry over the damping factors from the
            results of the preceding general step. This parameter must be used in conjunction with
            the **adaptiveDampingRatio** parameter. The default value is OFF.

        Returns
        -------
        CoupledThermalElectricalStructuralStep
            A :py:class:`~abaqus.Step.CoupledThermalElectricalStructuralStep.CoupledThermalElectricalStructuralStep` object.

        Raises
        ------
        RangeError
        """
        super().__init__()
        pass

    def setValues(self, description: str='', response: SymbolicConstant=TRANSIENT, timePeriod: float=1, nlgeom: Boolean=OFF, stabilizationMethod: SymbolicConstant=NONE, stabilizationMagnitude: float=None, timeIncrementationMethod: SymbolicConstant=AUTOMATIC, maxNumInc: int=100, initialInc: float=None, minInc: float=None, maxInc: float=None, deltmx: float=0, cetol: float=0, creepIntegration: SymbolicConstant=IMPLICIT, matrixStorage: SymbolicConstant=SOLVER_DEFAULT, amplitude: SymbolicConstant=STEP, extrapolation: SymbolicConstant=LINEAR, convertSDI: SymbolicConstant=PROPAGATED, adaptiveDampingRatio: float=0, continueDampingFactors: Boolean=OFF):
        """This method modifies the CoupledThermalElectricalStructuralStep object.

        Parameters
        ----------
        description
            A String specifying a description of the new step. The default value is an empty string.
        response
            A SymbolicConstant specifying the analysis type. Possible values are STEADY_STATE and
            TRANSIENT. The default value is TRANSIENT.
        timePeriod
            A Float specifying the total time period for the step. The default value is 1.0.
        nlgeom
            A Boolean specifying whether geometric nonlinearities should be accounted for during the
            step. The default value is OFF.
        stabilizationMethod
            A SymbolicConstant specifying the stabilization type. Possible values are NONE,
            DISSIPATED_ENERGY_FRACTION, and DAMPING_FACTOR. The default value is NONE.
        stabilizationMagnitude
            A Float specifying the damping intensity of the automatic damping algorithm if the
            problem is expected to be unstable and **stabilizationMethod**≠NONE. The default value is
            2×10-4.
        timeIncrementationMethod
            A SymbolicConstant specifying the time incrementation method to be used. Possible values
            are FIXED and AUTOMATIC. The default value is AUTOMATIC.
        maxNumInc
            An Int specifying the maximum number of increments in a step. The default value is 100.
        initialInc
            A Float specifying the initial time increment. The default value is the total time
            period for the step.
        minInc
            A Float specifying the minimum time increment allowed. The default value is the smaller
            of the suggested initial time increment or 10−5 times the total time period.
        maxInc
            A Float specifying the maximum time increment allowed. The default value is the total
            time period for the step.
        deltmx
            A Float specifying the maximum temperature change to be allowed in an increment in a
            transient analysis. The default value is 0.0.
        cetol
            A Float specifying the maximum difference in the creep strain increment calculated from
            the creep strain rates at the beginning and end of the increment. The default value is
            0.0.
        creepIntegration
            A SymbolicConstant specifying the type of integration to be used for creep and swelling
            effects throughout the step. Possible values are IMPLICIT, EXPLICIT, and NONE. The
            default value is IMPLICIT.
        matrixStorage
            A SymbolicConstant specifying the type of matrix storage. Possible values are SYMMETRIC,
            UNSYMMETRIC, and SOLVER_DEFAULT. The default value is SOLVER_DEFAULT.
        amplitude
            A SymbolicConstant specifying the amplitude variation for loading magnitudes during the
            step. The default value is STEP. Possible values are STEP and RAMP.
        extrapolation
            A SymbolicConstant specifying the type of extrapolation to use in determining the
            incremental solution for a nonlinear analysis. Possible values are NONE, LINEAR, and
            PARABOLIC. The default value is LINEAR.
        convertSDI
            A SymbolicConstant specifying whether to force a new iteration if severe discontinuities
            occur during an iteration. Possible values are PROPAGATED, CONVERT_SDI_OFF, and
            CONVERT_SDI_ON. The default value is PROPAGATED.
        adaptiveDampingRatio
            A Float specifying the maximum allowable ratio of the stabilization energy to the total
            strain energy and can be used only if **stabilizationMethod** is not NONE. The default
            value is 0.05.
        continueDampingFactors
            A Boolean specifying whether this step will carry over the damping factors from the
            results of the preceding general step. This parameter must be used in conjunction with
            the **adaptiveDampingRatio** parameter. The default value is OFF.

        Raises
        ------
        RangeError
        """
        pass
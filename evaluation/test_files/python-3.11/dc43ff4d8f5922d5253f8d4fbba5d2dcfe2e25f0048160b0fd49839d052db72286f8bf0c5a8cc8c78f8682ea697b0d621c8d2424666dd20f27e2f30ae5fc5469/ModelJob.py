from .Job import Job
from .MessageArray import MessageArray
from ..UtilityAndView.abaqusConstants import *
from .._decorators import abaqus_class_doc, abaqus_method_doc

@abaqus_class_doc
class ModelJob(Job):
    """The ModelJob object defines a Job object which analyzes a model on a model database
    (MDB).
    The ModelJob object is derived from the Job object.

    .. note:: 
        This object can be accessed by:

        .. code-block:: python

            import job
            mdb.adaptivityProcesses[name].job
            mdb.jobs[name]
    """
    name: str = ''
    echoPrint: Boolean = OFF
    contactPrint: Boolean = OFF
    modelPrint: Boolean = OFF
    historyPrint: Boolean = OFF
    model: str = ''
    description: str = ''
    type: SymbolicConstant = ANALYSIS
    waitHours: int = 0
    waitMinutes: int = 0
    numCpus: int = 1
    memory: int = 90
    memoryUnits: SymbolicConstant = PERCENTAGE
    getMemoryFromAnalysis: Boolean = ON
    explicitPrecision: SymbolicConstant = SINGLE
    nodalOutputPrecision: SymbolicConstant = SINGLE
    parallelizationMethodExplicit: SymbolicConstant = DOMAIN
    numDomains: int = 1
    activateLoadBalancing: Boolean = OFF
    multiprocessingMode: SymbolicConstant = DEFAULT
    analysis: SymbolicConstant = None
    status: SymbolicConstant = None
    queue: str = ''
    atTime: str = ''
    scratch: str = ''
    userSubroutine: str = ''
    messages: MessageArray = []
    environment: tuple = ()

    @abaqus_method_doc
    def __init__(self, name: str, model: str, description: str='', type: SymbolicConstant=ANALYSIS, queue: str='', waitHours: int=0, waitMinutes: int=0, atTime: str='', echoPrint: Boolean=OFF, contactPrint: Boolean=OFF, modelPrint: Boolean=OFF, historyPrint: Boolean=OFF, scratch: str='', userSubroutine: str='', numCpus: int=1, memory: int=90, memoryUnits: SymbolicConstant=PERCENTAGE, explicitPrecision: SymbolicConstant=SINGLE, nodalOutputPrecision: SymbolicConstant=SINGLE, parallelizationMethodExplicit: SymbolicConstant=DOMAIN, numDomains: int=1, activateLoadBalancing: Boolean=OFF, multiprocessingMode: SymbolicConstant=DEFAULT, *args, **kwargs):
        """This method creates an analysis job using a model on a model database (MDB) for the
        model definition.

        .. note:: 
            This function can be accessed by:

            .. code-block:: python

                mdb.Job

        Parameters
        ----------
        name
            A String specifying the name of the new job. The name must be a valid Abaqus/CAE object
            name.
        model
            A String specifying the name of the model to be analyzed or a Model object specifying
            the model to be analyzed.
        description
            A String specifying a description of the job.
        type
            A SymbolicConstant specifying the type of job. Possible values are ANALYSIS,
            SYNTAXCHECK, RECOVER, and RESTART. The default value is ANALYSIS.If the object has the
            type JobFromInputFile, **type** = RESTART is not available.
        queue
            A String specifying the name of the queue to which to submit the job. The default value
            is an empty string.Note:You can use the **queue** argument when creating a Job object on a
            Windows workstation; however, remote queues are available only on Linux platforms.
        waitHours
            An Int specifying the number of hours to wait before submitting the job. This argument
            is ignored if **queue** is set. The default value is 0.This argument works in conjunction
            with **waitMinutes**. **waitHours** and **atTime** are mutually exclusive.
        waitMinutes
            An Int specifying the number of minutes to wait before submitting the job. This argument
            is ignored if **queue** is set. The default value is 0.This argument works in conjunction
            with **waitHours**. **waitMinutes** and **atTime** are mutually exclusive.
        atTime
            A String specifying the time at which to submit the job. If **queue** is empty, the string
            syntax must be valid for the Linux `at` command. If **queue** is set, the syntax must be
            valid according to the system administrator. The default value is an empty
            string.Note:You can use the **atTime** argument when creating a Job object on a Windows
            workstation; however, the `at` command is available only on Linux platforms.
        echoPrint
            A Boolean specifying whether an echo of the input data is printed. The default value is
            OFF.
        contactPrint
            A Boolean specifying whether contact constraint data are printed. The default value is
            OFF.
        modelPrint
            A Boolean specifying whether model definition data are printed. The default value is
            OFF.
        historyPrint
            A Boolean specifying whether history data are printed. The default value is OFF.
        scratch
            A String specifying the location of the scratch directory. The default value is an empty
            string.
        userSubroutine
            A String specifying the file containing the user's subroutine definitions. The default
            value is an empty string.
        numCpus
            An Int specifying the number of CPUs to use for this analysis if parallel processing is
            available. Possible values are **numCpus** >> 0. The default value is 1.
        memory
            An Int specifying the amount of memory available to Abaqus analysis. The value should be
            expressed in the units supplied in **memoryUnits**. The default value is 90.
        memoryUnits
            A SymbolicConstant specifying the units for the amount of memory used in an Abaqus
            analysis. Possible values are PERCENTAGE, MEGA_BYTES, and GIGA_BYTES. The default value
            is PERCENTAGE.
        explicitPrecision
            A SymbolicConstant specifying whether to use the double precision version of
            Abaqus/Explicit. Possible values are SINGLE, FORCE_SINGLE, DOUBLE,
            DOUBLE_CONSTRAINT_ONLY, and DOUBLE_PLUS_PACK. The default value is SINGLE.
        nodalOutputPrecision
            A SymbolicConstant specifying the precision of the nodal output written to the output
            database. Possible values are SINGLE and FULL. The default value is SINGLE.
        parallelizationMethodExplicit
            A SymbolicConstant specifying the parallelization method for Abaqus/Explicit.
            Possible values are LOOP and DOMAIN. The default value is DOMAIN.

            .. versionchanged:: 2017
                The default value for parallelizationMethodExplicit is now `DOMAIN`
        numDomains
            An Int specifying the number of domains for parallel execution in Abaqus/Explicit. When
            **parallelizationMethodExplicit** = DOMAIN, **numDomains** must be a multiple of **numCpus**.
            The default value is 1.
        activateLoadBalancing
            A Boolean specifying whether to activate dyanmic load balancing for jobs running on
            multiple processors with multiple domains in Abaqus/Explicit. The default value is OFF.
        multiprocessingMode
            A SymbolicConstant specifying whether an analysis is decomposed into threads or into
            multiple processes that communicate through a message passing interface (MPI). Possible
            values are DEFAULT, THREADS, and MPI. The default value is DEFAULT.

        Returns
        -------
        ModelJob
            A :py:class:`~abaqus.Job.ModelJob.ModelJob` object.
        """
        ...

    @abaqus_method_doc
    def writeInput(self, consistencyChecking: Boolean=ON):
        """This method writes an input file.

        Parameters
        ----------
        consistencyChecking
            A Boolean specifying whether to perform consistency checking for the job. The default
            value is ON.It is not recommended to turn the consistency checking off unless you are
            absolutely sure the model is consistent.
        """
        ...

    @abaqus_method_doc
    def setValues(self, *args, **kwargs):
        """This method modifies the ModelJob object."""
        ...
import typing
from .AdaptiveMeshConstraint import AdaptiveMeshConstraint
from ..Region.Region import Region
from ..UtilityAndView.abaqusConstants import *
from .._decorators import abaqus_class_doc, abaqus_method_doc

@abaqus_class_doc
class DisplacementAdaptiveMeshConstraint(AdaptiveMeshConstraint):
    """The AdaptivityProcess object defines a series of jobs that will be submitted for
    analysis. Abaqus performs adaptive remeshing between each job.

    .. note:: 
        This object can be accessed by:

        .. code-block:: python

            import step
            mdb.models[name].adaptiveMeshConstraints[name]
    """
    name: str = ''
    category: SymbolicConstant = None
    region: Region = Region()
    localCsys: str = None

    @abaqus_method_doc
    def __init__(self, name: str, createStepName: str, region: Region, u1: typing.Union[SymbolicConstant, float]=UNSET, u2: typing.Union[SymbolicConstant, float]=UNSET, u3: typing.Union[SymbolicConstant, float]=UNSET, ur1: typing.Union[SymbolicConstant, float]=UNSET, ur2: typing.Union[SymbolicConstant, float]=UNSET, ur3: typing.Union[SymbolicConstant, float]=UNSET, amplitude: str=UNSET, motionType: SymbolicConstant=INDEPENDENT, localCsys: str=None):
        """This method creates a DisplacementAdaptiveMeshConstraint object.

        .. note:: 
            This function can be accessed by:

            .. code-block:: python

                mdb.models[name].DisplacementAdaptiveMeshConstraint

        Parameters
        ----------
        name
            A String specifying the adaptive mesh constraint repository key.
        createStepName
            A String specifying the name of the step in which the adaptive mesh constraint is
            created.
        region
            A :py:class:`~abaqus.Region.Region.Region` object specifying the region to which the adaptive mesh constraint is applied.
        u1
            A Float or a SymbolicConstant specifying the displacement component in the 1-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is
            UNSET.Note:Although **u1**, **u2**, **u3**, **ur1**, **ur2**, and **ur3** are optional arguments, at
            least one of them must be specified.
        u2
            A Float or a SymbolicConstant specifying the displacement component in the 2-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is UNSET.
        u3
            A Float or a SymbolicConstant specifying the displacement component in the 3-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is UNSET.
        ur1
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            1-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        ur2
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            2-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        ur3
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            3-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference.
            UNSET should be used if the adaptive mesh constraint has no amplitude reference. The
            default value is UNSET. You should provide the **amplitude** argument only if it is valid
            for the specified step.
        motionType
            A SymbolicConstant specifying the mesh motion in relation to the underlying material.
            Possible values are INDEPENDENT, FOLLOW and USER_DEFINED. The default value is
            INDEPENDENT.
        localCsys
            None or a DatumCsys object specifying the local coordinate system of the adaptive mesh
            constraint's degrees of freedom. If **localCsys** = None, the degrees of freedom are defined
            in the global coordinate system. The default value is None.

        Returns
        -------
        DisplacementAdaptiveMeshConstraint
            A :py:class:`~abaqus.Adaptivity.DisplacementAdaptiveMeshConstraint.DisplacementAdaptiveMeshConstraint` object.
        """
        super().__init__(name, region=region, category=MECHANICAL, localCsys=localCsys)

    @abaqus_method_doc
    def setValues(self, u1: typing.Union[SymbolicConstant, float]=UNSET, u2: typing.Union[SymbolicConstant, float]=UNSET, u3: typing.Union[SymbolicConstant, float]=UNSET, ur1: typing.Union[SymbolicConstant, float]=UNSET, ur2: typing.Union[SymbolicConstant, float]=UNSET, ur3: typing.Union[SymbolicConstant, float]=UNSET, amplitude: str=UNSET, motionType: SymbolicConstant=INDEPENDENT, localCsys: str=None):
        """This method modifies the data for an existing DisplacementAdaptiveMeshConstraint object
        in the step where it is created.

        Parameters
        ----------
        u1
            A Float or a SymbolicConstant specifying the displacement component in the 1-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is
            UNSET.Note:Although **u1**, **u2**, **u3**, **ur1**, **ur2**, and **ur3** are optional arguments, at
            least one of them must be specified.
        u2
            A Float or a SymbolicConstant specifying the displacement component in the 2-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is UNSET.
        u3
            A Float or a SymbolicConstant specifying the displacement component in the 3-direction.
            Possible values for the SymbolicConstant are UNSET and SET. The default value is UNSET.
        ur1
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            1-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        ur2
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            2-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        ur3
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            3-direction. Possible values for the SymbolicConstant are UNSET and SET. The default
            value is UNSET.
        amplitude
            A String or the SymbolicConstant UNSET specifying the name of the amplitude reference.
            UNSET should be used if the adaptive mesh constraint has no amplitude reference. The
            default value is UNSET. You should provide the **amplitude** argument only if it is valid
            for the specified step.
        motionType
            A SymbolicConstant specifying the mesh motion in relation to the underlying material.
            Possible values are INDEPENDENT, FOLLOW and USER_DEFINED. The default value is
            INDEPENDENT.
        localCsys
            None or a DatumCsys object specifying the local coordinate system of the adaptive mesh
            constraint's degrees of freedom. If **localCsys** = None, the degrees of freedom are defined
            in the global coordinate system. The default value is None.
        """
        ...

    @abaqus_method_doc
    def setValuesInStep(self, stepName: str, u1: typing.Union[SymbolicConstant, float]=None, u2: typing.Union[SymbolicConstant, float]=None, u3: typing.Union[SymbolicConstant, float]=None, ur1: typing.Union[SymbolicConstant, float]=None, ur2: typing.Union[SymbolicConstant, float]=None, ur3: typing.Union[SymbolicConstant, float]=None, amplitude: str=''):
        """This method modifies the propagating data for an existing
        DisplacementAdaptiveMeshConstraint object in the specified step.

        Parameters
        ----------
        stepName
            A String specifying the name of the step in which the adaptive mesh constraint is
            modified.
        u1
            A Float or a SymbolicConstant specifying the displacement component in the 1-direction.
            Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        u2
            A Float or a SymbolicConstant specifying the displacement component in the 2-direction.
            Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        u3
            A Float or a SymbolicConstant specifying the displacement component in the 3-direction.
            Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        ur1
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            1-direction. Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        ur2
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            2-direction. Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        ur3
            A Float or a SymbolicConstant specifying the rotational displacement component about the
            3-direction. Possible values for the SymbolicConstant are SET, UNCHANGED, and FREED.
        amplitude
            A String or a SymbolicConstant specifying the name of the amplitude reference. Possible
            values for the SymbolicConstant are UNCHANGED and FREED. UNCHANGED should be used if the
            amplitude is propagated from the previous analysis step. FREED should be used if the
            adaptive mesh constraint is changed to have no amplitude reference. You should provide
            the **amplitude** argument only if it is valid for the specified step.
        """
        ...
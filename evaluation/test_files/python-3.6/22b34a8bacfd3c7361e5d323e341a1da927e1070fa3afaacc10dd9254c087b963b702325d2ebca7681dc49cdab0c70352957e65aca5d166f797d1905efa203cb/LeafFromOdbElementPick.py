from abaqusConstants import *
from .Leaf import Leaf

class LeafFromOdbElementPick(Leaf):
    """The LeafFromOdbElementPick object can be used whenever a Leaf object is expected as an
    argument. Leaf objects are used to specify the items in a display group. Leaf objects
    are constructed as temporary objects, which are then used as arguments to DisplayGroup
    commands.
    The LeafFromOdbElementPick object is derived from the Leaf object.

    .. note:: 
        This object can be accessed by:

        .. code-block:: python

            import displayGroupOdbToolset
    """
    leafType: SymbolicConstant = None

    def __init__(self, elementPick: tuple):
        """This method creates a Leaf object from a tuple containing machine readable, compact
        strings defining the elements picked for each part instance. Leaf objects specify the
        items in a display group.

        .. note:: 
            This function can be accessed by:

            .. code-block:: python

                LeafFromOdbElementPick

        Parameters
        ----------
        elementPick
            A sequence of tuples of the form [part name, entity count, machine readable pick
            strings].

        Returns
        -------
        LeafFromOdbElementPick
            A :py:class:`~abaqus.DisplayGroup.LeafFromOdbElementPick.LeafFromOdbElementPick` object.
        """
        super().__init__(DEFAULT_MODEL)
        pass
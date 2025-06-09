from .ConstrainedSketchGeometry import ConstrainedSketchGeometry

class ArcByStartEndTangent(ConstrainedSketchGeometry):

    def __init__(self, point1: tuple[float], point2: tuple[float], vector: tuple):
        """This method constructs an arc using two vertices. The Arc object is added to the
        geometry repository of the ConstrainedSketch object.

        .. note:: 
            This function can be accessed by:

            .. code-block:: python

                mdb.models[name].sketches[name].ArcByStartEndTangent

        Parameters
        ----------
        point1
            A pair of Floats specifying the first endpoint of the arc.
        point2
            A pair of Floats specifying the second endpoint of the arc.
        vector
            A sequence of two Floats specifying the start direction for constructing the arc.

        Returns
        -------
        ConstrainedSketchGeometry
            A :py:class:`~abaqus.Sketcher.ConstrainedSketchGeometry.ConstrainedSketchGeometry.ConstrainedSketchGeometry` object (None if the arc cannot be created).

        """
        pass
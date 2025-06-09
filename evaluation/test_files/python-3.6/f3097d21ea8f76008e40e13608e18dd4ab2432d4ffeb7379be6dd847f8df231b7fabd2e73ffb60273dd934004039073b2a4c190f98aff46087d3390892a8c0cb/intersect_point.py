import numpy as np
import shapely.geometry as geom

def intersect_point(Points1, Points2):
    """determine the intersectoint points between 2 lines
	* Compulsory inputs: 
		dataPoints1, dataPoints2: Nx2 arrays, contains data points of lines 
	"""
    Points1 = np.asarray(Points1)
    Points2 = np.asarray(Points2)
    line1 = geom.LineString(Points1)
    line2 = geom.LineString(Points2)
    intersectPoint = line1.intersection(line2)
    if intersectPoint.is_empty:
        raise Exception('2 lines are not intersected')
    elif isinstance(intersectPoint, geom.Point):
        Points = np.array(intersectPoint)
    else:
        list_arrays = [np.array((geom.xy[0][0], geom.xy[1][0])) for geom in intersectPoint]
        Points = np.array(list_arrays)
    return Points
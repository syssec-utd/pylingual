"""Identify interfaces for CRA extended assembly data structures."""
from math import fabs
from numpy import array
from numpy import float64
from scipy.linalg import solve
from scipy.spatial import cKDTree
from shapely.geometry import Polygon
from compas.geometry import Frame
from compas.geometry import local_to_world_coordinates_numpy

def find_nearest_neighbours(cloud, nmax):
    tree = cKDTree(cloud)
    nnbrs = [tree.query(root, nmax) for root in cloud]
    nnbrs = [(d.flatten().tolist(), n.flatten().tolist()) for d, n in nnbrs]
    return nnbrs

def assembly_interfaces_numpy(assembly, nmax=10, tmax=1e-06, amin=0.1):
    """
    Identify the interfaces between the blocks of an assembly.

    Parameters
    ----------
    assembly : :class:`~compas_assembly.datastructures.Assembly`
        An assembly of discrete blocks.
    nmax : int, optional
        Maximum number of neighbours per block.
    tmax : float, optional
        Maximum deviation from the perfectly flat interface plane.
    amin : float, optional
        Minimum area of a "face-face" interface.

    References
    ----------

    """
    node_index = {node: index for index, node in enumerate(assembly.nodes())}
    index_node = {index: node for index, node in enumerate(assembly.nodes())}
    blocks = list(assembly.blocks())
    nmax = min(nmax, len(blocks))
    block_cloud = [block.centroid() for block in blocks]
    block_nnbrs = find_nearest_neighbours(block_cloud, nmax)
    for node in assembly.nodes():
        i = node_index[node]
        block = blocks[i]
        nbrs = block_nnbrs[i][1]
        frames = block.frames()
        for f0, frame in frames.items():
            origin = frame.point
            uvw = [frame.xaxis, frame.yaxis, frame.zaxis]
            A = array(uvw, dtype=float64)
            o = array(origin, dtype=float64).reshape((-1, 1))
            xyz0 = array(block.face_coordinates(f0), dtype=float64).reshape((-1, 3)).T
            rst0 = solve(A.T, xyz0 - o).T.tolist()
            p0 = Polygon(rst0)
            for j in nbrs:
                n = index_node[j]
                if n == node:
                    continue
                if n in assembly.graph.edge and node in assembly.graph.edge[n]:
                    continue
                if assembly.graph.node_attribute(node, 'is_support') and assembly.graph.node_attribute(n, 'is_support'):
                    continue
                nbr = blocks[j]
                k_i = {key: index for index, key in enumerate(nbr.vertices())}
                xyz = array(nbr.vertices_attributes('xyz'), dtype=float64).reshape((-1, 3)).T
                rst = solve(A.T, xyz - o).T.tolist()
                rst = {key: rst[k_i[key]] for key in nbr.vertices()}
                faces = nbr.faces()
                for f1 in faces:
                    rst1 = [rst[key] for key in nbr.face_vertices(f1)]
                    if any((fabs(t) > tmax for r, s, t in rst1)):
                        continue
                    p1 = Polygon(rst1)
                    if p1.area < amin:
                        continue
                    if p0.intersects(p1):
                        intersection = p0.intersection(p1)
                        area = intersection.area
                        if area >= amin:
                            coords = [[x, y, 0.0] for x, y, z in intersection.exterior.coords]
                            coords = local_to_world_coordinates_numpy(Frame(o, A[0], A[1]), coords)
                            assembly.add_to_interfaces(node, n, type='face_face', size=area, points=coords.tolist()[:-1], frame=Frame(origin, uvw[0], uvw[1]))
    return assembly
if __name__ == '__main__':
    pass
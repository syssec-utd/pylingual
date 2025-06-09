"""The ``templates`` module allows for fast creation of a few select sample types and diffraction geometries without having to
worry about any of the "under the hood" scripting.

"""
import numpy as np
import pygalmesh
from scipy.spatial.transform import Rotation
from xrd_simulator.detector import Detector
from xrd_simulator.beam import Beam
from xrd_simulator.motion import RigidBodyMotion
from xrd_simulator.polycrystal import Polycrystal
from xrd_simulator.mesh import TetraMesh
from xrd_simulator.phase import Phase
from xrd_simulator import utils
PARAMETER_KEYS = ['detector_distance', 'number_of_detector_pixels_z', 'number_of_detector_pixels_y', 'detector_center_pixel_z', 'detector_center_pixel_y', 'pixel_side_length_z', 'pixel_side_length_y', 'wavelength', 'beam_side_length_z', 'beam_side_length_y', 'rotation_step', 'rotation_axis']

def s3dxrd(parameters):
    """Construct a scaning-three-dimensional-xray diffraction experiment.

    This is a helper/utility function for quickly creating an experiment. For full controll
    over the diffraction geometry consider custom creation of the primitive quantities:
    (:obj:`xrd_simulator.beam.Beam`), and (:obj:`xrd_simulator.detector.Detector`) seperately.

    Args:
        parameters (:obj:`dict`): Dictionary with fields as 

            ``"detector_distance"``           : (:obj:`float`) Distance form sample origin to
                detector centre in units of microns. 

            ``"number_of_detector_pixels_z"`` : (:obj:`int`) Number of detector pixels
                along z-axis. 

            ``"number_of_detector_pixels_y"`` : (:obj:`int`) Number of detector pixels
                along y-axis. 

            ``"detector_center_pixel_z"``     : (:obj:`float`) Intersection pixel coordinate between
                 beam centroid line and detector along z-axis. 

            ``"detector_center_pixel_y"``     : (:obj:`float`) Intersection pixel coordinate between
                 beam centroid line and detector along y-axis. 

            ``"pixel_side_length_z"``         : (:obj:`float`) Detector pixel side length in units
                of microns along z-axis. 

            ``"pixel_side_length_y"``         : (:obj:`float`) Detector pixel side length in units
                of microns along y-axis. 

            ``"wavelength"``                  : (:obj:`float`) Wavelength in units of Angstrom. 

            ``"beam_side_length_z"``          : (:obj:`float`) Beam side length in units
                of microns. 

            ``"beam_side_length_y"``          : (:obj:`float`) Beam side length in units
                of microns. 

            ``"rotation_step"``               : (:obj:`float`) Angular frame integration step in
                units of radians. 

            ``"rotation_axis"``               : (:obj:`numpy array`)  Axis around which to
                positively rotate the sample by ``rotation_step`` radians. 


    Returns:
        (:obj:`xrd_simulator`) objects defining an experiment: (:obj:`xrd_simulator.beam.Beam`),
        (:obj:`xrd_simulator.detector.Detector`), (:obj:`xrd_simulator.motion.RigidBodyMotion`).

    Examples:
        .. literalinclude:: examples/example_s3dxrd.py

    """
    for key in PARAMETER_KEYS:
        if key not in list(parameters):
            raise ValueError('No keyword ' + key + ' found in the input parameters dictionary')
    detector = _get_detector_from_params(parameters)
    beam = _get_beam_from_params(parameters)
    motion = _get_motion_from_params(parameters)
    return (beam, detector, motion)

def polycrystal_from_odf(orientation_density_function, number_of_crystals, sample_bounding_cylinder_height, sample_bounding_cylinder_radius, unit_cell, sgname, path_to_cif_file=None, maximum_sampling_bin_seperation=np.radians(5.0), strain_tensor=lambda x: np.zeros((3, 3))):
    """Fill a cylinder with crystals from a given orientation density function.

    The ``orientation_density_function`` is sampled by discretizing orientation space over the unit
    quarternions. Each bin is assigned its apropiate probability, assuming the
    ``orientation_density_function`` is approximately constant over a single bin. Each sampled
    orientation is constructed by first drawing a random bin and next drawing uniformly from
    within that bin, again assuming that ``orientation_density_function`` is approximately constant
    over a bin.

    Args:
        orientation_density_function (:obj:`callable`): orientation_density_function(x, q) ->
            :obj:`float` where input variable ``x`` is a :obj:`numpy array` of shape ``(3,)``
            representing a spatial coordinate in the cylinder (x,y,z) and ``q`` is a
            :obj:`numpy array` of shape ``(4,)`` representing a orientation in so3 by a unit
            quarternion. The format of the quarternion is "scalar last"
            (same as in scipy.spatial.transform.Rotation).
        number_of_crystals (:obj:`int`): Approximate number of crystal elements to compose the
            cylinder volume.
        sample_bounding_cylinder_height (:obj:`float`): Height of sample cylinder in units of
             microns.
        sample_bounding_cylinder_radius (:obj:`float`): Radius of sample cylinder in units of
            microns.
        unit_cell (:obj:`list` of :obj:`float`): Crystal unit cell representation of the form
            [a,b,c,alpha,beta,gamma], where alpha,beta and gamma are in units of degrees while
            a,b and c are in units of anstrom.
        sgname (:obj:`string`): Name of space group , e.g 'P3221' for quartz, SiO2, for instance
        path_to_cif_file (:obj:`string`): Path to CIF file. Defaults to None, in which case no structure
            factors are computed.
        maximum_sampling_bin_seperation (:obj:`float`): Discretization steplength of orientation
            space using spherical coordinates over the unit quarternions in units of radians.
            A smaller steplength gives more accurate sampling of the input
            ``orientation_density_function`` but is computationally slower.
        strain_tensor (:obj:`callable`): Strain tensor field over sample cylinder.
            strain_tensor(x) -> :obj:`numpy array` of shape ``(3,3)`` where input variable ``x`` is
            a :obj:`numpy array` of shape ``(3,)`` representing a spatial coordinate in the
            cylinder (x,y,z).

    Returns:
        (:obj:`xrd_simulator.polycrystal.Polycrystal`)

    Examples:
        .. literalinclude:: examples/example_polycrystal_from_odf.py

    More complicated ODFs are also possible to use. Why not use a von-Mises-Fisher distribution for instance:

    Examples:
        .. literalinclude:: examples/example_polycrystal_from_von_mises_fisher_odf.py

    """
    volume_per_crystal = np.pi * sample_bounding_cylinder_radius ** 2 * sample_bounding_cylinder_height / number_of_crystals
    max_cell_circumradius = (3 * volume_per_crystal / (np.pi * 4.0)) ** (1 / 3.0)
    max_cell_circumradius = 2.65 * max_cell_circumradius
    dz = sample_bounding_cylinder_height / 2.0
    R = float(sample_bounding_cylinder_radius)
    cylinder = pygalmesh.generate_mesh(pygalmesh.Cylinder(-dz, dz, R, max_cell_circumradius), max_cell_circumradius=max_cell_circumradius, max_edge_size_at_feature_edges=max_cell_circumradius, verbose=False)
    mesh = TetraMesh._build_tetramesh(cylinder)
    phases = [Phase(unit_cell, sgname, path_to_cif_file)]
    element_phase_map = np.zeros((mesh.number_of_elements,)).astype(int)
    orientation = _sample_ODF(orientation_density_function, maximum_sampling_bin_seperation, mesh.ecentroids)
    strain_lab = np.zeros((mesh.number_of_elements, 3, 3))
    for ei in range(mesh.number_of_elements):
        strain_lab[ei] = strain_tensor(mesh.ecentroids[ei])
    return Polycrystal(mesh, orientation, strain=strain_lab, phases=phases, element_phase_map=element_phase_map)

def get_uniform_powder_sample(sample_bounding_radius, number_of_grains, unit_cell, sgname, strain_tensor=np.zeros((3, 3)), path_to_cif_file=None):
    """Generate a polycyrystal with grains overlayed at the origin and orientations drawn uniformly.

    Args:
        sample_bounding_radius (:obj:`float`): Bounding radius of sample. All tetrahedral crystal
            elements will be overlayed within a sphere of ``sample_bounding_radius`` radius.
        number_of_grains (:obj:`int`): Number of grains composing the polycrystal sample.
        unit_cell (:obj:`list` of :obj:`float`): Crystal unit cell representation of the form
            [a,b,c,alpha,beta,gamma], where alpha,beta and gamma are in units of degrees while
            a,b and c are in units of anstrom.
        sgname (:obj:`string`):  Name of space group , e.g 'P3221' for quartz, SiO2, for instance
        strain_tensor (:obj:`numpy array`): Strain tensor to apply to all tetrahedral crystal
            elements contained within the sample. ``shape=(3,3)``.
        path_to_cif_file (:obj:`string`): Path to CIF file. Defaults to None, in which case no structure
            factors are computed.

    Returns:
        (:obj:`xrd_simulator.polycrystal`) A polycyrystal sample with ``number_of_grains`` grains.

    Examples:
        .. literalinclude:: examples/example_get_uniform_powder_sample.py

    """
    coord, enod, node_number = ([], [], 0)
    r = sample_bounding_radius
    for _ in range(number_of_grains):
        coord.append([r / np.sqrt(3.0), r / np.sqrt(3.0), -r / np.sqrt(3.0)])
        coord.append([r / np.sqrt(3.0), -r / np.sqrt(3.0), -r / np.sqrt(3.0)])
        coord.append([-r / np.sqrt(2.0), 0, -r / np.sqrt(2.0)])
        coord.append([0, 0, r])
        enod.append(list(range(node_number, node_number + 4)))
        node_number += 3
    coord, enod = (np.array(coord), np.array(enod))
    mesh = TetraMesh.generate_mesh_from_vertices(coord, enod)
    orientation = Rotation.random(mesh.number_of_elements).as_matrix()
    element_phase_map = np.zeros((mesh.number_of_elements,)).astype(int)
    phases = [Phase(unit_cell, sgname, path_to_cif_file)]
    return Polycrystal(mesh, orientation, strain=strain_tensor, phases=phases, element_phase_map=element_phase_map)

def _get_motion_from_params(parameters):
    """Produce a ``xrd_simulator.motion.RigidBodyMotion`` from the s3dxrd params dictionary.
    """
    translation = np.array([0.0, 0.0, 0.0])
    return RigidBodyMotion(parameters['rotation_axis'], parameters['rotation_step'], translation)

def _get_beam_from_params(parameters):
    """Produce a ``xrd_simulator.beam.Beam`` from the s3dxrd params dictionary.
    """
    dz = parameters['beam_side_length_z'] / 2.0
    dy = parameters['beam_side_length_y'] / 2.0
    beam_vertices = np.array([[-parameters['detector_distance'], -dy, -dz], [-parameters['detector_distance'], dy, -dz], [-parameters['detector_distance'], -dy, dz], [-parameters['detector_distance'], dy, dz], [parameters['detector_distance'], -dy, -dz], [parameters['detector_distance'], dy, -dz], [parameters['detector_distance'], -dy, dz], [parameters['detector_distance'], dy, dz]])
    beam_direction = np.array([1.0, 0.0, 0.0])
    polarization_vector = np.array([0.0, 1.0, 0.0])
    return Beam(beam_vertices, beam_direction, parameters['wavelength'], polarization_vector)

def _get_detector_from_params(parameters):
    """Produce a ``xrd_simulator.detector.Detector`` from the s3dxrd params dictionary.
    """
    p_z, p_y = (parameters['pixel_side_length_z'], parameters['pixel_side_length_y'])
    det_dist = parameters['detector_distance']
    det_pix_y = parameters['number_of_detector_pixels_y']
    det_pix_z = parameters['number_of_detector_pixels_z']
    det_cz, det_cy = (parameters['detector_center_pixel_z'], parameters['detector_center_pixel_y'])
    d_0 = np.array([det_dist, -det_cy * p_y, -det_cz * p_z])
    d_1 = np.array([det_dist, (det_pix_y - det_cy) * p_y, -det_cz * p_z])
    d_2 = np.array([det_dist, -det_cy * p_y, (det_pix_z - det_cz) * p_z])
    return Detector(p_z, p_y, d_0, d_1, d_2)

def _sample_ODF(ODF, maximum_sampling_bin_seperation, coordinates):
    """Draw orientation matrices form an ODF at spatial locations ``coordinates``.
    """
    dalpha = maximum_sampling_bin_seperation / 2.0
    dalpha = np.pi / 2.0 / int(np.pi / (dalpha * 2.0))
    alpha_1 = np.arange(0 + dalpha / 2.0 + 1e-08, np.pi / 2.0 - dalpha / 2.0 - 1e-08 + dalpha, dalpha)
    alpha_2 = np.arange(0 + dalpha / 2.0 + 1e-08, np.pi - dalpha / 2.0 - 1e-08 + dalpha, dalpha)
    alpha_3 = np.arange(0 + dalpha / 2.0 + 1e-08, 2 * np.pi - dalpha / 2.0 - 1e-08 + dalpha, dalpha)
    A1, A2, A3 = np.meshgrid(alpha_1, alpha_2, alpha_3, indexing='ij')
    A1, A2, A3 = (A1.flatten(), A2.flatten(), A3.flatten())
    q = utils.alpha_to_quarternion(A1, A2, A3)
    da = dalpha / 2.0
    a = 1 / 2.0 * (A1 + da - np.sin(A1 + da) * np.cos(A1 + da)) - 1 / 2.0 * (A1 - da - np.sin(A1 - da) * np.cos(A1 - da))
    b = -np.cos(A2 + da) + np.cos(A2 - da)
    c = A3 + da - (A3 - da)
    volume_element = a * b * c
    assert np.abs(np.sum(volume_element) - np.pi ** 2) < 1e-05
    rotations = []
    for x in coordinates:
        probability = volume_element * ODF(x, q)
        assert np.abs(np.sum(probability) - 1.0) < 0.05, 'Orientation density function must be be normalised.'
        probability = probability / np.sum(probability)
        indices = np.linspace(0, len(probability) - 1, len(probability)).astype(int)
        draw = np.random.choice(indices, size=1, replace=True, p=probability)
        a1 = A1[draw] + dalpha * (np.random.rand() - 0.5)
        a2 = A2[draw] + dalpha * (np.random.rand() - 0.5)
        a3 = A3[draw] + dalpha * (np.random.rand() - 0.5)
        q_pertubated = utils.alpha_to_quarternion(a1, a2, a3)
        rotations.append(Rotation.from_quat(q_pertubated).as_matrix().reshape(3, 3))
    return np.array(rotations)
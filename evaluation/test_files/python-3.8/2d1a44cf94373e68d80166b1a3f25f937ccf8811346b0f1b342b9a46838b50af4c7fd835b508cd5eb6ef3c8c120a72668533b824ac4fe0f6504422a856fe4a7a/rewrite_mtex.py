"""
Created on Mon Mar 21 23:21:19 2022

@author: PURUSHOT
"""
import numpy as np
import _pickle as cPickle
import time, datetime
import sys
sys.path.append('C:\\Users\\purushot\\Desktop\\github_version_simple\\lauetoolsnn')
from tqdm import trange
ct = time.time()
now = datetime.datetime.fromtimestamp(ct)
c_time = now.strftime('%Y-%m-%d_%H-%M-%S')
save_directory_ = 'E:\\vijaya_lauedata\\ZnCuOCl_ravi\\results_ZnCuOCl_2022-03-25_00-22-24'
with open(save_directory_ + '\\results.pickle', 'rb') as input_file:
    (best_match, mat_global, rotation_matrix1, strain_matrix, strain_matrixs, col, colx, coly, match_rate, files_treated, lim_x, lim_y, spots_len, iR_pix, fR_pix, material_, material1_, lattice_, lattice1_, symmetry0, symmetry1, crystal, crystal1) = cPickle.load(input_file)
material0_lauegroup = '7'
material1_lauegroup = '7'
rotation_matrix = [[] for i in range(len(rotation_matrix1))]
for i in range(len(rotation_matrix1)):
    rotation_matrix[i].append(np.zeros((lim_x * lim_y, 3, 3)))
for i in trange(len(rotation_matrix1)):
    temp_mat = rotation_matrix1[i][0]
    for j in range(len(temp_mat)):
        orientation_matrix = temp_mat[j, :, :]
        omega = np.deg2rad(-40)
        cw = np.cos(omega)
        sw = np.sin(omega)
        mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]])
        orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
        omega = np.deg2rad(1.5)
        cw = np.cos(omega)
        sw = np.sin(omega)
        mat_from_lab_to_sample_frame = np.array([[1.0, 0.0, 0.0], [0.0, cw, -sw], [0.0, sw, cw]])
        orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
        if np.linalg.det(orientation_matrix) < 0:
            orientation_matrix = -orientation_matrix
        rotation_matrix[i][0][j, :, :] = orientation_matrix

def OrientationMatrix2Euler(g):
    """
    Compute the Euler angles from the orientation matrix.
    This conversion follows the paper of Rowenhorst et al. :cite:`Rowenhorst2015`.
    In particular when :math:`g_{33} = 1` within the machine precision,
    there is no way to determine the values of :math:`\\phi_1` and :math:`\\phi_2`
    (only their sum is defined). The convention is to attribute
    the entire angle to :math:`\\phi_1` and set :math:`\\phi_2` to zero.
    :param g: The 3x3 orientation matrix
    :return: The 3 euler angles in degrees.
    """
    eps = np.finfo('float').eps
    (phi1, Phi, phi2) = (0.0, 0.0, 0.0)
    if np.abs(g[2, 2]) >= 1 - eps:
        if g[2, 2] > 0.0:
            phi1 = np.arctan2(g[0][1], g[0][0])
        else:
            phi1 = -np.arctan2(-g[0][1], g[0][0])
            Phi = np.pi
    else:
        Phi = np.arccos(g[2][2])
        zeta = 1.0 / np.sqrt(1.0 - g[2][2] ** 2)
        phi1 = np.arctan2(g[2][0] * zeta, -g[2][1] * zeta)
        phi2 = np.arctan2(g[0][2] * zeta, g[1][2] * zeta)
    if phi1 < 0.0:
        phi1 += 2 * np.pi
    if Phi < 0.0:
        Phi += 2 * np.pi
    if phi2 < 0.0:
        phi2 += 2 * np.pi
    return np.degrees([phi2, Phi, phi1])
if material_ == material1_:
    lattice = lattice_
    material0_LG = material0_lauegroup
    header = ['Channel Text File', 'Prj     lauetoolsnn', 'Author    [Ravi raj purohit]', 'JobMode    Grid', 'XCells    ' + str(lim_x), 'YCells    ' + str(lim_y), 'XStep    1.0', 'YStep    1.0', 'AcqE1    0', 'AcqE2    0', 'AcqE3    0', 'Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0', 'Phases    1', str(round(lattice._lengths[0] * 10, 5)) + ';' + str(round(lattice._lengths[1] * 10, 5)) + ';' + str(round(lattice._lengths[2] * 10, 5)) + '\t' + str(round(lattice._angles[0], 5)) + ';' + str(round(lattice._angles[1], 5)) + ';' + str(round(lattice._angles[2], 5)) + '\t' + 'Material1' + '\t' + material0_LG + '\t' + '????' + '\t' + '????', 'Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS']
else:
    lattice = lattice_
    lattice1 = lattice1_
    material0_LG = material0_lauegroup
    material1_LG = material1_lauegroup
    header = ['Channel Text File', 'Prj     lauetoolsnn', 'Author    [Ravi raj purohit]', 'JobMode    Grid', 'XCells    ' + str(lim_x), 'YCells    ' + str(lim_y), 'XStep    1.0', 'YStep    1.0', 'AcqE1    0', 'AcqE2    0', 'AcqE3    0', 'Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0', 'Phases    2', str(round(lattice._lengths[0] * 10, 5)) + ';' + str(round(lattice._lengths[1] * 10, 5)) + ';' + str(round(lattice._lengths[2] * 10, 5)) + '\t' + str(round(lattice._angles[0], 5)) + ';' + str(round(lattice._angles[1], 5)) + ';' + str(round(lattice._angles[2], 5)) + '\t' + 'Material1' + '\t' + material0_LG + '\t' + '????' + '\t' + '????', str(round(lattice1._lengths[0] * 10, 5)) + ';' + str(round(lattice1._lengths[1] * 10, 5)) + ';' + str(round(lattice1._lengths[2] * 10, 5)) + '\t' + str(round(lattice1._angles[0], 5)) + ';' + str(round(lattice1._angles[1], 5)) + ';' + str(round(lattice1._angles[2], 5)) + '\t' + 'Material2' + '\t' + material1_LG + '\t' + '????' + '\t' + '????', 'Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS']
for index in range(len(rotation_matrix)):
    euler_angles = np.zeros((len(rotation_matrix[index][0]), 3))
    phase_euler_angles = np.zeros(len(rotation_matrix[index][0]))
    for i in range(len(rotation_matrix[index][0])):
        if np.all(rotation_matrix[index][0][i, :, :] == 0):
            continue
        euler_angles[i, :] = OrientationMatrix2Euler(rotation_matrix[index][0][i, :, :])
        phase_euler_angles[i] = mat_global[index][0][i]
    euler_angles = euler_angles.reshape((lim_x, lim_y, 3))
    phase_euler_angles = phase_euler_angles.reshape((lim_x, lim_y, 1))
    a = euler_angles
    if material_ != material1_:
        filename125 = save_directory_ + '//' + material_ + '_' + material1_ + '_MTEX_UBmat_' + str(index) + '_LT_modified' + '.ctf'
    else:
        filename125 = save_directory_ + '//' + material_ + '_MTEX_UBmat_' + str(index) + '_LT_modified' + '.ctf'
    f = open(filename125, 'w')
    for ij in range(len(header)):
        f.write(header[ij] + ' \n')
    for i123 in range(euler_angles.shape[1]):
        y_step = 1 * i123
        for j123 in range(euler_angles.shape[0]):
            x_step = 1 * j123
            phase_id = int(phase_euler_angles[j123, i123, 0])
            eul = str(phase_id) + '\t' + '%0.4f' % x_step + '\t' + '%0.4f' % y_step + '\t8\t0\t' + '%0.4f' % a[j123, i123, 0] + '\t' + '%0.4f' % a[j123, i123, 1] + '\t' + '%0.4f' % a[j123, i123, 2] + '\t0.0001\t180\t0\n'
            string = eul
            f.write(string)
    f.close()
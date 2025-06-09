"""
Created on Nov 26, 2017

@author: fan

Most type of state grid generation:
    Given N Vectors,
"""
import logging
logger = logging.getLogger(__name__)
'\nCreated on Mar 17, 2017\n\n@author: fan\n'
import numpy as np

def two_mat_mesh(mat_one, mat_two, return_joint=False, return_single_col=False):
    """
    Parameters
    ----------
    return_single_col: boolean
        mat_one and mat_two are single vector, shape them into 2d array with
        1 column, rather than 1d. If not, could cause multiplication problems
        when we have both 1 column 2d array and single column 1d array in the
        same formula. But this can not always to set to True, hence default
        is actually false, because this function could take as input a matrix
        for mat_one, in that case, already 2d array.
    """
    logger.debug('return_joint:%s', return_joint)
    logger.debug('return_single_col:%s', return_single_col)
    mat_one_len = check_length(mat_one)
    mat_two_len = check_length(mat_two)
    logger.debug('mat_one_len:%s', mat_one_len)
    logger.debug('mat_one:\n%s', mat_one)
    logger.debug('mat_two_len:%s', mat_two_len)
    logger.debug('mat_two:\n%s', mat_two)
    mat_one_meshed = np.repeat(mat_one, mat_two_len, axis=0)
    mat_two_meshed = np.tile(mat_two, (mat_one_len, 1))
    if return_joint == True:
        return np.concatenate((mat_one_meshed, mat_two_meshed), axis=1)
    else:
        if return_single_col:
            mat_one_meshed = np.reshape(mat_one_meshed, (-1, 1))
            mat_two_meshed = np.reshape(mat_two_meshed, (-1, 1))
        return (mat_one_meshed, mat_two_meshed)

def three_mat_mesh(mat_one, mat_two, mat_three, return_joint=False, return_single_col=False):
    """
    Parameters
    ----------
    return_single_col: boolean
        mat_one and mat_two are single vector, shape them into 2d array with
        1 column, rather than 1d. If not, could cause multiplication problems
        when we have both 1 column 2d array and single column 1d array in the
        same formula. But this can not always to set to True, hence default
        is actually false, because this function could take as input a matrix
        for mat_one, in that case, already 2d array.
    """
    mat_one_len = check_length(mat_one)
    mat_two_len = check_length(mat_two)
    mat_three_len = check_length(mat_three)
    mat_one_meshed, mat_two_meshed = two_mat_mesh(mat_one, mat_two)
    mat_one_meshed_threed = np.repeat(mat_one_meshed, mat_three_len, axis=0)
    mat_two_meshed_threed = np.repeat(mat_two_meshed, mat_three_len, axis=0)
    mat_three_mesh_threed = np.tile(mat_three, (mat_one_len * mat_two_len, 1))
    if return_joint == True:
        return np.concatenate((mat_one_meshed_threed, mat_two_meshed_threed, mat_three_mesh_threed), axis=1)
    else:
        if return_single_col:
            mat_one_meshed_threed = np.reshape(mat_one_meshed_threed, (-1, 1))
            mat_two_meshed_threed = np.reshape(mat_two_meshed_threed, (-1, 1))
            mat_three_mesh_threed = np.reshape(mat_three_mesh_threed, (-1, 1))
        return (mat_one_meshed_threed, mat_two_meshed_threed, mat_three_mesh_threed)

def multipl_mat_mesh(mat_one, mat_two, mat_three=None, mat_four=None, mat_five=None, mat_six=None):
    mat_left = two_mat_mesh(mat_one, mat_two, return_joint=True)
    for mat_ctr in range(3, 6, 1):
        if mat_ctr == 3:
            mat_left = two_mat_mesh(mat_left, mat_three, return_joint=True)
        if mat_ctr == 4:
            mat_left = two_mat_mesh(mat_left, mat_four, return_joint=True)
        if mat_ctr == 5:
            mat_left = two_mat_mesh(mat_left, mat_five, return_joint=True)
        if mat_ctr == 6:
            mat_left = two_mat_mesh(mat_left, mat_six, return_joint=True)
    return mat_left

def check_length(mat):
    if mat.ndim == 1:
        mat_len = len(mat)
    else:
        mat_len = len(mat[:, 0])
    return mat_len
if __name__ == '__main__':
    print('Two Matrix Mesh')
    mat_one = np.array([[1, 2, 3], [3, 4, 5]])
    mat_two = np.array([[2.1, 3.2], [3.5, 4.5], [5.5, 9.5]])
    mat_one_two_joint = two_mat_mesh(mat_one, mat_two, return_joint=True)
    print(mat_one_two_joint)
    print('Three Matrix Mesh')
    mat_one = np.array([[1, 2, 3], [3, 4, 5]])
    mat_two = np.floor(np.random.rand(2, 1) * 100)
    mat_three = np.array([[2.1, 3.2], [3.5, 4.5], [5.5, 9.5]])
    mat_one_two_joint = three_mat_mesh(mat_one, mat_two, mat_three, return_joint=True)
    print(mat_one_two_joint)
    print('Two horizontal array Mesh')
    mat_one = np.array([[1, 2, 3]])
    mat_two = np.array([[2.1, 3.2]])
    mat_one_two_joint = two_mat_mesh(mat_one, mat_two, return_joint=True)
    print(mat_one_two_joint)
    print('Two vertical array Mesh')
    mat_one = np.array([[1], [2], [3]])
    mat_two = np.array([[2.1], [3.2]])
    mat_one_two_joint = two_mat_mesh(mat_one, mat_two, return_joint=True)
    print(mat_one_two_joint)
    print('Horizontal and Vertical Arrays Mesh')
    mat_one = np.array([[1], [2], [3]])
    mat_two = np.array([[2.1, 3.2]])
    mat_one_two_joint = two_mat_mesh(mat_one, mat_two, return_joint=True)
    print(mat_one_two_joint)
    print('linspace arrays mesh')
    mat_one = np.reshape(np.linspace(1, 2, 5), (-1, 1))
    mat_two = np.reshape(np.linspace(-2, -1, 2), (-1, 1))
    mat_one_two_joint = two_mat_mesh(mat_one, mat_two, return_joint=True)
    print(mat_one_two_joint)
    print('linspace arrays mesh')
    mat_one = np.reshape(np.linspace(1, 2, 5), (-1, 1))
    mat_two = np.reshape(np.linspace(-2, -1, 2), (-1, 1))
    mat_three = np.array([[1], [2], [3]])
    mat_four = np.array([[2.1], [3.2]])
    mat_five = np.array([[2.1, 3.2], [3.5, 4.5], [5.5, 9.5]])
    mat_joint = multipl_mat_mesh(mat_one, mat_two, mat_three, mat_four, mat_five)
    print(mat_joint)
def xyz_to_mat(foci, xyz_dims=None, mat_dims=None):
    """ Convert an N x 3 array of XYZ coordinates to matrix indices. """
    foci = np.hstack((foci, np.ones((foci.shape[0], 1))))
    mat = np.array([[-0.5, 0, 0, 45], [0, 0.5, 0, 63], [0, 0, 0.5, 36]]).T
    result = np.dot(foci, mat)[:, ::-1]
    return np.round_(result).astype(int)
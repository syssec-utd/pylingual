def two_way(cells):
    """ Two-way chi-square test of independence.
    Takes a 3D array as input: N(voxels) x 2 x 2, where the last two dimensions
    are the contingency table for each of N voxels. Returns an array of
    p-values.
    """
    warnings.simplefilter('ignore', RuntimeWarning)
    cells = cells.astype('float64')
    total = np.apply_over_axes(np.sum, cells, [1, 2]).ravel()
    chi_sq = np.zeros(cells.shape, dtype='float64')
    for i in range(2):
        for j in range(2):
            exp = np.sum(cells[:, i, :], 1).ravel() * np.sum(cells[:, :, j], 1).ravel() / total
            bad_vox = np.where(exp == 0)[0]
            chi_sq[:, i, j] = (cells[:, i, j] - exp) ** 2 / exp
            chi_sq[bad_vox, i, j] = 1.0
    chi_sq = np.apply_over_axes(np.sum, chi_sq, [1, 2]).ravel()
    return special.chdtrc(1, chi_sq)
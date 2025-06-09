def export_obj(filename, cutout, level=0):
    """
    Converts a dense annotation to a obj, using Marching Cubes (PyMCubes).

    Arguments:
        filename (str): The filename to write out to
        cutout (numpy.ndarray): The dense annotation
        level (int): The level at which to run mcubes

    Returns:
        boolean success
    """
    if '.obj' not in filename:
        filename = filename + '.obj'
    (vs, fs) = mcubes.marching_cubes(cutout, level)
    mcubes.export_obj(vs, fs, filename)
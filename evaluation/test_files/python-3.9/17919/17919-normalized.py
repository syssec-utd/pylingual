def load(nifti_filename):
    """
    Import a nifti file into a numpy array. TODO:  Currently only
    transfers raw data for compatibility with annotation and ND formats

    Arguments:
        nifti_filename (str):  A string filename of a nifti datafile

    Returns:
        A numpy array with data from the nifti file
    """
    nifti_filename = os.path.expanduser(nifti_filename)
    try:
        data = nib.load(nifti_filename)
        img = data.get_data()
    except Exception as e:
        raise ValueError('Could not load file {0} for conversion.'.format(nifti_filename))
        raise
    return img
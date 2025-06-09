def save_img(data, filename, masker, header=None):
    """ Save a vectorized image to file. """
    if not header:
        header = masker.get_header()
    header.set_data_dtype(data.dtype)
    header['cal_max'] = data.max()
    header['cal_min'] = data.min()
    img = nifti1.Nifti1Image(masker.unmask(data), None, header)
    img.to_filename(filename)
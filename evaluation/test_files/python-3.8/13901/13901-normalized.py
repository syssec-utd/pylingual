def _getbitmap_type(self, filename):
    """
        Get the type of an image from the file's extension ( .jpg, etc. )
        """
    if filename is None or filename == '':
        return None
    (name, ext) = os.path.splitext(filename)
    ext = ext[1:].upper()
    if ext == 'BMP':
        return wx.BITMAP_TYPE_BMP
    elif ext == 'GIF':
        return wx.BITMAP_TYPE_GIF
    elif ext == 'JPG' or ext == 'JPEG':
        return wx.BITMAP_TYPE_JPEG
    elif ext == 'PCX':
        return wx.BITMAP_TYPE_PCX
    elif ext == 'PNG':
        return wx.BITMAP_TYPE_PNG
    elif ext == 'PNM':
        return wx.BITMAP_TYPE_PNM
    elif ext == 'TIF' or ext == 'TIFF':
        return wx.BITMAP_TYPE_TIF
    elif ext == 'XBM':
        return wx.BITMAP_TYPE_XBM
    elif ext == 'XPM':
        return wx.BITMAP_TYPE_XPM
    else:
        raise RuntimeError('invalid graphics format')
def get_region(self, x1, y1, x2, y2):
    """Get an image that refers to the given rectangle within this image.  The image data is not actually
        copied; if the image region is rendered into, it will affect this image.

        :param int x1: left edge of the image region to return
        :param int y1: top edge of the image region to return
        :param int x2: right edge of the image region to return
        :param int y2: bottom edge of the image region to return
        :return: :class:`Image`
        """
    handle = c_int()
    lib.GetImageRegion(byref(handle), self._handle, x1, y1, x2, y2)
    return Image(width=x2 - x1, height=y2 - y1, content_scale=self._content_scale, handle=handle)
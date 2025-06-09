def from_image(cls, filename, start, stop, legend, source='Image', col_offset=0.1, row_offset=2, tolerance=0):
    """
        Read an image and generate Striplog.

        Args:
            filename (str): An image file, preferably high-res PNG.
            start (float or int): The depth at the top of the image.
            stop (float or int): The depth at the bottom of the image.
            legend (Legend): A legend to look up the components in.
            source (str): A source for the data. Default: 'Image'.
            col_offset (Number): The proportion of the way across the image
                from which to extract the pixel column. Default: 0.1 (ie 10%).
            row_offset (int): The number of pixels to skip at the top of
                each change in colour. Default: 2.
            tolerance (float): The Euclidean distance between hex colours,
                which has a maximum (black to white) of 441.67 in base 10.
                Default: 0.

        Returns:
            Striplog: The ``striplog`` object.
        """
    rgb = utils.loglike_from_image(filename, col_offset)
    loglike = np.array([utils.rgb_to_hex(t) for t in rgb])
    (tops, hexes) = utils.tops_from_loglike(loglike, offset=row_offset)
    nonconsecutive = np.append(np.diff(tops), 2)
    tops = tops[nonconsecutive > 1]
    hexes = hexes[nonconsecutive > 1]
    hexes_reduced = list(set(hexes))
    components = [legend.get_component(h, tolerance=tolerance) for h in hexes_reduced]
    values = [hexes_reduced.index(i) for i in hexes]
    basis = np.linspace(start, stop, loglike.size)
    list_of_Intervals = cls.__intervals_from_tops(tops, values, basis, components)
    return cls(list_of_Intervals, source='Image')
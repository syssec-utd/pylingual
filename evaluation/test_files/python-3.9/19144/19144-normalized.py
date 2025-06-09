def merge_svg_files(svg_file1, svg_file2, x_coord, y_coord, scale=1):
    """ Merge `svg_file2` in `svg_file1` in the given positions `x_coord`, `y_coord` and `scale`.

    Parameters
    ----------
    svg_file1: str or svgutils svg document object
        Path to a '.svg' file.

    svg_file2: str or svgutils svg document object
        Path to a '.svg' file.

    x_coord: float
        Horizontal axis position of the `svg_file2` content.

    y_coord: float
        Vertical axis position of the `svg_file2` content.

    scale: float
        Scale to apply to `svg_file2` content.

    Returns
    -------
    `svg1` svgutils object with the content of 'svg_file2'
    """
    svg1 = _check_svg_file(svg_file1)
    svg2 = _check_svg_file(svg_file2)
    svg2_root = svg2.getroot()
    svg1.append([svg2_root])
    svg2_root.moveto(x_coord, y_coord, scale=scale)
    return svg1
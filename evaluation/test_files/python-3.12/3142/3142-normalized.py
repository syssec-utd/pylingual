def healpix_plot(self, healpix_expression='source_id/34359738368', healpix_max_level=12, healpix_level=8, what='count(*)', selection=None, grid=None, healpix_input='equatorial', healpix_output='galactic', f=None, colormap='afmhot', grid_limits=None, image_size=800, nest=True, figsize=None, interactive=False, title='', smooth=None, show=False, colorbar=True, rotation=(0, 0, 0), **kwargs):
    """Viz data in 2d using a healpix column.

        :param healpix_expression: {healpix_max_level}
        :param healpix_max_level: {healpix_max_level}
        :param healpix_level: {healpix_level}
        :param what: {what}
        :param selection: {selection}
        :param grid: {grid}
        :param healpix_input: Specificy if the healpix index is in "equatorial", "galactic" or "ecliptic".
        :param healpix_output: Plot in "equatorial", "galactic" or "ecliptic".
        :param f: function to apply to the data
        :param colormap: matplotlib colormap
        :param grid_limits: Optional sequence [minvalue, maxvalue] that determine the min and max value that map to the colormap (values below and above these are clipped to the the min/max). (default is [min(f(grid)), max(f(grid)))
        :param image_size: size for the image that healpy uses for rendering
        :param nest: If the healpix data is in nested (True) or ring (False)
        :param figsize: If given, modify the matplotlib figure size. Example (14,9)
        :param interactive: (Experimental, uses healpy.mollzoom is True)
        :param title: Title of figure
        :param smooth: apply gaussian smoothing, in degrees
        :param show: Call matplotlib's show (True) or not (False, defaut)
        :param rotation: Rotatate the plot, in format (lon, lat, psi) such that (lon, lat) is the center, and rotate on the screen by angle psi. All angles are degrees.
        :return:
        """
    import healpy as hp
    import pylab as plt
    if grid is None:
        reduce_level = healpix_max_level - healpix_level
        NSIDE = 2 ** healpix_level
        nmax = hp.nside2npix(NSIDE)
        scaling = 4 ** reduce_level
        epsilon = 1.0 / scaling / 2
        grid = self._stat(what=what, binby='%s/%s' % (healpix_expression, scaling), limits=[-epsilon, nmax - epsilon], shape=nmax, selection=selection)
    if grid_limits:
        grid_min, grid_max = grid_limits
    else:
        grid_min = grid_max = None
    f_org = f
    f = _parse_f(f)
    if smooth:
        if nest:
            grid = hp.reorder(grid, inp='NEST', out='RING')
            nest = False
        grid = hp.smoothing(grid, sigma=np.radians(smooth))
    fgrid = f(grid)
    coord_map = dict(equatorial='C', galactic='G', ecliptic='E')
    fig = plt.gcf()
    if figsize is not None:
        fig.set_size_inches(*figsize)
    what_label = what
    if f_org:
        what_label = f_org + ' ' + what_label
    f = hp.mollzoom if interactive else hp.mollview
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        coord = (coord_map[healpix_input], coord_map[healpix_output])
        if coord_map[healpix_input] == coord_map[healpix_output]:
            coord = None
        f(fgrid, unit=what_label, rot=rotation, nest=nest, title=title, coord=coord, cmap=colormap, hold=True, xsize=image_size, min=grid_min, max=grid_max, cbar=colorbar, **kwargs)
    if show:
        plt.show()
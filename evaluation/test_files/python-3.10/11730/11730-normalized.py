def plot_waterfall(self, f_start=None, f_stop=None, if_id=0, logged=True, cb=True, MJD_time=False, **kwargs):
    """ Plot waterfall of data

        Args:
            f_start (float): start frequency, in MHz
            f_stop (float): stop frequency, in MHz
            logged (bool): Plot in linear (False) or dB units (True),
            cb (bool): for plotting the colorbar
            kwargs: keyword args to be passed to matplotlib imshow()
        """
    (plot_f, plot_data) = self.grab_data(f_start, f_stop, if_id)
    if self.header[b'foff'] < 0:
        plot_data = plot_data[..., ::-1]
        plot_f = plot_f[::-1]
    if logged:
        plot_data = db(plot_data)
    (dec_fac_x, dec_fac_y) = (1, 1)
    if plot_data.shape[0] > MAX_IMSHOW_POINTS[0]:
        dec_fac_x = int(plot_data.shape[0] / MAX_IMSHOW_POINTS[0])
    if plot_data.shape[1] > MAX_IMSHOW_POINTS[1]:
        dec_fac_y = int(plot_data.shape[1] / MAX_IMSHOW_POINTS[1])
    plot_data = rebin(plot_data, dec_fac_x, dec_fac_y)
    try:
        plt.title(self.header[b'source_name'])
    except KeyError:
        plt.title(self.filename)
    extent = self._calc_extent(plot_f=plot_f, plot_t=self.timestamps, MJD_time=MJD_time)
    plt.imshow(plot_data, aspect='auto', origin='lower', rasterized=True, interpolation='nearest', extent=extent, cmap='viridis', **kwargs)
    if cb:
        plt.colorbar()
    plt.xlabel('Frequency [MHz]')
    if MJD_time:
        plt.ylabel('Time [MJD]')
    else:
        plt.ylabel('Time [s]')
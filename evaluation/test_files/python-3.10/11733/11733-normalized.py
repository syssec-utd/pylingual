def plot_all(self, t=0, f_start=None, f_stop=None, logged=False, if_id=0, kurtosis=True, **kwargs):
    """ Plot waterfall of data as well as spectrum; also, placeholder to make even more complicated plots in the future.

        Args:
            f_start (float): start frequency, in MHz
            f_stop (float): stop frequency, in MHz
            logged (bool): Plot in linear (False) or dB units (True),
            t (int): integration number to plot (0 -> len(data))
            logged (bool): Plot in linear (False) or dB units (True)
            if_id (int): IF identification (if multiple IF signals in file)
            kwargs: keyword args to be passed to matplotlib plot() and imshow()
        """
    if self.header[b'nbits'] <= 2:
        logged = False
    nullfmt = NullFormatter()
    (left, width) = (0.35, 0.5)
    (bottom, height) = (0.45, 0.5)
    (width2, height2) = (0.1125, 0.15)
    (bottom2, left2) = (bottom - height2 - 0.025, left - width2 - 0.02)
    (bottom3, left3) = (bottom2 - height2 - 0.025, 0.075)
    rect_waterfall = [left, bottom, width, height]
    rect_colorbar = [left + width, bottom, 0.025, height]
    rect_spectrum = [left, bottom2, width, height2]
    rect_min_max = [left, bottom3, width, height2]
    rect_timeseries = [left + width, bottom, width2, height]
    rect_kurtosis = [left3, bottom3, 0.25, height2]
    rect_header = [left3 - 0.05, bottom, 0.2, height]
    axMinMax = plt.axes(rect_min_max)
    print('Plotting Min Max')
    self.plot_spectrum_min_max(logged=logged, f_start=f_start, f_stop=f_stop, t=t)
    plt.title('')
    axMinMax.yaxis.tick_right()
    axMinMax.yaxis.set_label_position('right')
    axSpectrum = plt.axes(rect_spectrum, sharex=axMinMax)
    print('Plotting Spectrum')
    self.plot_spectrum(logged=logged, f_start=f_start, f_stop=f_stop, t=t)
    plt.title('')
    axSpectrum.yaxis.tick_right()
    axSpectrum.yaxis.set_label_position('right')
    plt.xlabel('')
    plt.setp(axSpectrum.get_xticklabels(), visible=False)
    axWaterfall = plt.axes(rect_waterfall, sharex=axMinMax)
    print('Plotting Waterfall')
    self.plot_waterfall(f_start=f_start, f_stop=f_stop, logged=logged, cb=False)
    plt.xlabel('')
    plt.setp(axWaterfall.get_xticklabels(), visible=False)
    axTimeseries = plt.axes(rect_timeseries)
    print('Plotting Timeseries')
    self.plot_time_series(f_start=f_start, f_stop=f_stop, orientation='v')
    axTimeseries.yaxis.set_major_formatter(nullfmt)
    if kurtosis:
        axKurtosis = plt.axes(rect_kurtosis)
        print('Plotting Kurtosis')
        self.plot_kurtosis(f_start=f_start, f_stop=f_stop)
    axHeader = plt.axes(rect_header)
    print('Plotting Header')
    telescopes = {0: 'Fake data', 1: 'Arecibo', 2: 'Ooty', 3: 'Nancay', 4: 'Parkes', 5: 'Jodrell', 6: 'GBT', 8: 'Effelsberg', 10: 'SRT', 64: 'MeerKAT', 65: 'KAT7'}
    telescope = telescopes.get(self.header[b'telescope_id'], self.header[b'telescope_id'])
    plot_header = '%14s: %s\n' % ('TELESCOPE_ID', telescope)
    for key in (b'SRC_RAJ', b'SRC_DEJ', b'TSTART', b'NCHANS', b'NBEAMS', b'NIFS', b'NBITS'):
        try:
            plot_header += '%14s: %s\n' % (key, self.header[key.lower()])
        except KeyError:
            pass
    fch1 = '%6.6f MHz' % self.header[b'fch1']
    foff = self.header[b'foff'] * 1000000.0 * u.Hz
    if np.abs(foff) > 1000000.0 * u.Hz:
        foff = str(foff.to('MHz'))
    elif np.abs(foff) > 1000.0 * u.Hz:
        foff = str(foff.to('kHz'))
    else:
        foff = str(foff.to('Hz'))
    plot_header += '%14s: %s\n' % ('FCH1', fch1)
    plot_header += '%14s: %s\n' % ('FOFF', foff)
    plt.text(0.05, 0.95, plot_header, ha='left', va='top', wrap=True)
    axHeader.set_facecolor('white')
    axHeader.xaxis.set_major_formatter(nullfmt)
    axHeader.yaxis.set_major_formatter(nullfmt)
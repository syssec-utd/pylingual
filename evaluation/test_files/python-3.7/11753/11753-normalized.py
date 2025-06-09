def plot_calibrated_diode(dio_cross, chan_per_coarse=8, feedtype='l', **kwargs):
    """
    Plots the corrected noise diode spectrum for a given noise diode measurement
    after application of the inverse Mueller matrix for the electronics chain.
    """
    obs = Waterfall(dio_cross, max_load=150)
    freqs = obs.populate_freqs()
    tsamp = obs.header['tsamp']
    data = obs.data
    obs = None
    (I, Q, U, V) = get_stokes(data, feedtype)
    data = None
    psis = phase_offsets(I, Q, U, V, tsamp, chan_per_coarse, feedtype, **kwargs)
    G = gain_offsets(I, Q, U, V, tsamp, chan_per_coarse, feedtype, **kwargs)
    (I, Q, U, V) = apply_Mueller(I, Q, U, V, G, psis, chan_per_coarse, feedtype)
    (I_OFF, I_ON) = foldcal(I, tsamp, **kwargs)
    (Q_OFF, Q_ON) = foldcal(Q, tsamp, **kwargs)
    (U_OFF, U_ON) = foldcal(U, tsamp, **kwargs)
    (V_OFF, V_ON) = foldcal(V, tsamp, **kwargs)
    I = None
    Q = None
    U = None
    V = None
    plt.plot(freqs, I_ON - I_OFF, 'k-', label='I')
    plt.plot(freqs, Q_ON - Q_OFF, 'r-', label='Q')
    plt.plot(freqs, U_ON - U_OFF, 'g-', label='U')
    plt.plot(freqs, V_ON - V_OFF, 'm-', label='V')
    plt.legend()
    plt.xlabel('Frequency (MHz)')
    plt.title('Calibrated Full Stokes Noise Diode Spectrum')
    plt.ylabel('Power (Counts)')
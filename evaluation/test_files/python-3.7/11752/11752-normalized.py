def plot_Stokes_diode(dio_cross, diff=True, feedtype='l', **kwargs):
    """
    Plots the uncalibrated full stokes spectrum of the noise diode.
    Use diff=False to plot both ON and OFF, or diff=True for ON-OFF
    """
    if diff == True:
        (Idiff, Qdiff, Udiff, Vdiff, freqs) = get_diff(dio_cross, feedtype, **kwargs)
    else:
        obs = Waterfall(dio_cross, max_load=150)
        freqs = obs.populate_freqs()
        tsamp = obs.header['tsamp']
        data = obs.data
        (I, Q, U, V) = get_stokes(data, feedtype)
        (I_OFF, I_ON) = foldcal(I, tsamp, **kwargs)
        (Q_OFF, Q_ON) = foldcal(Q, tsamp, **kwargs)
        (U_OFF, U_ON) = foldcal(U, tsamp, **kwargs)
        (V_OFF, V_ON) = foldcal(V, tsamp, **kwargs)
    if diff == True:
        plt.plot(freqs, Idiff, 'k-', label='I')
        plt.plot(freqs, Qdiff, 'r-', label='Q')
        plt.plot(freqs, Udiff, 'g-', label='U')
        plt.plot(freqs, Vdiff, 'm-', label='V')
    else:
        plt.plot(freqs, I_ON, 'k-', label='I ON')
        plt.plot(freqs, I_OFF, 'k--', label='I OFF')
        plt.plot(freqs, Q_ON, 'r-', label='Q ON')
        plt.plot(freqs, Q_OFF, 'r--', label='Q OFF')
        plt.plot(freqs, U_ON, 'g-', label='U ON')
        plt.plot(freqs, U_OFF, 'g--', label='U OFF')
        plt.plot(freqs, V_ON, 'm-', label='V ON')
        plt.plot(freqs, V_OFF, 'm--', label='V OFF')
    plt.legend()
    plt.xlabel('Frequency (MHz)')
    plt.title('Uncalibrated Full Stokes Noise Diode Spectrum')
    plt.ylabel('Power (Counts)')
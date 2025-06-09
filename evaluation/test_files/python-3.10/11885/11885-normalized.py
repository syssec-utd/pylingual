def makePlot(args):
    """
  Make the plot with proper motion performance predictions. The predictions are for the TOTAL proper
  motion under the assumption of equal components mu_alpha* and mu_delta.

  :argument args: command line arguments
  """
    gmag = np.linspace(5.7, 20.0, 101)
    vminiB1V = vminiFromSpt('B1V')
    vminiG2V = vminiFromSpt('G2V')
    vminiM6V = vminiFromSpt('M6V')
    vmagB1V = gmag - gminvFromVmini(vminiB1V)
    vmagG2V = gmag - gminvFromVmini(vminiG2V)
    vmagM6V = gmag - gminvFromVmini(vminiM6V)
    (sigmualphaB1V, sigmudeltaB1V) = properMotionErrorSkyAvg(gmag, vminiB1V)
    sigmuB1V = np.sqrt(0.5 * sigmualphaB1V ** 2 + 0.5 * sigmudeltaB1V ** 2)
    (sigmualphaB1V, sigmudeltaB1V) = properMotionMinError(gmag, vminiB1V)
    sigmuB1Vmin = np.sqrt(0.5 * sigmualphaB1V ** 2 + 0.5 * sigmudeltaB1V ** 2)
    (sigmualphaB1V, sigmudeltaB1V) = properMotionMaxError(gmag, vminiB1V)
    sigmuB1Vmax = np.sqrt(0.5 * sigmualphaB1V ** 2 + 0.5 * sigmudeltaB1V ** 2)
    (sigmualphaG2V, sigmudeltaG2V) = properMotionErrorSkyAvg(gmag, vminiG2V)
    sigmuG2V = np.sqrt(0.5 * sigmualphaG2V ** 2 + 0.5 * sigmudeltaG2V ** 2)
    (sigmualphaG2V, sigmudeltaG2V) = properMotionMinError(gmag, vminiG2V)
    sigmuG2Vmin = np.sqrt(0.5 * sigmualphaG2V ** 2 + 0.5 * sigmudeltaG2V ** 2)
    (sigmualphaG2V, sigmudeltaG2V) = properMotionMaxError(gmag, vminiG2V)
    sigmuG2Vmax = np.sqrt(0.5 * sigmualphaG2V ** 2 + 0.5 * sigmudeltaG2V ** 2)
    (sigmualphaM6V, sigmudeltaM6V) = properMotionErrorSkyAvg(gmag, vminiM6V)
    sigmuM6V = np.sqrt(0.5 * sigmualphaM6V ** 2 + 0.5 * sigmudeltaM6V ** 2)
    (sigmualphaM6V, sigmudeltaM6V) = properMotionMinError(gmag, vminiM6V)
    sigmuM6Vmin = np.sqrt(0.5 * sigmualphaM6V ** 2 + 0.5 * sigmudeltaM6V ** 2)
    (sigmualphaM6V, sigmudeltaM6V) = properMotionMaxError(gmag, vminiM6V)
    sigmuM6Vmax = np.sqrt(0.5 * sigmualphaM6V ** 2 + 0.5 * sigmudeltaM6V ** 2)
    fig = plt.figure(figsize=(10, 6.5))
    if args['gmagAbscissa']:
        plt.semilogy(gmag, sigmuB1V, 'b', label='B1V')
        plt.semilogy(gmag, sigmuG2V, 'g', label='G2V')
        plt.semilogy(gmag, sigmuM6V, 'r', label='M6V')
        plt.xlim((5, 20))
        plt.ylim((1, 500))
        plt.legend(loc=4)
    else:
        ax = fig.add_subplot(111)
        plt.semilogy(vmagB1V, sigmuB1V, 'b', label='B1V')
        plt.semilogy(vmagM6V, sigmuM6V, 'r', label='M6V')
        plt.fill_between(vmagB1V, sigmuB1Vmin, sigmuB1Vmax, color='b', alpha=0.3)
        plt.fill_between(vmagM6V, sigmuM6Vmin, sigmuM6Vmax, color='r', alpha=0.3)
        plt.xlim((5, 22.5))
        plt.ylim((1, 500))
        plt.text(17.5, 100, 'B1V', color='b')
        plt.text(18, 10, 'M6V', color='r')
        plt.text(7, 11, 'calibration noise floor', size=12, bbox=dict(boxstyle='round,pad=0.3', ec=(0.0, 0.0, 0.0), fc=(1.0, 1.0, 1.0)))
        plt.text(14.75, 50, 'photon noise', rotation=45, size=12, bbox=dict(boxstyle='round,pad=0.3', ec=(0.0, 0.0, 0.0), fc=(1.0, 1.0, 1.0)))
        ax.annotate('non-uniformity\nover the sky', xy=(21.5, 80), xycoords='data', xytext=(21.5, 30), textcoords='data', ha='center', size='12', bbox=dict(boxstyle='round,pad=0.3', ec=(0, 0, 0), fc=(1, 1, 1)), arrowprops=dict(facecolor='black', shrink=0.15, width=1, headwidth=6), horizontalalignment='right', verticalalignment='top')
        ax.annotate('', xy=(21.5, 170), xycoords='data', xytext=(21.5, 380), textcoords='data', ha='center', size='12', arrowprops=dict(facecolor='black', shrink=0.15, width=1, headwidth=6), horizontalalignment='right', verticalalignment='bottom')
    plt.xticks(np.arange(6, 24, 2))
    ax = plt.gca().yaxis
    ax.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    plt.ticklabel_format(axis='y', style='plain')
    plt.grid(which='both')
    plt.xlabel('$V$ [mag]')
    plt.ylabel('End-of-mission $\\sigma_\\mu$ [$\\mu$as/yr]')
    basename = 'ProperMotionErrors'
    if args['pdfOutput']:
        plt.savefig(basename + '.pdf')
    elif args['pngOutput']:
        plt.savefig(basename + '.png')
    else:
        plt.show()
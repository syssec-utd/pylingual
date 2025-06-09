def makePlot(args):
    """
  Make the plot with parallax horizons. The plot shows V-band magnitude vs distance for a number of
  spectral types and over the range 5.7<G<20. In addition a set of crudely drawn contours show the points
  where 0.1, 1, and 10 per cent relative parallax accracy are reached.

  Parameters
  ----------
  
  args - Command line arguments.
  """
    distances = 10.0 ** np.linspace(1, 6, 10001)
    spts = ['B0V', 'A0V', 'F0V', 'G0V', 'K0V', 'K4V', 'K1III']
    twokmsRV = []
    twokmsV = []
    vabsTwokms = []
    fivekmsRV = []
    fivekmsV = []
    vabsFivekms = []
    tenkmsRV = []
    tenkmsV = []
    vabsTenkms = []
    fig = plt.figure(figsize=(11, 7.8))
    deltaHue = 240.0 / (len(spts) - 1)
    hues = (240.0 - np.arange(len(spts)) * deltaHue) / 360.0
    hsv = np.zeros((1, 1, 3))
    hsv[0, 0, 1] = 1.0
    hsv[0, 0, 2] = 0.9
    for hue, spt in zip(hues, spts):
        hsv[0, 0, 0] = hue
        vmags = vabsFromSpt(spt) + 5.0 * np.log10(distances) - 5.0
        vmini = vminiFromSpt(spt)
        grvsmags = vmags - vminGrvsFromVmini(vmini)
        rvError = vradErrorSkyAvg(vmags, spt)
        observed = (grvsmags >= 5.7) & (grvsmags <= 16.1)
        rvError = rvError[observed]
        if rvError.min() <= 2.0:
            index = len(rvError[rvError <= 2.0]) - 1
            twokmsRV.append(distances[observed][index])
            twokmsV.append(vmags[observed][index])
            vabsTwokms.append(vabsFromSpt(spt))
        if rvError.min() <= 5.0:
            index = len(rvError[rvError <= 5.0]) - 1
            fivekmsRV.append(distances[observed][index])
            fivekmsV.append(vmags[observed][index])
            vabsFivekms.append(vabsFromSpt(spt))
        if rvError.min() <= 10.0:
            index = len(rvError[rvError <= 10.0]) - 1
            tenkmsRV.append(distances[observed][index])
            tenkmsV.append(vmags[observed][index])
            vabsTenkms.append(vabsFromSpt(spt))
        plt.semilogx(distances[observed], vmags[observed], '-', label=spt, color=hsv_to_rgb(hsv)[0, 0, :])
        plt.text(distances[observed][-1], vmags[observed][-1], spt, horizontalalignment='center', verticalalignment='bottom', fontsize=14)
    twokmsRV = np.array(twokmsRV)
    twokmsV = np.array(twokmsV)
    indices = np.argsort(vabsTwokms)
    plt.semilogx(twokmsRV[indices], twokmsV[indices], 'k--')
    plt.text(twokmsRV[indices][-1] * 0.8, twokmsV[indices][-1], '$2$ km s$^{-1}$', ha='right', size=16, bbox=dict(boxstyle='round, pad=0.3', ec=(0.0, 0.0, 0.0), fc=(1.0, 1.0, 1.0)))
    fivekmsRV = np.array(fivekmsRV)
    fivekmsV = np.array(fivekmsV)
    indices = np.argsort(vabsFivekms)
    plt.semilogx(fivekmsRV[indices], fivekmsV[indices], 'k--')
    plt.text(fivekmsRV[indices][-1] * 0.8, fivekmsV[indices][-1], '$5$ km s$^{-1}$', ha='right', size=16, bbox=dict(boxstyle='round, pad=0.3', ec=(0.0, 0.0, 0.0), fc=(1.0, 1.0, 1.0)))
    tenkmsRV = np.array(tenkmsRV)
    tenkmsV = np.array(tenkmsV)
    indices = np.argsort(vabsTenkms)
    plt.semilogx(tenkmsRV[indices], tenkmsV[indices], 'k--')
    plt.text(tenkmsRV[indices][-1] * 0.8, tenkmsV[indices][-1] + 0.5, '$10$ km s$^{-1}$', ha='right', size=16, bbox=dict(boxstyle='round, pad=0.3', ec=(0.0, 0.0, 0.0), fc=(1.0, 1.0, 1.0)))
    plt.title('Radial velocity accuracy horizons ($A_V=0$)')
    plt.xlabel('Distance [pc]')
    plt.ylabel('V')
    plt.grid()
    plt.ylim(5, 20)
    basename = 'RadialVelocityHorizons'
    if args['pdfOutput']:
        plt.savefig(basename + '.pdf')
    elif args['pngOutput']:
        plt.savefig(basename + '.png')
    else:
        plt.show()
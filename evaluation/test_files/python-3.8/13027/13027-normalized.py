def capacity_terzaghi_1943(sl, fd, round_footing=False, verbose=0, **kwargs):
    """
    Calculates the foundation capacity according Terzaghi (1943)
    Ref: http://geo.cv.nctu.edu.tw/foundation/
    download/BearingCapacityOfFoundations.pdf

    :param sl: Soil object
    :param fd: Foundation object
    :param round_footing: if True, then foundation is round
    :param verbose: verbosity
    :return: ultimate bearing stress
    Note: the shape factor of 1.3 is used for aspect ratio > 6
    """
    if not kwargs.get('disable_requires', False):
        models.check_required(sl, ['phi_r', 'cohesion', 'unit_dry_weight'])
        models.check_required(fd, ['length', 'width', 'depth'])
    a02 = np.exp(np.pi * (0.75 - sl.phi / 360) * np.tan(sl.phi_r)) ** 2
    a0_check = np.exp((270 - sl.phi) / 180 * np.pi * np.tan(sl.phi_r))
    if (a02 - a0_check) / a02 > 0.001:
        raise DesignError
    fd.nq_factor = a02 / (2 * np.cos((45 + sl.phi / 2) * np.pi / 180) ** 2)
    fd.ng_factor = 2 * (fd.nq_factor + 1) * np.tan(sl.phi_r) / (1 + 0.4 * np.sin(4 * sl.phi_r))
    if sl.phi_r == 0:
        fd.nc_factor = 5.7
    else:
        fd.nc_factor = (fd.nq_factor - 1) / np.tan(sl.phi_r)
    if round_footing:
        s_c = 1.3
        s_g = 0.6
    elif fd.length / fd.width < 5:
        s_c = 1.3
        s_g = 0.8
    else:
        s_c = 1.0
        s_g = 1.0
    s_q = 1.0
    q_d = sl.unit_dry_weight * fd.depth
    fd.q_ult = sl.cohesion * fd.nc_factor * s_c + q_d * fd.nq_factor * s_q + 0.5 * fd.width * sl.unit_dry_weight * fd.ng_factor * s_g
    if verbose:
        log('Nc: ', fd.nc_factor)
        log('Nq: ', fd.nq_factor)
        log('Ng: ', fd.ng_factor)
        log('s_c: ', s_c)
        log('s_q: ', s_q)
        log('s_g: ', s_g)
        log('qult: ', fd.q_ult)
    return fd.q_ult
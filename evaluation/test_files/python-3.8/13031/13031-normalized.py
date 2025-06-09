def capacity_salgado_2008(sl, fd, h_l=0, h_b=0, vertical_load=1, verbose=0, **kwargs):
    """
    calculates the capacity according to
     THe Engineering of Foundations textbook by Salgado

     ISBN: 0072500581

    :param sl: Soil object
    :param fd: Foundation object
    :param h_l: Horizontal load parallel to length
    :param h_b: Horizontal load parallel to width
    :param vertical_load: Vertical load
    :param verbose: verbosity
    :return: ultimate bearing stress
    """
    if not kwargs.get('disable_requires', False):
        models.check_required(sl, ['phi_r', 'cohesion', 'unit_dry_weight'])
        models.check_required(fd, ['length', 'width', 'depth'])
    h_eff_b = kwargs.get('h_eff_b', 0)
    h_eff_l = kwargs.get('h_eff_l', 0)
    loc_v_l = kwargs.get('loc_v_l', fd.length / 2)
    loc_v_b = kwargs.get('loc_v_b', fd.width / 2)
    ecc_b = h_b * h_eff_b / vertical_load
    ecc_l = h_l * h_eff_l / vertical_load
    width_eff = min(fd.width, 2 * (loc_v_b + ecc_b), 2 * (fd.width - loc_v_b - ecc_b))
    length_eff = min(fd.length, 2 * (loc_v_l + ecc_l), 2 * (fd.length - loc_v_l - ecc_l))
    if width_eff / 2 < fd.width / 6:
        DesignError('failed on eccentricity')
    fd.nq_factor = np.exp(np.pi * np.tan(sl.phi_r)) * (1 + np.sin(sl.phi_r)) / (1 - np.sin(sl.phi_r))
    fd.ng_factor = 1.5 * (fd.nq_factor - 1) * np.tan(sl.phi_r)
    if sl.phi_r == 0:
        fd.nc_factor = 5.14
    else:
        fd.nc_factor = (fd.nq_factor - 1) / np.tan(sl.phi_r)
    s_q = 1 + width_eff / length_eff * np.tan(sl.phi_r)
    s_g = max(1 - 0.4 * width_eff / length_eff, 0.6)
    s_c = 1.0
    d_q = 1 + 2 * np.tan(sl.phi_r) * (1 - np.sin(sl.phi_r)) ** 2 * fd.depth / width_eff
    d_g = 1.0
    d_c = 1.0
    q_d = sl.unit_dry_weight * fd.depth
    if verbose:
        log('width_eff: ', width_eff)
        log('length_eff: ', length_eff)
        log('Nc: ', fd.nc_factor)
        log('Nq: ', fd.nq_factor)
        log('Ng: ', fd.ng_factor)
        log('s_c: ', s_c)
        log('s_q: ', s_q)
        log('s_g: ', s_g)
        log('d_c: ', d_c)
        log('d_q: ', d_q)
        log('d_g: ', d_g)
        log('q_d: ', q_d)
    fd.q_ult = sl.cohesion * fd.nc_factor * s_c * d_c + q_d * fd.nq_factor * s_q * d_q + 0.5 * width_eff * sl.unit_dry_weight * fd.ng_factor * s_g * d_g
    if verbose:
        log('qult: ', fd.q_ult)
    return fd.q_ult
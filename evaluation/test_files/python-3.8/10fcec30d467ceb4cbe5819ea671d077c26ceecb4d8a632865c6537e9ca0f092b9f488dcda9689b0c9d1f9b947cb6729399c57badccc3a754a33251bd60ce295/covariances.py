import numpy as np
from . import ccllib as lib
from .pyutils import check, integ_types, _check_array_params
from .background import comoving_radial_distance, comoving_angular_distance
from .tk3d import Tk3D
from .pk2d import parse_pk2d
NoneArr = np.array([])

def angular_cl_cov_cNG(cosmo, cltracer1, cltracer2, ell, tkka, fsky=1.0, cltracer3=None, cltracer4=None, ell2=None, integration_method='qag_quad'):
    """Calculate the connected non-Gaussian covariance for a pair of
    power spectra :math:`C_{\\ell_1}^{ab}` and :math:`C_{\\ell_2}^{cd}`,
    between two pairs of tracers (:math:`(a,b)` and :math:`(c,d)`).

    Specifically, it computes:

    .. math::
        {\\rm Cov}_{\\rm cNG}(\\ell_1,\\ell_2)=
        \\int \\frac{d\\chi}{\\chi^6}
        \\tilde{\\Delta}^a_{\\ell_1}(\\chi)
        \\tilde{\\Delta}^b_{\\ell_1}(\\chi)
        \\tilde{\\Delta}^c_{\\ell_2}(\\chi)
        \\tilde{\\Delta}^d_{\\ell_2}(\\chi)\\,
        \\bar{T}_{abcd}\\left[\\frac{\\ell_1+1/2}{\\chi},
                              \\frac{\\ell_2+1/2}{\\chi}, a(\\chi)\\right]

    where :math:`\\Delta^x_\\ell(\\chi)` is the transfer function for tracer
    :math:`x` (see Eq. 39 in the CCL note), and
    :math:`\\bar{T}_{abcd}(k_1,k_2,a)` is the isotropized connected
    trispectrum of the four tracers (see the documentation of the
    :class:`~pyccl.tk3d.Tk3D` class for details).

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): A Cosmology object.
        cltracer1 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind.
        cltracer2 (:class:`~pyccl.tracers.Tracer`): a second `Tracer` object,
            of any kind.
        ell (float or array_like): Angular wavenumber(s) at which to evaluate
            the first dimension of the angular power spectrum covariance.
        tkka (:class:`~pyccl.tk3d.Tk3D` or None): 3D connected trispectrum.
        fsky (float): sky fraction.
        cltracer3 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind. If `None`, `cltracer1` will be used instead.
        cltracer4 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind. If `None`, `cltracer1` will be used instead.
        ell2 (float or array_like): Angular wavenumber(s) at which to evaluate
            the second dimension of the angular power spectrum covariance. If
            `None`, `ell` will be used instead.
        integration_method (string) : integration method to be used
            for the Limber integrals. Possibilities: 'qag_quad' (GSL's `qag`
            method backed up by `quad` when it fails) and 'spline' (the
            integrand is splined and then integrated analytically).

    Returns:
        float or array_like: 2D array containing the connected non-Gaussian             Angular power spectrum covariance             :math:`Cov_{\\rm cNG}(\\ell_1,\\ell_2)`, for the             four input tracers, as a function of :math:`\\ell_1` and             :math:`\\ell_2`. The ordering is such that             `out[i2, i1] = Cov(ell2[i2], ell[i1])`.
    """
    if integration_method not in ['qag_quad', 'spline']:
        raise ValueError('Integration method %s not supported' % integration_method)
    cosmo.compute_distances()
    cosmo_in = cosmo
    cosmo = cosmo.cosmo
    if isinstance(tkka, Tk3D):
        tsp = tkka.tsp
    else:
        raise ValueError('tkka must be a pyccl.Tk3D')
    status = 0
    (clt1, status) = lib.cl_tracer_collection_t_new(status)
    for t in cltracer1._trc:
        status = lib.add_cl_tracer_to_collection(clt1, t, status)
    (clt2, status) = lib.cl_tracer_collection_t_new(status)
    for t in cltracer2._trc:
        status = lib.add_cl_tracer_to_collection(clt2, t, status)
    if cltracer3 is None:
        clt3 = clt1
    else:
        (clt3, status) = lib.cl_tracer_collection_t_new(status)
        for t in cltracer3._trc:
            status = lib.add_cl_tracer_to_collection(clt3, t, status)
    if cltracer4 is None:
        clt4 = clt2
    else:
        (clt4, status) = lib.cl_tracer_collection_t_new(status)
        for t in cltracer4._trc:
            status = lib.add_cl_tracer_to_collection(clt4, t, status)
    ell1_use = np.atleast_1d(ell)
    if ell2 is None:
        ell2 = ell
    ell2_use = np.atleast_1d(ell2)
    (cov, status) = lib.angular_cov_vec(cosmo, clt1, clt2, clt3, clt4, tsp, ell1_use, ell2_use, integ_types[integration_method], 6, 1.0 / (4 * np.pi * fsky), ell1_use.size * ell2_use.size, status)
    cov = cov.reshape([ell2_use.size, ell1_use.size])
    if np.ndim(ell2) == 0:
        cov = np.squeeze(cov, axis=0)
    if np.ndim(ell) == 0:
        cov = np.squeeze(cov, axis=-1)
    lib.cl_tracer_collection_t_free(clt1)
    lib.cl_tracer_collection_t_free(clt2)
    if cltracer3 is not None:
        lib.cl_tracer_collection_t_free(clt3)
    if cltracer4 is not None:
        lib.cl_tracer_collection_t_free(clt4)
    check(status, cosmo=cosmo_in)
    return cov

def sigma2_B_disc(cosmo, a=None, fsky=1.0, p_of_k_a=None):
    """Returns the variance of the projected linear density field
    over a circular disc covering a sky fraction `fsky` as a function
    of scale factor. This is given by

    .. math::
        \\sigma^2_B(z) = \\int_0^\\infty \\frac{k\\,dk}{2\\pi}
            P_L(k,z)\\,\\left[\\frac{2J_1(k R(z))}{k R(z)}\\right]^2,

    where :math:`R(z)` is the corresponding radial aperture as a
    function of redshift. This quantity is used to compute the
    super-sample covariance.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): a Cosmology object.
        a_arr (float, array_like or `None`): an array of scale factor
            values at which to evaluate the projected variance. If
            `None`, a default sampling will be used.
        fsky (float): sky fraction.
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, str, or `None`): Linear
            power spectrum to use. Defaults to `None`, in which case the
            internal linear power spectrum from `cosmo` is used.

    Returns:
        float or array_like: values of the projected variance.
    """
    status = 0
    if a is None:
        na = lib.get_pk_spline_na(cosmo.cosmo)
        (a_arr, status) = lib.get_pk_spline_a(cosmo.cosmo, na, status)
        check(status, cosmo=cosmo)
    else:
        a_arr = np.atleast_1d(a)
        na = len(a_arr)
    chi_arr = comoving_radial_distance(cosmo, a_arr)
    R_arr = chi_arr * np.arccos(1 - 2 * fsky)
    psp = parse_pk2d(cosmo, p_of_k_a, is_linear=True)
    (s2B_arr, status) = lib.sigma2b_vec(cosmo.cosmo, a_arr, R_arr, psp, na, status)
    check(status, cosmo=cosmo)
    if a is None:
        return (a_arr, s2B_arr)
    elif np.ndim(a) == 0:
        return s2B_arr[0]
    else:
        return s2B_arr

def sigma2_B_from_mask(cosmo, a=None, mask_wl=None, p_of_k_a=None):
    """ Returns the variance of the projected linear density field, given the
        angular power spectrum of the footprint mask and scale factor.
        This is given by

    .. math::
        \\sigma^2_B(z) = \\frac{1}{\\chi^2{z}}\\sum_\\ell
            P_L(\\frac{\\ell+\\frac{1}{2}}{\\chi(z)},z)\\,
            (2\\ell+1)\\sum_m W^A_{\\ell m} {W^B}^*_{\\ell m},

    where :math:`W^A_{\\ell m}` and :math:`W^B_{\\ell m}` are the spherical
    harmonics decomposition of the footprint masks of fields `A` and `B`,
    normalized by their area.

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): a Cosmology object.
        a (float, array_like or `None`): an array of scale factor
            values at which to evaluate the projected variance.
        mask_wl (array_like): Array with the angular power spectrum of the
            masks. The power spectrum should be given at integer multipoles,
            starting at :math:`\\ell=0`. The power spectrum is normalized
            as :math:`(2\\ell+1)\\sum_m W^A_{\\ell m} {W^B}^*_{\\ell m}`. It is
            the responsibility of the user to the provide the mask power out to
            sufficiently high ell for their required precision.
        p_of_k_a (:class:`~pyccl.pk2d.Pk2D`, str, or `None`): Linear
            power spectrum to use. Defaults to `None`, in which case the
            internal linear power spectrum from `cosmo` is used.

    Returns:
        float or array_like: values of the projected variance.
    """
    if p_of_k_a is None:
        cosmo.compute_linear_power()
        p_of_k_a = cosmo.get_linear_power()
    a_arr = np.atleast_1d(a)
    chi = comoving_angular_distance(cosmo, a=a_arr)
    ell = np.arange(mask_wl.size)
    sigma2_B = np.zeros(a_arr.size)
    for i in range(sigma2_B.size):
        if 1 - a_arr[i] < 1e-06:
            sigma2_B[i] = sigma2_B_disc(cosmo=cosmo, a=a_arr[i], p_of_k_a=p_of_k_a)
        else:
            k = (ell + 0.5) / chi[i]
            pk = p_of_k_a.eval(k, a_arr[i], cosmo)
            sigma2_B[i] = np.sum(pk * mask_wl) / chi[i] ** 2
    if np.ndim(a) == 0:
        return sigma2_B[0]
    else:
        return sigma2_B

def angular_cl_cov_SSC(cosmo, cltracer1, cltracer2, ell, tkka, sigma2_B=None, fsky=1.0, cltracer3=None, cltracer4=None, ell2=None, integration_method='qag_quad'):
    """Calculate the super-sample contribution to the connected
    non-Gaussian covariance for a pair of power spectra
    :math:`C_{\\ell_1}^{ab}` and :math:`C_{\\ell_2}^{cd}`,
    between two pairs of tracers (:math:`(a,b)` and :math:`(c,d)`).

    Specifically, it computes:

    .. math::
        {\\rm Cov}_{\\rm cNG}(\\ell_1,\\ell_2)=
        \\int \\frac{d\\chi}{\\chi^6}
        \\tilde{\\Delta}^a_{\\ell_1}(\\chi)
        \\tilde{\\Delta}^b_{\\ell_1}(\\chi)
        \\tilde{\\Delta}^c_{\\ell_2}(\\chi)
        \\tilde{\\Delta}^d_{\\ell_2}(\\chi)\\,
        \\bar{T}_{abcd}\\left[\\frac{\\ell_1+1/2}{\\chi},
                              \\frac{\\ell_2+1/2}{\\chi}, a(\\chi)\\right]

    where :math:`\\Delta^x_\\ell(\\chi)` is the transfer function for tracer
    :math:`x` (see Eq. 39 in the CCL note), and
    :math:`\\bar{T}_{abcd}(k_1,k_2,a)` is the isotropized connected
    trispectrum of the four tracers (see the documentation of the
    :class:`~pyccl.tk3d.Tk3D` class for details).

    Args:
        cosmo (:class:`~pyccl.core.Cosmology`): A Cosmology object.
        cltracer1 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind.
        cltracer2 (:class:`~pyccl.tracers.Tracer`): a second `Tracer` object,
            of any kind.
        ell (float or array_like): Angular wavenumber(s) at which to evaluate
            the first dimension of the angular power spectrum covariance.
        tkka (:class:`~pyccl.tk3d.Tk3D` or None): 3D connected trispectrum.
        sigma2_B (tuple of arrays or `None`): A tuple of arrays
            (a, sigma2_B(a)) containing the variance of the projected matter
            overdensity over the footprint as a function of the scale factor.
            If `None`, a compact circular footprint will be assumed covering
            a sky fraction `fsky`.
        fsky (float): sky fraction.
        cltracer3 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind. If `None`, `cltracer1` will be used instead.
        cltracer4 (:class:`~pyccl.tracers.Tracer`): a `Tracer` object,
            of any kind. If `None`, `cltracer1` will be used instead.
        ell2 (float or array_like): Angular wavenumber(s) at which to evaluate
            the second dimension of the angular power spectrum covariance. If
            `None`, `ell` will be used instead.
        integration_method (string) : integration method to be used
            for the Limber integrals. Possibilities: 'qag_quad' (GSL's `qag`
            method backed up by `quad` when it fails) and 'spline' (the
            integrand is splined and then integrated analytically).

    Returns:
        float or array_like: 2D array containing the super-sample             Angular power spectrum covariance             :math:`Cov_{\\rm SSC}(\\ell_1,\\ell_2)`, for the             four input tracers, as a function of :math:`\\ell_1` and             :math:`\\ell_2`. The ordering is such that             `out[i2, i1] = Cov(ell2[i2], ell[i1])`.
    """
    if integration_method not in ['qag_quad', 'spline']:
        raise ValueError('Integration method %s not supported' % integration_method)
    cosmo.compute_distances()
    cosmo_in = cosmo
    cosmo = cosmo.cosmo
    if isinstance(tkka, Tk3D):
        tsp = tkka.tsp
    else:
        raise ValueError('tkka must be a pyccl.Tk3D')
    status = 0
    (clt1, status) = lib.cl_tracer_collection_t_new(status)
    for t in cltracer1._trc:
        status = lib.add_cl_tracer_to_collection(clt1, t, status)
    (clt2, status) = lib.cl_tracer_collection_t_new(status)
    for t in cltracer2._trc:
        status = lib.add_cl_tracer_to_collection(clt2, t, status)
    if cltracer3 is None:
        clt3 = clt1
    else:
        (clt3, status) = lib.cl_tracer_collection_t_new(status)
        for t in cltracer3._trc:
            status = lib.add_cl_tracer_to_collection(clt3, t, status)
    if cltracer4 is None:
        clt4 = clt2
    else:
        (clt4, status) = lib.cl_tracer_collection_t_new(status)
        for t in cltracer4._trc:
            status = lib.add_cl_tracer_to_collection(clt4, t, status)
    ell1_use = np.atleast_1d(ell)
    if ell2 is None:
        ell2 = ell
    ell2_use = np.atleast_1d(ell2)
    if sigma2_B is None:
        (a_arr, s2b_arr) = sigma2_B_disc(cosmo_in, fsky=fsky)
    else:
        (a_arr, s2b_arr) = _check_array_params(sigma2_B, 'sigma2_B')
    (cov, status) = lib.angular_cov_ssc_vec(cosmo, clt1, clt2, clt3, clt4, tsp, a_arr, s2b_arr, ell1_use, ell2_use, integ_types[integration_method], 4, 1.0, ell1_use.size * ell2_use.size, status)
    cov = cov.reshape([ell2_use.size, ell1_use.size])
    if np.ndim(ell2) == 0:
        cov = np.squeeze(cov, axis=0)
    if np.ndim(ell) == 0:
        cov = np.squeeze(cov, axis=-1)
    lib.cl_tracer_collection_t_free(clt1)
    lib.cl_tracer_collection_t_free(clt2)
    if cltracer3 is not None:
        lib.cl_tracer_collection_t_free(clt3)
    if cltracer4 is not None:
        lib.cl_tracer_collection_t_free(clt4)
    check(status, cosmo=cosmo_in)
    return cov
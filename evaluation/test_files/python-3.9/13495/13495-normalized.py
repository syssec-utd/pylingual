def _interp_dep_vector(wave, indep_vector):
    """Create new dependent variable vector."""
    dep_vector_is_int = wave.dep_vector.dtype.name.startswith('int')
    dep_vector_is_complex = wave.dep_vector.dtype.name.startswith('complex')
    if (wave.interp, wave.indep_scale) == ('CONTINUOUS', 'LOG'):
        wave_interp_func = scipy.interpolate.interp1d(np.log10(wave.indep_vector), wave.dep_vector)
        ret = wave_interp_func(np.log10(indep_vector))
    elif (wave.interp, wave.indep_scale) == ('CONTINUOUS', 'LINEAR'):
        dep_vector = wave.dep_vector.astype(np.float64) if not dep_vector_is_complex else wave.dep_vector
        wave_interp_func = scipy.interpolate.interp1d(wave.indep_vector, dep_vector)
        ret = wave_interp_func(indep_vector)
    else:
        wave_interp_func = scipy.interpolate.interp1d(wave.indep_vector, wave.dep_vector, kind='zero')
        ret = wave_interp_func(indep_vector)
        eq_comp = np.all(np.isclose(wave.indep_vector[-1], indep_vector[-1], FP_RTOL, FP_ATOL))
        if eq_comp:
            ret[-1] = wave.dep_vector[-1]
    round_ret = np.round(ret, 0)
    return round_ret.astype('int') if dep_vector_is_int and np.all(np.isclose(round_ret, ret, FP_RTOL, FP_ATOL)) else ret
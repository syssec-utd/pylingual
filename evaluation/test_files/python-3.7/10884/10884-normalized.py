def K80(mu=1.0, kappa=0.1, **kwargs):
    """
    Kimura 1980 model. Assumes equal concentrations across nucleotides, but
    allows different rates between transitions and transversions. The ratio
    of the transversion/transition rates is given by kappa parameter.
    For more info, see
    Kimura (1980),  J. Mol. Evol. 16 (2): 111–120. doi:10.1007/BF01731581.

    Current implementation of the model does not account for the gaps.

    Parameters
    -----------

     mu : float
        Overall substitution rate

     kappa : float
        Ratio of transversion/transition rates
    """
    num_chars = len(alphabets['nuc_nogap'])
    pi = np.ones(len(alphabets['nuc_nogap']), dtype=float) / len(alphabets['nuc_nogap'])
    W = _create_transversion_transition_W(kappa)
    gtr = GTR(alphabet=alphabets['nuc_nogap'])
    gtr.assign_rates(mu=mu, pi=pi, W=W)
    return gtr
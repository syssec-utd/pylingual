def HKY85(mu=1.0, pi=None, kappa=0.1, **kwargs):
    """
    Hasegawa, Kishino and Yano 1985 model. Allows different concentrations of the
    nucleotides (as in F81) + distinguishes between transition/transversionsubstitutions
    (similar to K80). Link:
    Hasegawa, Kishino, Yano (1985), J. Mol. Evol. 22 (2): 160–174. doi:10.1007/BF02101694

    Current implementation of the model does not account for the gaps

    Parameters
    -----------


     mu : float
        Substitution rate

     pi : numpy.array
        Nucleotide concentrations

     kappa : float
        Ratio of transversion/transition substitution rates

    """
    if pi is None:
        pi = 0.25 * np.ones(4, dtype=float)
    num_chars = len(alphabets['nuc_nogap'])
    if num_chars != pi.shape[0]:
        pi = np.ones((num_chars,), dtype=float)
        print('GTR: Warning!The number of the characters in the alphabet does not match the shape of the vector of equilibrium frequencies Pi -- assuming equal frequencies for all states.')
    W = _create_transversion_transition_W(kappa)
    pi /= pi.sum()
    gtr = GTR(alphabet=alphabets['nuc_nogap'])
    gtr.assign_rates(mu=mu, pi=pi, W=W)
    return gtr
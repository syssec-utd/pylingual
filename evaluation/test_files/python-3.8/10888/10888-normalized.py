def TN93(mu=1.0, kappa1=1.0, kappa2=1.0, pi=None, **kwargs):
    """
    Tamura and Nei 1993. The model distinguishes between the two different types of
    transition: (A <-> G) is allowed to have a different rate to (C<->T).
    Transversions have the same rate. The frequencies of the nucleotides are allowed
    to be different. Link:
    Tamura, Nei (1993), MolBiol Evol. 10 (3): 512–526. DOI:10.1093/oxfordjournals.molbev.a040023

    Parameters
    -----------

     mu : float
        Substitution rate

     kappa1 : float
        relative A<-->C, A<-->T, T<-->G and G<-->C rates

     kappa2 : float
        relative C<-->T rate

    Note
    ----

     Rate of A<-->G substitution is set to one. All other rates (kappa1, kappa2)
    are specified relative to this rate

    """
    if pi is None:
        pi = 0.25 * np.ones(4, dtype=float)
    W = np.ones((4, 4))
    W = np.array([[1, kappa1, 1, kappa1], [kappa1, 1, kappa1, kappa2], [1, kappa1, 1, kappa1], [kappa1, kappa2, kappa1, 1]], dtype=float)
    pi /= pi.sum()
    num_chars = len(alphabets['nuc_nogap'])
    if num_chars != pi.shape[0]:
        pi = np.ones((num_chars,), dtype=float)
        print('GTR: Warning!The number of the characters in the alphabet does not match the shape of the vector of equilibrium frequencies Pi -- assuming equal frequencies for all states.')
    gtr = GTR(alphabet=alphabets['nuc'])
    gtr.assign_rates(mu=mu, pi=pi, W=W)
    return gtr
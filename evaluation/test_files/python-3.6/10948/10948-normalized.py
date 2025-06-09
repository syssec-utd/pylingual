def random(cls, mu=1.0, alphabet='nuc'):
    """
        Creates a random GTR model

        Parameters
        ----------

         mu : float
            Substitution rate

         alphabet : str
            Alphabet name (should be standard: 'nuc', 'nuc_gap', 'aa', 'aa_gap')


        """
    alphabet = alphabets[alphabet]
    gtr = cls(alphabet)
    n = gtr.alphabet.shape[0]
    pi = 1.0 * np.random.randint(0, 100, size=n)
    W = 1.0 * np.random.randint(0, 100, size=(n, n))
    gtr.assign_rates(mu=mu, pi=pi, W=W)
    return gtr
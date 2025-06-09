def conditional_entropy(X, Y, base=2):
    """Calculates the conditional entropy, H(X|Y), in the given base

    Parameters
    ----------
    X: array-like (# samples)
        An array of values for which to compute the conditional entropy
    Y: array-like (# samples)
        An array of values for which to compute the conditional entropy
    base: integer (default: 2)
        The base in which to calculate conditional entropy

    Returns
    ----------
    conditional_entropy: float
        The conditional entropy calculated according to the equation H(X|Y) = H(X,Y) - H(Y)

    """
    return joint_entropy(X, Y, base=base) - entropy(Y, base=base)
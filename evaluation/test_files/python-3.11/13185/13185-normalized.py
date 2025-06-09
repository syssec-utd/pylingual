def three_way_information_gain(W, X, Y, Z, base=2):
    """Calculates the three-way information gain between three variables, I(W;X;Y;Z), in the given base

    IG(W;X;Y;Z) indicates the information gained about variable Z by the joint variable W_X_Y, after removing
    the information that W, X, and Y have about Z individually and jointly in pairs. Thus, 3-way information gain
    measures the synergistic predictive value of variables W, X, and Y about variable Z.

    Parameters
    ----------
    W: array-like (# samples)
        An array of values for which to compute the 3-way information gain
    X: array-like (# samples)
        An array of values for which to compute the 3-way information gain
    Y: array-like (# samples)
        An array of values for which to compute the 3-way information gain
    Z: array-like (# samples)
        An array of outcome values for which to compute the 3-way information gain
    base: integer (default: 2)
        The base in which to calculate 3-way information

    Returns
    ----------
    mutual_information: float
        The information gain calculated according to the equation:
            IG(W;X;Y;Z) = I(W,X,Y;Z) - IG(W;X;Z) - IG(W;Y;Z) - IG(X;Y;Z) - I(W;Z) - I(X;Z) - I(Y;Z)

    """
    W_X_Y = ['{}{}{}'.format(w, x, y) for w, x, y in zip(W, X, Y)]
    return mutual_information(W_X_Y, Z, base=base) - two_way_information_gain(W, X, Z, base=base) - two_way_information_gain(W, Y, Z, base=base) - two_way_information_gain(X, Y, Z, base=base) - mutual_information(W, Z, base=base) - mutual_information(X, Z, base=base) - mutual_information(Y, Z, base=base)
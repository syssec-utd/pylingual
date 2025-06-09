def discrete_alpha_mle(data, xmin):
    """
    Equation B.17 of Clauset et al 2009

    The Maximum Likelihood Estimator of the "scaling parameter" alpha in the
    discrete case is similar to that in the continuous case
    """
    gexmin = data >= xmin
    nn = gexmin.sum()
    if nn < 2:
        return 0
    xx = data[gexmin]
    alpha = 1.0 + float(nn) * sum(log(xx / (float(xmin) - 0.5))) ** (-1)
    return alpha
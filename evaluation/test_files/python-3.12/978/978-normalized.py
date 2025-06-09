def logistic_regression(features):
    """Bayesian logistic regression, which returns labels given features."""
    coeffs = ed.MultivariateNormalDiag(loc=tf.zeros(features.shape[1]), name='coeffs')
    labels = ed.Bernoulli(logits=tf.tensordot(features, coeffs, [[1], [0]]), name='labels')
    return labels
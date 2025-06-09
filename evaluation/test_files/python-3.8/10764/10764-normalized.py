def compute_bic(self, D, means, labels, K, R):
    """Computes the Bayesian Information Criterion."""
    D = vq.whiten(D)
    Rn = D.shape[0]
    M = D.shape[1]
    if R == K:
        return 1
    mle_var = 0
    for k in range(len(means)):
        X = D[np.argwhere(labels == k)]
        X = X.reshape((X.shape[0], X.shape[-1]))
        for x in X:
            mle_var += distance.euclidean(x, means[k])
    mle_var /= float(R - K)
    l_D = -Rn / 2.0 * np.log(2 * np.pi) - Rn * M / 2.0 * np.log(mle_var) - (Rn - K) / 2.0 + Rn * np.log(Rn) - Rn * np.log(R)
    p = K - 1 + M * K + mle_var
    return l_D - p / 2.0 * np.log(R)
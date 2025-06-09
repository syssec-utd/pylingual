def compute_nc(X, G):
    """Computes the novelty curve from the self-similarity matrix X and
        the gaussian kernel G."""
    N = X.shape[0]
    M = G.shape[0]
    nc = np.zeros(N)
    for i in range(M // 2, N - M // 2 + 1):
        nc[i] = np.sum(X[i - M // 2:i + M // 2, i - M // 2:i + M // 2] * G)
    nc += nc.min()
    nc /= nc.max()
    return nc
def fit(self, Z):
    """Learn the idf vector (global term weights)

        Parameters
        ----------
        Z : ArrayRDD or DictRDD containing (sparse matrices|ndarray)
            a matrix of term/token counts

        Returns
        -------
        self : TfidfVectorizer
        """
    X = Z[:, 'X'] if isinstance(Z, DictRDD) else Z
    check_rdd(X, (sp.spmatrix, np.ndarray))

    def mapper(X, use_idf=self.use_idf):
        if not sp.issparse(X):
            X = sp.csc_matrix(X)
        if use_idf:
            return _document_frequency(X)
    if self.use_idf:
        n_samples, n_features = X.shape
        df = X.map(mapper).treeReduce(operator.add)
        df += int(self.smooth_idf)
        n_samples += int(self.smooth_idf)
        idf = np.log(float(n_samples) / df) + 1.0
        self._idf_diag = sp.spdiags(idf, diags=0, m=n_features, n=n_features)
    return self
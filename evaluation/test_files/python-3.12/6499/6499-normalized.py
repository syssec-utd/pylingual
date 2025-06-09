def fit(self, Z, **fit_params):
    """TODO: rewrite docstring
        Fit all transformers using X.
        Parameters
        ----------
        X : array-like or sparse matrix, shape (n_samples, n_features)
            Input data, used to fit transformers.
        """
    fit_params_steps = dict(((step, {}) for step, _ in self.transformer_list))
    for pname, pval in six.iteritems(fit_params):
        step, param = pname.split('__', 1)
        fit_params_steps[step][param] = pval
    transformers = Parallel(n_jobs=self.n_jobs, backend='threading')((delayed(_fit_one_transformer)(trans, Z, **fit_params_steps[name]) for name, trans in self.transformer_list))
    self._update_transformer_list(transformers)
    return self
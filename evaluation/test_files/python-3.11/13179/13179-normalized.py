def score(self, features, targets):
    """Estimates the quality of the ContinuousMDR model using a t-statistic.

        Parameters
        ----------
        features: array-like {n_samples, n_features}
            Feature matrix to predict from
        targets: array-like {n_samples}
            List of true target values

        Returns
        -------
        quality_score: float
            The estimated quality of the Continuous MDR model

        """
    if self.feature_map is None:
        raise ValueError('The Continuous MDR model must be fit before score() can be called.')
    group_0_trait_values = []
    group_1_trait_values = []
    for feature_instance in self.feature_map:
        if self.feature_map[feature_instance] == 0:
            group_0_trait_values.extend(self.mdr_matrix_values[feature_instance])
        else:
            group_1_trait_values.extend(self.mdr_matrix_values[feature_instance])
    return abs(ttest_ind(group_0_trait_values, group_1_trait_values).statistic)
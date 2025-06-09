def fit_transform(self, features, class_labels):
    """Convenience function that fits the provided data then constructs a new feature from the provided features.

        Parameters
        ----------
        features: array-like {n_samples, n_features}
            Feature matrix
        class_labels: array-like {n_samples}
            List of true class labels

        Returns
        ----------
        array-like: {n_samples, 1}
            Constructed features from the provided feature matrix

        """
    self.fit(features, class_labels)
    return self.transform(features)
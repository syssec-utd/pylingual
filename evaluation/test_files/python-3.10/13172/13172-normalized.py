def fit(self, features, class_labels):
    """Constructs the MDR feature map from the provided training data.

        Parameters
        ----------
        features: array-like {n_samples, n_features}
            Feature matrix
        class_labels: array-like {n_samples}
            List of true class labels

        Returns
        -------
        self: A copy of the fitted model

        """
    unique_labels = sorted(np.unique(class_labels))
    if len(unique_labels) != 2:
        raise ValueError('MDR only supports binary endpoints.')
    self.class_count_matrix = defaultdict(lambda : defaultdict(int))
    for row_i in range(features.shape[0]):
        feature_instance = tuple(features[row_i])
        self.class_count_matrix[feature_instance][class_labels[row_i]] += 1
    self.class_count_matrix = dict(self.class_count_matrix)
    overall_class_fraction = float(sum(class_labels == unique_labels[0])) / class_labels.size
    self.feature_map = {}
    for feature_instance in self.class_count_matrix:
        counts = self.class_count_matrix[feature_instance]
        fraction = float(counts[unique_labels[0]]) / np.sum(list(counts.values()))
        if fraction > overall_class_fraction:
            self.feature_map[feature_instance] = unique_labels[0]
        elif fraction == overall_class_fraction:
            self.feature_map[feature_instance] = self.tie_break
        else:
            self.feature_map[feature_instance] = unique_labels[1]
    return self
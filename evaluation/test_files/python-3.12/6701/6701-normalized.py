def add_features(self, features, append=True, merge='outer', duplicates='ignore', min_studies=0.0, threshold=0.001):
    """ Construct a new FeatureTable from file.

        Args:
            features: Feature data to add. Can be:
                (a) A text file containing the feature data, where each row is
                a study in the database, with features in columns. The first
                column must contain the IDs of the studies to match up with the
                image data.
                (b) A pandas DataFrame, where studies are in rows, features are
                in columns, and the index provides the study IDs.
            append (bool): If True, adds new features to existing ones
                incrementally. If False, replaces old features.
            merge, duplicates, min_studies, threshold: Additional arguments
                passed to FeatureTable.add_features().
         """
    if not append or not hasattr(self, 'feature_table'):
        self.feature_table = FeatureTable(self)
    self.feature_table.add_features(features, merge=merge, duplicates=duplicates, min_studies=min_studies, threshold=threshold)
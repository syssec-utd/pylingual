def add_features(self, features, merge='outer', duplicates='ignore', min_studies=0, threshold=0.0001):
    """ Add new features to FeatureTable.
        Args:
            features (str, DataFrame): A filename to load data from, or a
                pandas DataFrame. In either case, studies are in rows and
                features are in columns. Values in cells reflect the weight of
                the intersecting feature for the intersecting study. Feature
                names and study IDs should be included as the first column
                and first row, respectively.
            merge (str): The merge strategy to use when merging new features
                with old. This is passed to pandas.merge, so can be 'left',
                'right', 'outer', or 'inner'. Defaults to outer (i.e., all data
                in both new and old will be kept, and missing values will be
                assigned zeros.)
            duplicates (str): string indicating how to handle features whose
                name matches an existing feature. Valid options:
                    'ignore' (default): ignores the new feature, keeps old data
                    'replace': replace the old feature's data with the new data
                    'merge': keeps both features, renaming them so they're
                        different
            min_studies (int): minimum number of studies that pass threshold in
                order to add feature.
            threshold (float): minimum frequency threshold each study must
                exceed in order to count towards min_studies.
        """
    if isinstance(features, string_types):
        if not os.path.exists(features):
            raise ValueError('%s cannot be found.' % features)
        try:
            features = pd.read_csv(features, sep='\t', index_col=0)
        except Exception as e:
            logger.error('%s cannot be parsed: %s' % (features, e))
    if min_studies:
        valid = np.where((features.values >= threshold).sum(0) >= min_studies)[0]
        features = features.iloc[:, valid]
    n_studies = len(features)
    n_common_ids = len(set(features.index) & set(self.dataset.image_table.ids))
    if float(n_common_ids) / n_studies < 0.01:
        msg = 'Only %d' % n_common_ids if n_common_ids else 'None of the'
        logger.warning(msg + " studies in the feature file matched studies currently the Dataset. The most likely cause for this is that you're pairing a newer feature set with an older, incompatible database file. You may want to try regenerating the Dataset instance from a newer database file that uses PMIDs rather than doi's as the study identifiers in the first column.")
    old_data = self.data.to_dense()
    common_features = list(set(old_data.columns) & set(features.columns))
    if duplicates == 'ignore':
        features = features.drop(common_features, axis=1)
    elif duplicates == 'replace':
        old_data = old_data.drop(common_features, axis=1)
    data = old_data.merge(features, how=merge, left_index=True, right_index=True)
    self.data = data.fillna(0.0).to_sparse()
def processFlat(self):
    """Main process.
        Returns
        -------
        est_idx : np.array(N)
            Estimated indeces for the segment boundaries in frames.
        est_labels : np.array(N-1)
            Estimated labels for the segments.
        """
    F = self._preprocess()
    F = U.normalize(F, norm_type=self.config['label_norm_feats'], floor=self.config['label_norm_floor'], min_db=self.config['label_norm_min_db'])
    est_labels = compute_similarity(F, self.in_bound_idxs, dirichlet=self.config['dirichlet'], xmeans=self.config['xmeans'], k=self.config['k'], offset=self.config['2dfmc_offset'])
    (self.in_bound_idxs, est_labels) = self._postprocess(self.in_bound_idxs, est_labels)
    return (self.in_bound_idxs, est_labels)
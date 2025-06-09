def _sdf_to_csr(self):
    """ Convert FeatureTable to SciPy CSR matrix. """
    data = self.data.to_dense()
    self.data = {'columns': list(data.columns), 'index': list(data.index), 'values': sparse.csr_matrix(data.values)}
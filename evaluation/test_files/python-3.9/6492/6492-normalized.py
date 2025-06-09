def to_scikit(self):
    """
        Convert to equivalent StandardScaler
        """
    scaler = StandardScaler(with_mean=self.with_mean, with_std=self.with_std, copy=self.copy)
    scaler.__dict__ = self.__dict__
    return scaler
def expQsdsds(self, s):
    """
        Returns
        -------
        Qtdtdt :  Returns V_{ij} \\lambda_j^2 e^{\\lambda_j s**2} V^{-1}_{jk}
                This is the second derivative of the branch probability wrt time
        """
    t = s ** 2
    elt = self._exp_lt(t)
    lambda_eLambdaT = np.diag(elt * (4.0 * t * self.eigenvals ** 2 + 2.0 * self.eigenvals))
    Qsdsds = self.v.dot(lambda_eLambdaT.dot(self.v_inv))
    return Qsdsds
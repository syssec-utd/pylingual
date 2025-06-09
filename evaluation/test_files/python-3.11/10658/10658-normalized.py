def factorize(self):
    """ Factorize s.t. CUR = data

            Updated Values
            --------------
            .C : updated values for C.
            .U : updated values for U.
            .R : updated values for R.
        """
    [prow, pcol] = self.sample_probability()
    self._rid = self.sample(self._rrank, prow)
    self._cid = self.sample(self._crank, pcol)
    self._cmdinit()
    self.computeUCR()
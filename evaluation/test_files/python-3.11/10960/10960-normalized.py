def evolve(self, profile, t, return_log=False):
    """
        Compute the probability of the sequence state of the child
        at time t later, given the parent profile.

        Parameters
        ----------

         profile : numpy.array
            Sequence profile. Shape = (L, a),
            where L - sequence length, a - alphabet size.

         t : double
            Time to propagate

         return_log: bool
            If True, return log-probability

        Returns
        -------

         res : np.array
            Profile of the sequence after time t in the future.
            Shape = (L, a), where L - sequence length, a - alphabet size.

        """
    Qt = self.expQt(t).T
    res = profile.dot(Qt)
    return np.log(res) if return_log else res
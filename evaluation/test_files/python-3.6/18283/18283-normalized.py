def param_values(self, pnames=None):
    """ Return an array with the parameter values

        Parameters
        ----------

        pname : list or None
           If a list, get the values of the `Parameter` objects with those names

           If none, get all values of all the `Parameter` objects

        Returns
        -------

        values : `np.array`
            Parameter values

        """
    l = self.get_params(pnames)
    v = [p.value for p in l]
    return np.array(v)
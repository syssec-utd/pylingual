def remove(self, name=None, setn=None):
    """
        Remove filter.

        Parameters
        ----------
        name : str
            name of the filter to remove
        setn : int or True
            int: number of set to remove
            True: remove all filters in set that 'name' belongs to

        Returns
        -------
        None
        """
    if isinstance(name, int):
        name = self.index[name]
    if setn is not None:
        name = self.sets[setn]
        del self.sets[setn]
    elif isinstance(name, (int, str)):
        name = [name]
    if setn is True:
        for n in name:
            for (k, v) in self.sets.items():
                if n in v:
                    name.append([m for m in v if m != n])
    for n in name:
        for (k, v) in self.sets.items():
            if n in v:
                self.sets[k] = [m for m in v if n != m]
        del self.components[n]
        del self.info[n]
        del self.params[n]
        del self.keys[n]
        for a in self.analytes:
            del self.switches[a][n]
        return
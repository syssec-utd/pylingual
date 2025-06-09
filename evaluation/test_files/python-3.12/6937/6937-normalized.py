def get(self):
    """
        Return the hash of the given file
        """
    result = {}
    if self.algorithm in self.valid_algorithms:
        if self.algorithm == 'all':
            del self.valid_algorithms[0]
            for algo in self.valid_algorithms:
                if self.path and path.isfile(self.path):
                    result[algo] = self._hash_file(algo)
                elif self.data:
                    result[algo] = self._hash_data(algo)
                else:
                    return None
        elif self.path and path.isfile(self.path):
            result[self.algorithm] = self._hash_file(self.algorithm)
        elif self.data:
            result[self.algorithm] = self._hash_data(self.algorithm)
        else:
            return None
    else:
        return None
    if self.algorithm != 'all' and self.only_hash:
        return result[self.algorithm]
    return result
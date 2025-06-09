def setBatchSize(self, val):
    """
        Sets the value of :py:attr:`batchSize`.
        """
    self._paramMap[self.batchSize] = val
    pythonBigDL_method_name = 'setBatchSize' + self.__class__.__name__
    callBigDlFunc(self.bigdl_type, pythonBigDL_method_name, self.value, val)
    return self
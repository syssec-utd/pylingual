def transform(self, transformer, bigdl_type='float'):
    """
        transformImageFrame
        """
    self.value = callBigDlFunc(bigdl_type, 'transformImageFrame', transformer, self.value)
    return self
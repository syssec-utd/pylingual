def read(self):
    """
        Load the metrics file from the given path
        """
    f = open(self.path, 'r')
    self.manifest_json = f.read()
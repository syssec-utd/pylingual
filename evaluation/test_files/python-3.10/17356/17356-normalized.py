def read(self):
    """Read the chunks data"""
    self.__fileobj.seek(self.data_offset)
    self.data = self.__fileobj.read(self.data_size)
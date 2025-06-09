def read_data(self, f_start=None, f_stop=None, t_start=None, t_stop=None):
    """ Reads data selection if small enough.
        """
    self.container.read_data(f_start=f_start, f_stop=f_stop, t_start=t_start, t_stop=t_stop)
    self.__load_data()
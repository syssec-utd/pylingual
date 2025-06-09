def write_to(self, out):
    """ Write the raw header content to the out stream

        Parameters:
        ----------
        out : {file object}
            The output stream
        """
    out.write(bytes(self.header))
    out.write(self.record_data)
def x_fit(self, test_length):
    """ Test to see if the line can has enough space for the given length. """
    if self.x + test_length >= self.xmax:
        return False
    else:
        return True
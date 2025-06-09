def print_stats(self):
    """ Compute some basic stats on the next block of data """
    header, data = self.read_next_data_block()
    data = data.view('float32')
    print('AVG: %2.3f' % data.mean())
    print('STD: %2.3f' % data.std())
    print('MAX: %2.3f' % data.max())
    print('MIN: %2.3f' % data.min())
    import pylab as plt
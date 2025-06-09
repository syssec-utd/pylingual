def calc_n_coarse_chan(self, chan_bw=None):
    """ This makes an attempt to calculate the number of coarse channels in a given file.

            Note:
                This is unlikely to work on non-Breakthrough Listen data, as a-priori knowledge of
                the digitizer system is required.

        """
    nchans = int(self.header[b'nchans'])
    if chan_bw is not None:
        bandwidth = abs(self.f_stop - self.f_start)
        n_coarse_chan = int(bandwidth / chan_bw)
        return n_coarse_chan
    elif nchans >= 2 ** 20:
        if nchans % 2 ** 20 == 0:
            n_coarse_chan = nchans // 2 ** 20
            return n_coarse_chan
        elif self.header[b'telescope_id'] == 6:
            coarse_chan_bw = 2.9296875
            bandwidth = abs(self.f_stop - self.f_start)
            n_coarse_chan = int(bandwidth / coarse_chan_bw)
            return n_coarse_chan
        else:
            logger.warning("Couldn't figure out n_coarse_chan")
    elif self.header[b'telescope_id'] == 6 and nchans < 2 ** 20:
        coarse_chan_bw = 2.9296875
        bandwidth = abs(self.f_stop - self.f_start)
        n_coarse_chan = int(bandwidth / coarse_chan_bw)
        return n_coarse_chan
    else:
        logger.warning('This function currently only works for hires BL Parkes or GBT data.')
def is_changed(self, item):
    """
        Find out if this item has been modified since last

        :param item: A key
        :return: True/False
        """
    fname = os.path.join(self.fdir, item)
    if os.path.isfile(fname):
        mtime = self.get_mtime(fname)
        try:
            _ftime = self.fmtime[item]
        except KeyError:
            self.fmtime[item] = mtime
            return True
        if mtime > _ftime:
            self.fmtime[item] = mtime
            return True
        else:
            return False
    else:
        logger.error('Could not access {}'.format(fname))
        raise KeyError(item)
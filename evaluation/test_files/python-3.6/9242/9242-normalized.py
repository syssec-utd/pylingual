def skip(self, n_batches, n_epochs=0):
    """
        Skip N batches in the training.
        """
    logging.info('skip %d epochs and %d batches' % (n_epochs, n_batches))
    self._skip_batches = n_batches
    self._skip_epochs = n_epochs
def as_tryte_string(self):
    """
        Returns a TryteString representation of the transaction.
        """
    if not self.bundle_hash:
        raise with_context(exc=RuntimeError('Cannot get TryteString representation of {cls} instance without a bundle hash; call ``bundle.finalize()`` first (``exc.context`` has more info).'.format(cls=type(self).__name__)), context={'transaction': self})
    return super(ProposedTransaction, self).as_tryte_string()
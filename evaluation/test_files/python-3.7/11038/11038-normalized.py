def range(self, chromosome, start, stop, exact=False):
    """
        Shortcut to do range filters on genomic datasets.
        """
    return self._clone(filters=[GenomicFilter(chromosome, start, stop, exact)])
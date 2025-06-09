def get_coding_intervals(self, build='37', genes=None):
    """Return a dictionary with chromosomes as keys and interval trees as values

        Each interval represents a coding region of overlapping genes.

        Args:
            build(str): The genome build
            genes(iterable(scout.models.HgncGene)):

        Returns:
            intervals(dict): A dictionary with chromosomes as keys and overlapping genomic intervals as values
        """
    intervals = {}
    if not genes:
        genes = self.all_genes(build=build)
    LOG.info('Building interval trees...')
    for i, hgnc_obj in enumerate(genes):
        chrom = hgnc_obj['chromosome']
        start = max(hgnc_obj['start'] - 5000, 1)
        end = hgnc_obj['end'] + 5000
        if chrom not in intervals:
            intervals[chrom] = intervaltree.IntervalTree()
            intervals[chrom].addi(start, end, i)
            continue
        res = intervals[chrom].search(start, end)
        if not res:
            intervals[chrom].addi(start, end, i)
            continue
        for interval in res:
            if interval.begin < start:
                start = interval.begin
            if interval.end > end:
                end = interval.end
            intervals[chrom].remove(interval)
        intervals[chrom].addi(start, end, i)
    return intervals
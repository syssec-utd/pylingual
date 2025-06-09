def next(self):
    """
        Expands multiple alleles into one record each
        using an internal buffer (_next).
        """

    def _alt(alt):
        """Parses the VCF row ALT object."""
        if not alt:
            return '.'
        else:
            return str(alt)
    if not self._next:
        row = next(self.reader)
        alternate_alleles = list(map(_alt, row.ALT))
        for allele in alternate_alleles:
            self._next.append(self.row_to_dict(row, allele=allele, alternate_alleles=alternate_alleles))
        self._line_number += 1
    return self._next.pop()
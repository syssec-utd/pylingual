def concat(*seqs) -> ISeq:
    """Concatenate the sequences given by seqs into a single ISeq."""
    allseqs = lseq.sequence(itertools.chain(*filter(None, map(to_seq, seqs))))
    if allseqs is None:
        return lseq.EMPTY
    return allseqs
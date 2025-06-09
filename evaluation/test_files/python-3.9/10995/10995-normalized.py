def timetree_likelihood(self):
    """
        Return the likelihood of the data given the current branch length in the tree
        """
    LH = 0
    for node in self.tree.find_clades(order='preorder'):
        if node.up is None:
            continue
        LH -= node.branch_length_interpolator(node.branch_length)
    if self.aln:
        LH += self.gtr.sequence_logLH(self.tree.root.cseq, pattern_multiplicity=self.multiplicity)
    return LH
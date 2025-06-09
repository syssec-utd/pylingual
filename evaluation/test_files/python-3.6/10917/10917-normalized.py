def get_mutations(self, node, keep_var_ambigs=False):
    """
        Get the mutations on a tree branch. Take compressed sequences from both sides
        of the branch (attached to the node), compute mutations between them, and
        expand these mutations to the positions in the real sequences.

        Parameters
        ----------
        node : PhyloTree.Clade
           Tree node, which is the child node attached to the branch.

        keep_var_ambigs : boolean
           If true, generates mutations based on the *original* compressed sequence, which
           may include ambiguities. Note sites that only have 1 unambiguous base and ambiguous
           bases ("AAAAANN") are stripped of ambiguous bases *before* compression, so ambiguous
           bases will **not** be preserved.

        Returns
        -------
        muts : list
          List of mutations. Each mutation is represented as tuple of
          :code:`(parent_state, position, child_state)`.
        """
    node_seq = node.cseq
    if keep_var_ambigs and hasattr(node, 'original_cseq') and node.is_terminal():
        node_seq = node.original_cseq
    muts = []
    diff_pos = np.where(node.up.cseq != node_seq)[0]
    for p in diff_pos:
        anc = node.up.cseq[p]
        der = node_seq[p]
        muts.extend([(anc, pos, der) for pos in self.reduced_to_full_sequence_map[p]])
    return sorted(muts, key=lambda x: x[1])
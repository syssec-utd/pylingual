def get_tree_dict(self, keep_var_ambigs=False):
    """
        For VCF-based objects, returns a nested dict with all the information required to
        reconstruct sequences for all nodes (terminal and internal).

        Parameters
        ----------
        keep_var_ambigs : boolean
            If true, generates dict sequences based on the *original* compressed sequences, which
            may include ambiguities. Note sites that only have 1 unambiguous base and ambiguous
            bases ("AAAAANN") are stripped of ambiguous bases *before* compression, so ambiguous
            bases at this sites will *not* be preserved.


        Returns
        -------
        tree_dict : dict
           Format: ::

               {
               'reference':'AGCTCGA...A',
               'sequences': { 'seq1':{4:'A', 7:'-'}, 'seq2':{100:'C'} },
               'positions': [1,4,7,10,100...],
               'inferred_const_sites': [7,100....]
               }

           reference: str
               The reference sequence to which the variable sites are mapped
           sequences: nested dict
               A dict for each sequence with the position and alternative call for each variant
           positions: list
               All variable positions in the alignment
           inferred_cost_sites: list
               *(optional)* Positions that were constant except ambiguous bases, which were
               converted into constant sites by TreeAnc (ex: 'AAAN' -> 'AAAA')

        Raises
        ------
        TypeError
            Description

        """
    if self.is_vcf:
        tree_dict = {}
        tree_dict['reference'] = self.ref
        tree_dict['positions'] = self.nonref_positions
        tree_aln = {}
        for n in self.tree.find_clades():
            if hasattr(n, 'sequence'):
                if keep_var_ambigs:
                    tree_aln[n.name] = self.dict_sequence(n, keep_var_ambigs)
                else:
                    tree_aln[n.name] = n.sequence
        tree_dict['sequences'] = tree_aln
        if len(self.inferred_const_sites) != 0:
            tree_dict['inferred_const_sites'] = self.inferred_const_sites
        return tree_dict
    else:
        raise TypeError('A dict can only be returned for trees created with VCF-input!')
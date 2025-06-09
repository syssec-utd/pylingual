def id_transcripts_by_gene(self, build='37'):
    """Return a dictionary with hgnc_id as keys and a set of id transcripts as value
        
        Args:
            build(str)
        
        Returns:
            hgnc_id_transcripts(dict)
        """
    hgnc_id_transcripts = {}
    LOG.info('Fetching all id transcripts')
    for gene_obj in self.hgnc_collection.find({'build': build}):
        hgnc_id = gene_obj['hgnc_id']
        id_transcripts = self.get_id_transcripts(hgnc_id=hgnc_id, build=build)
        hgnc_id_transcripts[hgnc_id] = id_transcripts
    return hgnc_id_transcripts
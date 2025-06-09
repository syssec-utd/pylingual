def all_genes(self, build='37'):
    """Fetch all hgnc genes

            Returns:
                result()
        """
    LOG.info('Fetching all genes')
    return self.hgnc_collection.find({'build': build}).sort('chromosome', 1)
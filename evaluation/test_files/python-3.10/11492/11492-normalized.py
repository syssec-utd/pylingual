def get_hgnc_id(gene_info, adapter):
    """Get the hgnc id for a gene

        The proprity order will be
        1. if there is a hgnc id this one will be choosen
        2. if the hgnc symbol matches a genes proper hgnc symbol
        3. if the symbol ony matches aliases on several genes one will be
           choosen at random

        Args:
            gene_info(dict)
            adapter

        Returns:
            true_id(int)
    """
    hgnc_id = gene_info.get('hgnc_id')
    hgnc_symbol = gene_info.get('hgnc_symbol')
    true_id = None
    if hgnc_id:
        true_id = int(hgnc_id)
    else:
        gene_result = adapter.hgnc_genes(hgnc_symbol)
        if gene_result.count() == 0:
            raise Exception('No gene could be found for {}'.format(hgnc_symbol))
        for gene in gene_result:
            if hgnc_symbol.upper() == gene.hgnc_symbol.upper():
                true_id = gene.hgnc_id
        if not gene_info['hgnc_id']:
            true_id = gene.hgnc_id
    return true_id
def parse_hpo_to_genes(hpo_lines):
    """Parse the map from hpo term to hgnc symbol
    
    Args:
        lines(iterable(str)):
    
    Yields:
        hpo_to_gene(dict): A dictionary with information on how a term map to a hgnc symbol
    """
    for line in hpo_lines:
        if line.startswith('#') or len(line) < 1:
            continue
        line = line.rstrip().split('\t')
        hpo_id = line[0]
        hgnc_symbol = line[3]
        yield {'hpo_id': hpo_id, 'hgnc_symbol': hgnc_symbol}
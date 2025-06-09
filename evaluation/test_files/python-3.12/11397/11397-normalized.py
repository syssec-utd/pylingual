def update_panel(store, panel_name, csv_lines, option):
    """Update an existing gene panel with genes.

    Args:
        store(scout.adapter.MongoAdapter)
        panel_name(str)
        csv_lines(iterable(str)): Stream with genes
        option(str): 'add' or 'replace'

    Returns:
        panel_obj(dict)
    """
    new_genes = []
    panel_obj = store.gene_panel(panel_name)
    if panel_obj is None:
        return None
    try:
        new_genes = parse_genes(csv_lines)
    except SyntaxError as error:
        flash(error.args[0], 'danger')
        return None
    if option == 'replace':
        for gene in panel_obj['genes']:
            gene['hgnc_symbol'] = gene['symbol']
            store.add_pending(panel_obj, gene, action='delete', info=None)
    for new_gene in new_genes:
        if not new_gene['hgnc_id']:
            flash('gene missing hgnc id: {}'.format(new_gene['hgnc_symbol']), 'danger')
            continue
        gene_obj = store.hgnc_gene(new_gene['hgnc_id'])
        if gene_obj is None:
            flash('gene not found: {} - {}'.format(new_gene['hgnc_id'], new_gene['hgnc_symbol']), 'danger')
            continue
        if new_gene['hgnc_symbol'] and gene_obj['hgnc_symbol'] != new_gene['hgnc_symbol']:
            flash('symbol mis-match: {0} | {1}'.format(gene_obj['hgnc_symbol'], new_gene['hgnc_symbol']), 'warning')
        info_data = {'disease_associated_transcripts': new_gene['transcripts'], 'reduced_penetrance': new_gene['reduced_penetrance'], 'mosaicism': new_gene['mosaicism'], 'inheritance_models': new_gene['inheritance_models'], 'database_entry_version': new_gene['database_entry_version']}
        if option == 'replace':
            action = 'add'
        else:
            existing_genes = {gene['hgnc_id'] for gene in panel_obj['genes']}
            action = 'edit' if gene_obj['hgnc_id'] in existing_genes else 'add'
        store.add_pending(panel_obj, gene_obj, action=action, info=info_data)
    return panel_obj
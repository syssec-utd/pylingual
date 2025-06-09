def gene(hgnc_id=None, hgnc_symbol=None):
    """Render information about a gene."""
    if hgnc_symbol:
        query = store.hgnc_genes(hgnc_symbol)
        if query.count() == 1:
            hgnc_id = query.first()['hgnc_id']
        else:
            return redirect(url_for('.genes', query=hgnc_symbol))
    try:
        genes = controllers.gene(store, hgnc_id)
    except ValueError as error:
        return abort(404)
    return genes
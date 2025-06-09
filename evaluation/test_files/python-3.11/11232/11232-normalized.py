def panel(panel_id):
    """Display (and add pending updates to) a specific gene panel."""
    panel_obj = store.gene_panel(panel_id) or store.panel(panel_id)
    if request.method == 'POST':
        raw_hgnc_id = request.form['hgnc_id']
        if '|' in raw_hgnc_id:
            raw_hgnc_id = raw_hgnc_id.split(' | ', 1)[0]
        hgnc_id = 0
        try:
            hgnc_id = int(raw_hgnc_id)
        except:
            flash("Provided HGNC is not valid : '{}'".format(raw_hgnc_id), 'danger')
            return redirect(request.referrer)
        action = request.form['action']
        gene_obj = store.hgnc_gene(hgnc_id)
        if gene_obj is None:
            flash('HGNC id not found: {}'.format(hgnc_id), 'warning')
            return redirect(request.referrer)
        if action == 'add':
            panel_gene = controllers.existing_gene(store, panel_obj, hgnc_id)
            if panel_gene:
                flash('gene already in panel: {}'.format(panel_gene['symbol']), 'warning')
            else:
                return redirect(url_for('.gene_edit', panel_id=panel_id, hgnc_id=hgnc_id))
        elif action == 'delete':
            log.debug('marking gene to be deleted: %s', hgnc_id)
            panel_obj = store.add_pending(panel_obj, gene_obj, action='delete')
    data = controllers.panel(store, panel_obj)
    if request.args.get('case_id'):
        data['case'] = store.case(request.args['case_id'])
    if request.args.get('institute_id'):
        data['institute'] = store.institute(request.args['institute_id'])
    return data
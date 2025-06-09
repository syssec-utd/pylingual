def upload_panel(institute_id, case_name):
    """Parse gene panel file and fill in HGNC symbols for filter."""
    file = form.symbol_file.data
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(request.referrer)
    try:
        stream = io.StringIO(file.stream.read().decode('utf-8'), newline=None)
    except UnicodeDecodeError as error:
        flash('Only text files are supported!', 'warning')
        return redirect(request.referrer)
    category = request.args.get('category')
    if category == 'sv':
        form = SvFiltersForm(request.args)
    else:
        form = FiltersForm(request.args)
    hgnc_symbols = set(form.hgnc_symbols.data)
    new_hgnc_symbols = controllers.upload_panel(store, institute_id, case_name, stream)
    hgnc_symbols.update(new_hgnc_symbols)
    form.hgnc_symbols.data = ','.join(hgnc_symbols)
    form.gene_panels.data = ''
    if category == 'sv':
        return redirect(url_for('.sv_variants', institute_id=institute_id, case_name=case_name, **form.data), code=307)
    else:
        return redirect(url_for('.variants', institute_id=institute_id, case_name=case_name, **form.data), code=307)
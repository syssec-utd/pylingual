def autocompleter():
    """Return autocompleter results"""
    disabled_engines = request.preferences.engines.get_disabled()
    if PY3:
        raw_text_query = RawTextQuery(request.form.get('q', b''), disabled_engines)
    else:
        raw_text_query = RawTextQuery(request.form.get('q', u'').encode('utf-8'), disabled_engines)
    raw_text_query.parse_query()
    if not raw_text_query.getSearchQuery():
        return ('', 400)
    completer = autocomplete_backends.get(request.preferences.get_value('autocomplete'))
    raw_results = searx_bang(raw_text_query)
    if len(raw_results) <= 3 and completer:
        language = request.preferences.get_value('language')
        if not language or language == 'all':
            language = 'en'
        else:
            language = language.split('-')[0]
        raw_results.extend(completer(raw_text_query.getSearchQuery(), language))
    results = []
    for result in raw_results:
        raw_text_query.changeSearchQuery(result)
        results.append(raw_text_query.getFullQuery())
    if request.form.get('format') == 'x-suggestions':
        return Response(json.dumps([raw_text_query.query, results]), mimetype='application/json')
    return Response(json.dumps(results), mimetype='application/json')
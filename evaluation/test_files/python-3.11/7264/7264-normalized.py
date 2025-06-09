def register_jinja(app):
    """Register jinja filters, vars, functions."""
    import jinja2
    from .utils import filters, permissions, helpers
    if app.debug or app.testing:
        my_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader([os.path.join(app.config.get('PROJECT_PATH'), 'application/macros'), os.path.join(app.config.get('PROJECT_PATH'), 'application/pages')])])
    else:
        my_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader([os.path.join(app.config.get('PROJECT_PATH'), 'output/macros'), os.path.join(app.config.get('PROJECT_PATH'), 'output/pages')])])
    app.jinja_loader = my_loader
    app.jinja_env.filters.update({'timesince': filters.timesince})

    def url_for_other_page(page):
        """Generate url for pagination."""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        combined_args['page'] = page
        return url_for(request.endpoint, **combined_args)
    rules = {}
    for endpoint, _rules in iteritems(app.url_map._rules_by_endpoint):
        if any((item in endpoint for item in ['_debug_toolbar', 'debugtoolbar', 'static'])):
            continue
        rules[endpoint] = [{'rule': rule.rule} for rule in _rules]
    app.jinja_env.globals.update({'absolute_url_for': helpers.absolute_url_for, 'url_for_other_page': url_for_other_page, 'rules': rules, 'permissions': permissions})
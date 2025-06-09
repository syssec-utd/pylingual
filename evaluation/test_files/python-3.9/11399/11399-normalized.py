def panel_export(store, panel_obj):
    """Preprocess a panel of genes."""
    panel_obj['institute'] = store.institute(panel_obj['institute'])
    full_name = '{}({})'.format(panel_obj['display_name'], panel_obj['version'])
    panel_obj['name_and_version'] = full_name
    return dict(panel=panel_obj)
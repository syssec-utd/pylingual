def djfrontend_jquery_datatables_css(version=None):
    """
    Returns the jQuery DataTables CSS file according to version number.
    """
    if version is None:
        if not getattr(settings, 'DJFRONTEND_JQUERY_DATATABLES_CSS', False):
            version = getattr(settings, 'DJFRONTEND_JQUERY_DATATABLES_VERSION', DJFRONTEND_JQUERY_DATATABLES_VERSION_DEFAULT)
        else:
            version = getattr(settings, 'DJFRONTEND_JQUERY_DATATABLES_CSS', DJFRONTEND_JQUERY_DATATABLES_VERSION_DEFAULT)
    return format_html('<link rel="stylesheet" href="{static}djfrontend/css/jquery/jquery.dataTables/{v}/jquery.dataTables{min}.css">', static=_static_url, v=version, min=_min)
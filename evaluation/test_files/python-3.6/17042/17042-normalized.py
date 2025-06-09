def djfrontend_h5bp_css(version=None):
    """
    Returns HTML5 Boilerplate CSS file.
    Included in HTML5 Boilerplate.
    """
    if version is None:
        version = getattr(settings, 'DJFRONTEND_H5BP_CSS', DJFRONTEND_H5BP_CSS_DEFAULT)
    return format_html('<link rel="stylesheet" href="{0}djfrontend/css/h5bp/{1}/h5bp.css">', _static_url, version)
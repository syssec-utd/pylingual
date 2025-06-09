"""Configuration for Invenio-Admin."""
ADMINISTRATION_BASE_TEMPLATE = 'invenio_administration/base.html'
'Admin panel base template.\nBy default (``None``) uses the Flask-Admin template.'
ADMINISTRATION_APPNAME = 'Invenio-Administration'
'Name of the Flask-Admin app (also the page title of admin panel).'
ADMINISTRATION_DASHBOARD_VIEW = 'invenio_administration.views.dashboard.AdminDashboardView'
'Administration dashboard view class.'
ADMINISTRATION_THEME_BASE_TEMPLATE = 'invenio_theme/page.html'
'Administration base template.'
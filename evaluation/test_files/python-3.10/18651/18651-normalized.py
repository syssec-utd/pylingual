def init_app_context():
    """Initialize app context for Invenio 2.x."""
    try:
        from invenio.base.factory import create_app
        app = create_app()
        app.test_request_context('/').push()
        app.preprocess_request()
    except ImportError:
        pass
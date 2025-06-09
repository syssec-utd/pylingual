def get(*args, **kwargs):
    """Get users."""
    from invenio.modules.oauth2server.models import Client
    q = Client.query
    return (q.count(), q.all())
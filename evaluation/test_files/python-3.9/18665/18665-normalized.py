def _get_users_invenio2(*args, **kwargs):
    """Get user accounts from Invenio 2."""
    from invenio.modules.accounts.models import User
    q = User.query
    return (q.count(), q.all())
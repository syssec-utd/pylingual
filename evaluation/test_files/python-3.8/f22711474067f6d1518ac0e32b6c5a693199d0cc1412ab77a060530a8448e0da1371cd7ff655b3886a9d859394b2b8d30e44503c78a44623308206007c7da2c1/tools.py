"""Generic tool definitions for RDBMS submodule."""

def get_or_create(session, model, **kwargs):
    """Create or get (if exists) instance of SQLAlchemy models with kwargs."""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        return instance
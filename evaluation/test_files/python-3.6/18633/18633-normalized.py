def get_check():
    """Get bibdocs to check."""
    try:
        from invenio.dbquery import run_sql
    except ImportError:
        from invenio.legacy.dbquery import run_sql
    return (run_sql('select count(id) from bibdoc', run_on_slave=True)[0][0], [id[0] for id in run_sql('select id from bibdoc', run_on_slave=True)])
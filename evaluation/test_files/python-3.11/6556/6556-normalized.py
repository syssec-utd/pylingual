def compatibility(session, install):
    """Run the unit test suite with each support library and Python version."""
    session.install('-e', '.[dev]')
    session.install(install)
    _run_tests(session)
def update_import_errors(session, dagbag):
    """
        For the DAGs in the given DagBag, record any associated import errors and clears
        errors for files that no longer have them. These are usually displayed through the
        Airflow UI so that users know that there are issues parsing DAGs.

        :param session: session for ORM operations
        :type session: sqlalchemy.orm.session.Session
        :param dagbag: DagBag containing DAGs with import errors
        :type dagbag: airflow.models.DagBag
        """
    for dagbag_file in dagbag.file_last_changed:
        session.query(errors.ImportError).filter(errors.ImportError.filename == dagbag_file).delete()
    for filename, stacktrace in six.iteritems(dagbag.import_errors):
        session.add(errors.ImportError(filename=filename, stacktrace=stacktrace))
    session.commit()
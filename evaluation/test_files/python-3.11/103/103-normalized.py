def clear_dag_runs():
    """
    Remove any existing DAG runs for the perf test DAGs.
    """
    session = settings.Session()
    drs = session.query(DagRun).filter(DagRun.dag_id.in_(DAG_IDS)).all()
    for dr in drs:
        logging.info('Deleting DagRun :: {}'.format(dr))
        session.delete(dr)
def next_execution(args):
    """
    Returns the next execution datetime of a DAG at the command line.
    >>> airflow next_execution tutorial
    2018-08-31 10:38:00
    """
    dag = get_dag(args)
    if dag.is_paused:
        print('[INFO] Please be reminded this DAG is PAUSED now.')
    if dag.latest_execution_date:
        next_execution_dttm = dag.following_schedule(dag.latest_execution_date)
        if next_execution_dttm is None:
            print('[WARN] No following schedule can be found. ' + "This DAG may have schedule interval '@once' or `None`.")
        print(next_execution_dttm)
    else:
        print('[WARN] Only applicable when there is execution record found for the DAG.')
        print(None)
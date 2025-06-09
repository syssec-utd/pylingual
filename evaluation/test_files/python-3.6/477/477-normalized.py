def _create_dagruns(dag, execution_dates, state, run_id_template):
    """
    Infers from the dates which dag runs need to be created and does so.
    :param dag: the dag to create dag runs for
    :param execution_dates: list of execution dates to evaluate
    :param state: the state to set the dag run to
    :param run_id_template:the template for run id to be with the execution date
    :return: newly created and existing dag runs for the execution dates supplied
    """
    drs = DagRun.find(dag_id=dag.dag_id, execution_date=execution_dates)
    dates_to_create = list(set(execution_dates) - set([dr.execution_date for dr in drs]))
    for date in dates_to_create:
        dr = dag.create_dagrun(run_id=run_id_template.format(date.isoformat()), execution_date=date, start_date=timezone.utcnow(), external_trigger=False, state=state)
        drs.append(dr)
    return drs
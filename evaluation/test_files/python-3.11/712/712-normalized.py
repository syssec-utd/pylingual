def reset_state_for_orphaned_tasks(self, filter_by_dag_run=None, session=None):
    """
        This function checks if there are any tasks in the dagrun (or all)
        that have a scheduled state but are not known by the
        executor. If it finds those it will reset the state to None
        so they will get picked up again.
        The batch option is for performance reasons as the queries are made in
        sequence.

        :param filter_by_dag_run: the dag_run we want to process, None if all
        :type filter_by_dag_run: airflow.models.DagRun
        :return: the TIs reset (in expired SQLAlchemy state)
        :rtype: list[airflow.models.TaskInstance]
        """
    queued_tis = self.executor.queued_tasks
    running_tis = self.executor.running
    resettable_states = [State.SCHEDULED, State.QUEUED]
    TI = models.TaskInstance
    DR = models.DagRun
    if filter_by_dag_run is None:
        resettable_tis = session.query(TI).join(DR, and_(TI.dag_id == DR.dag_id, TI.execution_date == DR.execution_date)).filter(DR.state == State.RUNNING, DR.run_id.notlike(BackfillJob.ID_PREFIX + '%'), TI.state.in_(resettable_states)).all()
    else:
        resettable_tis = filter_by_dag_run.get_task_instances(state=resettable_states, session=session)
    tis_to_reset = []
    for ti in resettable_tis:
        if ti.key not in queued_tis and ti.key not in running_tis:
            tis_to_reset.append(ti)
    if len(tis_to_reset) == 0:
        return []

    def query(result, items):
        filter_for_tis = [and_(TI.dag_id == ti.dag_id, TI.task_id == ti.task_id, TI.execution_date == ti.execution_date) for ti in items]
        reset_tis = session.query(TI).filter(or_(*filter_for_tis), TI.state.in_(resettable_states)).with_for_update().all()
        for ti in reset_tis:
            ti.state = State.NONE
            session.merge(ti)
        return result + reset_tis
    reset_tis = helpers.reduce_in_chunks(query, tis_to_reset, [], self.max_tis_per_query)
    task_instance_str = '\n\t'.join([repr(x) for x in reset_tis])
    session.commit()
    self.log.info('Reset the following %s TaskInstances:\n\t%s', len(reset_tis), task_instance_str)
    return reset_tis
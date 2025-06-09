def _find_executable_task_instances(self, simple_dag_bag, states, session=None):
    """
        Finds TIs that are ready for execution with respect to pool limits,
        dag concurrency, executor state, and priority.

        :param simple_dag_bag: TaskInstances associated with DAGs in the
            simple_dag_bag will be fetched from the DB and executed
        :type simple_dag_bag: airflow.utils.dag_processing.SimpleDagBag
        :param executor: the executor that runs task instances
        :type executor: BaseExecutor
        :param states: Execute TaskInstances in these states
        :type states: tuple[airflow.utils.state.State]
        :return: list[airflow.models.TaskInstance]
        """
    executable_tis = []
    TI = models.TaskInstance
    DR = models.DagRun
    DM = models.DagModel
    ti_query = session.query(TI).filter(TI.dag_id.in_(simple_dag_bag.dag_ids)).outerjoin(DR, and_(DR.dag_id == TI.dag_id, DR.execution_date == TI.execution_date)).filter(or_(DR.run_id == None, not_(DR.run_id.like(BackfillJob.ID_PREFIX + '%')))).outerjoin(DM, DM.dag_id == TI.dag_id).filter(or_(DM.dag_id == None, not_(DM.is_paused)))
    if None in states:
        ti_query = ti_query.filter(or_(TI.state == None, TI.state.in_(states)))
    else:
        ti_query = ti_query.filter(TI.state.in_(states))
    task_instances_to_examine = ti_query.all()
    if len(task_instances_to_examine) == 0:
        self.log.debug('No tasks to consider for execution.')
        return executable_tis
    task_instance_str = '\n\t'.join([repr(x) for x in task_instances_to_examine])
    self.log.info('%s tasks up for execution:\n\t%s', len(task_instances_to_examine), task_instance_str)
    pools = {p.pool: p for p in session.query(models.Pool).all()}
    pool_to_task_instances = defaultdict(list)
    for task_instance in task_instances_to_examine:
        pool_to_task_instances[task_instance.pool].append(task_instance)
    states_to_count_as_running = [State.RUNNING, State.QUEUED]
    (dag_concurrency_map, task_concurrency_map) = self.__get_concurrency_maps(states=states_to_count_as_running, session=session)
    for (pool, task_instances) in pool_to_task_instances.items():
        pool_name = pool
        if not pool:
            open_slots = models.Pool.default_pool_open_slots()
            pool_name = models.Pool.default_pool_name
        elif pool not in pools:
            self.log.warning("Tasks using non-existent pool '%s' will not be scheduled", pool)
            open_slots = 0
        else:
            open_slots = pools[pool].open_slots(session=session)
        num_ready = len(task_instances)
        self.log.info('Figuring out tasks to run in Pool(name=%s) with %s open slots and %s task instances ready to be queued', pool, open_slots, num_ready)
        priority_sorted_task_instances = sorted(task_instances, key=lambda ti: (-ti.priority_weight, ti.execution_date))
        num_starving_tasks = 0
        for (current_index, task_instance) in enumerate(priority_sorted_task_instances):
            if open_slots <= 0:
                self.log.info('Not scheduling since there are %s open slots in pool %s', open_slots, pool)
                num_starving_tasks = len(priority_sorted_task_instances) - current_index
                break
            dag_id = task_instance.dag_id
            simple_dag = simple_dag_bag.get_dag(dag_id)
            current_dag_concurrency = dag_concurrency_map[dag_id]
            dag_concurrency_limit = simple_dag_bag.get_dag(dag_id).concurrency
            self.log.info('DAG %s has %s/%s running and queued tasks', dag_id, current_dag_concurrency, dag_concurrency_limit)
            if current_dag_concurrency >= dag_concurrency_limit:
                self.log.info("Not executing %s since the number of tasks running or queued from DAG %s is >= to the DAG's task concurrency limit of %s", task_instance, dag_id, dag_concurrency_limit)
                continue
            task_concurrency_limit = simple_dag.get_task_special_arg(task_instance.task_id, 'task_concurrency')
            if task_concurrency_limit is not None:
                current_task_concurrency = task_concurrency_map[task_instance.dag_id, task_instance.task_id]
                if current_task_concurrency >= task_concurrency_limit:
                    self.log.info('Not executing %s since the task concurrency for this task has been reached.', task_instance)
                    continue
            if self.executor.has_task(task_instance):
                self.log.debug('Not handling task %s as the executor reports it is running', task_instance.key)
                continue
            executable_tis.append(task_instance)
            open_slots -= 1
            dag_concurrency_map[dag_id] += 1
            task_concurrency_map[task_instance.dag_id, task_instance.task_id] += 1
        Stats.gauge('pool.starving_tasks.{pool_name}'.format(pool_name=pool_name), num_starving_tasks)
    task_instance_str = '\n\t'.join([repr(x) for x in executable_tis])
    self.log.info('Setting the following tasks to queued state:\n\t%s', task_instance_str)
    for ti in executable_tis:
        copy_dag_id = ti.dag_id
        copy_execution_date = ti.execution_date
        copy_task_id = ti.task_id
        make_transient(ti)
        ti.dag_id = copy_dag_id
        ti.execution_date = copy_execution_date
        ti.task_id = copy_task_id
    return executable_tis
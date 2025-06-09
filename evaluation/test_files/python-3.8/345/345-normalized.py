def command_as_list(self, mark_success=False, ignore_all_deps=False, ignore_task_deps=False, ignore_depends_on_past=False, ignore_ti_state=False, local=False, pickle_id=None, raw=False, job_id=None, pool=None, cfg_path=None):
    """
        Returns a command that can be executed anywhere where airflow is
        installed. This command is part of the message sent to executors by
        the orchestrator.
        """
    dag = self.task.dag
    should_pass_filepath = not pickle_id and dag
    if should_pass_filepath and dag.full_filepath != dag.filepath:
        path = 'DAGS_FOLDER/{}'.format(dag.filepath)
    elif should_pass_filepath and dag.full_filepath:
        path = dag.full_filepath
    else:
        path = None
    return TaskInstance.generate_command(self.dag_id, self.task_id, self.execution_date, mark_success=mark_success, ignore_all_deps=ignore_all_deps, ignore_task_deps=ignore_task_deps, ignore_depends_on_past=ignore_depends_on_past, ignore_ti_state=ignore_ti_state, local=local, pickle_id=pickle_id, file_path=path, raw=raw, job_id=job_id, pool=pool, cfg_path=cfg_path)
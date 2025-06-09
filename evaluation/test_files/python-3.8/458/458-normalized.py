def _get_dep_statuses(self, ti, session, dep_context):
    """
        Determines whether a task is ready to be rescheduled. Only tasks in
        NONE state with at least one row in task_reschedule table are
        handled by this dependency class, otherwise this dependency is
        considered as passed. This dependency fails if the latest reschedule
        request's reschedule date is still in future.
        """
    if dep_context.ignore_in_reschedule_period:
        yield self._passing_status(reason='The context specified that being in a reschedule period was permitted.')
        return
    if ti.state not in self.RESCHEDULEABLE_STATES:
        yield self._passing_status(reason='The task instance is not in State_UP_FOR_RESCHEDULE or NONE state.')
        return
    task_reschedules = TaskReschedule.find_for_task_instance(task_instance=ti)
    if not task_reschedules:
        yield self._passing_status(reason='There is no reschedule request for this task instance.')
        return
    now = timezone.utcnow()
    next_reschedule_date = task_reschedules[-1].reschedule_date
    if now >= next_reschedule_date:
        yield self._passing_status(reason='Task instance id ready for reschedule.')
        return
    yield self._failing_status(reason='Task is not ready for reschedule yet but will be rescheduled automatically. Current date is {0} and task will be rescheduled at {1}.'.format(now.isoformat(), next_reschedule_date.isoformat()))
def start_step(self, step_name):
    """ Start a step. """
    if self.finished is not None:
        raise AlreadyFinished()
    step_data = self._get_step(step_name)
    if step_data is not None:
        if 'stop' in step_data:
            raise StepAlreadyFinished()
        else:
            raise StepAlreadyStarted()
    steps = copy.deepcopy(self.steps)
    steps.append({'start': datetime.utcnow(), 'name': step_name})
    self._save(steps=steps)
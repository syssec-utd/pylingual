def _build_worklfow_json(self):
    """
        Build a workflow definition from the cloud_harness task.
        """
    wf_json = {'tasks': [], 'name': 'cloud-harness_%s' % str(uuid.uuid4())}
    task_def = json.loads(self.task_template.json())
    d = {'name': task_def['name'], 'outputs': [], 'inputs': [], 'taskType': task_def['taskType']}
    for port in self.task_template.input_ports:
        port_value = port.value
        if port_value is False:
            port_value = 'false'
        if port_value is True:
            port_value = 'true'
        d['inputs'].append({'name': port._name, 'value': port_value})
    for port in self.task_template.output_ports:
        d['outputs'].append({'name': port._name})
    wf_json['tasks'].append(d)
    for port in self.task_template.output_ports:
        if hasattr(port, 'stageToS3') and port.stageToS3:
            save_location = '{customer_storage}/{run_name}/{port}'.format(customer_storage=self.storage.location, run_name=self.task_template.run_name, port=port.name)
            new_task = dict(**self.STAGE_TO_S3)
            new_task['inputs'] = [{'name': 'data', 'source': '%s:%s' % (task_def['name'], port._name)}, {'name': 'destination', 'value': save_location}]
            wf_json['tasks'].append(new_task)
    return wf_json
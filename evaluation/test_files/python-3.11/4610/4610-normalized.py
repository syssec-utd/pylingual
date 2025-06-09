def _execute_core_transform(transform_context, inputs):
    """
    Execute the user-specified transform for the solid. Wrap in an error boundary and do
    all relevant logging and metrics tracking
    """
    check.inst_param(transform_context, 'transform_context', SystemTransformExecutionContext)
    check.dict_param(inputs, 'inputs', key_type=str)
    step = transform_context.step
    solid = step.solid
    transform_context.log.debug('Executing core transform for solid {solid}.'.format(solid=solid.name))
    all_results = []
    for step_output in _yield_transform_results(transform_context, inputs):
        yield step_output
        if isinstance(step_output, StepOutputValue):
            all_results.append(step_output)
    if len(all_results) != len(solid.definition.output_defs):
        emitted_result_names = {r.output_name for r in all_results}
        solid_output_names = {output_def.name for output_def in solid.definition.output_defs}
        omitted_outputs = solid_output_names.difference(emitted_result_names)
        transform_context.log.info('Solid {solid} did not fire outputs {outputs}'.format(solid=solid.name, outputs=repr(omitted_outputs)))
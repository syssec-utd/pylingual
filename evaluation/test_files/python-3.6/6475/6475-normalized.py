def profile_function(self):
    """Calculates heatmap for function."""
    with _CodeHeatmapCalculator() as prof:
        result = self._run_object(*self._run_args, **self._run_kwargs)
    (code_lines, start_line) = inspect.getsourcelines(self._run_object)
    source_lines = []
    for line in code_lines:
        source_lines.append(('line', start_line, line))
        start_line += 1
    filename = os.path.abspath(inspect.getsourcefile(self._run_object))
    heatmap = prof.heatmap[filename]
    run_time = sum((time for time in heatmap.values()))
    return {'objectName': self._object_name, 'runTime': run_time, 'result': result, 'timestamp': int(time.time()), 'heatmaps': [{'name': self._object_name, 'heatmap': heatmap, 'executionCount': prof.execution_count[filename], 'srcCode': source_lines, 'runTime': run_time}]}